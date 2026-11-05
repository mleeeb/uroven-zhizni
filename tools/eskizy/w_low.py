"""Низ и обувь."""
from outfit import item, pants
from px32 import Item, shade, K

W, Wd = '#F4F1DE', '#C9CBDD'
GOLD, GOLD_D = '#F2CC8F', '#C9A15F'
LEGS = {(x, y) for y in range(32, 39) for x in range(8, 24)}


def legs_below(it, y0, color, color_d=None, y1=38):
    """Ноги (кожа или колготки) ниже подола/штанины, уже штанин."""
    it.clear = set(LEGS)
    it.rect(10, y0, 13, y1, color); it.rect(18, y0, 21, y1, color)
    if color_d: it.rect(13, y0, 13, y1, color_d); it.rect(21, y0, 21, y1, color_d)


# ---------------- низ ----------------
@item('bottom', 'Шаровары', 'народный')
def sharovary(sex, ctx):
    C = '#3A3F63'
    it = Item()
    pants(it, C, shade(C, 0.8), wide=1)
    for x in (11, 19): it.rect(x, 34, x, 38, '#4A4F6E')
    it.rect(8, 32, 23, 32, shade(C, 0.8))
    return it


@item('bottom', 'Хакама', 'народный', long=True)
def hakama(sex, ctx):
    HK, HKd = '#5A5F7A', '#464A62'
    it = Item()
    it.clear = set(LEGS)
    it.rect(8, 31, 23, 36, HK); it.rect(7, 37, 14, 40, HK); it.rect(17, 37, 24, 40, HK)
    for x in (10, 13, 18, 21): it.rect(x, 32, x, 40, HKd)
    it.rect(15, 33, 16, 36, HKd)
    for y in range(37, 41): it.line(15, y); it.line(16, y)
    return it


@item('bottom', 'Лыжные штаны', 'зима')
def ski_pants(sex, ctx):
    C, Cd = '#2E3A6B', '#222B52'
    it = Item()
    pants(it, C, Cd, wide=1)
    it.rect(8, 35, 14, 35, '#3F4E86'); it.rect(17, 35, 23, 35, '#3F4E86')
    it.rect(8, 37, 14, 37, '#C9CBDD'); it.rect(17, 37, 23, 37, '#C9CBDD')
    it.rect(8, 32, 23, 32, '#E07A5F')
    return it


@item('bottom', 'Вельветовые брюки', 'осень')
def corduroy(sex, ctx):
    C, Cd = '#8A5A3B', '#6B4430'
    it = Item()
    pants(it, C, Cd)
    for x in (10, 12, 18, 20):
        for y in range(33, 39): it.px(x, y, Cd)
    it.rect(9, 32, 22, 32, '#4A3426'); it.px(15, 32, GOLD)
    return it


@item('bottom', 'Бермуды', 'лето')
def bermuda(sex, ctx):
    C, Cd = '#C9B48A', '#A8946A'
    it = Item()
    legs_below(it, 36, ctx['skin'], shade(ctx['skin'], 0.86))
    pants(it, C, Cd, bottom=35)
    it.rect(9, 32, 22, 32, Cd)
    it.rect(10, 34, 11, 34, Cd); it.rect(20, 34, 21, 34, Cd)
    return it


@item('bottom', 'Джинсы с подворотами', 'весна')
def cuffed(sex, ctx):
    C, Cd, Cl = '#3D5A80', shade('#3D5A80', 0.72), shade('#3D5A80', 1.3)
    it = Item()
    legs_below(it, 37, ctx['skin'], shade(ctx['skin'], 0.86))
    pants(it, C, Cd, bottom=36)
    it.rect(9, 35, 14, 36, Cl); it.rect(17, 35, 22, 36, Cl)
    it.rect(9, 32, 22, 32, Cd); it.px(15, 32, GOLD)
    return it


def skirt(it, A, B, Bd, tights, hem=36, tartan=True):
    legs_below(it, hem + 1, tights, shade(tights, 0.8))
    it.rect(9, 32, 22, 33, A); it.rect(8, 34, 23, hem, A)
    if tartan:
        for x in range(8, 24, 3): it.rect(x, 32, x, hem, B)
        for y in (33, 35): it.rect(8, y, 23, y, B)
        for x in range(8, 24, 3):
            for y in (33, 35): it.px(x, y, Bd)
    it.rect(9, 32, 22, 32, shade(A, 0.75))


@item('bottom', 'Юбка в клетку', 'осень')
def plaid_skirt(sex, ctx):
    it = Item()
    skirt(it, '#B8343A', '#2A3A7A', '#1A2450', '#2A2D45')
    return it


@item('bottom', 'Килт', 'народный')
def kilt(sex, ctx):
    it = Item()
    skirt(it, '#2E6650', '#C4473F', '#8E2830', ctx['skin'])
    it.rect(14, 33, 17, 35, '#6B4A30'); it.rect(14, 33, 17, 33, W); it.px(15, 35, W); it.px(16, 35, W)
    return it


@item('bottom', 'Длинная юбка в цветочек', 'лето', long=True)
def long_skirt(sex, ctx):
    C, Cd = '#3D5A80', '#2E4466'
    it = Item()
    it.clear = set(LEGS)
    it.rect(9, 32, 22, 34, C); it.rect(8, 35, 23, 37, C); it.rect(7, 38, 24, 40, C)
    it.rect(21, 33, 22, 40, Cd); it.rect(23, 38, 24, 40, Cd)
    for x, y, c in ((11, 34, '#E8A0A8'), (17, 36, '#F2CC8F'), (13, 38, '#F4F1DE'), (20, 39, '#E8A0A8'),
                    (9, 39, '#F2CC8F'), (19, 33, '#F4F1DE'), (14, 36, '#E8A0A8')):
        it.px(x, y, c); it.px(x + 1, y + 1, '#81B29A')
    it.rect(9, 32, 22, 32, Cd)
    return it


@item('bottom', 'Штаны скафандра', 'космос')
def space_pants(sex, ctx):
    S, Sd = '#E8E6DA', '#B8B6C8'
    it = Item()
    pants(it, S, Sd, wide=1)
    it.rect(9, 35, 13, 36, '#9AA0C0'); it.rect(18, 35, 22, 36, '#9AA0C0')
    it.rect(8, 32, 23, 32, '#9AA0C0'); it.px(10, 33, '#E07A5F')
    return it


@item('bottom', 'Штаны скелета', 'хэллоуин')
def skeleton_pants(sex, ctx):
    B = '#1E1A22'
    it = Item()
    pants(it, B, '#2E2836')
    for x in (11, 19):
        it.rect(x - 1, 33, x + 2, 33, W); it.rect(x, 34, x + 1, 37, W); it.rect(x - 1, 38, x + 2, 38, W)
        it.px(x, 35, Wd)
    return it


# ---------------- обувь ----------------
def boot(it, C, top, Cd=None, sole=None, toe=True):
    it.rect(9, top, 14, 42, C); it.rect(17, top, 22, 42, C)
    if toe:
        it.rect(7, 40, 8, 42, C); it.rect(23, 40, 24, 42, C)
    if Cd:
        it.rect(14, top + 1, 14, 42, Cd); it.rect(22, top + 1, 22, 42, Cd); it.rect(23, 40, 24, 41, Cd)
    if sole:
        it.rect(7, 42, 14, 42, sole); it.rect(17, 42, 24, 42, sole)
    for y in range(top, 43): it.line(15, y); it.line(16, y)


@item('shoes', 'Валенки', 'зима', tall=True)
def valenki(sex, ctx):
    V, Vd, Vl = '#6E6A7C', '#55516A', '#8A8698'
    it = Item()
    boot(it, V, 35, Vd, Vd)
    for x0, x1 in ((9, 14), (17, 22)):
        it.rect(x0, 35, x1, 35, Vl)
        for i, x in enumerate(range(x0, x1 + 1)): it.px(x, 36, '#C4473F' if i % 2 == 0 else W)
    return it


@item('shoes', 'Сапоги', 'народный', tall=True)
def sapogi(sex, ctx):
    B, Bl = '#1E1A22', '#4A4458'
    it = Item()
    boot(it, B, 37, None, '#0F0D12')
    it.rect(10, 38, 10, 40, Bl); it.rect(18, 38, 18, 40, Bl)
    it.rect(9, 37, 14, 37, '#2E2A36'); it.rect(17, 37, 22, 37, '#2E2A36')
    return it


@item('shoes', 'Красные сапожки', 'народный', tall=True)
def red_boots(sex, ctx):
    R, Rd = '#C4473F', '#9A3530'
    it = Item()
    boot(it, R, 37, Rd, '#6B2420')
    it.rect(9, 37, 14, 37, GOLD); it.rect(17, 37, 22, 37, GOLD)
    it.px(10, 39, GOLD_D); it.px(18, 39, GOLD_D)
    return it


@item('shoes', 'Белые сапожки', 'новый год', tall=True)
def white_boots(sex, ctx):
    it = Item()
    boot(it, W, 37, Wd, '#8FB3E0')
    it.rect(9, 37, 14, 37, '#8FB3E0'); it.rect(17, 37, 22, 37, '#8FB3E0')
    it.px(11, 39, '#8FB3E0'); it.px(19, 39, '#8FB3E0')
    return it


def tabi(it, sole, strap):
    it.rect(9, 39, 13, 41, W); it.rect(18, 39, 22, 41, W)
    it.rect(13, 39, 13, 41, Wd); it.rect(22, 39, 22, 41, Wd)
    it.rect(8, 42, 14, 42, sole); it.rect(17, 42, 23, 42, sole)
    it.px(11, 41, strap); it.px(20, 41, strap); it.px(10, 40, strap); it.px(12, 40, strap)
    it.px(19, 40, strap); it.px(21, 40, strap)
    for y in range(39, 43): it.line(15, y); it.line(16, y)
    it.no_outline.update({(x, 38) for x in range(8, 24)})


@item('shoes', 'Гэта с носками-таби', 'народный')
def geta(sex, ctx):
    it = Item()
    tabi(it, '#A0784A', '#1E1A22')
    return it


@item('shoes', 'Дзори с носками-таби', 'народный')
def zori(sex, ctx):
    it = Item()
    tabi(it, '#C4473F', '#C4473F')
    return it


@item('shoes', 'Резиновые сапоги', 'весна', tall=True)
def rubber(sex, ctx):
    Y, Yd = '#E8C547', '#C4A030'
    it = Item()
    boot(it, Y, 35, Yd, '#6B5A20')
    it.rect(9, 35, 14, 35, Yd); it.rect(17, 35, 22, 35, Yd)
    it.px(10, 37, '#F4DC7A'); it.px(18, 37, '#F4DC7A')
    return it


def bare_feet(it, skin):
    it.rect(9, 39, 13, 41, skin); it.rect(18, 39, 22, 41, skin)
    it.rect(8, 41, 13, 41, skin); it.rect(18, 41, 23, 41, skin)
    for y in range(39, 43): it.line(15, y); it.line(16, y)
    it.no_outline.update({(x, 38) for x in range(8, 24)})


@item('shoes', 'Сандалии', 'лето')
def sandals(sex, ctx):
    B = '#8A5A3B'
    it = Item()
    bare_feet(it, ctx['skin'])
    it.rect(8, 42, 14, 42, '#6B4430'); it.rect(17, 42, 24, 42, '#6B4430')
    it.rect(9, 40, 13, 40, B); it.rect(18, 40, 22, 40, B)
    it.px(11, 39, B); it.px(20, 39, B)
    return it


@item('shoes', 'Вьетнамки', 'лето')
def flipflops(sex, ctx):
    C = '#3D8FC4'
    it = Item()
    bare_feet(it, ctx['skin'])
    it.rect(8, 42, 14, 42, C); it.rect(17, 42, 24, 42, C)
    it.px(10, 41, C); it.px(11, 40, C); it.px(12, 41, C)
    it.px(19, 41, C); it.px(20, 40, C); it.px(21, 41, C)
    return it


@item('shoes', 'Челси', 'осень', tall=True)
def chelsea(sex, ctx):
    C, Cd = '#6B4430', '#4E3122'
    it = Item()
    boot(it, C, 38, Cd, '#2A1E16')
    it.rect(9, 38, 9, 40, '#4A4F6E'); it.rect(22, 38, 22, 40, '#4A4F6E')
    it.px(11, 38, '#8A5A3B'); it.px(19, 38, '#8A5A3B')
    return it


@item('shoes', 'Лапти с онучами', 'народный', tall=True)
def lapti(sex, ctx):
    L, Ld = '#D9B26A', '#A8864A'
    it = Item()
    it.rect(9, 34, 14, 39, W); it.rect(17, 34, 22, 39, W)
    for y in range(34, 40):
        it.px(9 + (y % 3) * 2, y, '#4A3426'); it.px(17 + ((y + 1) % 3) * 2, y, '#4A3426')
    it.rect(8, 40, 14, 42, L); it.rect(17, 40, 23, 42, L)
    for x in range(8, 24):
        for y in (40, 42):
            if (x + y) % 2: it.px(x, y, Ld)
    it.erase(15, 40); it.erase(16, 40); it.erase(15, 41); it.erase(16, 41); it.erase(15, 42); it.erase(16, 42)
    for y in range(34, 43): it.line(15, y); it.line(16, y)
    return it


@item('shoes', 'Космические ботинки', 'космос', tall=True)
def space_boots(sex, ctx):
    it = Item()
    boot(it, '#E8E6DA', 36, '#B8B6C8', '#6A6F90')
    it.rect(9, 38, 14, 38, '#E07A5F'); it.rect(17, 38, 22, 38, '#E07A5F')
    it.rect(9, 36, 14, 36, '#9AA0C0'); it.rect(17, 36, 22, 36, '#9AA0C0')
    return it


@item('shoes', 'Угги', 'зима', tall=True)
def uggs(sex, ctx):
    C, Cd, F = '#C9A878', '#A68858', '#EFE3C6'
    it = Item()
    boot(it, C, 36, Cd, '#8A6A3B')
    it.rect(9, 36, 14, 37, F); it.rect(17, 36, 22, 37, F)
    for x in (10, 13, 18, 21): it.px(x, 37, '#D9C7A3')
    return it


@item('shoes', 'Коньки', 'зима', tall=True)
def skates(sex, ctx):
    it = Item()
    it.rect(9, 37, 14, 41, W); it.rect(17, 37, 22, 41, W)
    it.rect(7, 40, 8, 41, W); it.rect(23, 40, 24, 41, W)
    it.rect(14, 38, 14, 41, Wd); it.rect(22, 38, 22, 41, Wd)
    for y in (38, 39, 40): it.px(11, y, '#4A4F6E'); it.px(19, y, '#4A4F6E')
    it.rect(8, 41, 14, 41, '#4A4F6E'); it.rect(17, 41, 23, 41, '#4A4F6E')
    it.rect(6, 42, 14, 42, '#DDE1EE'); it.rect(17, 42, 25, 42, '#DDE1EE')
    it.px(6, 41, '#DDE1EE'); it.px(25, 41, '#DDE1EE'); it.erase(7, 40); it.erase(24, 40)
    for y in range(37, 43): it.line(15, y); it.line(16, y)
    return it
