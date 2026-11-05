"""Лицо, шея, руки."""
from outfit import item, hand_box
from px32 import Item, shade, K

W, Wd = '#F4F1DE', '#C9CBDD'
GOLD, GOLD_D = '#F2CC8F', '#C9A15F'


# ---------------- лицо ----------------
@item('face', 'Круглые очки')
def glasses(sex, ctx):
    F = '#3A2A1F'
    it = Item(); it.plain = True
    for x0 in (10, 17):
        it.rect(x0 + 1, 11, x0 + 3, 11, F); it.rect(x0 + 1, 14, x0 + 3, 14, F)
        it.rect(x0, 12, x0, 13, F); it.rect(x0 + 4, 12, x0 + 4, 13, F)
        it.px(x0 + 3, 12, '#FFFFFF')
    it.rect(15, 12, 16, 12, F); it.rect(8, 12, 9, 12, F); it.rect(22, 12, 23, 12, F)
    return it


@item('face', 'Солнечные очки', 'лето')
def sunglasses(sex, ctx):
    L = '#1E1A22'
    it = Item(); it.plain = True
    it.rect(10, 11, 21, 11, K)
    for x0 in (10, 17):
        it.rect(x0, 12, x0 + 4, 13, L); it.rect(x0 + 1, 14, x0 + 3, 14, L)
        it.px(x0 + 1, 12, '#6A70A0'); it.px(x0 + 2, 12, '#4A4F6E')
    it.rect(15, 12, 16, 12, K); it.rect(8, 12, 9, 12, K); it.rect(22, 12, 23, 12, K)
    return it


@item('face', 'Борода Деда Мороза', 'новый год')
def ded_beard(sex, ctx):
    it = Item()
    it.rect(9, 16, 22, 21, W); it.rect(10, 22, 21, 24, W); it.rect(12, 25, 19, 26, W); it.rect(14, 27, 17, 27, W)
    it.rect(11, 15, 20, 15, W)
    it.rect(13, 16, 18, 16, Wd); it.px(15, 17, '#9E4A4E'); it.px(16, 17, '#9E4A4E')
    for x, y in ((11, 20), (14, 23), (18, 22), (20, 19), (16, 25)): it.px(x, y, Wd)
    it.no_outline.update({(x, 14) for x in range(10, 22)})
    return it


@item('face', 'Усы', only='m')
def mustache(sex, ctx):
    H = shade(ctx['hair'], 0.85)
    it = Item(); it.plain = True
    it.rect(13, 15, 18, 15, H); it.rect(12, 16, 13, 16, H); it.rect(18, 16, 19, 16, H)
    it.px(11, 15, H); it.px(20, 15, H)
    return it


@item('face', 'Карнавальная маска', 'новый год')
def mask(sex, ctx):
    V, Vd = '#9B6BC9', '#7A4FA8'
    it = Item(); it.plain = True
    it.rect(10, 10, 21, 10, K)
    it.rect(9, 11, 22, 11, V); it.rect(8, 12, 23, 13, V); it.rect(9, 14, 14, 14, V); it.rect(17, 14, 22, 14, V)
    it.rect(11, 12, 13, 13, K); it.rect(18, 12, 20, 13, K)
    it.px(12, 12, '#0C0E22')
    for x in (10, 13, 18, 21): it.px(x, 11, GOLD)
    it.px(9, 13, Vd); it.px(22, 13, Vd); it.rect(15, 14, 16, 14, '.')
    it.erase(15, 14); it.erase(16, 14)
    it.rect(9, 15, 13, 15, K); it.rect(18, 15, 22, 15, K); it.px(7, 12, K); it.px(7, 13, K); it.px(24, 12, K); it.px(24, 13, K)
    it.px(14, 15, K); it.px(17, 15, K)
    return it


@item('face', 'Пиратская повязка')
def eyepatch(sex, ctx):
    it = Item(); it.plain = True
    for x in range(7, 11): it.px(x, 9 + (x - 7) // 2, K)
    for x in range(15, 25): it.px(x, 11 - (x - 15) // 4, K)
    it.rect(10, 11, 14, 14, '#1E1A22'); it.erase(10, 14); it.erase(14, 14)
    it.px(11, 12, '#4A4458')
    return it


@item('face', 'Красный нос', 'новый год')
def rednose(sex, ctx):
    it = Item(); it.plain = True
    it.rect(15, 14, 16, 15, '#D9443F'); it.px(15, 14, '#F08A80')
    it.rect(15, 13, 16, 13, K); it.px(14, 14, K); it.px(14, 15, K); it.px(17, 14, K); it.px(17, 15, K)
    it.rect(15, 16, 16, 16, K)
    return it


# ---------------- шея ----------------
@item('neck', 'Вязаный шарф', 'зима')
def scarf(sex, ctx):
    R, Rd = '#C4473F', '#9A3530'
    it = Item()
    it.rect(11, 21, 20, 23, R)
    it.rect(11, 22, 20, 22, W)
    it.rect(17, 24, 19, 30, R)
    for y in (25, 28): it.rect(17, y, 19, y, W)
    it.rect(19, 21, 20, 23, Rd); it.rect(19, 24, 19, 30, Rd)
    for x in (17, 19): it.px(x, 31, W)
    it.no_outline.update({(x, 20) for x in range(10, 22)})
    return it


@item('neck', 'Галстук-бабочка')
def bowtie(sex, ctx):
    R, Rd = '#C4473F', '#9A3530'
    it = Item()
    it.rect(12, 21, 13, 24, R); it.px(14, 22, R); it.px(14, 23, R)
    it.rect(18, 21, 19, 24, R); it.px(17, 22, R); it.px(17, 23, R)
    it.rect(15, 22, 16, 23, Rd)
    it.px(12, 21, shade(R, 1.2)); it.px(18, 21, shade(R, 1.2))
    it.no_outline.update({(x, 20) for x in range(10, 22)})
    return it


@item('neck', 'Коралловые бусы', 'народный')
def beads(sex, ctx):
    it = Item(); it.plain = True
    for i, x in enumerate(range(10, 22)):
        y = 22 + round(3 * (1 - ((x - 15.5) / 6) ** 2))
        it.px(x, y, '#D9443F' if i % 2 == 0 else '#F08A80')
        it.px(x, y + 1, '#7A2A28')
    return it


@item('neck', 'Фотоаппарат', 'путешествия')
def camera(sex, ctx):
    it = Item()
    it.rect(12, 26, 19, 29, '#3A3F63'); it.rect(12, 26, 19, 26, '#4A4F6E')
    it.rect(14, 27, 17, 29, '#1E1A22'); it.rect(15, 27, 16, 28, '#8FB3E0'); it.px(15, 27, '#E8F0F8')
    it.px(18, 27, W); it.rect(12, 25, 13, 25, '#3A3F63')
    for (x, y) in ((11, 22), (11, 23), (12, 24), (20, 22), (20, 23), (19, 24)): it.line(x, y)
    return it


@item('neck', 'Гавайские цветы', 'лето')
def lei(sex, ctx):
    cols = ['#E8A0A8', '#F2CC8F', '#F4F1DE', '#E07A5F']
    it = Item(); it.plain = True
    for i, x in enumerate(range(10, 22)):
        y = 22 + round(3 * (1 - ((x - 15.5) / 6) ** 2))
        it.px(x, y, cols[i % 4]); it.px(x, y - 1, cols[(i + 2) % 4])
        it.px(x, y + 1, shade(cols[i % 4], 0.7))
    return it


@item('neck', 'Медаль', 'спорт')
def medal(sex, ctx):
    it = Item(); it.plain = True
    for i in range(4):
        it.px(12 + i // 2 + i % 2, 22 + i, '#3D5A80'); it.px(19 - i // 2 - i % 2, 22 + i, '#C4473F')
    it.rect(14, 26, 17, 29, GOLD); it.rect(14, 29, 17, 29, GOLD_D); it.px(15, 27, '#FFF6D8')
    it.rect(14, 30, 17, 30, K); it.rect(13, 26, 13, 29, K); it.rect(18, 26, 18, 29, K)
    return it


# ---------------- руки ----------------
def mitts(ctx, sex, C, cuff, pattern=None, grow=0):
    it = Item()
    for x0, y0, x1, y1 in hand_box(sex, ctx['sleeve']):
        it.rect(x0 - grow, y0, x1 + grow, y1 + grow, C)
        it.rect(x0 - grow, y0, x1 + grow, y0, cuff)
        it.erase(x0 - grow, y1 + grow); it.erase(x1 + grow, y1 + grow)
        if pattern: it.px(x0 + 1, y0 + 2, pattern)
    return it


@item('hands', 'Красные варежки', 'зима')
def mittens_red(sex, ctx):
    return mitts(ctx, sex, '#C4473F', W, W)


@item('hands', 'Белые варежки', 'зима')
def mittens_white(sex, ctx):
    return mitts(ctx, sex, W, '#8FB3E0', '#8FB3E0')


@item('hands', 'Кожаные перчатки', 'осень')
def gloves(sex, ctx):
    it = mitts(ctx, sex, '#2A2226', '#4A3A3E')
    for x0, y0, x1, y1 in hand_box(sex, ctx['sleeve']):
        it.px(x0 + 1, y1, '#4A3A3E')
    return it


@item('hands', 'Боксёрские перчатки', 'спорт')
def boxing(sex, ctx):
    it = mitts(ctx, sex, '#C4473F', W, None, grow=1)
    for x0, y0, x1, y1 in hand_box(sex, ctx['sleeve']):
        it.px(x0, y0 + 1, '#E8706A')
    return it
