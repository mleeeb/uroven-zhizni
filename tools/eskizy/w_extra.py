"""Волна 3 (по предложению): профессии, спорт, сказка."""
from outfit import item, geo, hands, long_top, short_top, pants
from px32 import Item, shade, K
from w_top import floor_coat
from w_low import legs_below, boot

W, Wd = '#F4F1DE', '#C9CBDD'
GOLD, GOLD_D = '#F2CC8F', '#C9A15F'
HIVIS = '#E8D83A'


# ---------------- профессии ----------------
@item('head', 'Поварской колпак', 'профессии')
def chef_hat(sex, ctx):
    it = Item()
    for cx in (11, 16, 21): it.rect(cx - 3, 0, cx + 2, 4, W)
    it.rect(9, 2, 22, 6, W); it.rect(9, 7, 22, 9, W)
    for x in (12, 17): it.rect(x, 1, x, 5, Wd)
    it.rect(9, 7, 22, 7, Wd); it.rect(20, 2, 22, 9, Wd)
    return it


@item('top', 'Поварской китель', 'профессии', sleeve='long')
def chef_jacket(sex, ctx):
    it = Item()
    g = long_top(it, sex, W, hem=33, Cd=Wd)
    it.rect(13, 21, 18, 21, Wd)
    for y in (24, 27, 30): it.px(12, y, '#4A4F6E'); it.px(19, y, '#4A4F6E')
    for y in range(22, 34): it.px(16, y, Wd)
    it.px(g['bx0'] + 1, 25, '#C4473F'); it.px(g['bx0'] + 2, 25, '#3D5A80')
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Халат врача', 'профессии', sleeve='long')
def doctor(sex, ctx):
    it = Item()
    g = long_top(it, sex, W, hem=37, Cd=Wd)
    it.rect(g['bx0'] - 1, 33, g['bx1'] + 1, 37, W); it.rect(g['bx1'] - 1, 33, g['bx1'] + 1, 37, Wd)
    it.rect(14, 21, 17, 24, '#5A9AB0')
    for i in range(5): it.px(13 - i // 3, 21 + i, Wd); it.px(18 + i // 3, 21 + i, Wd)
    for y in range(25, 38): it.px(15, y, Wd)
    it.rect(g['bx0'] + 1, 31, g['bx0'] + 3, 31, Wd); it.rect(g['bx1'] - 3, 31, g['bx1'] - 1, 31, Wd)
    it.rect(g['bx1'] - 3, 24, g['bx1'] - 2, 25, '#3D5A80'); it.px(g['bx1'] - 2, 23, '#C4473F')
    hands(it, sex, ctx['skin'])
    return it


@item('neck', 'Стетоскоп', 'профессии')
def stethoscope(sex, ctx):
    it = Item(); it.plain = True
    for y in range(22, 28): it.px(12 + (y - 22) // 3, y, '#4A4F6E'); it.px(19 - (y - 22) // 3, y, '#4A4F6E')
    for x in range(13, 19): it.px(x, 28, '#4A4F6E')
    it.rect(16, 29, 17, 30, '#9AA0C0'); it.px(16, 29, '#DDE1EE')
    return it


@item('head', 'Каска пожарного', 'профессии')
def fire_helmet(sex, ctx):
    R, Rd = '#C4473F', '#9A3530'
    it = Item()
    it.rect(11, 1, 20, 1, R); it.rect(9, 2, 22, 7, R); it.rect(15, 0, 16, 7, GOLD)
    it.rect(10, 2, 13, 3, shade(R, 1.25)); it.rect(20, 2, 22, 7, Rd)
    it.rect(5, 8, 26, 8, R); it.rect(4, 9, 27, 9, Rd); it.rect(24, 9, 28, 10, Rd)
    it.rect(14, 4, 17, 6, GOLD); it.px(15, 5, '#C4473F')
    return it


@item('top', 'Куртка пожарного', 'профессии', sleeve='long')
def fire_jacket(sex, ctx):
    C, Cd = '#2A2D45', '#1E2036'
    it = Item()
    g = long_top(it, sex, C, hem=34, Cd=Cd)
    for y in (27, 32):
        it.rect(g['bx0'], y, g['bx1'], y, HIVIS)
    it.rect(g['sl'][0], 26, g['sl'][1], 26, HIVIS); it.rect(g['sr'][0], 26, g['sr'][1], 26, HIVIS)
    for y in range(21, 35): it.px(15, y, '#4A4F6E')
    for y in (23, 29): it.px(16, y, GOLD)
    it.rect(12, 21, 19, 21, '#3A3F63')
    hands(it, sex, ctx['skin'])
    return it


@item('head', 'Строительная каска', 'профессии')
def hard_hat(sex, ctx):
    Y, Yd = '#E8A03A', '#C0802A'
    it = Item()
    it.rect(11, 1, 20, 1, Y); it.rect(9, 2, 22, 6, Y); it.rect(15, 1, 16, 6, Yd)
    it.rect(10, 2, 13, 2, shade(Y, 1.2)); it.rect(20, 2, 22, 6, Yd)
    it.rect(6, 7, 25, 8, Y); it.rect(6, 8, 25, 8, Yd)
    return it


@item('top', 'Светоотражающий жилет', 'профессии')
def hivis(sex, ctx):
    it = Item()
    short_top(it, sex, '#6A7C98', hem=31, Cd='#55657E')
    x0, x1 = (9, 22) if sex == 'm' else (11, 20)
    for y in range(22, 32):
        for x in range(x0, x1 + 1):
            if not (14 <= x <= 17 and y < 25): it.px(x, y, '#E8783A' if (x + y) % 9 else '#C05A2A')
    for y in (26, 29): it.rect(x0, y, x1, y, '#E8E6DA')
    return it


@item('top', 'Фартук художника', 'профессии')
def painter(sex, ctx):
    it = Item()
    short_top(it, sex, '#3D5A80', hem=31, Cd='#2E4466')
    it.rect(12, 23, 19, 34, '#E3D3B0'); it.rect(12, 23, 19, 23, '#C9B48A')
    it.rect(13, 21, 13, 22, '#C9B48A'); it.rect(18, 21, 18, 22, '#C9B48A')
    for x, y, c in ((13, 25, '#E0473F'), (17, 27, '#5A9ADA'), (14, 30, '#F2CC8F'), (18, 32, '#5FA37E'), (16, 24, '#B794E0')):
        it.px(x, y, c); it.px(x + 1, y, c); it.px(x, y + 1, c)
    it.rect(14, 29, 17, 30, '#C9B48A')
    return it


# ---------------- спорт ----------------
@item('top', 'Футбольная форма', 'спорт')
def jersey(sex, ctx):
    C, Cd = '#3D82C0', '#2E68A0'
    it = Item()
    g = short_top(it, sex, C, hem=31, Cd=Cd)
    for y in range(22, 32): it.px(12, y, W); it.px(19, y, W)
    it.rect(14, 21, 17, 21, W)
    it.rect(15, 25, 16, 28, W); it.px(14, 25, W); it.px(17, 28, W)
    return it


@item('bottom', 'Футбольные шорты', 'спорт')
def football_shorts(sex, ctx):
    it = Item()
    legs_below(it, 36, ctx['skin'], shade(ctx['skin'], 0.86))
    pants(it, W, Wd, bottom=35)
    it.rect(9, 35, 14, 35, '#3D82C0'); it.rect(17, 35, 22, 35, '#3D82C0')
    return it


@item('shoes', 'Гетры и бутсы', 'спорт', tall=True)
def cleats(sex, ctx):
    it = Item()
    it.rect(9, 36, 14, 39, '#3D82C0'); it.rect(17, 36, 22, 39, '#3D82C0')
    it.rect(9, 37, 14, 37, W); it.rect(17, 37, 22, 37, W)
    it.rect(8, 40, 14, 41, '#1E1A22'); it.rect(17, 40, 23, 41, '#1E1A22')
    it.rect(10, 40, 12, 40, '#E8D83A'); it.rect(19, 40, 21, 40, '#E8D83A')
    for x in (8, 10, 13, 17, 20, 23): it.px(x, 42, '#9AA0C0')
    for y in range(36, 43): it.line(15, y); it.line(16, y)
    return it


@item('head', 'Хоккейный шлем', 'спорт')
def hockey_helmet(sex, ctx):
    C, Cd = '#C4473F', '#9A3530'
    it = Item()
    it.rect(10, 2, 21, 2, C); it.rect(8, 3, 23, 9, C); it.rect(7, 10, 9, 15, C); it.rect(22, 10, 24, 15, C)
    it.rect(20, 3, 23, 9, Cd); it.rect(22, 10, 24, 15, Cd)
    for x in range(10, 22, 3): it.rect(x, 4, x, 5, Cd)
    for y in range(11, 19, 2):
        for x in range(10, 22): it.px(x, y, '#9AA0C0')
    for x in range(11, 21, 3):
        for y in range(10, 19): it.px(x, y, '#9AA0C0')
    it.plain_cells = True
    return it


@item('top', 'Хоккейный свитер', 'спорт', sleeve='long')
def hockey_jersey(sex, ctx):
    C, Cd = '#C4473F', '#9A3530'
    it = Item()
    g = long_top(it, sex, C, hem=34, Cd=Cd)
    it.rect(g['bx0'] - 1, 31, g['bx1'] + 1, 34, C)
    for y in (32, 33): it.rect(g['bx0'] - 1, y, g['bx1'] + 1, y, W if y == 32 else '#2A3A7A')
    it.rect(g['sl'][0], 26, g['sl'][1], 27, W); it.rect(g['sr'][0], 26, g['sr'][1], 27, W)
    it.rect(13, 21, 18, 21, W)
    it.rect(14, 24, 17, 28, W); it.rect(15, 25, 16, 27, C)
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Кимоно для карате', 'спорт', sleeve='long')
def karate(sex, ctx):
    it = Item()
    g = long_top(it, sex, W, hem=33, Cd=Wd)
    for x, y in ((17, 21), (17, 22), (16, 23), (15, 24), (14, 25), (13, 26), (12, 27)): it.px(x, y, Wd)
    it.rect(14, 21, 16, 22, ctx['skin']); it.px(15, 23, ctx['skin'])
    it.rect(g['bx0'], 29, g['bx1'], 30, '#1E1A22')
    it.rect(13, 31, 13, 33, '#1E1A22'); it.rect(17, 31, 17, 33, '#1E1A22')
    hands(it, sex, ctx['skin'])
    return it


# ---------------- сказка ----------------
@item('head', 'Корона', 'сказка')
def crown(sex, ctx):
    it = Item()
    it.rect(8, 4, 23, 7, GOLD); it.rect(8, 7, 23, 7, GOLD_D)
    for x in (8, 12, 15, 16, 19, 23):
        it.rect(x, 1, x, 3, GOLD)
    it.px(8, 0, GOLD); it.px(23, 0, GOLD); it.rect(15, 0, 16, 0, GOLD)
    it.px(11, 5, '#C4473F'); it.rect(15, 5, 16, 5, '#5A9ADA'); it.px(20, 5, '#5FA37E')
    it.px(15, 4, '#FFF6D8')
    return it


@item('top', 'Королевская мантия', 'сказка', long=True, sleeve='long')
def royal_robe(sex, ctx):
    R, Rd = '#7A2A5A', '#5A1E44'
    it = Item()
    g = floor_coat(it, sex, R, Rd)
    it.rect(g['bx0'] - 2, 22, g['bx1'] + 2, 24, W)
    for x in range(g['bx0'] - 2, g['bx1'] + 3, 3): it.px(x, 23, '#1E1A22')
    it.rect(15, 25, 16, 40, W)
    for y in range(26, 41, 3): it.px(15, y, '#1E1A22')
    it.rect(g['bx0'] - 1, 40, g['bx1'] + 1, 40, W)
    it.rect(g['bx0'], 30, g['bx1'], 30, GOLD)
    hands(it, sex, ctx['skin'])
    return it


@item('head', 'Шляпа волшебника', 'сказка')
def wizard_hat(sex, ctx):
    C, Cd = '#2E3A8A', '#1E2A6A'
    it = Item()
    rows = {0: (17, 18), 1: (16, 18), 2: (15, 19), 3: (14, 19), 4: (13, 20), 5: (12, 21), 6: (11, 21), 7: (10, 22)}
    for y, (a, b) in rows.items(): it.rect(a, y, b, y, C); it.px(b, y, Cd)
    it.rect(4, 8, 27, 8, C); it.rect(3, 9, 28, 9, Cd)
    for x, y in ((14, 5), (18, 2), (12, 7), (19, 6)): it.px(x, y, GOLD)
    it.rect(16, 3, 16, 3, '#FFF6D8')
    return it


@item('top', 'Мантия волшебника', 'сказка', long=True, sleeve='long')
def wizard_robe(sex, ctx):
    C, Cd = '#2E3A8A', '#1E2A6A'
    it = Item()
    g = floor_coat(it, sex, C, Cd)
    it.rect(g['sl'][0] - 1, 26, g['sl'][1], 31, C); it.rect(g['sr'][0], 26, g['sr'][1] + 1, 31, Cd)
    for x, y in ((11, 26), (19, 29), (12, 34), (18, 37), (14, 38), (20, 33)):
        it.px(x, y, GOLD); it.px(x - 1, y, GOLD_D); it.px(x + 1, y, GOLD_D); it.px(x, y - 1, GOLD_D)
    it.rect(g['bx0'], 30, g['bx1'], 30, '#B794E0')
    hands(it, sex, ctx['skin'])
    return it


@item('head', 'Рыцарский шлем', 'сказка')
def knight(sex, ctx):
    S, Sd, Sl = '#B8BCD0', '#8E92A8', '#DDE1EE'
    it = Item()
    it.rect(10, 1, 21, 1, S); it.rect(8, 2, 23, 20, S)
    it.rect(9, 2, 12, 4, Sl); it.rect(20, 2, 23, 20, Sd)
    it.rect(10, 11, 21, 12, '#1E1A22'); it.rect(15, 13, 16, 18, Sd)
    for y in (15, 17): it.rect(11, y, 13, y, Sd); it.rect(18, y, 20, y, Sd)
    it.rect(15, 0, 16, 0, '#C4473F'); it.rect(14, -1, 17, -1, '#C4473F')
    for y in range(0, 2): it.px(15, y, '#C4473F')
    return it
