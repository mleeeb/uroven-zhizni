"""Праздники: 8 Марта, 1 Сентября, День космонавтики, Масленица, 23 Февраля, Выпускной, Карнавал."""
from outfit import item, geo, hands, long_top, short_top, pants, hand_box
from px32 import Item, shade, K
from w_top import floor_coat
from w_low import legs_below, LEGS

W, Wd = '#F4F1DE', '#C9CBDD'
GOLD, GOLD_D = '#F2CC8F', '#C9A15F'
GREEN, GREEN_D = '#5FA37E', '#417A5C'
MIMOSA, MIMOSA_D = '#F2D64A', '#C9AE2A'


def right_hand(sex, ctx):
    return hand_box(sex, ctx['sleeve'])[1]


def fist(it, sex, ctx):
    """Кулак поверх правой кисти, чтобы предмет был «в руке»."""
    x0, y0, x1, y1 = right_hand(sex, ctx)
    it.rect(x0, y0 + 1, x1, y1, ctx['skin']); it.px(x0 + 1, y1, shade(ctx['skin'], 0.86))
    return x0, y0, x1, y1


def short_dress(it, sex, ctx, C, Cd, hem=36):
    """Платье до колена: корпус + юбка, ноги ниже подола."""
    it.clear = set(LEGS)
    sk = ctx['skin']
    it.rect(10, hem + 1, 13, 38, sk); it.rect(18, hem + 1, 21, 38, sk)
    for y in range(hem + 1, 39): it.line(14, y); it.line(17, y); it.line(15, y); it.line(16, y)
    it.rect(10, 32, 21, 33, C); it.rect(9, 34, 22, hem, C)
    it.rect(20, 32, 21, hem, Cd); it.rect(22, 34, 22, hem, Cd)


# ---------------- 8 Марта ----------------
@item('head', 'Ободок с мимозой', '8 марта')
def mimosa_band(sex, ctx):
    it = Item()
    it.rect(7, 6, 24, 6, GREEN_D)
    for x, y in ((8, 4), (10, 3), (12, 4), (9, 5), (11, 5), (21, 4), (23, 5), (22, 3), (20, 5)):
        it.rect(x, y, x + 1, y, MIMOSA); it.px(x, y + 1, MIMOSA_D)
    it.px(13, 5, GREEN); it.px(14, 5, GREEN); it.px(19, 4, GREEN); it.px(18, 5, GREEN)
    it.no_outline.update({(x, 7) for x in range(7, 25)})
    return it


@item('hands', 'Букет тюльпанов', '8 марта')
def tulips(sex, ctx):
    it = Item()
    x0, y0, x1, y1 = fist(it, sex, ctx)
    cx = x0 + 1
    for k, dx in enumerate((-2, 0, 2)):
        for y in range(y0 - 5 + abs(dx) // 2, y0 + 1): it.px(cx + dx // 2 + (1 if dx > 0 and y < y0 - 2 else 0) - (1 if dx < 0 and y < y0 - 2 else 0), y, GREEN)
    for fx, fy, c in ((cx - 2, y0 - 8, '#E8607A'), (cx, y0 - 9, '#C4243A'), (cx + 2, y0 - 8, '#F2CC8F')):
        it.rect(fx - 1, fy, fx + 1, fy + 2, c); it.px(fx, fy, shade(c, 1.25)); it.px(fx + 1, fy + 2, shade(c, 0.75))
    it.px(cx - 2, y0 - 3, GREEN_D); it.px(cx + 2, y0 - 4, GREEN_D)
    it.rect(x0 - 1, y0 - 1, x1 + 1, y0, '#E8A0A8')
    return it


@item('hands', 'Веточка мимозы', '8 марта')
def mimosa_branch(sex, ctx):
    it = Item()
    x0, y0, x1, y1 = fist(it, sex, ctx)
    cx = x0 + 1
    for y in range(y0 - 7, y0 + 1): it.px(cx + (y0 - y) // 4, y, GREEN_D)
    for x, y in ((cx - 1, y0 - 8), (cx + 1, y0 - 9), (cx + 3, y0 - 8), (cx, y0 - 6), (cx + 2, y0 - 6), (cx - 1, y0 - 4),
                 (cx + 3, y0 - 5), (cx + 1, y0 - 11), (cx + 2, y0 - 3)):
        it.rect(x, y, x + 1, y + 1, MIMOSA); it.px(x + 1, y + 1, MIMOSA_D)
    it.px(cx - 2, y0 - 6, GREEN); it.px(cx + 4, y0 - 7, GREEN)
    return it


@item('top', 'Весеннее платье', '8 марта', long=True, only='f')
def spring_dress(sex, ctx):
    C, Cd = '#E8A0A8', '#C27880'
    it = Item()
    short_top(it, sex, C, hem=31, Cd=Cd)
    short_dress(it, sex, ctx, C, Cd)
    it.rect(11, 31, 20, 31, '#C4243A')
    for x, y in ((12, 24), (18, 27), (13, 29), (11, 34), (17, 33), (20, 35), (14, 36), (19, 23)):
        it.px(x, y, W); it.px(x + 1, y, MIMOSA)
    return it


@item('top', 'Рубашка с бутоньеркой', '8 марта', sleeve='long')
def boutonniere(sex, ctx):
    it = Item()
    g = long_top(it, sex, W, hem=31, Cd=Wd)
    it.rect(14, 21, 17, 21, Wd)
    for y in range(22, 32): it.px(15, y, Wd)
    for y in (24, 27, 30): it.px(16, y, '#9AA0C0')
    it.rect(18, 23, 19, 24, '#C4243A'); it.px(18, 23, '#E8607A'); it.px(19, 25, GREEN); it.px(18, 25, GREEN_D)
    hands(it, sex, ctx['skin'])
    return it


# ---------------- 1 Сентября ----------------
@item('head', 'Белые банты', '1 сентября')
def bows(sex, ctx):
    it = Item()
    for cx in (6, 25):
        it.rect(cx - 3, 4, cx - 1, 8, W); it.rect(cx + 1, 4, cx + 3, 8, W); it.rect(cx, 5, cx, 7, Wd)
        it.px(cx - 3, 4, Wd); it.px(cx + 3, 8, Wd); it.px(cx - 2, 6, Wd); it.px(cx + 2, 6, Wd)
        it.erase(cx - 3, 8); it.erase(cx + 3, 4)
    return it


@item('top', 'Школьный пиджак', '1 сентября', sleeve='long')
def school_blazer(sex, ctx):
    N, Nd = '#2A3A6B', '#1E2A52'
    it = Item()
    g = long_top(it, sex, N, hem=33, Cd=Nd)
    it.rect(14, 21, 17, 22, W); it.rect(15, 23, 16, 25, W)
    for i in range(6): it.px(13 - i // 3, 21 + i, Nd); it.px(18 + i // 3, 21 + i, Nd)
    it.rect(g['bx0'] + 1, 24, g['bx0'] + 3, 25, GOLD); it.px(g['bx0'] + 2, 24, '#C4473F')
    for y in (27, 30): it.px(16, y, GOLD)
    it.rect(g['bx0'] + 1, 30, g['bx0'] + 3, 30, Nd); it.rect(g['bx1'] - 3, 30, g['bx1'] - 1, 30, Nd)
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Школьное платье с фартуком', '1 сентября', long=True, sleeve='long', only='f')
def school_dress(sex, ctx):
    C, Cd = '#6B4430', '#4E3122'
    it = Item()
    g = long_top(it, sex, C, hem=31, Cd=Cd)
    short_dress(it, sex, ctx, C, Cd)
    it.rect(13, 21, 18, 21, W)
    it.rect(12, 24, 19, 36, W); it.rect(12, 24, 19, 24, Wd)
    for y in range(25, 37, 3): it.px(12, y, Wd); it.px(19, y, Wd)
    for y in range(22, 25): it.px(11, y, W); it.px(20, y, W)
    it.rect(g['sl'][0], 28, g['sl'][1], 28, W); it.rect(g['sr'][0], 28, g['sr'][1], 28, W)
    hands(it, sex, ctx['skin'])
    return it


@item('bottom', 'Школьные брюки', '1 сентября')
def school_pants(sex, ctx):
    it = Item()
    pants(it, '#4A4F6E', '#3A3F5A')
    it.rect(9, 32, 22, 32, '#1E1A22'); it.px(15, 32, '#9AA0C0')
    it.rect(11, 34, 11, 38, '#5A6080'); it.rect(19, 34, 19, 38, '#5A6080')
    return it


@item('bottom', 'Юбка в складку', '1 сентября')
def pleated(sex, ctx):
    N, Nd = '#2A3A6B', '#1E2A52'
    it = Item()
    legs_below(it, 37, ctx['skin'], shade(ctx['skin'], 0.86))
    it.rect(9, 32, 22, 33, N); it.rect(8, 34, 23, 36, N)
    for x in range(9, 24, 2): it.rect(x, 33, x, 36, Nd)
    it.rect(9, 32, 22, 32, Nd)
    return it


@item('hands', 'Букет гладиолусов', '1 сентября')
def gladiolus(sex, ctx):
    it = Item()
    x0, y0, x1, y1 = fist(it, sex, ctx)
    cx = x0 + 1
    for k, (dx, c) in enumerate(((-1, '#E8607A'), (1, W), (3, '#E8943A'))):
        top = y0 - 12 + k
        for y in range(top, y0): it.px(cx + dx // 2, y, GREEN_D if y > y0 - 4 else GREEN)
        for y in range(top, y0 - 4, 2): it.px(cx + dx - 1, y, c); it.px(cx + dx, y + 1, c)
    it.rect(x0 - 1, y0 - 2, x1 + 1, y0, '#E3D3B0')
    return it


@item('shoes', 'Туфли с белыми носками', '1 сентября')
def school_shoes(sex, ctx):
    it = Item()
    it.rect(9, 38, 14, 39, W); it.rect(17, 38, 22, 39, W)
    it.rect(8, 40, 14, 42, '#1E1A22'); it.rect(17, 40, 23, 42, '#1E1A22')
    it.px(10, 40, '#6A6F90'); it.px(19, 40, '#6A6F90')
    for y in range(38, 43): it.line(15, y); it.line(16, y)
    return it


# ---------------- День космонавтики ----------------
@item('head', 'Ретро-шлем', 'день космонавтики')
def retro_helmet(sex, ctx):
    it = Item()
    it.rect(10, 0, 21, 0, W); it.rect(7, 1, 24, 3, W); it.rect(5, 4, 26, 9, W)
    it.rect(5, 10, 9, 20, W); it.rect(22, 10, 26, 20, W); it.rect(6, 21, 25, 22, W)
    it.rect(11, 0, 20, 2, '#C4473F')
    it.rect(7, 4, 24, 4, '#C4473F')
    it.rect(23, 5, 26, 20, Wd); it.rect(5, 10, 6, 18, Wd)
    it.rect(8, 9, 23, 9, '#9AA0C0'); it.rect(9, 10, 9, 20, '#9AA0C0'); it.rect(22, 10, 22, 20, '#9AA0C0')
    it.rect(10, 21, 21, 21, '#9AA0C0')
    it.px(4, 14, '#6A6F90'); it.px(27, 14, '#6A6F90')
    return it


@item('top', 'Оранжевый скафандр', 'день космонавтики', sleeve='long')
def orange_suit(sex, ctx):
    C, Cd = '#E8783A', '#C05A2A'
    it = Item()
    g = long_top(it, sex, C, hem=33, Cd=Cd)
    it.rect(13, 21, 18, 22, '#9AA0C0')
    it.rect(12, 25, 15, 28, W); it.px(13, 26, '#C4473F'); it.px(14, 27, '#3D5A80')
    it.rect(17, 24, 19, 24, '#3D5A80'); it.rect(17, 26, 19, 26, '#3D5A80')
    it.rect(g['bx0'], 31, g['bx1'], 31, '#9AA0C0')
    it.rect(g['sl'][0], 28, g['sl'][1], 28, '#9AA0C0'); it.rect(g['sr'][0], 28, g['sr'][1], 28, '#9AA0C0')
    hands(it, sex, ctx['skin'])
    return it


@item('bottom', 'Оранжевые штаны скафандра', 'день космонавтики')
def orange_pants(sex, ctx):
    it = Item()
    pants(it, '#E8783A', '#C05A2A', wide=1)
    it.rect(8, 32, 23, 32, '#9AA0C0')
    it.rect(9, 35, 13, 35, '#C05A2A'); it.rect(18, 35, 22, 35, '#C05A2A')
    return it


@item('top', 'Футболка с ракетой', 'день космонавтики')
def rocket_tee(sex, ctx):
    N, Nd = '#2A3A6B', '#1E2A52'
    it = Item()
    short_top(it, sex, N, hem=31, Cd=Nd)
    it.rect(15, 24, 16, 28, W); it.px(15, 23, '#C4473F'); it.px(16, 23, '#C4473F')
    it.px(14, 27, '#C4473F'); it.px(17, 27, '#C4473F'); it.px(14, 28, '#C4473F'); it.px(17, 28, '#C4473F')
    it.px(15, 29, '#F2CC8F'); it.px(16, 29, '#E8783A'); it.px(15, 30, '#E8783A')
    it.px(15, 25, '#8FB3E0')
    for x, y in ((12, 24), (19, 25), (13, 29), (19, 29)): it.px(x, y, GOLD)
    return it


@item('head', 'Ободок с планетами', 'день космонавтики')
def planets(sex, ctx):
    it = Item()
    it.rect(7, 6, 24, 6, '#4A4F6E')
    for x in (10, 21):
        it.rect(x, 2, x, 5, '#4A4F6E')
    it.rect(9, 0, 11, 2, '#E8783A'); it.px(9, 0, '#F2A070')
    it.rect(20, 0, 22, 2, '#B794E0'); it.rect(18, 1, 24, 1, GOLD)
    it.no_outline.update({(x, 7) for x in range(7, 25)})
    return it


@item('hands', 'Ракета-игрушка', 'день космонавтики')
def toy_rocket(sex, ctx):
    it = Item()
    x0, y0, x1, y1 = fist(it, sex, ctx)
    cx = x0 + 1
    it.rect(cx - 1, y0 - 7, cx + 1, y0 - 1, W)
    it.px(cx, y0 - 8, '#C4473F'); it.rect(cx - 1, y0 - 7, cx + 1, y0 - 7, '#C4473F')
    it.px(cx, y0 - 5, '#8FB3E0')
    it.px(cx - 2, y0 - 2, '#C4473F'); it.px(cx + 2, y0 - 2, '#C4473F'); it.px(cx - 2, y0 - 1, '#C4473F'); it.px(cx + 2, y0 - 1, '#C4473F')
    return it


# ---------------- Масленица ----------------
@item('head', 'Цветастый платок', 'масленица', only='f')
def pavlov_shawl(sex, ctx):
    R, Rd = '#B8343A', '#8E2830'
    it = Item()
    rows = {3: (10, 21), 4: (8, 23), 5: (7, 24)}
    for y in range(6, 19): rows[y] = (6, 25)
    rows.update({19: (7, 24), 20: (8, 23), 21: (10, 21)})
    for y, (a, b) in rows.items():
        for x in range(a, b + 1):
            if not ((10 <= x <= 21 and 9 <= y <= 19) or (11 <= x <= 20 and y == 20)): it.px(x, y, R)
    for x, y in ((9, 5), (14, 4), (19, 5), (7, 10), (24, 9), (7, 15), (24, 16), (12, 7), (18, 7)):
        it.px(x, y, GOLD); it.px(x + 1, y, '#E8A0A8') if x < 24 else None; it.px(x, y + 1, GREEN)
    it.rect(6, 8, 25, 8, '#1E1A22')
    it.rect(14, 21, 17, 22, R); it.px(15, 22, Rd); it.px(13, 23, R); it.px(18, 23, R); it.px(13, 24, Rd); it.px(18, 24, Rd)
    return it


@item('neck', 'Шаль с бахромой', 'масленица')
def fringe_shawl(sex, ctx):
    C, Cd = '#2A2D45', '#1E2036'
    it = Item()
    g = geo(sex)
    x0, x1 = g['sl'][0], g['sr'][1]
    it.rect(x0, 22, x1, 23, C); it.rect(x0, 24, x1, 25, C)
    for y in range(26, 30):
        a, b = 9 + (y - 26) * 2 + (0 if sex == 'm' else 1), 22 - (y - 26) * 2 - (0 if sex == 'm' else 1)
        it.rect(a, y, b, y, C)
    for x, y in ((8 if sex == 'm' else 9, 23), (13, 24), (18, 24), (23 if sex == 'm' else 22, 23), (15, 27), (12, 26), (19, 26)):
        it.px(x, y, '#C4473F'); it.px(x + 1, y, GOLD)
    for x in range(14, 18): it.px(x, 30, Cd)
    for x in range(x0, x1 + 1, 2): it.px(x, 26, GOLD_D) if x < 9 or x > 22 else None
    it.rect(14, 21, 17, 21, C)
    it.no_outline.update({(x, 20) for x in range(9, 23)})
    return it


@item('top', 'Тулуп', 'масленица', sleeve='long')
def tulup(sex, ctx):
    C, Cd, F = '#A8784A', '#86603A', '#EFE3C6'
    it = Item()
    g = long_top(it, sex, C, hem=37, Cd=Cd)
    it.rect(g['bx0'] - 1, 33, g['bx1'] + 1, 37, C); it.rect(g['bx1'] - 1, 33, g['bx1'] + 1, 37, Cd)
    it.rect(g['bx0'] + 1, 20, g['bx1'] - 1, 22, F); it.rect(15, 23, 16, 37, F)
    it.rect(g['sl'][0], 27, g['sl'][1], 28, F); it.rect(g['sr'][0], 27, g['sr'][1], 28, F)
    it.rect(g['bx0'] - 1, 37, g['bx1'] + 1, 37, F)
    it.rect(g['bx0'], 30, g['bx1'], 31, '#C4473F'); it.px(g['bx0'] + 2, 32, '#C4473F')
    for y in range(23, 37, 3): it.px(12, y, Cd); it.px(19, y, Cd)
    hands(it, sex, ctx['skin'])
    return it


@item('hands', 'Стопка блинов', 'масленица')
def pancakes(sex, ctx):
    it = Item()
    x0, y0, x1, y1 = fist(it, sex, ctx)
    px0 = x0 - 2
    it.rect(px0, y0, px0 + 6, y0, W); it.rect(px0 + 1, y0 + 1, px0 + 5, y0 + 1, Wd)
    for k in range(4):
        it.rect(px0 + 1, y0 - 1 - k, px0 + 5, y0 - 1 - k, '#E8B45A' if k % 2 else '#D9963A')
    it.rect(px0 + 2, y0 - 5, px0 + 4, y0 - 5, '#C4243A'); it.px(px0 + 3, y0 - 6, '#E8607A')
    return it


# ---------------- 23 Февраля ----------------
@item('head', 'Лётный шлем с очками', '23 февраля')
def aviator(sex, ctx):
    L, Ld, Ll = '#6B4430', '#4E3122', '#8A5A3B'
    it = Item()
    it.rect(10, 2, 21, 2, L); it.rect(8, 3, 23, 9, L)
    it.rect(7, 10, 9, 17, L); it.rect(22, 10, 24, 17, L)
    it.rect(10, 2, 14, 2, Ll); it.rect(9, 3, 10, 5, Ll)
    it.rect(21, 3, 23, 9, Ld); it.rect(22, 10, 24, 17, Ld); it.rect(15, 2, 16, 9, Ld)
    it.rect(7, 18, 8, 19, Ld); it.rect(23, 18, 24, 19, Ld)
    for cx in (12, 19):
        it.rect(cx - 2, 5, cx + 2, 8, '#9AA0C0'); it.rect(cx - 1, 6, cx + 1, 7, '#8FC0D8'); it.px(cx - 1, 6, '#E8F4F8')
    it.rect(14, 6, 17, 6, '#9AA0C0')
    return it


@item('top', 'Лётная куртка', '23 февраля', sleeve='long')
def bomber(sex, ctx):
    L, Ld, F = '#6B4430', '#4E3122', '#D9C7A3'
    it = Item()
    g = long_top(it, sex, L, hem=32, Cd=Ld)
    it.rect(g['bx0'] + 1, 20, g['bx1'] - 1, 22, F); it.rect(12, 23, 13, 25, F); it.rect(18, 23, 19, 25, F)
    for y in range(22, 32): it.px(15, y, '#3A281C')
    it.rect(g['bx0'], 31, g['bx1'], 32, '#3A281C')
    it.rect(g['sl'][0], 28, g['sl'][1], 28, '#3A281C'); it.rect(g['sr'][0], 28, g['sr'][1], 28, '#3A281C')
    it.rect(g['bx0'] + 1, 27, g['bx0'] + 3, 27, Ld); it.rect(g['bx1'] - 3, 27, g['bx1'] - 1, 27, Ld)
    hands(it, sex, ctx['skin'])
    return it


@item('neck', 'Белый шарф лётчика', '23 февраля')
def pilot_scarf(sex, ctx):
    it = Item()
    it.rect(11, 21, 20, 22, W); it.rect(12, 23, 14, 24, W)
    it.rect(12, 25, 13, 29, W); it.rect(12, 29, 13, 29, Wd)
    it.rect(18, 21, 20, 22, Wd); it.px(13, 26, Wd)
    it.no_outline.update({(x, 20) for x in range(10, 22)})
    return it


# ---------------- Выпускной ----------------
@item('head', 'Шапочка выпускника', 'выпускной')
def mortarboard(sex, ctx):
    B, Bd = '#1E1A22', '#2E2836'
    it = Item()
    it.rect(4, 2, 27, 3, B); it.rect(6, 1, 25, 1, Bd); it.rect(8, 0, 23, 0, Bd)
    it.rect(9, 4, 22, 7, B); it.rect(19, 4, 22, 7, Bd)
    it.px(15, 1, GOLD); it.px(16, 1, GOLD)
    for x in range(17, 25): it.px(x, 2, GOLD) if x % 2 else None
    it.rect(25, 3, 25, 9, GOLD); it.rect(24, 10, 26, 11, GOLD); it.px(25, 12, GOLD_D)
    return it


@item('top', 'Мантия выпускника', 'выпускной', long=True, sleeve='long')
def gown(sex, ctx):
    B, Bd = '#1E1A22', '#2E2836'
    it = Item()
    g = floor_coat(it, sex, B, Bd)
    it.rect(g['sl'][0] - 1, 25, g['sl'][1], 30, B); it.rect(g['sr'][0], 25, g['sr'][1] + 1, 30, Bd)
    it.rect(13, 21, 18, 23, '#3D5A80'); it.rect(14, 22, 17, 23, '#F2CC8F')
    for y in range(24, 41): it.px(15, y, Bd); it.px(16, y, Bd)
    hands(it, sex, ctx['skin'])
    return it


@item('neck', 'Лента выпускника', 'выпускной')
def grad_ribbon(sex, ctx):
    it = Item(); it.plain = True
    for y in range(22, 33):
        x0 = (10 if sex == 'm' else 11) + (y - 22)
        it.px(x0, y, '#C4473F'); it.px(x0 + 1, y, W); it.px(x0 + 2, y, '#3D5A80')
        it.px(x0 - 1, y, K); it.px(x0 + 3, y, K)
        if y % 3 == 0: it.px(x0 + 1, y, GOLD)
    return it


@item('top', 'Смокинг', 'выпускной', sleeve='long')
def tuxedo(sex, ctx):
    B, Bd = '#1E1A22', '#2E2836'
    it = Item()
    g = long_top(it, sex, B, hem=33, Cd=Bd)
    it.rect(13, 21, 18, 23, W); it.rect(14, 24, 17, 26, W); it.rect(15, 27, 16, 28, W)
    for i in range(7): it.px(13 - i // 3, 21 + i, '#3A3646'); it.px(18 + i // 3, 21 + i, '#3A3646')
    it.rect(13, 21, 14, 22, '#1E1A22'); it.rect(17, 21, 18, 22, '#1E1A22'); it.rect(15, 21, 16, 22, '#2E2836')
    it.px(15, 25, '#1E1A22'); it.px(15, 27, '#1E1A22'); it.px(16, 30, '#9AA0C0')
    it.px(g['bx0'] + 2, 24, W)
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Вечернее платье', 'выпускной', long=True, only='f')
def evening_gown(sex, ctx):
    C, Cd, S = '#3D5A9A', '#2E4478', '#B8C8F0'
    it = Item()
    it.rect(11, 22, 20, 31, C); it.rect(10, 32, 21, 35, C); it.rect(9, 36, 22, 38, C); it.rect(8, 39, 23, 40, C)
    it.rect(12, 21, 13, 21, C); it.rect(18, 21, 19, 21, C)
    it.rect(19, 23, 20, 31, Cd); it.rect(20, 32, 21, 40, Cd); it.rect(22, 36, 23, 40, Cd)
    for (x, y) in list(it.c):
        if (x * 7 + y * 3) % 11 == 0: it.px(x, y, S)
    it.rect(11, 30, 20, 30, '#C9CBDD')
    it.clear = {(x, y) for y in range(22, 27) for x in range(5, 27)}
    sk = ctx['skin']
    it.rect(9, 22, 10, 23, sk); it.rect(21, 22, 22, 23, sk)
    it.rect(7, 24, 9, 30, sk); it.rect(22, 24, 24, 30, sk)
    it.rect(14, 22, 17, 22, sk)
    for y in range(24, 31): it.line(10, y); it.line(21, y)
    it.no_outline.update({(x, 21) for x in range(9, 23)} | {(x, 20) for x in range(8, 24)})
    return it


@item('hands', 'Диплом', 'выпускной')
def diploma(sex, ctx):
    it = Item()
    x0, y0, x1, y1 = fist(it, sex, ctx)
    it.rect(x0 - 3, y0, x1 + 3, y0 + 1, W); it.rect(x0 - 3, y0 + 1, x1 + 3, y0 + 1, Wd)
    it.px(x0 - 4, y0, Wd); it.px(x1 + 4, y0, Wd); it.px(x0 - 4, y0 + 1, Wd); it.px(x1 + 4, y0 + 1, Wd)
    it.rect(x0 + 1, y0, x0 + 1, y0 + 1, '#C4473F')
    return it


# ---------------- Карнавал ----------------
@item('head', 'Корона из перьев', 'карнавал')
def feather_crown(sex, ctx):
    cols = ['#E8607A', '#F2CC8F', '#5FA37E', '#8FB3E0', '#B794E0', '#E8783A']
    it = Item()
    it.rect(7, 6, 24, 8, GOLD); for_ = [it.px(x, 7, '#C4243A' if x % 3 == 0 else GOLD_D) for x in range(8, 24)]
    for i, x in enumerate(range(6, 26, 2)):
        h = 6 - abs(x - 15.5) // 2
        c = cols[i % 6]
        for y in range(int(6 - h), 6): it.px(x, y, c); it.px(x + 1, y, shade(c, 0.8))
    it.px(15, 7, '#8FB3E0'); it.px(16, 7, '#8FB3E0')
    return it


@item('top', 'Костюм с пайетками', 'карнавал')
def sequins(sex, ctx):
    C, Cd = '#C2306A', '#962250'
    it = Item()
    short_top(it, sex, C, hem=31, Cd=Cd)
    for (x, y) in list(it.c):
        if (x + y) % 3 == 0: it.px(x, y, '#F2CC8F')
        elif (x * 2 + y) % 5 == 0: it.px(x, y, '#E8A0C0')
    g = geo(sex)
    for x in range(11 if sex == 'f' else 9, (20 if sex == 'f' else 22) + 1):
        it.px(x, 31, GOLD if x % 2 else '#8FB3E0')
    return it


@item('neck', 'Боа из перьев', 'карнавал')
def boa(sex, ctx):
    P, Pd, Pl = '#E8A0C0', '#C27898', '#F8C8DC'
    it = Item()
    g = geo(sex)
    for x in range(10, 22):
        it.px(x, 21 + (x % 2), P); it.px(x, 22 - (x % 2), Pl); it.px(x, 23, Pd if x % 3 else P)
    for y in range(24, 32):
        for x0 in (11, 19):
            it.px(x0 + (y % 2), y, P); it.px(x0 + 1 - (y % 2), y, Pd)
    it.no_outline.update({(x, 21) for x in range(9, 23)} | {(x, 20) for x in range(9, 23)})
    return it


@item('hands', 'Маракасы', 'карнавал')
def maracas(sex, ctx):
    it = Item()
    for i, (x0, y0, x1, y1) in enumerate(hand_box(sex, ctx['sleeve'])):
        it.rect(x0, y0 + 1, x1, y1, ctx['skin'])
        c = '#E8783A' if i == 0 else '#5FA37E'
        it.rect(x0 + 1, y0 - 2, x0 + 1, y0, '#8A6A3B')
        it.rect(x0, y0 - 6, x1, y0 - 3, c); it.px(x0 + 1, y0 - 7, c)
        it.px(x0, y0 - 5, GOLD); it.px(x1, y0 - 4, W); it.px(x0 + 1, y0 - 6, shade(c, 1.25))
    return it


@item('bottom', 'Юбка с воланами', 'карнавал')
def ruffle_skirt(sex, ctx):
    it = Item()
    legs_below(it, 38, ctx['skin'], shade(ctx['skin'], 0.86))
    for k, (y, c) in enumerate(((32, '#C2306A'), (33, '#C2306A'), (34, '#F2CC8F'), (35, '#F2CC8F'),
                                 (36, '#5FA37E'), (37, '#5FA37E'))):
        it.rect(9 - k // 2, y, 22 + k // 2, y, c)
    for y in (33, 35, 37):
        for x in range(7, 25, 2): it.px(x, y, shade(it.c.get((x, y), '#C2306A'), 0.8)) if (x, y) in it.c else None
    return it
