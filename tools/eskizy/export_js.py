"""Выгружает героя 32x44, вещи, снаряжение, питомцев и фоны в hero32.js для приложения.
Цвета кожи/волос/футболки заменены «метками» и подставляются в приложении (S/H/T + коэффициент оттенка)."""
import base64
import io
import json
import sys
import w_head, w_small, w_top, w_low, w_folk, w_fest, w_extra, w_folk2  # noqa
from outfit import CATALOG, hair_front
from w_basic import BASIC, GEAR32
from px32 import Canvas, base, shade, W as GW, H as GH
from pets import pet_canvas, CAT, CAT_PAL, DRAGON, DRAGON_PAL
from pets2 import PETS2
from pets3 import PETS3
from bg2 import SCENES

SK, HA, SH = '#C800C8', '#00B400', '#0000C8'
ALPHA = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&()*+,-/:;<=>?@[]^_{|}'
PAL, PIDX, LAYERS, LIDX = [], {}, [], {}


def tok(c):
    r, g, b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
    f = lambda v, d: ('%.3f' % (v / d)).rstrip('0').rstrip('.')
    if r == b and g == 0 and r > 0: return 'S' + f(r, 200)
    if r == 0 and b == 0 and g > 0: return 'H' + f(g, 180)
    if r == 0 and g == 0 and b > 0: return 'T' + f(b, 200)
    return c.upper()


def gidx(c):
    t = tok(c)
    if t not in PIDX: PIDX[t] = len(PAL); PAL.append(t)
    return PIDX[t]


def encode(grid):
    """grid: строки клеток: None — не трогать, '~' — стереть, иначе цвет. -> индекс слоя."""
    local, lmap, rows = [], {}, []
    for y, row in enumerate(grid):
        xs = [x for x, c in enumerate(row) if c is not None]
        if not xs: continue
        x0, x1 = min(xs), max(xs)
        s = ''
        for c in row[x0:x1 + 1]:
            if c is None: s += '.'
            elif c == '~': s += '~'
            else:
                gi = gidx(c)
                if gi not in lmap: lmap[gi] = len(local); local.append(gi)
                s += ALPHA[lmap[gi]]
        rows.append([y, x0, s])
    assert len(local) <= len(ALPHA)
    key = json.dumps([local, rows])
    if key not in LIDX: LIDX[key] = len(LAYERS); LAYERS.append([local, rows])
    return LIDX[key]


def sim(apply_fn, w=GW, h=GH):
    cv = Canvas(w, h); cv.g = [['U'] * w for _ in range(h)]
    apply_fn(cv)
    return encode([[None if c == 'U' else ('~' if c == '.' else c) for c in row] for row in cv.g])


def full(cv):
    return encode([[None if c == '.' else c for c in row] for row in cv.g])


def ctx(sex, sleeve):
    return dict(skin=SK, hair=HA, sleeve=sleeve, sex=sex, shirt=SH)


STYLES = {'m': ['short', 'buzz', 'bangs'], 'f': ['long', 'pony', 'bob']}
out = {'base': {}, 'hf': {}, 'items': {}, 'basic': {}, 'gear': {}, 'pets': [], 'bgs': []}
for sex, sts in STYLES.items():
    for st in sts:
        for beard in ((False, True) if sex == 'm' else (False,)):
            cv = base(sex, SK, HA, SH, 'A', st, beard=beard)
            out['base'][f'{sex}/{st}' + ('/b' if beard else '')] = full(cv)
        cv = base(sex, SK, HA, SH, 'A', st)
        hf = hair_front(cv, sex, st, {HA, shade(HA, 0.72), shade(HA, 1.35)})
        if hf: out['hf'][f'{sex}/{st}'] = sim(hf.apply)


def variants(fn, only):
    v = {}
    for sex in ('m', 'f'):
        if only and only != sex: continue
        a = fn(sex, ctx(sex, 'short')); b = fn(sex, ctx(sex, 'long'))
        if a is None: continue
        la, lb = sim(a.apply), sim(b.apply)
        v[sex] = la
        if lb != la: v[sex + '/l'] = lb
    return v


for k, it in CATALOG.items():
    out['items'][k] = dict(s=it['slot'], n=it['name'], t=it['theme'] or 'разное', v=variants(it['fn'], it['only']),
                           **({'l': 1} if it['long'] else {}), **({'tl': 1} if it['tall'] else {}),
                           **({'sl': it['sleeve']} if it['sleeve'] != 'short' else {}), **({'o': it['only']} if it['only'] else {}))
for k, it in BASIC.items():
    out['basic'][k] = dict(s=it['slot'], v=variants(it['fn'], it['only']),
                           **({'l': 1} if it['long'] else {}), **({'tl': 1} if it['tall'] else {}),
                           **({'sl': it['sleeve']} if it['sleeve'] != 'short' else {}))
for k, g in GEAR32.items():
    out['gear'][k] = dict(s=g['slot'], v=variants(g['fn'], None), **({'bh': 1} if g['behind'] else {}))

PET_IDS = ['cat', 'dragon', 'corgi', 'owl', 'hamster', 'fox', 'ferret', 'dog', 'lamb', 'pig']
pets = [('Кот', CAT, CAT_PAL), ('Дракончик', DRAGON, DRAGON_PAL)] + PETS2 + PETS3
for pid, (name, mask, pal) in zip(PET_IDS, pets):
    out['pets'].append(dict(id=pid, n=name, L=full(pet_canvas(mask, pal))))

FX = {
    'Снежная ночь': [['fall', 45, ['#F4F1DE', '#C9CBDD'], 0.6, 0.4, 1], ['twinkle', 6, 0, 30]],
    'Сад': [['fly', 3, ['#F4F1DE', '#E8A0B8', '#F2CC8F'], 30, 75]],
    'Море': [['sparkle', 14, 46, 69, '#C8E2F0'], ['drift', 2, ['#0C0E22'], 0.3, 14, 26, 'bird']],
    'Листопад': [['fall', 18, ['#E8943A', '#C4473F', '#F2CC8F'], 0.5, 0.8, 2]],
    'Космос': [['twinkle', 14, 0, 70], ['shoot', 1]],
    'Горы': [['drift', 3, ['#3A3F63'], 0.35, 6, 24, 'bird']],
    'Северное сияние': [['twinkle', 10, 0, 50], ['shimmer', 14, 10, 40, ['#4FD0A0', '#81E0B8', '#B794E0']], ['fall', 12, ['#F4F1DE'], 0.4, 0.3, 1]],
    'Ночной город': [['twinkle', 6, 0, 28], ['windows', 8]],
    'Пустыня': [['drift', 14, ['#F2D49A', '#E8C080'], 1.2, 50, 86, 'sand']],
    'Сакура': [['fall', 22, ['#F4B8CC', '#E8A0B8'], 0.5, 0.7, 1]],
    'Джунгли': [['fly', 6, ['#F8E08A'], 10, 72, 'firefly']],
    'Подводный мир': [['rise', 14, ['#C8EEFA', '#8FD0F0'], 0.5, 0, 76]],
    'Подсолнухи': [['fly', 4, ['#F2C83A'], 40, 76, 'bee']],
    'Сказочный замок': [['rise', 10, ['#F8E08A', '#F4F1DE'], 0.25, 10, 70, 'spark']],
    'Костёр в лесу': [['fire', 16, 80], ['rise', 6, ['#F8E08A', '#E8943A'], 0.4, 60, 79, 'ember', 16], ['twinkle', 6, 0, 30]],
}
BG_IDS = ['snow', 'garden', 'sea', 'autumn', 'space', 'mountains', 'aurora', 'city', 'desert', 'sakura', 'jungle',
          'underwater', 'sunflowers', 'castle', 'campfire']
empty = Canvas(32, 44)
for bid, sc in zip(BG_IDS, SCENES):
    im = sc(empty).image(1)
    buf = io.BytesIO(); im.save(buf, 'PNG', optimize=True)
    out['bgs'].append(dict(id=bid, n=sc.title, png='data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode(),
                           fx=FX.get(sc.title, [])))

out['P'] = PAL
out['L'] = LAYERS
js = '/* Сгенерировано tools/eskizy/export_js.py — не править руками. Герой 32x44, вещи, снаряжение, питомцы, фоны. */\nconst H32=' + \
     json.dumps(out, ensure_ascii=False, separators=(',', ':')) + ';\n'
open(sys.argv[1], 'w', encoding='utf-8').write(js)
print('size', len(js.encode()), 'layers', len(LAYERS), 'palette', len(PAL), 'items', len(out['items']),
      'basic', len(out['basic']), 'gear', len(out['gear']), 'pets', len(out['pets']), 'bgs', len(out['bgs']))
print([p for p in PAL if not p.startswith('#')])
