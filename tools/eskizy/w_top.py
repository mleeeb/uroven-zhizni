"""Верх: куртки, шубы, рубашки, свитеры, костюмы."""
from outfit import item, geo, hands, long_top, short_top
from px32 import Item, shade, K

W, Wd = '#F4F1DE', '#C9CBDD'
GOLD, GOLD_D = '#F2CC8F', '#C9A15F'


def flake(it, x, y, col):
    for dx, dy in ((0, 0), (-1, -1), (1, -1), (-1, 1), (1, 1)): it.px(x + dx, y + dy, col)


def floor_coat(it, sex, C, Cd, hem=40):
    """Длинное пальто до пола: корпус расширяется книзу."""
    g = long_top(it, sex, C, hem=hem, Cd=Cd)
    it.rect(g['bx0'] - 1, 34, g['bx1'] + 1, hem, C)
    it.rect(g['bx1'] - 1, 34, g['bx1'] + 1, hem, Cd)
    return g


@item('top', 'Пуховик', 'зима', sleeve='long')
def puhovik(sex, ctx):
    J = '#4F78A8'; Jd, Jl = shade(J, 0.72), shade(J, 1.25)
    it = Item()
    g = long_top(it, sex, J)
    bx0, bx1, sl, sr = g['bx0'], g['bx1'], g['sl'], g['sr']
    for y in (25, 29, 33): it.rect(bx0, y, bx1, y, Jd)
    it.rect(sl[0], 26, sl[1], 26, Jd); it.rect(sr[0], 26, sr[1], 26, Jd)
    it.rect(sl[0], 28, sl[1], 28, Jd); it.rect(sr[0], 28, sr[1], 28, Jd)
    for y in (23, 27, 31): it.rect(bx0 + 1, y, bx0 + 3, y, Jl)
    it.rect(bx0 + 3, 21, bx1 - 3, 22, Jd)
    for y in range(22, 34): it.px(15, y, Wd)
    it.px(16, 23, Wd)
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Шуба Деда Мороза', 'новый год', long=True, sleeve='long')
def ded_coat(sex, ctx):
    R, Rd, Rl = '#B8343A', shade('#B8343A', 0.74), '#F0C9C3'
    it = Item()
    g = floor_coat(it, sex, R, Rd)
    x0, x1 = g['bx0'] - 1, g['bx1'] + 1
    it.rect(x0 - 1, 40, x1 + 1, 41, W); it.rect(x0, 40, x1, 40, W)
    it.rect(g['sl'][0], 28, g['sl'][1], 28, W); it.rect(g['sr'][0], 28, g['sr'][1], 28, W)
    it.rect(15, 23, 16, 40, W)
    it.rect(g['bx0'] + 2, 21, g['bx1'] - 2, 22, W)
    it.rect(g['bx0'], 30, g['bx1'], 31, GOLD); it.rect(g['bx0'], 31, g['bx1'], 31, GOLD_D)
    it.px(g['bx0'] + 2, 32, GOLD); it.px(g['bx0'] + 2, 33, GOLD_D)
    for x, y in ((12, 36), (19, 36), (12, 26), (19, 26)): flake(it, x, y, Rl)
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Шубка Снегурочки', 'новый год', long=True, sleeve='long')
def sneg_coat(sex, ctx):
    B, Bd = '#6F9FD6', shade('#6F9FD6', 0.74)
    it = Item()
    g = floor_coat(it, sex, B, Bd)
    x0, x1 = g['bx0'] - 1, g['bx1'] + 1
    it.rect(x0 - 1, 40, x1 + 1, 41, W); it.rect(x0, 40, x1, 40, W)
    it.rect(g['sl'][0], 28, g['sl'][1], 28, W); it.rect(g['sr'][0], 28, g['sr'][1], 28, W)
    it.rect(15, 23, 16, 40, W)
    it.rect(g['bx0'] + 1, 21, g['bx1'] - 1, 22, W)
    for x, y in ((12, 26), (19, 29), (12, 32), (19, 36), (12, 38)): flake(it, x, y, '#E3EEFA')
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Косоворотка', 'народный', sleeve='long')
def kosovorotka(sex, ctx):
    R, Rd = '#C0392F', shade('#C0392F', 0.74)
    it = Item()
    g = long_top(it, sex, R, hem=33, Cd=Rd)
    bx0, bx1, sl, sr = g['bx0'], g['bx1'], g['sl'], g['sr']
    it.rect(12, 21, 19, 22, R); it.rect(12, 22, 19, 22, GOLD)
    for y in range(22, 27): it.px(12, y, GOLD)
    it.px(11, 23, GOLD_D); it.px(11, 25, GOLD_D)
    for x in range(bx0, bx1 + 1): it.px(x, 33, GOLD if x % 2 else GOLD_D)
    it.rect(sl[0], 28, sl[1], 28, GOLD); it.rect(sr[0], 28, sr[1], 28, GOLD)
    it.rect(bx0, 29, bx1, 30, GOLD); it.rect(bx0, 30, bx1, 30, GOLD_D)
    it.px(bx1 - 3, 31, GOLD); it.px(bx1 - 3, 32, GOLD_D); it.px(bx1 - 2, 31, GOLD); it.px(bx1 - 2, 32, GOLD_D)
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Сарафан с рубахой', 'народный', long=True, sleeve='long', only='f')
def sarafan(sex, ctx):
    R, Rd, BL, BLd = '#A8323E', shade('#A8323E', 0.74), '#F4F1DE', '#D3CFB8'
    it = Item()
    it.rect(9, 22, 22, 23, BL)
    it.rect(6, 24, 9, 28, BL); it.rect(22, 24, 25, 28, BL)
    it.rect(6, 28, 9, 28, '#C0392F'); it.rect(22, 28, 25, 28, '#C0392F')
    it.rect(9, 26, 9, 27, BLd); it.rect(22, 26, 22, 27, BLd)
    for y in range(25, 29): it.line(10, y); it.line(21, y)
    it.rect(11, 24, 20, 31, R); it.rect(11, 23, 12, 23, R); it.rect(19, 23, 20, 23, R)
    it.rect(10, 32, 21, 35, R); it.rect(9, 36, 22, 38, R); it.rect(8, 39, 23, 40, R)
    it.rect(19, 26, 20, 38, Rd); it.rect(21, 34, 22, 40, Rd); it.rect(23, 39, 23, 40, Rd)
    for y in range(24, 41): it.px(15, y, GOLD); it.px(16, y, GOLD_D)
    for y in range(25, 40, 3): it.px(15, y, BL)
    for x in range(8, 24): it.px(x, 39, GOLD if x % 2 else GOLD_D)
    it.rect(11, 24, 20, 24, GOLD)
    hands(it, sex, ctx['skin'])
    it.no_outline.update({(x, 21) for x in range(9, 23)})
    return it


def kimono_body(it, sex, C, Cd, hem, sleeve_bottom):
    g = geo(sex)
    sl, sr = ((3, 8), (23, 28)) if sex == 'm' else ((5, 9), (22, 26))
    it.rect(g['bx0'], 22, g['bx1'], hem, C); it.rect(12, 21, 19, 21, C)
    it.rect(sl[0], 23, sr[1], 24, C)
    it.rect(sl[0], 25, sl[1], sleeve_bottom, C); it.rect(sr[0], 25, sr[1], sleeve_bottom, C)
    it.rect(sl[0], sleeve_bottom, sl[1], sleeve_bottom, Cd); it.rect(sr[0], sleeve_bottom, sr[1], sleeve_bottom, Cd)
    it.rect(sr[1] - 1, 25, sr[1], sleeve_bottom, Cd)
    for y in range(25, sleeve_bottom): it.line(sl[1] + 1, y); it.line(sr[0] - 1, y)
    # ворот «левая пола сверху»
    for x, y in ((17, 21), (17, 22), (16, 23), (15, 24), (14, 25), (13, 26), (12, 27)):
        it.px(x, y, '#14162A'); it.px(x + 1, y, Cd)
    it.rect(14, 21, 16, 22, W); it.px(15, 23, W); it.px(13, 22, W); it.px(14, 23, W)
    it.no_outline.update({(x, 20) for x in range(8, 24)})
    return g


@item('top', 'Кимоно с поясом', 'народный', sleeve='long')
def kimono(sex, ctx):
    C, Cd = '#2E3A6B', '#222B52'
    it = Item()
    g = kimono_body(it, sex, C, Cd, hem=31, sleeve_bottom=31)
    it.rect(g['bx0'], 29, g['bx1'], 30, '#B8A27A'); it.rect(g['bx0'], 30, g['bx1'], 30, '#8F7C58')
    it.rect(g['bx0'], 31, g['bx1'], 31, Cd)
    it.px(19, 25, '#D9D4BE'); it.px(20, 25, '#D9D4BE')
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Кимоно длинное', 'народный', long=True, sleeve='long')
def furisode(sex, ctx):
    C, Cd = '#8E5FB8', '#6E4691'
    SAK, SAK_C = '#F4C6D4', '#E07A9A'
    it = Item()
    g = kimono_body(it, sex, C, Cd, hem=40, sleeve_bottom=35)
    it.rect(g['bx0'] - 1, 36, g['bx1'] + 1, 40, C)
    it.rect(g['bx1'] - 2, 32, g['bx1'] + 1, 40, Cd)
    for i, y in enumerate(range(32, 41)): it.px(13 - i // 3, y, Cd)
    it.rect(g['bx0'], 27, g['bx1'], 31, GOLD); it.rect(g['bx0'], 31, g['bx1'], 31, GOLD_D)
    it.rect(g['bx0'], 29, g['bx1'], 29, '#C4473F'); it.rect(15, 28, 16, 30, '#C4473F')
    for x, y in ((6, 27), (25, 31), (12, 34), (18, 37), (6, 32), (13, 39), (19, 24)):
        flake_ = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in flake_: it.px(x + dx, y + dy, SAK)
        it.px(x, y, SAK_C)
    hands(it, sex, ctx['skin'])
    return it


def long_sweater(it, sex, C, Cd, hem=33):
    g = long_top(it, sex, C, hem=hem, Cd=Cd)
    for x in range(g['bx0'], g['bx1'] + 1, 2): it.px(x, hem, Cd)
    it.rect(g['sl'][0], 28, g['sl'][1], 28, Cd); it.rect(g['sr'][0], 28, g['sr'][1], 28, Cd)
    it.rect(13, 21, 18, 21, Cd)
    return g


@item('top', 'Новогодний свитер', 'новый год', sleeve='long')
def xmas_sweater(sex, ctx):
    R, Rd, G = '#B8343A', '#8E2830', '#81B29A'
    it = Item()
    g = long_sweater(it, sex, R, Rd)
    for x in range(g['bx0'], g['bx1'] + 1):
        it.px(x, 23, W if x % 2 else R); it.px(x, 24, W if x % 2 == 0 else R)
    for x in range(g['sl'][0], g['sl'][1] + 1): it.px(x, 24, W if x % 2 == 0 else R)
    for x in range(g['sr'][0], g['sr'][1] + 1): it.px(x, 24, W if x % 2 == 0 else R)
    for cx in (12, 19):
        it.px(cx, 26, W); it.rect(cx - 1, 27, cx + 1, 27, W); it.rect(cx - 2, 28, cx + 2, 28, W); it.px(cx, 29, GOLD_D)
    it.px(15, 27, GOLD); it.px(16, 30, GOLD)
    for x in range(g['bx0'], g['bx1'] + 1): it.px(x, 31, W if x % 2 else R)
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Дублёнка', 'зима', sleeve='long')
def dublyonka(sex, ctx):
    C, Cd = '#8A5A3B', '#6B4430'
    it = Item()
    g = long_top(it, sex, C, hem=35, Cd=Cd)
    it.rect(g['bx0'] - 1, 33, g['bx1'] + 1, 35, C); it.rect(g['bx1'] - 1, 33, g['bx1'] + 1, 35, Cd)
    it.rect(g['bx0'] + 1, 21, g['bx1'] - 1, 23, FUR := '#E3D3B0')
    it.rect(12, 24, 14, 26, FUR); it.rect(17, 24, 19, 26, FUR)
    it.rect(15, 24, 16, 35, FUR)
    it.rect(g['sl'][0], 28, g['sl'][1], 28, FUR); it.rect(g['sr'][0], 28, g['sr'][1], 28, FUR)
    it.rect(g['bx0'] - 1, 35, g['bx1'] + 1, 35, FUR)
    for x, y in ((11, 30), (20, 30)): it.rect(x - 1, y, x + 1, y, Cd)
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Дождевик', 'весна', sleeve='long')
def raincoat(sex, ctx):
    Y, Yd, Yl = '#E8C547', '#C4A030', '#F4DC7A'
    it = Item()
    g = long_top(it, sex, Y, hem=36, Cd=Yd)
    it.rect(g['bx0'] - 1, 34, g['bx1'] + 1, 36, Y); it.rect(g['bx1'] - 1, 34, g['bx1'] + 1, 36, Yd)
    it.rect(g['bx0'] + 1, 20, g['bx1'] - 1, 21, Yd)
    for y in range(23, 36): it.px(15, y, Yd)
    for y in (24, 27, 30, 33): it.px(16, y, '#3A3F63')
    it.rect(g['bx0'] + 1, 31, g['bx0'] + 3, 31, Yd); it.rect(g['bx1'] - 3, 31, g['bx1'] - 1, 31, Yd)
    it.px(g['bx0'] + 1, 23, Yl); it.px(g['bx0'] + 1, 24, Yl)
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Ветровка', 'весна', sleeve='long')
def windbreaker(sex, ctx):
    S, Sd, C, Cd = '#8FB3E0', '#6F93C0', '#E07A5F', '#B8604A'
    it = Item()
    g = long_top(it, sex, S, hem=32, Cd=Sd)
    it.rect(g['bx0'], 27, g['bx1'], 32, C); it.rect(g['bx1'] - 1, 27, g['bx1'], 32, Cd)
    it.rect(g['bx0'], 26, g['bx1'], 26, W)
    it.rect(g['sl'][0], 26, g['sl'][1], 28, C); it.rect(g['sr'][0], 26, g['sr'][1], 28, C)
    it.rect(g['sl'][0], 25, g['sl'][1], 25, W); it.rect(g['sr'][0], 25, g['sr'][1], 25, W)
    it.rect(g['bx0'], 32, g['bx1'], 32, '#3A3F63')
    for y in range(21, 32): it.px(15, y, '#3A3F63')
    it.rect(13, 20, 18, 21, Sd)
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Гавайская рубашка', 'лето')
def hawaiian(sex, ctx):
    C, Cd = '#2E8C86', '#22706A'
    it = Item()
    short_top(it, sex, C, hem=31, Cd=Cd)
    for x, y, col in ((11, 24), (18, 23), (13, 28), (20, 28), (6, 25), (24, 25), (16, 30)) and [
            (11, 24, '#E8A0A8'), (18, 23, '#F2CC8F'), (13, 28, '#F2CC8F'), (20, 28, '#E8A0A8'),
            (6 if sex == 'm' else 8, 25, '#F4F1DE'), (24 if sex == 'm' else 23, 25, '#E8A0A8'), (16, 30, '#E8A0A8')]:
        it.px(x, y, col); it.px(x - 1, y, col); it.px(x, y - 1, col); it.px(x + 1, y + 1, '#81B29A')
    it.rect(14, 22, 17, 22, '#F2CC8F' if False else ctx['skin']); it.px(15, 23, ctx['skin']); it.px(16, 23, ctx['skin'])
    it.px(13, 22, W); it.px(18, 22, W)
    for y in (25, 28): it.px(16, y, W)
    return it


@item('top', 'Тельняшка', 'лето', sleeve='long')
def telnyashka(sex, ctx):
    N = '#2A3A7A'
    it = Item()
    g = long_top(it, sex, W, hem=32)
    for (x, y), c in list(it.c.items()):
        if y % 2 == 0 and y >= 22: it.px(x, y, N)
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Тренч', 'осень', sleeve='long')
def trench(sex, ctx):
    C, Cd = '#C9A878', '#A68858'
    it = Item()
    g = long_top(it, sex, C, hem=37, Cd=Cd)
    it.rect(g['bx0'] - 1, 33, g['bx1'] + 1, 37, C); it.rect(g['bx1'] - 1, 33, g['bx1'] + 1, 37, Cd)
    for i in range(4): it.px(13 - i // 2, 21 + i, Cd); it.px(18 + i // 2, 21 + i, Cd)
    it.rect(g['bx0'] - 1, 30, g['bx1'] + 1, 30, Cd); it.px(15, 30, GOLD_D); it.px(16, 30, GOLD_D)
    for y in (25, 28, 33): it.px(13, y, '#6B4A30'); it.px(18, y, '#6B4A30')
    for y in range(31, 38): it.px(15, y, Cd)
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Скафандр', 'космос', sleeve='long')
def spacesuit(sex, ctx):
    S, Sd = '#E8E6DA', '#B8B6C8'
    it = Item()
    g = long_top(it, sex, S, hem=33, Cd=Sd)
    it.rect(13, 25, 18, 28, '#6A6F90')
    it.px(14, 26, '#E07A5F'); it.px(16, 26, '#F2CC8F'); it.px(17, 27, '#8FB3E0'); it.px(14, 27, '#81B29A')
    it.rect(g['sl'][0], 23, g['sl'][0] + 1, 24, '#E07A5F')
    it.rect(g['sl'][0], 28, g['sl'][1], 28, '#9AA0C0'); it.rect(g['sr'][0], 28, g['sr'][1], 28, '#9AA0C0')
    it.rect(g['bx0'], 31, g['bx1'], 31, '#9AA0C0')
    it.rect(g['bx1'] - 3, 23, g['bx1'] - 2, 24, '#3D5A80')
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Костюм скелета', 'хэллоуин', sleeve='long')
def skeleton(sex, ctx):
    B, Bl = '#1E1A22', '#2E2836'
    it = Item()
    g = long_top(it, sex, B, hem=33, Cd=Bl)
    for y in range(22, 33): it.px(15, y, W); it.px(16, y, W) if y % 2 else None
    for y in (24, 26, 28):
        it.rect(g['bx0'] + 2, y, 14, y, W); it.rect(17, y, g['bx1'] - 2, y, W)
    it.rect(12, 31, 19, 32, W); it.rect(14, 32, 17, 32, B)
    for y in range(24, 28): it.px(g['sl'][0] + 1, y, W); it.px(g['sr'][1] - 1, y, W)
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Вышитая рубаха', 'пасха', sleeve='long')
def vyshyvanka(sex, ctx):
    R = '#C0392F'
    it = Item()
    g = long_top(it, sex, W, hem=32, Cd=Wd)
    it.rect(13, 21, 18, 21, R)
    for y in range(22, 28):
        it.px(15 if y % 2 else 16, y, R); it.px(14 if y % 2 == 0 else 17, y, '#1E1A22')
    for x in range(g['bx0'], g['bx1'] + 1): it.px(x, 32, R if x % 2 else '#1E1A22')
    for side in (g['sl'], g['sr']):
        for x in range(side[0], side[1] + 1):
            it.px(x, 27, R if x % 2 else W); it.px(x, 28, R)
        it.px(side[0] + 1, 24, R); it.px(side[0] + 2, 25, R)
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Свитер с сердцем', '14 февраля', sleeve='long')
def heart_sweater(sex, ctx):
    P, Pd, R = '#E8A0A8', '#C27880', '#C4473F'
    it = Item()
    long_sweater(it, sex, P, Pd)
    for x in (13, 14, 17, 18): it.px(x, 25, R)
    it.rect(13, 26, 18, 26, R); it.rect(13, 27, 18, 27, R); it.rect(14, 28, 17, 28, R); it.rect(15, 29, 16, 29, R)
    it.px(13, 26, '#E8706A')
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Китайская куртка', 'китайский', sleeve='long')
def tangzhuang(sex, ctx):
    R, Rd = '#B8343A', '#8E2830'
    it = Item()
    g = long_top(it, sex, R, hem=33, Cd=Rd)
    it.rect(13, 21, 18, 21, GOLD)
    for y in range(22, 34): it.px(15, y, Rd)
    for y in (23, 26, 29, 32): it.rect(14, y, 17, y, GOLD)
    it.rect(g['sl'][0], 28, g['sl'][1], 28, GOLD); it.rect(g['sr'][0], 28, g['sr'][1], 28, GOLD)
    it.px(11, 27, GOLD_D); it.px(20, 30, GOLD_D); it.px(12, 31, GOLD_D)
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Ципао', 'китайский', long=True, only='f')
def qipao(sex, ctx):
    R, Rd = '#B8343A', '#8E2830'
    it = Item()
    short_top(it, sex, R, hem=31, Cd=Rd)
    it.rect(10, 32, 21, 35, R); it.rect(10, 36, 21, 40, R)
    it.rect(20, 32, 21, 40, Rd)
    it.rect(13, 21, 18, 21, GOLD)
    for x, y in ((14, 25), (17, 28), (13, 33), (18, 37), (12, 30)):
        it.px(x, y, GOLD); it.px(x + 1, y, GOLD_D); it.px(x, y + 1, GOLD_D)
    for y in range(22, 26): it.px(18 - (y - 22) // 2, y, GOLD)
    it.rect(11, 37, 11, 40, ctx['skin'])
    return it


@item('top', 'Пончо', 'мексиканский', sleeve='none')
def poncho(sex, ctx):
    cols = ['#C4473F', '#F2CC8F', '#4FA88A', '#F4F1DE', '#3D5A80']
    it = Item()
    rows = {22: (12, 19), 23: (10, 21), 24: (8, 23), 25: (6, 25)}
    for y in range(26, 33): rows[y] = (4, 27)
    for y, (a, b) in rows.items():
        it.rect(a, y, b, y, cols[(y // 2) % 5])
    for x in range(4, 28, 2): it.px(x, 33, cols[0])
    it.rect(14, 22, 17, 22, ctx['skin'])
    it.no_outline.update({(x, 21) for x in range(10, 22)})
    return it
