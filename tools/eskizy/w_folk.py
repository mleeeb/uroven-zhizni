"""Народные наряды, волна 2: кавказский, индийский, шотландский, баварский, французский, арабский."""
from outfit import item, geo, hands, long_top, short_top, pants, hand_box
from px32 import Item, shade, K
from w_top import floor_coat
from w_low import legs_below, skirt, boot, bare_feet

W, Wd = '#F4F1DE', '#C9CBDD'
GOLD, GOLD_D = '#F2CC8F', '#C9A15F'
SILVER = '#C9CBDD'


def face_window(x, y):
    """Клетки лица, которые не закрывает платок."""
    return (10 <= x <= 21 and 10 <= y <= 19) or (11 <= x <= 20 and y == 20)


# ---------------- кавказский ----------------
@item('top', 'Черкеска с газырями', 'кавказский', sleeve='long', only='m')
def cherkeska(sex, ctx):
    C, Cd, Cl = '#2E2A36', '#1F1C26', '#4A4458'
    it = Item()
    g = long_top(it, sex, C, hem=37, Cd=Cd)
    it.rect(g['bx0'] - 1, 33, g['bx1'] + 1, 37, C); it.rect(g['bx1'] - 1, 33, g['bx1'] + 1, 37, Cd)
    it.rect(14, 21, 17, 25, '#6B6680'); it.rect(14, 21, 17, 21, SILVER)          # бешмет со стойкой
    for i, y in enumerate(range(26, 30)): it.px(14 + i // 2, y, Cl); it.px(17 - i // 2, y, Cl)
    for x0 in (10, 18):                                                            # газыри
        it.rect(x0, 24, x0 + 3, 27, Cd)
        for x in range(x0, x0 + 4): it.px(x, 23, SILVER)
        for x in range(x0, x0 + 4, 2): it.rect(x, 24, x, 26, Cl)
    it.rect(g['bx0'], 30, g['bx1'], 30, SILVER); it.rect(14, 30, 17, 31, '#9AA0C0')
    for y in range(31, 38): it.px(15, y, Cd)
    it.rect(g['sl'][0], 27, g['sl'][1], 28, Cl); it.rect(g['sr'][0], 27, g['sr'][1], 28, Cl)
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Кавказское платье', 'кавказский', long=True, sleeve='long', only='f')
def kavkaz_dress(sex, ctx):
    C, Cd = '#5A1E36', '#41152A'
    it = Item()
    g = floor_coat(it, sex, C, Cd)
    it.rect(15, 22, 16, 40, '#E8D8C0')
    for y in range(23, 30, 2): it.px(13, y, SILVER); it.px(14, y, SILVER); it.px(17, y, SILVER); it.px(18, y, SILVER)
    it.rect(g['bx0'], 30, g['bx1'], 31, SILVER)
    for x in range(g['bx0'], g['bx1'] + 1, 3): it.px(x, 31, '#9AA0C0')
    for x in range(g['bx0'] - 1, g['bx1'] + 2): it.px(x, 40, GOLD if x % 2 else GOLD_D)
    it.rect(g['sl'][0], 28, g['sl'][1], 28, GOLD); it.rect(g['sr'][0], 28, g['sr'][1], 28, GOLD)
    hands(it, sex, ctx['skin'])
    return it


@item('head', 'Шапочка с вуалью', 'кавказский', only='f')
def kavkaz_veil(sex, ctx):
    it = Item()
    it.rect(11, 2, 20, 2, '#5A1E36'); it.rect(10, 3, 21, 5, '#5A1E36')
    for x in range(10, 22, 2): it.px(x, 4, GOLD)
    it.rect(10, 5, 21, 5, GOLD_D)
    for y in range(6, 25):
        for x in list(range(5, 10)) + list(range(22, 27)):
            if y < 9 and (x < 7 or x > 24): continue
            it.px(x, y, W if (x + y) % 5 else Wd)
    it.rect(8, 6, 23, 7, W)
    for y in range(8, 25): it.px(9, y, Wd); it.px(22, y, Wd)
    return it


# ---------------- индийский ----------------
@item('head', 'Тюрбан', 'индийский')
def turban(sex, ctx):
    C, Cd, Cl = '#E8943A', '#C0702A', '#F4B464'
    it = Item()
    it.rect(11, 0, 20, 0, C); it.rect(9, 1, 22, 2, C); it.rect(8, 3, 23, 9, C)
    for k in range(6):
        for x in range(8, 24):
            if (x - k * 3) % 9 == 0: it.px(x, 3 + k, Cd)
    it.rect(9, 1, 13, 1, Cl); it.rect(8, 3, 9, 5, Cl)
    it.rect(21, 3, 23, 9, Cd)
    it.rect(15, 4, 16, 6, '#C4473F'); it.px(15, 4, '#F08A80'); it.px(15, 3, GOLD); it.px(16, 3, GOLD)
    it.px(15, 7, GOLD); it.px(16, 7, GOLD)
    return it


@item('face', 'Бинди', 'индийский', only='f')
def bindi(sex, ctx):
    it = Item(); it.plain = True
    it.px(15, 11, '#C4243A'); it.px(16, 11, '#C4243A')
    return it


@item('top', 'Курта', 'индийский', sleeve='long')
def kurta(sex, ctx):
    C, Cd = '#EDE3C8', '#CFC2A0'
    it = Item()
    g = long_top(it, sex, C, hem=36, Cd=Cd)
    it.rect(g['bx0'] - 1, 33, g['bx1'] + 1, 36, C); it.rect(g['bx1'] - 1, 33, g['bx1'] + 1, 36, Cd)
    it.rect(13, 21, 18, 21, GOLD)
    for y in range(22, 29): it.px(14, y, GOLD); it.px(17, y, GOLD_D)
    for y in (23, 25, 27): it.px(15, y, '#C4473F')
    for x in range(g['bx0'] - 1, g['bx1'] + 2): it.px(x, 36, GOLD if x % 2 else GOLD_D)
    it.rect(g['sl'][0], 28, g['sl'][1], 28, GOLD); it.rect(g['sr'][0], 28, g['sr'][1], 28, GOLD)
    hands(it, sex, ctx['skin'])
    return it


@item('bottom', 'Пайджама', 'индийский')
def pyjama(sex, ctx):
    it = Item()
    pants(it, W, Wd)
    for y in (35, 37): it.rect(9, y, 14, y, Wd); it.rect(17, y, 22, y, Wd)
    it.rect(9, 32, 22, 32, Wd)
    return it


@item('top', 'Сари', 'индийский', long=True, only='f')
def sari(sex, ctx):
    C, Cd, Ch = '#C2306A', '#962250', '#E8943A'
    it = Item()
    short_top(it, sex, Ch, hem=27, Cd=shade(Ch, 0.8))
    it.rect(11, 28, 20, 31, C); it.rect(10, 32, 21, 35, C); it.rect(9, 36, 22, 38, C); it.rect(8, 39, 23, 40, C)
    it.rect(20, 32, 21, 40, Cd); it.rect(22, 36, 23, 40, Cd)
    for y in range(31, 41): it.px(15, y, Cd); it.px(17, y, Cd)
    for x in range(8, 24): it.px(x, 40, GOLD if x % 2 else GOLD_D)
    for y in range(22, 32):                                   # палу через плечо
        x0 = 10 + (y - 22)
        it.rect(x0, y, x0 + 2, y, C); it.px(x0 + 3, y, GOLD)
    for y in range(23, 34): it.px(9, y, C); it.px(10, y, Cd) if y > 26 else None
    it.px(9, 34, GOLD); it.px(10, 34, GOLD)
    return it


@item('hands', 'Браслеты', 'индийский')
def bangles(sex, ctx):
    it = Item(); it.plain = True
    for x0, y0, x1, y1 in hand_box(sex, ctx['sleeve']):
        it.rect(x0, y0, x1, y0, GOLD); it.rect(x0, y0 + 1, x1, y0 + 1, '#C4243A')
        it.px(x0 + 1, y0, '#FFF6D8')
    return it


@item('shoes', 'Джутти', 'индийский')
def jutti(sex, ctx):
    C = '#B8343A'
    it = Item()
    bare_feet(it, ctx['skin'])
    it.rect(9, 40, 14, 42, C); it.rect(17, 40, 22, 42, C)
    it.rect(7, 41, 8, 42, C); it.rect(23, 41, 24, 42, C); it.px(6, 40, GOLD); it.px(25, 40, GOLD)
    for x in (10, 12, 18, 20): it.px(x, 41, GOLD)
    it.rect(9, 40, 14, 40, GOLD); it.rect(17, 40, 22, 40, GOLD)
    return it


# ---------------- шотландский ----------------
@item('head', 'Берет тэм-о-шентер', 'шотландский')
def tam(sex, ctx):
    N, Nd = '#2A3A7A', '#1E2A5C'
    it = Item()
    it.rect(15, 0, 16, 1, '#C4473F'); it.px(16, 0, '#E8706A')
    it.rect(10, 2, 21, 2, N); it.rect(6, 3, 25, 5, N); it.rect(5, 4, 26, 4, N)
    it.rect(10, 2, 14, 2, shade(N, 1.4)); it.rect(7, 3, 10, 3, shade(N, 1.4))
    it.rect(21, 3, 25, 5, Nd)
    for x in range(8, 24):
        it.px(x, 6, '#B8343A' if (x // 2) % 2 else '#2E6650'); it.px(x, 7, '#2E6650' if (x // 2) % 2 else '#F2CC8F')
    return it


@item('bottom', 'Красный килт со спораном', 'шотландский')
def kilt_red(sex, ctx):
    it = Item()
    skirt(it, '#B8343A', '#1E2A5C', '#12183A', ctx['skin'])
    for y in (34,): it.rect(8, y, 23, y, '#2E6650')
    it.rect(14, 33, 17, 36, '#EFE3C6'); it.rect(14, 33, 17, 33, '#4A3A2E')
    for x in (14, 16): it.px(x, 35, '#1E1A22'); it.px(x, 36, '#1E1A22')
    it.px(15, 32, SILVER); it.px(16, 32, SILVER)
    return it


@item('neck', 'Плед-тартан через плечо', 'шотландский')
def tartan_sash(sex, ctx):
    it = Item(); it.plain = True
    for y in range(22, 32):
        x0 = 9 + (y - 22) if sex == 'm' else 10 + (y - 22)
        for k in range(4):
            c = ['#1E2A5C', '#B8343A', '#2E6650', '#B8343A'][(k + y) % 4]
            it.px(x0 + k, y, c)
        it.px(x0 - 1, y, K); it.px(x0 + 4, y, K)
    it.rect(10, 22, 12, 23, SILVER); it.px(11, 22, '#81B29A')
    return it


@item('shoes', 'Гольфы и гилли', 'шотландский', tall=True)
def ghillies(sex, ctx):
    S, Sd = '#EDE3C8', '#CFC2A0'
    it = Item()
    it.rect(9, 37, 14, 39, S); it.rect(17, 37, 22, 39, S)
    it.rect(9, 37, 14, 37, Sd); it.rect(17, 37, 22, 37, Sd)
    it.px(9, 38, '#B8343A'); it.px(22, 38, '#B8343A')
    it.rect(8, 40, 14, 42, '#1E1A22'); it.rect(17, 40, 23, 42, '#1E1A22')
    for x in (10, 12, 19, 21): it.px(x, 40, '#4A4458')
    it.px(11, 39, '#1E1A22'); it.px(20, 39, '#1E1A22')
    for y in range(37, 43): it.line(15, y); it.line(16, y)
    return it


@item('top', 'Твидовый жакет', 'шотландский', sleeve='long')
def tweed(sex, ctx):
    C, Cd, Cl = '#4E6040', '#3A4A30', '#6A7C58'
    it = Item()
    g = long_top(it, sex, C, hem=33, Cd=Cd)
    for (x, y) in list(it.c):
        if (x * 3 + y * 5) % 7 == 0 and y > 22: it.px(x, y, Cl)
    it.rect(14, 21, 17, 22, W); it.rect(15, 23, 16, 24, W)
    it.rect(15, 23, 16, 26, '#B8343A')                       # галстук
    for i in range(5): it.px(13 - i // 3, 21 + i, Cd); it.px(18 + i // 3, 21 + i, Cd)
    for y in (27, 30): it.px(16, y, SILVER)
    it.rect(g['bx0'] + 1, 29, g['bx0'] + 3, 29, Cd); it.rect(g['bx1'] - 3, 29, g['bx1'] - 1, 29, Cd)
    hands(it, sex, ctx['skin'])
    return it


# ---------------- баварский ----------------
@item('head', 'Тирольская шляпа с пером', 'баварский')
def tyrol(sex, ctx):
    C, Cd, Cl = '#3E6B48', '#2E5236', '#548A60'
    it = Item()
    it.rect(11, 1, 20, 1, C); it.rect(10, 2, 21, 6, C)
    it.px(15, 1, Cd); it.px(16, 1, Cd); it.rect(15, 2, 16, 3, Cd)
    it.rect(10, 2, 12, 2, Cl); it.rect(19, 2, 21, 6, Cd)
    it.rect(10, 5, 21, 5, '#C4473F'); for_ = [it.px(x, 5, W) for x in range(11, 21, 3)]
    it.rect(6, 7, 25, 7, C); it.rect(5, 8, 7, 8, Cd); it.rect(24, 8, 26, 8, Cd); it.rect(8, 8, 23, 8, Cd)
    for x, y in ((22, 4), (23, 3), (23, 2), (24, 1), (24, 0), (25, 0)): it.px(x, y, '#9AA0C0')
    it.px(23, 4, W); it.px(24, 2, W)
    return it


@item('top', 'Рубашка с подтяжками', 'баварский', sleeve='long')
def trachten_shirt(sex, ctx):
    S = '#C4473F'; G = '#3E6B48'
    it = Item()
    g = long_top(it, sex, W, hem=31, Cd=Wd)
    for (x, y) in list(it.c):
        if y >= 22 and (x // 2 + y // 2) % 2 == 0: it.px(x, y, '#E8B4AE')
    for x0 in (11, 19):
        it.rect(x0, 22, x0 + 1, 31, G)
    it.rect(11, 25, 20, 26, G); it.px(15, 25, W); it.px(16, 26, W); it.px(15, 26, GOLD)
    it.rect(14, 21, 17, 21, W)
    hands(it, sex, ctx['skin'])
    return it


@item('bottom', 'Ледерхозе', 'баварский')
def lederhosen(sex, ctx):
    C, Cd, Cl = '#6B4A30', '#4E3522', '#8A6A48'
    it = Item()
    legs_below(it, 37, ctx['skin'], shade(ctx['skin'], 0.86))
    pants(it, C, Cd, bottom=36)
    it.rect(12, 32, 19, 34, Cl)
    for x in range(12, 20, 2): it.px(x, 33, '#81B29A')
    it.px(15, 32, GOLD); it.px(16, 34, GOLD)
    it.rect(9, 36, 14, 36, Cd); it.rect(17, 36, 22, 36, Cd)
    it.px(10, 35, '#3E6B48'); it.px(21, 35, '#3E6B48')
    return it


@item('top', 'Дирндль', 'баварский', long=True, only='f')
def dirndl(sex, ctx):
    B, Bd, R, Rd, A = '#2E5A46', '#22463A', '#A8323E', '#86262F', '#8FB3E0'
    it = Item()
    short_top(it, sex, W, hem=31, Cd=Wd)
    it.rect(7, 24, 9, 25, W); it.rect(22, 24, 24, 25, W)                  # пышные рукава
    it.rect(11, 24, 20, 31, B); it.rect(19, 25, 20, 31, Bd)
    it.rect(12, 23, 19, 23, W)
    for y in range(25, 31): it.px(15 if y % 2 else 16, y, GOLD)
    it.rect(10, 32, 21, 35, R); it.rect(9, 36, 22, 38, R)
    it.rect(20, 33, 21, 38, Rd); it.rect(22, 36, 22, 38, Rd)
    it.rect(12, 32, 19, 37, A); it.rect(12, 37, 19, 37, W); it.rect(18, 32, 19, 37, shade(A, 0.82))
    it.rect(20, 31, 21, 32, A); it.px(21, 33, A)
    return it


@item('shoes', 'Вязаные гольфы и туфли', 'баварский', tall=True)
def trachten_socks(sex, ctx):
    S, Sd = '#EDEBDD', '#C9CBDD'
    it = Item()
    it.rect(9, 36, 14, 39, S); it.rect(17, 36, 22, 39, S)
    for y in range(36, 40): it.px(11, y, Sd if y % 2 else S); it.px(19, y, Sd if y % 2 else S)
    it.rect(9, 36, 14, 36, Sd); it.rect(17, 36, 22, 36, Sd)
    it.rect(8, 40, 14, 42, '#5A3E2B'); it.rect(17, 40, 23, 42, '#5A3E2B')
    it.rect(8, 42, 14, 42, '#3A281C'); it.rect(17, 42, 23, 42, '#3A281C')
    it.px(11, 40, '#8A6A48'); it.px(20, 40, '#8A6A48')
    for y in range(36, 43): it.line(15, y); it.line(16, y)
    return it


# ---------------- французский ----------------
@item('head', 'Бретонский чепец', 'французский', only='f')
def coiffe(sex, ctx):
    it = Item()
    it.rect(12, 0, 19, 6, W)
    for y in range(0, 7):
        for x in range(12, 20):
            if (x + y) % 3 == 0: it.px(x, y, Wd)
    it.rect(8, 6, 23, 9, W); it.rect(7, 8, 8, 12, W); it.rect(23, 8, 24, 12, W)
    for x in range(8, 24, 2): it.px(x, 9, Wd)
    it.rect(19, 1, 19, 6, Wd)
    return it


@item('head', 'Канотье', 'французский')
def canotier(sex, ctx):
    C, Cd, Cl = '#E3C46A', '#B89A48', '#F2DC94'
    it = Item()
    it.rect(10, 2, 21, 2, Cl); it.rect(10, 3, 21, 6, C)
    it.rect(10, 5, 21, 6, '#1E1A22'); it.rect(19, 3, 21, 4, Cd)
    it.rect(4, 7, 27, 7, C); it.rect(5, 8, 26, 8, Cd)
    for x in range(5, 27, 2): it.px(x, 7, Cl)
    return it


@item('neck', 'Шейный платок', 'французский')
def neckerchief(sex, ctx):
    R, Rd = '#C4473F', '#9A3530'
    it = Item()
    it.rect(12, 21, 19, 21, R); it.rect(13, 22, 18, 22, R); it.rect(14, 23, 17, 23, R)
    it.rect(15, 22, 16, 23, Rd)
    it.px(14, 24, R); it.px(13, 25, R); it.px(17, 24, R); it.px(18, 25, Rd)
    for x, y in ((13, 21), (17, 21), (19, 21), (14, 22)): it.px(x, y, W)
    it.no_outline.update({(x, 20) for x in range(10, 22)})
    return it


@item('top', 'Бретонское платье', 'французский', long=True, sleeve='long', only='f')
def breton_dress(sex, ctx):
    B, Bd = '#1E1A22', '#2E2836'
    it = Item()
    g = floor_coat(it, sex, B, Bd)
    for y, c in ((22, '#E8943A'), (23, GOLD), (24, '#E8943A'), (25, '#C4473F'), (26, GOLD), (27, '#E8943A')):
        it.rect(12, y, 19, y, c)
    it.rect(11, 28, 20, 39, W); it.rect(11, 39, 20, 39, Wd)
    for y in range(29, 39, 2):
        for x in range(11 + (y % 4) // 2, 21, 2): it.px(x, y, Wd)
    it.rect(g['sl'][0], 27, g['sl'][1], 28, '#E8943A'); it.rect(g['sr'][0], 27, g['sr'][1], 28, '#E8943A')
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Бретонская куртка', 'французский', sleeve='long')
def breton_jacket(sex, ctx):
    B, Bd = '#1E1A22', '#2E2836'
    it = Item()
    g = long_top(it, sex, B, hem=31, Cd=Bd)
    it.rect(14, 21, 17, 24, W)
    for y in range(22, 32): it.px(13, y, '#E8943A'); it.px(18, y, '#E8943A')
    for y in (25, 27, 29): it.px(11, y, GOLD); it.px(20, y, GOLD); it.px(12, y, GOLD_D); it.px(19, y, GOLD_D)
    it.rect(g['bx0'], 31, g['bx1'], 31, '#E8943A')
    it.rect(g['sl'][0], 28, g['sl'][1], 28, GOLD); it.rect(g['sr'][0], 28, g['sr'][1], 28, GOLD)
    hands(it, sex, ctx['skin'])
    return it


@item('shoes', 'Сабо', 'французский')
def sabots(sex, ctx):
    C, Cd, Cl = '#C9A15F', '#A07C40', '#E0C080'
    it = Item()
    it.rect(9, 39, 14, 42, C); it.rect(17, 39, 22, 42, C)
    it.rect(7, 40, 8, 42, C); it.rect(23, 40, 24, 42, C); it.px(6, 41, C); it.px(25, 41, C)
    it.rect(9, 39, 14, 39, Cd); it.rect(17, 39, 22, 39, Cd)
    it.rect(10, 40, 12, 40, Cl); it.rect(18, 40, 20, 40, Cl)
    it.rect(7, 42, 14, 42, Cd); it.rect(17, 42, 24, 42, Cd)
    for y in range(39, 43): it.line(15, y); it.line(16, y)
    it.no_outline.update({(x, 38) for x in range(8, 24)})
    return it


# ---------------- арабский ----------------
@item('head', 'Куфия с игалем', 'арабский', only='m')
def kufiya(sex, ctx):
    R = '#C4473F'
    it = Item()
    for y in range(3, 25):
        for x in range(5, 27):
            if face_window(x, y) or (y < 5 and (x < 9 or x > 22)) or (y >= 10 and 10 <= x <= 21): continue
            if y >= 21 and 10 <= x <= 21: continue
            it.px(x, y, W if (x // 2 + y // 2) % 2 else '#E8C8C0')
            if (x + y) % 4 == 0 and y < 10: it.px(x, y, R)
    for y in range(10, 25): it.px(9, y, Wd); it.px(22, y, Wd)
    it.rect(8, 5, 23, 6, '#1E1A22'); it.rect(9, 5, 22, 5, '#3A3646')
    return it


@item('head', 'Платок-хиджаб', 'арабский', only='f')
def hijab(sex, ctx):
    C, Cd, Cl = '#3D7A7A', '#2E6060', '#5A9A9A'
    it = Item()
    rows = {3: (10, 21), 4: (8, 23), 5: (7, 24)}
    for y in range(6, 20): rows[y] = (6, 25)
    rows.update({20: (6, 25), 21: (5, 26), 22: (5, 26), 23: (6, 25), 24: (8, 23), 25: (11, 20)})
    for y, (a, b) in rows.items():
        for x in range(a, b + 1):
            if not face_window(x, y): it.px(x, y, C)
    for y in range(10, 21): it.px(9, y, Cd); it.px(22, y, Cd)
    it.rect(11, 3, 15, 3, Cl); it.rect(8, 5, 9, 5, Cl); it.rect(7, 6, 7, 10, Cl)
    it.rect(24, 6, 25, 20, Cd); it.rect(10, 21, 21, 21, Cd); it.rect(9, 24, 22, 24, Cd); it.rect(24, 21, 26, 23, Cd)
    return it


@item('top', 'Тауб', 'арабский', long=True, sleeve='long', only='m')
def thobe(sex, ctx):
    it = Item()
    g = floor_coat(it, sex, W, Wd)
    it.rect(13, 21, 18, 21, Wd)
    for y in range(22, 29): it.px(15, y, Wd)
    for y in (23, 25, 27): it.px(16, y, '#9AA0C0')
    it.rect(g['bx0'] + 1, 31, g['bx0'] + 3, 31, Wd)
    hands(it, sex, ctx['skin'])
    return it


@item('top', 'Абая с узором', 'арабский', long=True, sleeve='long', only='f')
def abaya(sex, ctx):
    B, Bd = '#1E1A22', '#2E2836'
    it = Item()
    g = floor_coat(it, sex, B, Bd)
    for y in range(22, 41): it.px(14, y, GOLD if y % 2 else '#3D7A7A'); it.px(17, y, GOLD if y % 2 == 0 else '#3D7A7A')
    for side in (g['sl'], g['sr']):
        for x in range(side[0], side[1] + 1): it.px(x, 27, GOLD); it.px(x, 28, '#3D7A7A' if x % 2 else GOLD)
    for x in range(g['bx0'] - 1, g['bx1'] + 2): it.px(x, 40, GOLD if x % 2 else '#3D7A7A')
    hands(it, sex, ctx['skin'])
    return it


@item('shoes', 'Бабуши', 'арабский')
def babouche(sex, ctx):
    C, Cd = '#E8C547', '#C4A030'
    it = Item()
    bare_feet(it, ctx['skin'])
    it.rect(9, 40, 14, 42, C); it.rect(17, 40, 22, 42, C)
    it.rect(7, 41, 8, 42, C); it.rect(23, 41, 24, 42, C); it.px(6, 42, C); it.px(25, 42, C)
    it.rect(14, 40, 14, 42, Cd); it.rect(17, 40, 17, 42, Cd)
    it.rect(9, 42, 14, 42, Cd); it.rect(17, 42, 22, 42, Cd)
    return it
