"""Базовый гардероб приложения (верх/низ/обувь из v0.3) в размере 32x44 и снаряжение рангов."""
from outfit import item, geo, hands, long_top, short_top, pants, hand_box
from px32 import Item, Canvas, shade, K
from w_low import legs_below, boot
from w_fest import short_dress

W, Wd = '#F4F1DE', '#C9CBDD'
GOLD, GOLD_D = '#F2CC8F', '#C9A15F'
BASIC = {}   # id приложения -> функция


def basic(app_id, slot, sleeve='short', long=False, tall=False, only=None):
    def deco(fn):
        BASIC[app_id] = dict(id=app_id, slot=slot, sleeve=sleeve, long=long, tall=tall, only=only, fn=fn)
        return fn
    return deco


def T(ctx): return ctx['shirt'], shade(ctx['shirt'], 0.78)


# ---------- верх ----------
@basic('tee', 'top')
def b_tee(sex, ctx):
    it = Item(); c, cd = T(ctx); short_top(it, sex, c, hem=31, Cd=cd); return it


@basic('print', 'top')
def b_print(sex, ctx):
    it = Item(); c, cd = T(ctx); short_top(it, sex, c, hem=31, Cd=cd)
    it.rect(15, 25, 16, 28, GOLD); it.rect(14, 26, 17, 27, GOLD); it.px(16, 27, GOLD_D); it.px(16, 28, GOLD_D); it.px(17, 27, GOLD_D)
    return it


@basic('hoodie', 'top', sleeve='long')
def b_hoodie(sex, ctx):
    it = Item(); c, cd = T(ctx)
    g = long_top(it, sex, c, hem=32, Cd=cd)
    it.rect(g['bx0'] + 1, 21, g['bx1'] - 1, 22, cd); it.rect(14, 21, 17, 22, ctx['skin'])
    for y in range(23, 27): it.px(14, y, W); it.px(17, y, W)
    it.rect(12, 28, 19, 30, cd); it.rect(13, 28, 18, 28, c)
    it.rect(g['sl'][0], 28, g['sl'][1], 28, cd); it.rect(g['sr'][0], 28, g['sr'][1], 28, cd)
    hands(it, sex, ctx['skin']); return it


@basic('shirt', 'top', sleeve='long')
def b_shirt(sex, ctx):
    it = Item(); c, cd = T(ctx)
    if sex == 'm':
        long_top(it, sex, W, hem=31, Cd=Wd)
        it.rect(13, 21, 18, 21, Wd); it.rect(15, 22, 16, 22, cd); it.rect(15, 23, 16, 28, c); it.px(15, 29, c)
        for y in (25, 28): it.px(17, y, '#9AA0C0')
    else:
        long_top(it, sex, c, hem=31, Cd=cd)
        it.rect(12, 21, 14, 22, W); it.rect(17, 21, 19, 22, W)
        for y in (24, 27, 30): it.px(16, y, W)
    hands(it, sex, ctx['skin']); return it


@basic('jacket', 'top', sleeve='long')
def b_jacket(sex, ctx):
    J, Jd = '#33395A', '#262A44'
    it = Item(); c, cd = T(ctx)
    g = long_top(it, sex, J, hem=33, Cd=Jd)
    it.rect(14, 21, 17, 25, c); it.rect(15, 26, 16, 27, c)
    for i in range(7): it.px(13 - i // 3, 21 + i, '#4A5078'); it.px(18 + i // 3, 21 + i, '#4A5078')
    for y in (28, 31): it.px(16, y, GOLD_D)
    it.rect(g['bx0'] + 1, 30, g['bx0'] + 3, 30, Jd); it.rect(g['bx1'] - 3, 30, g['bx1'] - 1, 30, Jd)
    hands(it, sex, ctx['skin']); return it


@basic('sweater', 'top', sleeve='long')
def b_sweater(sex, ctx):
    it = Item(); c, cd = T(ctx)
    g = long_top(it, sex, c, hem=33, Cd=cd)
    for y in (24, 26): it.rect(g['bx0'], y, g['bx1'], y, cd)
    for x in range(g['bx0'], g['bx1'] + 1, 2): it.px(x, 33, cd)
    it.rect(g['sl'][0], 28, g['sl'][1], 28, cd); it.rect(g['sr'][0], 28, g['sr'][1], 28, cd); it.rect(13, 21, 18, 21, cd)
    hands(it, sex, ctx['skin']); return it


@basic('dress', 'top', long=True, only='f')
def b_dress(sex, ctx):
    it = Item(); c, cd = T(ctx)
    short_top(it, sex, c, hem=31, Cd=cd); short_dress(it, sex, ctx, c, cd)
    it.rect(11, 31, 20, 31, cd); return it


# ---------- низ ----------
def short_pants(it, ctx, C, Cd, bottom=35):
    legs_below(it, bottom + 1, ctx['skin'], shade(ctx['skin'], 0.86)); pants(it, C, Cd, bottom=bottom)


@basic('shorts', 'bottom')
def b_shorts(sex, ctx):
    it = Item(); short_pants(it, ctx, '#22263F', '#181B30')
    it.rect(9, 34, 9, 35, W); it.rect(22, 34, 22, 35, W); return it


@basic('track', 'bottom')
def b_track(sex, ctx):
    it = Item(); pants(it, '#4A4F6E', '#3A3F5A')
    for y in range(33, 39): it.px(9, y, W); it.px(22, y, W)
    it.rect(9, 38, 14, 38, '#3A3F5A'); it.rect(17, 38, 22, 38, '#3A3F5A'); return it


@basic('trousers', 'bottom')
def b_trousers(sex, ctx):
    it = Item(); pants(it, '#2A2D45', '#20223A')
    it.rect(9, 32, 22, 32, '#1E1A22'); it.px(15, 32, '#9AA0C0')
    it.rect(11, 34, 11, 38, '#3A3F5A'); it.rect(19, 34, 19, 38, '#3A3F5A'); return it


def pencil(it, ctx, C, Cd, hem=36):
    legs_below(it, hem + 1, ctx['skin'], shade(ctx['skin'], 0.86))
    it.rect(9, 32, 22, hem, C); it.rect(20, 33, 22, hem, Cd); it.rect(9, 32, 22, 32, Cd)


@basic('chinos', 'bottom')
def b_chinos(sex, ctx):
    it = Item()
    if sex == 'm':
        pants(it, '#C2A878', '#A68C5E'); it.rect(9, 32, 22, 32, '#6B4A30')
    else:
        pencil(it, ctx, '#2A2D45', '#20223A'); it.rect(15, 34, 15, 36, '#20223A')
    return it


@basic('jeans', 'bottom')
def b_jeans(sex, ctx):
    return None   # джинсы нарисованы в базе


@basic('cshorts', 'bottom')
def b_cshorts(sex, ctx):
    it = Item()
    if sex == 'm':
        short_pants(it, ctx, '#B8A27A', '#98845E')
    else:
        legs_below(it, 36, ctx['skin'], shade(ctx['skin'], 0.86))
        it.rect(9, 32, 22, 33, '#B5485A'); it.rect(8, 34, 23, 35, '#B5485A'); it.rect(20, 33, 23, 35, '#94384A')
    return it


# ---------- обувь ----------
def low_shoe(it, C, Cd, sole, top=39):
    it.rect(9, top, 14, 41, C); it.rect(17, top, 22, 41, C)
    it.rect(7, 40, 8, 41, C); it.rect(23, 40, 24, 41, C)
    it.rect(13, top, 14, 41, Cd); it.rect(22, top, 22, 41, Cd)
    it.rect(7, 42, 14, 42, sole); it.rect(17, 42, 24, 42, sole)
    for y in range(top, 43): it.line(15, y); it.line(16, y)


@basic('sneakers', 'shoes')
def b_sneakers(sex, ctx):
    it = Item(); low_shoe(it, W, Wd, '#9A99B0')
    it.px(11, 39, '#9AA0C0'); it.px(19, 39, '#9AA0C0'); it.px(10, 40, '#8FB3E0'); it.px(18, 40, '#8FB3E0'); return it


@basic('runners', 'shoes')
def b_runners(sex, ctx):
    it = Item(); low_shoe(it, '#4FA88A', '#3F8A70', W)
    it.px(11, 40, W); it.px(19, 40, W); return it


@basic('oxfords', 'shoes')
def b_oxfords(sex, ctx):
    it = Item(); low_shoe(it, '#1E1A22', '#141218', '#0C0A10', top=40)
    it.px(10, 40, '#4A4458'); it.px(18, 40, '#4A4458'); return it


@basic('boots', 'shoes', tall=True)
def b_boots(sex, ctx):
    it = Item(); boot(it, '#6B4A30', 37, '#4E3522', '#2A1E16')
    it.px(11, 38, '#8A6A48'); it.px(19, 38, '#8A6A48'); return it


@basic('keds', 'shoes')
def b_keds(sex, ctx):
    return None   # кеды нарисованы в базе


@basic('hightops', 'shoes', tall=True)
def b_hightops(sex, ctx):
    R, Rd = '#C4473F', '#9A3530'
    it = Item(); boot(it, R, 36, Rd, W)
    for y in (37, 39): it.px(11, y, W); it.px(19, y, W)
    it.rect(9, 36, 14, 36, W); it.rect(17, 36, 22, 36, W); return it


# ---------- снаряжение рангов ----------
GEAR32 = {}   # id -> dict(slot, behind?, fn(sex, ctx) -> Item)


def gear(gid, slot, behind=False):
    def deco(fn):
        GEAR32[gid] = dict(id=gid, slot=slot, behind=behind, fn=fn); return fn
    return deco


@gear('band', 'head')
def g_band(sex, ctx):
    it = Item(); it.plain = True
    it.rect(7, 8, 24, 9, '#E07A5F'); it.rect(7, 9, 24, 9, '#B85A42')
    it.rect(25, 9, 26, 10, '#E07A5F'); it.px(27, 11, '#B85A42'); it.px(26, 12, '#E07A5F')
    for x in (25, 26, 27): it.px(x, 8, K) if x == 25 else None
    return it


@gear('cap', 'head')
def g_cap(sex, ctx):
    C, Cd = '#6C9BD8', '#4F7EBA'
    it = Item()
    it.rect(11, 2, 20, 2, C); it.rect(9, 3, 22, 7, C); it.rect(19, 3, 22, 7, Cd)
    it.rect(15, 2, 16, 7, Cd); it.px(15, 1, W); it.px(16, 1, W)
    it.rect(8, 8, 23, 8, C); it.rect(8, 9, 23, 9, '#3A5A8A'); it.rect(20, 8, 27, 9, '#3A5A8A')
    return it


@gear('cape', 'back', behind=True)
def g_cape(sex, ctx):
    it = Item()
    for y in range(22, 42):
        w = 2 + (y - 22) // 5
        for x in range(3 - w // 2, 9): it.px(x, y, '#8E3B46')
        for x in range(23, 29 + w // 2): it.px(x, y, '#6E2A36' if x > 26 else '#8E3B46')
    return it


@gear('pack', 'back', behind=True)
def g_pack(sex, ctx):
    it = Item()
    it.rect(2, 23, 8, 35, '#8A6A3B'); it.rect(2, 23, 8, 24, '#6B4A30'); it.rect(3, 29, 7, 31, '#A8865A')
    it.px(5, 30, GOLD)
    return it


@gear('pack_front', 'back')
def g_pack_front(sex, ctx):
    it = Item(); it.plain = True
    x0, x1 = (10, 21) if sex == 'm' else (11, 20)
    for y in range(22, 31): it.px(x0, y, '#6B4A30'); it.px(x1, y, '#6B4A30')
    return it


@gear('sword', 'hand')
def g_sword(sex, ctx):
    it = Item()
    x0, y0, x1, y1 = hand_box(sex, ctx['sleeve'])[1]
    cx = x0 + 1
    it.rect(cx, y0 - 15, cx, y0 - 2, '#DDE1EE'); it.px(cx, y0 - 16, '#F4F4FA')
    it.rect(cx + 1, y0 - 14, cx + 1, y0 - 2, '#A8ACC4')
    it.rect(x0 - 1, y0 - 1, x1 + 1, y0 - 1, GOLD); it.px(x0 - 1, y0 - 1, GOLD_D)
    it.rect(x0, y0, x1, y1, ctx['skin']); it.px(cx, y1 + 1, GOLD)
    return it


@gear('dumbbell', 'hand')
def g_dumbbell(sex, ctx):
    it = Item()
    x0, y0, x1, y1 = hand_box(sex, ctx['sleeve'])[1]
    it.rect(x0 - 3, y0 + 1, x1 + 3, y0 + 1, '#6A6F90')
    for xa in (x0 - 4, x1 + 3):
        it.rect(xa, y0 - 1, xa + 1, y0 + 3, '#9AA0C0'); it.px(xa, y0 - 1, '#C9CBDD')
    it.rect(x0, y0, x1, y1, ctx['skin'])
    return it


@gear('crown', 'top')
def g_crown(sex, ctx):
    it = Item()
    it.rect(11, 2, 20, 3, GOLD); it.rect(11, 3, 20, 3, GOLD_D)
    for x in (11, 14, 17, 20): it.px(x, 1, GOLD)
    it.rect(15, 0, 16, 1, GOLD); it.px(15, 2, '#C4473F'); it.px(13, 2, '#5A9ADA'); it.px(18, 2, '#5FA37E')
    return it


@gear('wreath', 'top')
def g_wreath(sex, ctx):
    it = Item(); it.plain = True
    for x in range(7, 25):
        it.px(x, 4 + (1 if x in (7, 8, 23, 24) else 0), '#81B29A' if x % 2 else '#5F9A7E')
    for x in (7, 24): it.px(x, 6, '#81B29A'); it.px(x, 7, '#5F9A7E')
    for x in range(8, 24, 3): it.px(x, 3, '#81B29A')
    it.px(15, 3, GOLD); it.px(16, 3, GOLD)
    return it


def apply_gear(cv, gid, sex, ctx):
    g = GEAR32[gid]; it = g['fn'](sex, ctx)
    if not g['behind']:
        it.apply(cv); return
    tmp = Canvas(cv.w, cv.h); it.apply(tmp)
    for y in range(cv.h):
        for x in range(cv.w):
            if tmp.g[y][x] != '.' and cv.g[y][x] == '.': cv.g[y][x] = tmp.g[y][x]
