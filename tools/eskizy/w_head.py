"""Головные уборы."""
import math
from outfit import item
from px32 import Item, shade, K

W, Wd = '#F4F1DE', '#C9CBDD'
FUR, FUR_D, FUR_L = '#D9C7A3', '#B09A74', '#EFE3C6'
GOLD, GOLD_D = '#F2CC8F', '#C9A15F'


def heart(it, x, y, c, cd=None):
    for dx in (-2, -1, 1, 2): it.px(x + dx, y, c)
    it.rect(x - 2, y + 1, x + 2, y + 1, c); it.rect(x - 1, y + 2, x + 1, y + 2, c); it.px(x, y + 3, c)
    if cd: it.px(x + 1, y + 2, cd); it.px(x + 2, y + 1, cd)


@item('head', 'Ушанка', 'зима')
def ushanka(sex, ctx):
    CAP, CAP_D = '#6B4A30', '#4E3522'
    it = Item()
    it.rect(10, 2, 21, 2, CAP); it.rect(8, 3, 23, 5, CAP)
    it.rect(11, 2, 14, 2, shade(CAP, 1.3)); it.rect(9, 3, 11, 3, shade(CAP, 1.3))
    it.rect(15, 2, 16, 5, CAP_D); it.rect(21, 3, 23, 5, CAP_D)
    it.rect(5, 6, 26, 9, FUR)
    for x in (6, 9, 13, 18, 22, 25): it.px(x, 6, FUR_L)
    for x in (7, 11, 16, 20, 24): it.px(x, 9, FUR_D)
    it.rect(23, 7, 26, 9, FUR_D); it.px(24, 7, FUR)
    for x0 in (5, 23):
        it.rect(x0, 10, x0 + 3, 17, FUR); it.rect(x0 + 1, 18, x0 + 2, 18, FUR)
        sh = x0 + 3 if x0 == 5 else x0
        it.rect(sh, 10, sh, 17, FUR_D)
        it.px(x0 + 1, 12, FUR_L); it.px(x0 + 2, 15, FUR_L)
    for x in (6, 25): it.px(x, 19, CAP_D); it.px(x, 20, CAP_D)
    return it


@item('head', 'Шапка с помпоном', 'зима')
def pompom(sex, ctx):
    R, Rd = '#C4473F', shade('#C4473F', 0.75)
    it = Item()
    it.rect(14, 0, 17, 2, W); it.rect(13, 1, 18, 1, W); it.px(17, 2, Wd); it.px(18, 1, Wd)
    it.rect(11, 3, 20, 3, R); it.rect(9, 4, 22, 4, R); it.rect(8, 5, 23, 7, R)
    it.rect(8, 6, 23, 6, W)
    for x in range(9, 23, 3): it.px(x, 6, R)
    it.rect(21, 4, 23, 7, Rd); it.px(22, 6, Wd); it.px(23, 6, Wd)
    it.rect(7, 8, 24, 10, R)
    for x in range(8, 25, 2): it.rect(x, 8, x, 10, Rd)
    return it


@item('head', 'Шапка-бини', 'осень')
def beanie(sex, ctx):
    C, Cd, Cl = '#5E8C74', '#46705A', '#7AA88F'
    it = Item()
    it.rect(11, 1, 19, 1, C); it.rect(9, 2, 22, 2, C); it.rect(8, 3, 23, 7, C)
    it.rect(18, 1, 21, 2, Cd); it.rect(20, 3, 23, 7, Cd)
    it.rect(10, 2, 13, 2, Cl); it.px(9, 3, Cl)
    it.rect(7, 8, 24, 10, Cl)
    for x in range(8, 25, 2): it.rect(x, 8, x, 10, C)
    it.px(9, 9, '#F2CC8F'); it.px(10, 9, '#F2CC8F')   # нашивка
    return it


@item('head', 'Шапка Деда Мороза', 'новый год')
def ded_hat(sex, ctx):
    R, Rd, Rl = '#B8343A', shade('#B8343A', 0.74), shade('#B8343A', 1.2)
    it = Item()
    it.rect(10, 2, 21, 2, R); it.rect(8, 3, 23, 6, R)
    it.rect(11, 2, 14, 2, Rl); it.rect(20, 3, 23, 6, Rd)
    for x, y in ((12, 4), (17, 5), (10, 5)): it.px(x, y, '#F0C9C3')
    it.rect(6, 7, 25, 9, W)
    for x in (8, 12, 17, 21): it.px(x, 9, Wd)
    it.rect(23, 7, 25, 9, Wd)
    return it


@item('head', 'Венец Снегурочки', 'новый год')
def sneg_crown(sex, ctx):
    B, Bd, Bl = '#6F9FD6', shade('#6F9FD6', 0.74), shade('#6F9FD6', 1.18)
    SIL = '#E8E6DA'
    it = Item()
    it.rect(13, 0, 18, 0, B); it.rect(11, 1, 20, 1, B); it.rect(9, 2, 22, 3, B); it.rect(8, 4, 23, 6, B)
    it.rect(20, 2, 23, 6, Bd)
    for x, y in ((15, 1), (16, 1), (15, 4), (16, 4), (14, 2), (17, 2), (14, 3), (17, 3), (13, 2), (18, 2),
                 (15, 2), (16, 2), (15, 3), (16, 3)):
        it.px(x, y, SIL)
    it.px(15, 0, Bl); it.px(16, 0, Bl)
    for x in (10, 12, 19, 21): it.px(x, 5, SIL)
    it.rect(6, 7, 25, 8, W)
    for x in (9, 14, 19): it.px(x, 8, Wd)
    return it


@item('head', 'Картуз с цветком', 'народный')
def kartuz(sex, ctx):
    NAVY, NAVY_D = '#2A2D45', '#1E2036'
    it = Item()
    it.rect(9, 1, 22, 1, NAVY); it.rect(7, 2, 24, 5, NAVY)
    it.rect(10, 1, 15, 1, shade(NAVY, 1.45)); it.rect(8, 2, 11, 2, shade(NAVY, 1.45))
    it.rect(21, 2, 24, 5, NAVY_D)
    it.rect(8, 6, 23, 7, '#3A3F63'); it.rect(8, 7, 23, 7, NAVY_D)
    it.rect(9, 8, 22, 8, '#0F1120'); it.rect(11, 9, 20, 9, '#0F1120'); it.rect(12, 8, 15, 8, '#4A4F6E')
    it.px(9, 5, '#C4473F'); it.px(10, 5, '#E07A5F'); it.px(9, 6, '#C4473F'); it.px(10, 4, '#C4473F')
    it.px(11, 6, '#81B29A'); it.px(11, 5, '#C4473F')
    return it


@item('head', 'Кокошник', 'народный')
def kokoshnik(sex, ctx):
    R, Rd, BL = '#A8323E', shade('#A8323E', 0.74), '#F4F1DE'
    it = Item()
    it.rect(12, 0, 19, 0, R); it.rect(10, 1, 21, 1, R); it.rect(9, 2, 22, 2, R); it.rect(8, 3, 23, 8, R)
    it.rect(12, 0, 19, 0, GOLD); it.px(10, 1, GOLD); it.px(11, 1, GOLD); it.px(20, 1, GOLD); it.px(21, 1, GOLD)
    it.px(9, 2, GOLD); it.px(22, 2, GOLD); it.rect(8, 3, 8, 8, GOLD); it.rect(23, 3, 23, 8, GOLD)
    it.rect(19, 3, 22, 8, Rd)
    it.rect(15, 3, 16, 5, '#81B29A'); it.px(15, 3, '#B5E0C8')
    for x, y in ((12, 4), (19, 4), (11, 6), (20, 6), (14, 7), (17, 7), (13, 2), (18, 2)): it.px(x, y, BL)
    for x in range(9, 23):
        if x % 2: it.px(x, 9, BL)
    return it


@item('head', 'Берет', 'весна')
def beret(sex, ctx):
    C, Cd, Cl = '#7A3550', '#5C2740', '#9A4A6A'
    it = Item()
    it.px(17, 1, C); it.px(17, 2, C)
    it.rect(10, 3, 23, 3, C); it.rect(7, 4, 25, 5, C); it.rect(6, 6, 23, 6, Cd)
    it.rect(10, 3, 14, 3, Cl); it.rect(8, 4, 11, 4, Cl)
    it.rect(22, 4, 25, 5, Cd)
    return it


@item('head', 'Бандана', 'весна')
def bandana(sex, ctx):
    R, Rd = '#C4473F', '#9A3530'
    it = Item()
    it.rect(10, 3, 21, 3, R); it.rect(8, 4, 23, 9, R)
    it.rect(20, 4, 23, 9, Rd)
    for x, y in ((10, 5), (14, 4), (18, 6), (12, 8), (16, 8), (21, 7), (9, 7)): it.px(x, y, W)
    it.rect(24, 8, 25, 10, R); it.px(26, 11, R); it.px(26, 12, Rd); it.px(25, 12, R); it.px(27, 13, Rd)
    return it


@item('head', 'Панама', 'лето')
def panama(sex, ctx):
    C, Cd, Cl = '#D9C7A3', '#B09A74', '#EFE3C6'
    it = Item()
    it.rect(10, 2, 21, 2, C); it.rect(9, 3, 22, 6, C)
    it.rect(10, 2, 14, 2, Cl); it.rect(20, 3, 22, 6, Cd)
    it.rect(9, 6, 22, 6, '#6B8FB8')
    it.rect(6, 7, 25, 7, C); it.rect(5, 8, 26, 8, Cd); it.px(5, 9, Cd); it.px(26, 9, Cd)
    for x in range(10, 22, 3): it.px(x, 4, Cd)
    return it


@item('head', 'Соломенная шляпа', 'лето')
def straw(sex, ctx):
    C, Cd, Cl = '#E3C46A', '#B89A48', '#F2DC94'
    it = Item()
    it.rect(11, 1, 20, 1, C); it.rect(10, 2, 21, 5, C)
    it.rect(10, 5, 21, 5, '#C4473F')
    it.rect(2, 6, 29, 6, C); it.rect(3, 7, 28, 7, Cd)
    for x in range(3, 29, 2): it.px(x, 6, Cl)
    for y in (2, 4):
        for x in range(10 + y % 3, 22, 3): it.px(x, y, Cd)
    it.rect(19, 2, 21, 4, Cd)
    return it


@item('head', 'Праздничный колпак', 'день рождения')
def party(sex, ctx):
    cols = ['#E07A5F', '#F2CC8F', '#8FB3E0']
    it = Item()
    it.rect(15, 0, 16, 0, '#F4F1DE'); it.rect(14, 1, 17, 1, '#F4F1DE')
    for y in range(2, 8):
        half = 1 + (y - 2) * 2 // 3
        for x in range(15 - half, 17 + half):
            it.px(x, y, cols[((x - y) // 2) % 3])
    return it


@item('head', 'Ушки кролика', 'пасха')
def bunny(sex, ctx):
    P, Pd = '#E8A0A8', '#C27880'
    it = Item()
    it.rect(7, 6, 24, 6, P)
    for x0, top in ((9, 0), (19, 1)):
        it.rect(x0, top, x0 + 3, 5, W); it.rect(x0 + 1, top + 1, x0 + 2, 5, P)
        it.px(x0 + 3, top, Wd); it.rect(x0 + 3, top + 1, x0 + 3, 5, Wd)
    it.px(9, 0, '.'); it.erase(9, 0); it.erase(22, 1)
    return it


@item('head', 'Рога оленя', 'новый год')
def antlers(sex, ctx):
    A, Al = '#8A6A3B', '#A8865A'
    it = Item()
    it.rect(7, 5, 24, 5, '#C4473F')
    for side in (-1, 1):
        cx = 15.5 + side * 4.5
        x = int(cx)
        it.rect(x, 1, x, 4, A)
        it.px(x - side, 2, A); it.px(x - 2 * side, 1, Al)
        it.px(x + side, 3, A); it.px(x + 2 * side, 2, A); it.px(x + 3 * side, 1, Al)
        it.px(x, 0, Al)
    return it


@item('head', 'Шляпа ведьмы', 'хэллоуин')
def witch(sex, ctx):
    C, Cd, P = '#2E2547', '#221B36', '#9B6BC9'
    it = Item()
    rows = {0: (20, 22), 1: (18, 21), 2: (16, 20), 3: (14, 20), 4: (13, 20), 5: (12, 21), 6: (11, 21)}
    for y, (a, b) in rows.items(): it.rect(a, y, b, y, C)
    it.rect(19, 2, 21, 6, Cd)
    it.rect(10, 7, 22, 7, P); it.rect(15, 7, 16, 7, GOLD)
    it.rect(3, 8, 28, 8, C); it.rect(2, 9, 29, 9, Cd)
    return it


@item('head', 'Тюбетейка', 'народный')
def tubeteika(sex, ctx):
    C, Cd = '#24503F', '#1A3C2F'
    it = Item()
    it.rect(11, 2, 20, 2, C); it.rect(9, 3, 22, 7, C)
    it.rect(9, 8, 22, 8, GOLD)
    for x0 in (10, 15, 20):
        it.px(x0, 4, W); it.px(x0 + 1, 5, W); it.px(x0, 6, W)
    it.rect(21, 3, 22, 7, Cd)
    return it


@item('head', 'Цветок-канзаси', 'народный')
def kanzashi(sex, ctx):
    SAK, SAK_C = '#F4C6D4', '#E07A9A'
    it = Item()
    it.rect(20, 5, 22, 7, SAK); it.px(21, 4, SAK); it.px(23, 6, SAK); it.px(21, 6, SAK_C)
    it.px(23, 8, GOLD); it.px(24, 9, GOLD); it.px(24, 10, '#C4473F')
    it.no_outline.update({(x, y) for x in range(19, 26) for y in range(8, 11)})
    return it


@item('head', 'Ободок с сердечками', '14 февраля')
def hearts(sex, ctx):
    R = '#C4473F'
    it = Item()
    it.rect(7, 6, 24, 6, R)
    for x in (11, 20):
        it.rect(x, 3, x, 5, '#4A4F6E')
        heart(it, x, 0, '#E8607A', '#B8405A')
    return it


@item('head', 'Папаха', 'народный')
def papakha(sex, ctx):
    C, Cl, Cd = '#3A3646', '#625C72', '#272331'
    it = Item()
    it.rect(9, 0, 22, 0, C); it.rect(8, 1, 23, 9, C); it.erase(8, 1); it.erase(23, 1)
    # завитки каракуля: дуги 3×2
    for row, y in enumerate(range(1, 10, 2)):
        for x in range(8 + (row % 2) * 2, 23, 4):
            it.px(x, y, Cl); it.px(x + 1, y, Cl); it.px(x + 2, y + 1, Cd)
    it.rect(21, 1, 23, 9, Cd)
    for y in range(2, 10, 2): it.px(22, y, C)
    it.rect(10, 0, 14, 0, Cl)
    return it


@item('head', 'Сомбреро', 'мексиканский')
def sombrero(sex, ctx):
    C, Cd, Cl = '#D9B26A', '#B08A48', '#ECCB8A'
    it = Item()
    it.rect(12, 0, 19, 0, C); it.rect(11, 1, 20, 5, C)
    it.rect(11, 4, 20, 4, '#C4473F'); it.rect(11, 5, 20, 5, '#4FA88A')
    it.rect(18, 1, 20, 3, Cd)
    it.px(1, 5, C); it.px(30, 5, C)
    it.rect(1, 6, 30, 6, C); it.rect(2, 7, 29, 7, Cd)
    for x in range(3, 29, 3): it.px(x, 6, '#C4473F')
    it.rect(12, 1, 14, 1, Cl)
    return it


@item('head', 'Шлем космонавта', 'космос')
def helmet(sex, ctx):
    it = Item(); it.plain = True
    cx, cy, rx, ry = 15.5, 12.0, 13.2, 12.0
    for y in range(-1, 26):
        for x in range(1, 31):
            d = math.hypot((x - cx) / rx, (y - cy) / ry)
            if 0.93 <= d <= 1.06 and y <= 21: it.px(x, y, '#E8E6DA')
            elif 1.06 < d <= 1.15 and y <= 21: it.px(x, y, K)
    for x, y in ((8, 3), (7, 4), (6, 5), (6, 6), (9, 2)): it.px(x, y, '#BFE0F0')
    it.rect(7, 21, 24, 22, '#9AA0C0'); it.rect(7, 23, 24, 23, K); it.rect(8, 21, 23, 21, '#C9CBDD')
    it.px(6, 21, K); it.px(6, 22, K); it.px(25, 21, K); it.px(25, 22, K)
    return it


@item('head', 'Наушники', 'музыка')
def headphones(sex, ctx):
    B, C, Cd = '#4A4F6E', '#E07A5F', '#B8604A'
    it = Item()
    it.rect(9, 2, 22, 2, B); it.rect(7, 3, 8, 4, B); it.rect(23, 3, 24, 4, B)
    it.rect(6, 5, 6, 9, B); it.rect(25, 5, 25, 9, B)
    it.rect(4, 10, 7, 15, C); it.rect(24, 10, 27, 15, C)
    it.rect(4, 13, 7, 15, Cd); it.rect(24, 13, 27, 15, Cd)
    it.px(5, 11, '#F2A08A'); it.px(25, 11, '#F2A08A')
    return it
