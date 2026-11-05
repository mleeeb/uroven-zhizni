"""Слоты одежды и сборка героя из отдельных вещей.

Слоты: head (голова), face (лицо), neck (шея), hands (руки), top (верх), bottom (низ), shoes (обувь).
Каждая вещь — функция fn(sex, ctx) -> Item. ctx: skin, hair, sleeve ('short'|'long').
"""
from px32 import Item, Canvas, base, shade, SKINS, HAIRS, SHIRTS, K

SLOTS = ['head', 'face', 'neck', 'hands', 'top', 'bottom', 'shoes']
SLOT_NAMES = {'head': 'Головные уборы', 'face': 'Лицо', 'neck': 'Шея', 'hands': 'Руки',
              'top': 'Верх', 'bottom': 'Низ', 'shoes': 'Обувь'}
CATALOG = {}


def item(slot, name, theme='', long=False, sleeve='short', tall=False, only=None):
    """Регистрирует вещь. long — верх до пола (закрывает низ), tall — высокая обувь поверх штанин."""
    def deco(fn):
        CATALOG[fn.__name__] = dict(id=fn.__name__, slot=slot, name=name, theme=theme, long=long,
                                    sleeve=sleeve, tall=tall, only=only, fn=fn)
        return fn
    return deco


# ---------- геометрия тела ----------
def geo(sex):
    if sex == 'm':
        return dict(bx0=9, bx1=22, sl=(4, 7), sr=(24, 27), ssl=(5, 8), ssr=(23, 26), hl=5, hr=24, line=(8, 23))
    return dict(bx0=10, bx1=21, sl=(6, 9), sr=(22, 25), ssl=(7, 9), ssr=(22, 24), hl=7, hr=22, line=(10, 21))


def hand_box(sex, sleeve):
    g = geo(sex)
    y0, y1 = (29, 31) if sleeve == 'long' else (27, 30)
    return [(g['hl'], y0, g['hl'] + 2, y1), (g['hr'], y0, g['hr'] + 2, y1)]


def hands(it, sex, skin, sleeve='long'):
    sd = shade(skin, 0.86)
    for x0, y0, x1, y1 in hand_box(sex, sleeve):
        it.rect(x0, y0, x1, y1, skin)
        it.px(x0 + 1, y1, sd)


def long_top(it, sex, C, hem=33, Cd=None, shade_right=True):
    """Корпус с длинными рукавами до запястья; возвращает геометрию."""
    g = geo(sex)
    bx0, bx1, sl, sr = g['bx0'], g['bx1'], g['sl'], g['sr']
    it.rect(bx0, 22, bx1, hem, C)
    it.rect(bx0 + 1, 21, bx1 - 1, 21, C)
    it.rect(sl[0], 23, sr[1], 24, C)
    it.rect(sl[0], 25, sl[1], 28, C); it.rect(sr[0], 25, sr[1], 28, C)
    if Cd and shade_right:
        it.rect(bx1 - 1, 25, bx1, hem, Cd); it.rect(sr[0] + 2, 25, sr[1], 28, Cd)
    for y in range(25, 29):
        it.line(sl[1] + 1, y); it.line(sr[0] - 1, y)
    it.no_outline.update({(x, 20) for x in range(8, 24)})
    return g


def short_top(it, sex, C, hem=31, Cd=None):
    """Корпус с короткими рукавами (как футболка)."""
    g = geo(sex)
    bx0, bx1 = g['bx0'], g['bx1']
    if sex == 'f':
        bx0, bx1 = 11, 20
        it.rect(9, 23, 22, 23, C)
    it.rect(bx0, 22, bx1, hem, C); it.rect(bx0 + 1, 22, bx1 - 1, 22, C)
    it.rect(g['ssl'][0], 24, g['ssr'][1], 24 if sex == 'm' else 26, C)
    it.rect(g['ssl'][0], 24, g['ssl'][1], 26, C); it.rect(g['ssr'][0], 24, g['ssr'][1], 26, C)
    if Cd:
        it.rect(bx1, 24, bx1, hem, Cd)
        it.rect(g['ssl'][0], 26, g['ssl'][1], 26, Cd); it.rect(g['ssr'][0], 26, g['ssr'][1], 26, Cd)
    for y in range(27, 31):
        it.line(g['line'][0], y); it.line(g['line'][1], y)
    it.no_outline.update({(x, 21) for x in range(12, 20)} | {(x, 20) for x in range(8, 24)})
    return g


def pants(it, C, Cd=None, bottom=38, wide=0):
    """Штаны: пояс 32, ноги 34..bottom."""
    it.rect(9 - wide, 32, 22 + wide, 33, C)
    it.rect(9 - wide, 34, 14, bottom, C); it.rect(17, 34, 22 + wide, bottom, C)
    if Cd:
        it.rect(13, 34, 14, bottom, Cd); it.rect(21 + wide, 34, 22 + wide, bottom, Cd)
    for y in range(34, bottom + 1): it.line(15, y); it.line(16, y)


def bare_legs(it, skin, y0, y1, color=None):
    c = color or skin
    it.rect(10, y0, 13, y1, c); it.rect(18, y0, 21, y1, c)
    for y in range(y0, y1 + 1): it.line(14, y); it.line(17, y); it.line(15, y); it.line(16, y)


def feet_base(it, skin, top=39):
    """Голые стопы/щиколотки для открытой обуви."""
    it.rect(10, top, 13, 41, skin); it.rect(18, top, 21, 41, skin)
    for y in range(top, 43): it.line(15, y); it.line(16, y)


# ---------- сборка ----------
def hair_front(cv, sex, style, hair_cols=()):
    if style != 'long':
        return None
    it = Item()
    for y in range(19, 25):
        for x in list(range(4, 10)) + list(range(22, 28)):
            c = cv.g[y][x]
            if c in hair_cols:
                it.px(x, y, c)
    keep = {(x, y) for (x, y) in it.c}
    for (x, y) in keep:
        it.no_outline.add((x, y - 1))
    # волосы не перекрывают лицо и шею
    for (x, y) in list(it.c):
        if 9 <= x <= 22 and y < 22: it.erase(x, y)
    return it


def compose(sex, skin=0, hair=1, shirt=0, face_v='A', hair_style=None, beard=False, **slots):
    sk = SKINS[skin] if isinstance(skin, int) else skin
    hc = HAIRS[hair] if isinstance(hair, int) else hair
    cv = base(sex=sex, skin=skin, hair=hair, shirt=shirt, face_v=face_v, hair_style=hair_style, beard=beard)
    style = hair_style or ('short' if sex == 'm' else 'long')
    hf = hair_front(cv, sex, style, {hc, shade(hc, 0.72), shade(hc, 1.35)})
    top = CATALOG.get(slots.get('top'))
    sleeve = top['sleeve'] if top else 'short'
    ctx = dict(skin=sk, hair=hc, sleeve=sleeve, sex=sex, shirt=SHIRTS[shirt] if isinstance(shirt, int) else shirt)

    def put(key):
        it = CATALOG.get(slots.get(key))
        if it: it['fn'](sex, ctx).apply(cv)

    shoes = CATALOG.get(slots.get('shoes'))
    if shoes:
        for y in range(39, 44):
            for x in range(5, 27): cv.g[y][x] = '.'
    bot = CATALOG.get(slots.get('bottom'))
    under = shoes and (not shoes['tall'] or (bot and bot['long']))
    if under: put('shoes')
    put('bottom')
    if shoes and not under: put('shoes')
    put('top')
    put('hands')
    put('neck')
    if hf and (top or slots.get('neck')): hf.apply(cv)
    put('face')
    put('head')
    return cv
