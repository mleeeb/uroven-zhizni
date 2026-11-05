"""Герой 32 x 44: база (мужской и женский), лица, слой вещей с контуром, отрисовка в PNG."""
from PIL import Image, ImageDraw

W, H = 32, 44
K = '#0C0E22'
BG = '#1B1E3A'


def shade(hex_, k):
    n = int(hex_[1:], 16)
    return '#' + ''.join(f'{max(0, min(255, round(c * k))):02x}' for c in (n >> 16 & 255, n >> 8 & 255, n & 255))


SKINS = ['#F2CC8F', '#E0AC7E', '#B97A56', '#7A4E33']
HAIRS = ['#2B1D14', '#6B4226', '#C98A3D', '#E8D27A', '#A33B2E']
SHIRTS = ['#E07A5F', '#3D5A80', '#81B29A', '#9B6BC9', '#D9D4BE']
WHITE, GREY = '#E8E6DA', '#9A99B0'


class Canvas:
    def __init__(self, w=W, h=H):
        self.w, self.h = w, h
        self.g = [['.'] * w for _ in range(h)]

    def px(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h: self.g[y][x] = c

    def get(self, x, y):
        return self.g[y][x] if 0 <= x < self.w and 0 <= y < self.h else '.'

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): self.px(x, y, c)

    def outline(self):
        """Контур снаружи всего закрашенного."""
        f = [[c != '.' for c in row] for row in self.g]
        for y in range(self.h):
            for x in range(self.w):
                if f[y][x]: continue
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < self.w and 0 <= ny < self.h and f[ny][nx]:
                        self.g[y][x] = K; break

    def image(self, scale=8, bg=None, pad=0):
        img = Image.new('RGBA', ((self.w + 2 * pad) * scale, (self.h + 2 * pad) * scale), bg or (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        for y, row in enumerate(self.g):
            for x, c in enumerate(row):
                if c == '.': continue
                d.rectangle([(x + pad) * scale, (y + pad) * scale, (x + pad + 1) * scale - 1, (y + pad + 1) * scale - 1], fill=c)
        return img


class Item:
    """Вещь: набор клеток; кладётся поверх героя и обводится контуром.
    keep_line=False — не обводить там, где вещь граничит с героем (например, пояс к брюкам)."""

    def __init__(self):
        self.c = {}
        self.lines = set()      # клетки контура, которые надо добавить принудительно
        self.no_outline = set()  # клетки рядом, которые нельзя закрашивать контуром

    def px(self, x, y, col):
        self.c[(x, y)] = col

    def rect(self, x0, y0, x1, y1, col):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1): self.c[(x, y)] = col

    def erase(self, x, y):
        self.c.pop((x, y), None)

    def line(self, x, y):
        self.lines.add((x, y))

    def apply(self, cv: Canvas):
        for (x, y) in getattr(self, 'clear', ()): cv.px(x, y, '.')
        for (x, y), col in self.c.items(): cv.px(x, y, col)
        for (x, y) in ([] if getattr(self, 'plain', False) else list(self.c)):
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (x + dx, y + dy)
                if n not in self.c and n not in self.no_outline:
                    cv.px(n[0], n[1], K)
        for (x, y) in self.lines: cv.px(x, y, K)

    def alone(self, w=W, h=H):
        cv = Canvas(w, h)
        self.apply(cv)
        return cv


# ---------------- лица ----------------
def face(cv, sex, variant, skin, hair):
    S, Sd = skin, shade(skin, 0.86)
    Hd = shade(hair, 0.72)
    lip = '#9E4A4E' if sex == 'm' else '#B24E5E'
    p = cv.px
    if variant == 'A':      # спокойное: глаза 1×2, прямой рот
        cv.rect(11, 11, 13, 11, Hd); cv.rect(18, 11, 20, 11, Hd)
        cv.rect(12, 12, 12, 13, K); cv.rect(19, 12, 19, 13, K)
        p(16, 14, Sd); p(16, 15, Sd); p(15, 15, Sd)
        cv.rect(14, 17, 17, 17, lip)
    elif variant == 'B':    # улыбка: глаза 1×2, рот с поднятыми уголками
        cv.rect(11, 11, 13, 11, Hd); cv.rect(18, 11, 20, 11, Hd)
        cv.rect(12, 12, 12, 13, K); cv.rect(19, 12, 19, 13, K)
        p(16, 14, Sd); p(16, 15, Sd); p(15, 15, Sd)
        cv.rect(14, 17, 17, 17, lip); p(13, 16, lip); p(18, 16, lip)
    elif variant == 'C':    # мягкое: глаза 2×2 без блика, короткий рот
        cv.rect(11, 11, 13, 11, Hd); cv.rect(18, 11, 20, 11, Hd)
        cv.rect(12, 12, 13, 13, K); cv.rect(18, 12, 19, 13, K)
        p(16, 15, Sd); p(15, 15, Sd)
        cv.rect(15, 17, 17, 17, lip)
    elif variant == 'kid':  # первый (детский) вариант — для сравнения
        cv.rect(11, 11, 13, 11, Hd); cv.rect(18, 11, 20, 11, Hd)
        cv.rect(12, 12, 13, 14, K); cv.rect(18, 12, 19, 14, K)
        p(13, 12, WHITE); p(19, 12, WHITE)
        p(16, 15, Sd)
        for x in (10, 11, 20, 21): p(x, 16, '#E8A07A')
        cv.rect(14, 17, 17, 17, '#8E3B46'); p(13, 16, '#8E3B46'); p(18, 16, '#8E3B46')
    if sex == 'f':          # ресницы
        p(11, 12, K); p(20, 12, K)
    # скулы / тень по краям лица (взрослее)
    if variant in ('A', 'B', 'C'):
        for y in range(15, 18): p(8, y, Sd); p(23, y, Sd)


# ---------------- база ----------------
def base(sex='m', skin=0, hair=1, shirt=0, face_v='A', hair_style=None, beard=False):
    S = SKINS[skin] if isinstance(skin, int) else skin
    Sd = shade(S, 0.86)
    Hc = HAIRS[hair] if isinstance(hair, int) else hair
    Hd, Hl = shade(Hc, 0.72), shade(Hc, 1.35)
    T = SHIRTS[shirt] if isinstance(shirt, int) else shirt
    Td = shade(T, 0.78)
    JEANS, JD, JL = '#3D5A80', shade('#3D5A80', 0.72), shade('#3D5A80', 1.3)
    RED, RD = '#C4473F', shade('#C4473F', 0.75)
    GOLD, GOLD_D = '#F2CC8F', '#C9A15F'
    cv = Canvas()
    r, p = cv.rect, cv.px
    style = hair_style or ('short' if sex == 'm' else 'long')
    if style == 'long':   # волосы за шеей
        r(8, 18, 23, 23, Hd)
    if style == 'pony':   # хвост за головой
        r(24, 7, 27, 9, Hc); r(25, 10, 28, 19, Hc); r(26, 20, 27, 21, Hc); r(27, 11, 28, 19, Hd)
    # голова
    r(7, 5, 24, 17, S); r(8, 18, 23, 18, S); r(9, 19, 22, 19, S); r(11, 20, 20, 20, S)
    for xy in ((7, 5), (24, 5), (7, 17), (24, 17)): p(*xy, '.')
    r(14, 21, 17, 22, Sd)
    r(11, 20, 20, 20, Sd)
    # тело
    if sex == 'm':
        r(9, 23, 22, 31, T); r(10, 22, 21, 22, T)
        r(5, 24, 8, 26, T); r(23, 24, 26, 26, T)
        r(5, 26, 8, 26, Td); r(23, 26, 26, 26, Td)
        r(22, 24, 22, 31, Td); p(21, 30, Td)
        r(9, 31, 22, 31, Td)
        r(5, 27, 7, 30, S); p(6, 30, Sd); p(7, 30, Sd)
        r(24, 27, 26, 30, S); p(24, 30, Sd); p(25, 30, Sd)
        arm_l, arm_r = 8, 23
        cx0, cx1 = 9, 22
    else:
        r(11, 22, 20, 31, T); r(9, 23, 22, 23, T)
        r(7, 24, 24, 25, T); r(7, 26, 9, 26, Td); r(22, 26, 24, 26, Td)
        r(20, 24, 20, 31, Td); r(11, 31, 20, 31, Td)
        r(7, 27, 9, 30, S); p(8, 30, Sd); p(9, 30, Sd)
        r(22, 27, 24, 30, S); p(22, 30, Sd); p(23, 30, Sd)
        arm_l, arm_r = 10, 21
        cx0, cx1 = 11, 20
    # вырез
    r(14, 22, 17, 22, Sd); r(15, 23, 16, 23, Sd)
    # принт (только у мужского — как «футболка с принтом»)
    if sex == 'm':
        r(15, 25, 16, 28, GOLD); r(14, 26, 17, 27, GOLD); p(16, 27, GOLD_D); p(16, 28, GOLD_D); p(17, 27, GOLD_D)
    # джинсы
    r(9, 32, 22, 33, JEANS); r(9, 34, 14, 38, JEANS); r(17, 34, 22, 38, JEANS)
    r(9, 32, 22, 32, JD); p(15, 32, GOLD)
    p(11, 33, JL); p(20, 33, JL)
    r(13, 34, 14, 38, JD); r(21, 34, 22, 38, JD)
    p(10, 35, JL); p(18, 35, JL)
    r(9, 38, 14, 38, JL); r(17, 38, 22, 38, JL)
    # кеды
    r(9, 39, 14, 40, RED); r(17, 39, 22, 40, RED); r(8, 41, 14, 41, RED); r(17, 41, 23, 41, RED)
    p(11, 39, WHITE); p(12, 40, WHITE); p(20, 39, WHITE); p(19, 40, WHITE)
    r(13, 39, 14, 41, RD); r(22, 39, 23, 41, RD)
    r(7, 42, 14, 42, WHITE); r(17, 42, 24, 42, WHITE); p(7, 41, WHITE); p(24, 41, WHITE)
    r(13, 42, 14, 42, GREY); r(17, 42, 18, 42, GREY)
    # волосы
    r(7, 5, 24, 9, Hc); p(7, 5, '.'); p(24, 5, '.')
    if style == 'short':
        r(7, 10, 9, 12, Hc); r(22, 10, 24, 12, Hc)
        r(10, 10, 14, 10, Hc); p(10, 11, Hc)
        r(10, 6, 14, 6, Hl); p(9, 7, Hl)
        r(15, 9, 21, 9, Hd); p(8, 12, Hd); p(23, 12, Hd)
        r(15, 10, 21, 10, Sd)
    elif style == 'buzz':
        r(8, 8, 23, 9, S)
        for x in range(8, 24, 2): p(x, 8, Hd)
        r(7, 8, 7, 11, Hd); r(24, 8, 24, 11, Hd)
        r(10, 6, 14, 6, Hl)
    elif style == 'bangs':
        r(7, 10, 9, 12, Hc); r(22, 10, 24, 12, Hc)
        r(9, 10, 21, 10, Hc)
        for x in (10, 11, 13, 14, 16, 17, 19, 20): p(x, 11, Hc)
        r(10, 6, 14, 6, Hl); p(9, 7, Hl)
        r(16, 9, 21, 9, Hd); p(8, 12, Hd); p(23, 12, Hd)
    elif style == 'pony':
        r(7, 10, 8, 12, Hc); r(23, 10, 24, 12, Hc)
        r(9, 10, 13, 10, Hc); p(9, 11, Hc)
        r(10, 6, 14, 6, Hl); p(9, 7, Hl)
        r(15, 9, 21, 9, Hd); r(15, 10, 21, 10, Sd)
        p(24, 8, '#C4473F'); p(24, 9, '#C4473F')
    elif style == 'bob':
        r(5, 8, 8, 18, Hc); r(23, 8, 26, 18, Hc); r(6, 7, 7, 7, Hc); r(24, 7, 25, 7, Hc)
        r(9, 10, 22, 10, Hc)
        for x in (10, 13, 16, 19, 21): p(x, 11, Hc)
        r(10, 6, 15, 6, Hl); p(9, 7, Hl); r(6, 10, 6, 13, Hl)
        r(8, 13, 8, 18, Hd); r(23, 13, 23, 18, Hd); r(25, 10, 25, 17, Hd)
    elif style == 'long':
        r(5, 8, 8, 24, Hc); r(23, 8, 26, 24, Hc); p(5, 24, '.'); p(26, 24, '.')
        r(6, 7, 7, 7, Hc); r(24, 7, 25, 7, Hc)
        r(9, 10, 16, 10, Hc); r(9, 11, 11, 11, Hc); p(9, 12, Hc)
        r(17, 10, 22, 10, Sd)
        r(11, 6, 15, 6, Hl); p(10, 7, Hl); r(6, 10, 6, 12, Hl)
        r(8, 13, 8, 24, Hd); r(23, 13, 23, 24, Hd); r(16, 9, 22, 9, Hd)
        r(25, 10, 25, 23, Hd); p(26, 23, Hd)
    face(cv, sex, face_v, S, Hc)
    if beard:
        for y in range(14, 18): p(8, y, Hc); p(9, y, Hc); p(22, y, Hc); p(23, y, Hc)
        r(9, 18, 22, 18, Hc); r(10, 19, 21, 19, Hc); r(11, 20, 20, 20, Hc)
        r(13, 16, 18, 16, Hc); p(12, 17, Hc); p(19, 17, Hc)
        r(12, 19, 19, 20, Hd)
    if face_v in ('A', 'B', 'C') and style == 'long':
        for y in range(15, 18): p(8, y, Hd); p(23, y, Hd)
    cv.outline()
    # внутренние линии
    for y in range(27, 31): p(arm_l, y, K); p(arm_r, y, K)
    for y in range(34, 43): p(15, y, K); p(16, y, K)
    if style == 'long':
        for y in range(23, 26): p(9, y, K) if sex == 'm' else None
    return cv


def sheet(images, gap=24, bg=BG, pad=20):
    W_ = sum(i.width for i in images) + gap * (len(images) - 1) + 2 * pad
    H_ = max(i.height for i in images) + 2 * pad
    out = Image.new('RGBA', (W_, H_), bg)
    x = pad
    for i in images:
        out.paste(i, (x, pad + (H_ - 2 * pad - i.height)), i)
        x += i.width + gap
    return out
