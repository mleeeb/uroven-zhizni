"""Народные наряды, волна 3: мексиканский и китайский."""
from outfit import item, geo, hands, long_top, short_top, pants, hand_box
from px32 import Item, shade, K
from w_top import floor_coat
from w_low import bare_feet
from w_fest import fist

W, Wd = '#F4F1DE', '#C9CBDD'
GOLD, GOLD_D = '#F2CC8F', '#C9A15F'
SILVER = '#DDE1EE'


# ---------------- мексиканский ----------------
@item('head', 'Венок из цветов', 'мексиканский')
def flower_crown(sex, ctx):
    it = Item()
    it.rect(7, 7, 24, 7, '#4E8E6A')
    for cx, c in ((8, '#E0473F'), (12, '#F2CC8F'), (16, '#E8607A'), (20, '#E8783A'), (24, '#B794E0')):
        it.rect(cx - 1, 4, cx + 1, 6, c); it.px(cx, 3, c); it.px(cx, 5, GOLD if c != '#F2CC8F' else '#E8783A')
        it.px(cx + 1, 6, shade(c, 0.78))
    for x in (10, 14, 18, 22): it.px(x, 6, '#5FA37E'); it.px(x, 5, '#4E8E6A')
    return it


@item('top', 'Костюм чарро', 'мексиканский', sleeve='long')
def charro(sex, ctx):
    B, Bd = '#1E1A22', '#2E2836'
    it = Item()
    g = long_top(it, sex, B, hem=29, Cd=Bd)
    it.rect(g['bx0'] + 1, 30, g['bx1'] - 1, 31, W); it.rect(g['bx0'] + 1, 31, g['bx1'] - 1, 31, Wd)
    it.rect(14, 21, 17, 29, W)
    it.rect(13, 22, 18, 22, '#C4473F'); it.px(12, 23, '#C4473F'); it.px(19, 23, '#C4473F')
    for y in (24, 26, 28):
        it.px(12, y, SILVER); it.px(19, y, SILVER)
    for side in (g['sl'], g['sr']):
        for x in range(side[0], side[1] + 1, 2): it.px(x, 24, SILVER)
        it.rect(side[0], 28, side[1], 28, SILVER)
    hands(it, sex, ctx['skin'])
    return it


@item('bottom', 'Брюки чарро', 'мексиканский')
def charro_pants(sex, ctx):
    it = Item()
    pants(it, '#1E1A22', '#2E2836')
    for y in range(33, 39, 2): it.px(9, y, SILVER); it.px(22, y, SILVER)
    it.rect(9, 32, 22, 32, '#C4473F')
    return it


@item('top', 'Платье с вышивкой', 'мексиканский', long=True, only='f')
def poblana(sex, ctx):
    R, Rd, G = '#B8343A', '#8E2830', '#2E8C5A'
    it = Item()
    short_top(it, sex, W, hem=29, Cd=Wd)
    for x in range(9, 23):
        it.px(x, 23, ['#E0473F', '#F2CC8F', '#2E8C5A', '#5A9ADA'][x % 4])
    for x, y, c in ((13, 25, '#E8607A'), (18, 25, '#F2CC8F'), (15, 27, '#5A9ADA'), (8, 25, '#E0473F'), (23, 25, '#2E8C5A')):
        it.px(x, y, c); it.px(x + 1, y, c)
    it.rect(11, 30, 20, 31, G)
    it.rect(10, 32, 21, 35, R); it.rect(9, 36, 22, 38, R); it.rect(8, 39, 23, 40, R)
    it.rect(20, 32, 21, 40, Rd); it.rect(22, 36, 23, 40, Rd)
    for (x, y) in list(it.c):
        if y >= 32 and (x * 3 + y) % 7 == 0: it.px(x, y, GOLD)
    for x in range(8, 24): it.px(x, 37, G if x % 2 else GOLD)
    return it


@item('neck', 'Ребосо', 'мексиканский')
def rebozo(sex, ctx):
    cols = ['#6B4430', '#2E8C86', '#E8C547', '#6B4430', '#C4473F']
    it = Item()
    g = geo(sex)
    x0, x1 = g['ssl'][0], g['ssr'][1]
    for y in range(22, 25):
        for x in range(x0, x1 + 1): it.px(x, y, cols[(x // 2) % 5])
    for y in range(25, 33):
        for x in (x0, x0 + 1, x1 - 1, x1): it.px(x, y, cols[(y // 2) % 5])
    for x in (x0, x1): it.px(x, 33, '#6B4430')
    it.rect(14, 21, 17, 21, cols[1])
    it.no_outline.update({(x, 20) for x in range(9, 23)})
    return it


@item('shoes', 'Уарачи', 'мексиканский')
def huaraches(sex, ctx):
    L, Ld = '#A8784A', '#86603A'
    it = Item()
    bare_feet(it, ctx['skin'])
    it.rect(8, 42, 14, 42, Ld); it.rect(17, 42, 24, 42, Ld)
    for x in range(9, 14): it.px(x, 40 + (x % 2), L)
    for x in range(18, 23): it.px(x, 40 + (x % 2), L)
    it.rect(9, 39, 13, 39, L); it.rect(18, 39, 22, 39, L)
    return it


@item('hands', 'Гитара', 'мексиканский')
def guitar(sex, ctx):
    it = Item()
    x0, y0, x1, y1 = fist(it, sex, ctx)
    bx, by = x0 - 2, y0 + 1
    it.rect(bx, by, bx + 5, by + 5, '#C9853A'); it.rect(bx + 1, by - 2, bx + 4, by - 1, '#C9853A')
    it.erase(bx, by + 5); it.erase(bx + 5, by + 5)
    it.rect(bx + 2, by + 1, bx + 3, by + 2, '#3A2420')
    it.rect(bx + 5, by - 1, bx + 5, by + 4, '#A06A2A')
    for k in range(9): it.px(bx + 3 + k // 2, by - 3 - k, '#6B4430')
    it.rect(bx + 7, by - 13, bx + 8, by - 11, '#3A2420')
    it.rect(x0, y0, x1, y0 + 1, ctx['skin'])
    return it


# ---------------- китайский ----------------
@item('top', 'Ханьфу', 'китайский', long=True, sleeve='long')
def hanfu(sex, ctx):
    if sex == 'm':
        C, Cd, Col, Sash = '#3D7A7A', '#2E6060', '#E8E6DA', '#1E3A3A'
    else:
        C, Cd, Col, Sash = '#E8A0B8', '#C27898', W, '#B8343A'
    it = Item()
    g = floor_coat(it, sex, C, Cd)
    sl, sr = ((3, 8), (23, 28)) if sex == 'm' else ((4, 9), (22, 27))
    it.rect(sl[0], 23, sl[1], 32, C); it.rect(sr[0], 23, sr[1], 32, Cd)
    it.rect(sl[0], 32, sl[1], 32, Col); it.rect(sr[0], 32, sr[1], 32, Col)
    for y in range(25, 32): it.line(sl[1] + 1, y); it.line(sr[0] - 1, y)
    for i, y in enumerate(range(21, 29)):
        it.px(18 - i, y, Col); it.px(17 - i, y, Col)
    it.rect(14, 21, 16, 21, Col)
    it.rect(g['bx0'], 29, g['bx1'], 30, Sash); it.rect(15, 31, 15, 35, Sash); it.rect(17, 31, 17, 34, Sash)
    for x in range(g['bx0'] - 1, g['bx1'] + 2): it.px(x, 40, Col)
    hands(it, sex, ctx['skin'])
    return it


@item('head', 'Шапочка с узелком', 'китайский', only='m')
def skullcap(sex, ctx):
    B, Bd = '#1E1A22', '#2E2836'
    it = Item()
    it.rect(11, 3, 20, 3, B); it.rect(9, 4, 22, 8, B)
    for x in (12, 16, 20): it.rect(x, 4, x, 8, Bd)
    it.rect(9, 8, 22, 8, Bd)
    it.rect(15, 1, 16, 2, '#C4473F'); it.px(15, 1, '#E8706A')
    return it


@item('head', 'Шпилька с подвесками', 'китайский', only='f')
def buyao(sex, ctx):
    it = Item()
    it.rect(20, 5, 24, 5, GOLD); it.rect(21, 4, 23, 6, GOLD); it.px(22, 5, '#C4473F')
    for k, x in enumerate((21, 23, 25)):
        for y in range(7, 11 + k): it.px(x, y, GOLD_D)
        it.px(x, 11 + k, '#C4473F')
    it.rect(7, 6, 9, 8, '#E8A0B8'); it.px(8, 7, GOLD)
    it.no_outline.update({(x, y) for x in range(19, 27) for y in range(6, 14)})
    return it


@item('hands', 'Веер', 'китайский')
def fan(sex, ctx):
    it = Item()
    x0, y0, x1, y1 = fist(it, sex, ctx)
    cx, cy = x0 + 1, y0
    for y in range(cy - 7, cy):
        half = (cy - y) if cy - y < 5 else 9 - (cy - y)
        half = max(1, min(4, cy - y))
        for x in range(cx - half, cx + half + 1):
            it.px(x, y, '#C4473F' if (x - cx) % 2 else '#E0473F')
    for x in range(cx - 4, cx + 5): it.px(x, cy - 7, GOLD)
    it.px(cx, cy - 1, GOLD_D)
    for x, y in ((cx - 1, cy - 5), (cx + 2, cy - 4)): it.px(x, y, GOLD)
    return it


@item('hands', 'Красный фонарик', 'китайский')
def lantern(sex, ctx):
    it = Item()
    x0, y0, x1, y1 = fist(it, sex, ctx)
    cx = x0 + 1
    for y in range(y0 - 8, y0): it.px(cx, y, '#8A6A3B')
    for k in range(4): it.px(cx + 1 + k, y0 - 8 - (k % 2), '#8A6A3B')
    lx, ly = cx + 4, y0 - 6
    it.px(lx, ly, GOLD); it.rect(lx - 2, ly + 1, lx + 2, ly + 5, '#D9343A'); it.rect(lx - 1, ly + 1, lx + 1, ly + 1, GOLD)
    it.rect(lx - 1, ly + 5, lx + 1, ly + 5, GOLD); it.px(lx - 1, ly + 2, '#F08A80')
    it.px(lx, ly + 6, GOLD_D); it.px(lx, ly + 7, GOLD_D)
    return it


@item('shoes', 'Тканевые туфли', 'китайский')
def cloth_shoes(sex, ctx):
    it = Item()
    it.rect(9, 40, 14, 41, '#1E1A22'); it.rect(17, 40, 22, 41, '#1E1A22')
    it.rect(7, 41, 8, 41, '#1E1A22'); it.rect(23, 41, 24, 41, '#1E1A22')
    it.rect(7, 42, 14, 42, W); it.rect(17, 42, 24, 42, W)
    it.rect(9, 39, 14, 39, ctx['skin']) if False else None
    for y in range(40, 43): it.line(15, y); it.line(16, y)
    it.rect(9, 39, 14, 39, W); it.rect(17, 39, 22, 39, W)
    return it
