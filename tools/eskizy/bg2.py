"""Фоны на всю карточку героя, 96 x 88. Герой стоит в (32, 35), земля — y 78.
Слоты дохода/жилья закрывают бока (x 0–26 и 70–95, y 33–78): главное — сверху и по центру."""
import math
import random
from px32 import Canvas, K
from bg import paste, moon, twinkle, stars, tree as xmas_tree

WW, HH = 96, 88


def grad(cv, cols, y0, y1, x0=0, x1=WW - 1):
    n = len(cols) - 1
    for y in range(y0, y1 + 1):
        t = (y - y0) / max(1, y1 - y0) * n
        i = min(int(t), n); f = t - i
        for x in range(x0, x1 + 1):
            c = cols[i]
            if i < n and (f > 0.66 or (f > 0.33 and (x + y) % 2 == 0)): c = cols[i + 1]
            cv.px(x, y, c)


def disc(cv, cx, cy, r, col, edge=None):
    for y in range(int(cy - r - 1), int(cy + r + 2)):
        for x in range(int(cx - r - 1), int(cx + r + 2)):
            d = math.hypot(x - cx, y - cy)
            if d <= r: cv.px(x, y, col)
            elif edge and d <= r + 1: cv.px(x, y, edge)


def blob(cv, cx, cy, rx, ry, col, rnd=None, rough=0.0):
    for y in range(int(cy - ry - 1), int(cy + ry + 2)):
        for x in range(int(cx - rx - 1), int(cx + rx + 2)):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if d <= 1 - (rnd.random() * rough if rnd else 0): cv.px(x, y, col)


def cloud(cv, x, y, w, col='#F4F1DE', sh='#C9CBDD'):
    for k in range(0, w, 4):
        disc(cv, x + k, y - (2 if k % 8 else 0), 3, col)
    for xx in range(x - 2, x + w + 2): cv.px(xx, y + 3, sh)


def mountains(cv, rnd, base, peaks, col, light, snow=None):
    for (px_, top, w) in peaks:
        for y in range(top, base + 1):
            half = int((y - top) * w / max(1, base - top))
            for x in range(px_ - half, px_ + half + 1):
                cv.px(x, y, light if x < px_ else col)
            if snow and y < top + (base - top) // 4:
                for x in range(px_ - half, px_ + half + 1): cv.px(x, y, snow if x <= px_ else '#C9CBDD')


def ground(cv, y0, cols, rnd, dots=None):
    grad(cv, cols, y0, HH - 1)
    if dots:
        for _ in range(WW):
            cv.px(rnd.randrange(WW), rnd.randrange(y0 + 1, HH), rnd.choice(dots))


def leafy_tree(cv, rnd, x, base, h, crown, cols, trunk='#5A3E2B', fruit=None):
    for y in range(base - h, base): cv.px(x, y, trunk); cv.px(x + 1, y, trunk)
    cy = base - h
    for c, (dx, dy, r) in zip(cols * 3, ((0, 0, crown), (-crown // 2, 2, crown - 2), (crown // 2, 2, crown - 2),
                                          (-1, -2, crown - 3), (2, -1, crown - 4))):
        blob(cv, x + dx, cy + dy, r, r * 0.8, c, rnd, 0.25)
    if fruit:
        for _ in range(crown):
            cv.px(x + rnd.randint(-crown, crown), cy + rnd.randint(-crown // 2, crown // 2 + 2), fruit)


def scene(fn):
    def wrap(hero, seed=5):
        rnd = random.Random(seed)
        cv = Canvas(WW, HH)
        fn(cv, rnd)
        hp = paste(cv, hero, 32, 35)
        post = getattr(fn, 'post', None)
        if post: post(cv, rnd, hp)
        return cv
    wrap.__name__ = fn.__name__
    return wrap


SCENES = []


def register(title):
    def deco(fn):
        w = scene(fn); w.title = title; SCENES.append(w); return fn
    return deco


# ---------------- сад ----------------
@register('Сад')
def garden(cv, rnd):
    grad(cv, ['#8FC0E8', '#A8D0EC', '#C8E2F0'], 0, 50)
    disc(cv, 80, 10, 5, '#F8E08A', '#F2CC8F')
    cloud(cv, 10, 8, 16); cloud(cv, 52, 14, 12)
    grad(cv, ['#5FA37E', '#4E8E6A'], 46, 60)
    for x in range(0, WW, 3): blob(cv, x, 47, 2.5, 2, '#6FB58C')
    leafy_tree(cv, rnd, 14, 60, 14, 10, ['#4E8E6A', '#5FA37E', '#3F7A5A'], fruit='#E0473F')
    leafy_tree(cv, rnd, 82, 60, 16, 11, ['#4E8E6A', '#5FA37E', '#3F7A5A'], fruit='#F2CC8F')
    leafy_tree(cv, rnd, 48, 52, 8, 9, ['#5FA37E', '#6FB58C', '#4E8E6A'], fruit='#E8607A')
    for x in range(0, WW, 4):
        for y in range(58, 66): cv.px(x, y, '#E8E6DA')
        cv.px(x, 57, '#F4F1DE')
    for y in (60, 63):
        for x in range(WW): cv.px(x, y, '#E8E6DA')
    ground(cv, 66, ['#6FB58C', '#5FA37E', '#4E8E6A'], rnd)
    for x in range(36, 60):
        for y in range(76, HH): cv.px(x + (y - 76) // 2 - 3, y, '#D9C7A3')
    for _ in range(90):
        x, y = rnd.randrange(WW), rnd.randrange(68, HH)
        cv.px(x, y, rnd.choice(['#E8607A', '#F2CC8F', '#F4F1DE', '#B794E0', '#E07A5F']))


# ---------------- море ----------------
@register('Море')
def sea(cv, rnd):
    grad(cv, ['#6FA8DC', '#8FC0E8', '#C8E2F0'], 0, 44)
    disc(cv, 22, 12, 6, '#FFF0B0', '#F8E08A')
    cloud(cv, 50, 8, 14); cloud(cv, 76, 18, 10)
    for x, y in ((60, 22), (66, 20)): cv.px(x - 1, y, K); cv.px(x, y + 1, K); cv.px(x + 1, y, K)
    grad(cv, ['#2E6E9E', '#3D82B0', '#4F96C0'], 45, 70)
    for y in range(46, 70, 3):
        for x in range((y * 7) % 6, WW, 6): cv.px(x, y, '#8FC0E8'); cv.px(x + 1, y, '#8FC0E8')
    for x in range(70, 80):   # парусник
        cv.px(x, 44, '#6B4A30')
    for y in range(30, 44):
        for x in range(74 - (y - 30) // 3, 75): cv.px(x, y, '#F4F1DE')
        for x in range(76, 76 + (y - 30) // 4): cv.px(x, y, '#E07A5F')
    for x in range(WW):
        top = 70 + int(1.5 * math.sin(x * 0.3))
        for y in range(top, top + 2): cv.px(x, y, '#F4F1DE')
    ground(cv, 72, ['#F2DCA8', '#E8CC90', '#D9B878'], rnd, ['#C9A86A', '#F8ECC8'])
    for x, y in ((12, 82), (84, 80)):   # ракушки
        cv.px(x, y, '#E8A0A8'); cv.px(x + 1, y, '#E8A0A8'); cv.px(x, y - 1, '#F4C6D4')
    for x, y, c in ((76, 84, '#E07A5F'), (18, 76, '#F2CC8F')):
        disc(cv, x, y, 2, c)


# ---------------- листопад ----------------
@register('Листопад')
def autumn(cv, rnd):
    grad(cv, ['#E8B880', '#F2CC8F', '#F4DCAA'], 0, 54)
    disc(cv, 48, 30, 8, '#F8E0A0')
    for x, top, crown in ((8, 22, 11), (30, 30, 8), (66, 28, 9), (88, 20, 12)):
        leafy_tree(cv, rnd, x, 64, 64 - top, crown, ['#C4473F', '#E07A5F', '#E8943A', '#F2CC8F'])
    grad(cv, ['#A8784A', '#8A6038'], 60, 66)
    ground(cv, 66, ['#B8864A', '#A07040', '#8A6038'], rnd, ['#E8943A', '#C4473F', '#F2CC8F', '#E07A5F'])
    for x in range(70, 86):   # скамейка
        cv.px(x, 70, '#6B4430'); cv.px(x, 72, '#6B4430')
    for x in (71, 84):
        for y in range(70, 77): cv.px(x, y, '#3A281C')


def _leaves(cv, rnd, hp):
    for _ in range(40):
        x, y = rnd.randrange(WW), rnd.randrange(60)
        if (x, y) in hp: continue
        c = rnd.choice(['#E8943A', '#C4473F', '#F2CC8F'])
        cv.px(x, y, c); cv.px(x + 1, y + 1, c)
autumn.post = _leaves


# ---------------- космос ----------------
@register('Космос')
def space(cv, rnd):
    grad(cv, ['#0A0C1E', '#10132A', '#181C3C'], 0, 70)
    for _ in range(120):
        x, y = rnd.randrange(WW), rnd.randrange(70)
        cv.px(x, y, '#F4F1DE' if rnd.random() < 0.3 else '#6A70A0')
    for _ in range(260):   # туманность
        x = int(rnd.gauss(30, 14)); y = int(rnd.gauss(18, 8))
        if (x + y) % 2 == 0: cv.px(x, y, rnd.choice(['#3A2A6A', '#5A3A8A', '#2A3A7A']))
    disc(cv, 74, 18, 9, '#E8943A'); blob(cv, 74, 18, 9, 9, '#E8943A')
    for x in range(64, 85):
        for y in range(14, 23):
            if math.hypot(x - 74, y - 18) <= 9 and (y in (15, 19)): cv.px(x, y, '#C0702A')
    for x in range(60, 90):
        y = 20 + (x - 75) // 6
        if not (66 <= x <= 82 and y < 18): cv.px(x, y, '#F2CC8F')
    disc(cv, 16, 46, 4, '#5A9ADA'); cv.px(15, 45, '#5FA37E'); cv.px(17, 47, '#5FA37E'); cv.px(14, 44, '#9FD0F0')
    for xy in ((40, 10), (88, 40), (6, 26)): twinkle(cv, *xy)
    for x in range(WW):
        top = 74 + int(2 * math.sin(x * 0.12 + 1))
        for y in range(top, HH): cv.px(x, y, '#9AA0C0' if y > top + 1 else '#C9CBDD')
    for cx, cy, r in ((12, 82, 3), (80, 80, 4), (52, 85, 2), (28, 84, 2)):
        for x in range(cx - r, cx + r + 1):
            cv.px(x, cy, '#6A6F90'); cv.px(x, cy + 1, '#7A80A0')
        cv.px(cx - r, cy - 1, '#C9CBDD')


# ---------------- горы ----------------
@register('Горы')
def mountains_scene(cv, rnd):
    grad(cv, ['#7FB0E0', '#A8CCEC', '#D8EAF4'], 0, 50)
    cloud(cv, 64, 10, 14)
    mountains(cv, rnd, 56, [(18, 10, 22), (52, 4, 26), (84, 14, 20)], '#5A6A90', '#7A8AB0', '#F4F1DE')
    for x in range(0, WW, 4):   # ельник
        h = rnd.randint(8, 14)
        for k in range(h):
            for dx in range(-(k // 2), k // 2 + 1): cv.px(x + dx, 58 - h + k, '#2E5A46')
    grad(cv, ['#5A9ADA', '#4F8CC8'], 58, 66)
    for y in range(59, 66, 2):
        for x in range(y % 5, WW, 7): cv.px(x, y, '#9FD0F0')
    ground(cv, 66, ['#6FB58C', '#5FA37E', '#4E8E6A'], rnd, ['#F4F1DE', '#B794E0', '#F2CC8F'])


# ---------------- северное сияние ----------------
@register('Северное сияние')
def aurora(cv, rnd):
    grad(cv, ['#0C1028', '#121838', '#1A2448'], 0, 60)
    stars(cv, rnd, 60, 50)
    for k, (col, off) in enumerate((('#4FD0A0', 0), ('#81E0B8', 3), ('#B794E0', 7))):
        for x in range(WW):
            yc = 16 + off + 8 * math.sin(x * 0.07 + k) + 3 * math.sin(x * 0.21)
            for y in range(int(yc), int(yc) + 10 - k * 2):
                if (x + y) % (2 if y < yc + 4 else 3) == 0: cv.px(x, y, col)
    for x in range(0, WW, 5):
        h = rnd.randint(10, 18)
        for k in range(h):
            for dx in range(-(k // 2), k // 2 + 1): cv.px(x + dx, 66 - h + k, '#0E1A22')
        cv.px(x, 66 - h, '#C9CBDD')
    ground(cv, 66, ['#C9D4EC', '#A8B4D8', '#8E98C4'], rnd, ['#E8F0FA'])


# ---------------- ночной город ----------------
@register('Ночной город')
def city(cv, rnd):
    grad(cv, ['#141834', '#22264A', '#3A2E5A'], 0, 60)
    stars(cv, rnd, 25, 30)
    moon(cv, 82, 10, 5)
    x = 0
    while x < WW:
        w = rnd.randint(8, 14); h = rnd.randint(18, 44)
        top = 70 - h
        c = rnd.choice(['#1E2240', '#262A4E', '#2E3258'])
        for yy in range(top, 70):
            for xx in range(x, x + w): cv.px(xx, yy, c)
        for yy in range(top + 2, 68, 3):
            for xx in range(x + 1, x + w - 1, 3):
                if rnd.random() < 0.55: cv.px(xx, yy, rnd.choice(['#F2CC8F', '#F8E08A', '#E8A65A']))
        if rnd.random() < 0.3:
            for yy in range(top - 4, top): cv.px(x + w // 2, yy, '#4A4F6E')
            cv.px(x + w // 2, top - 5, '#E0473F')
        x += w + rnd.randint(0, 2)
    ground(cv, 70, ['#2A2D45', '#22253A', '#1A1C2E'], rnd)
    for x in range(0, WW, 8): cv.px(x, 79, '#F2CC8F'); cv.px(x + 1, 79, '#F2CC8F')
    for lx in (12, 84):
        for y in range(62, 78): cv.px(lx, y, '#4A4F6E')
        cv.rect(lx - 1, 60, lx + 1, 61, '#F8E08A')


# ---------------- пустыня ----------------
@register('Пустыня')
def desert(cv, rnd):
    grad(cv, ['#E8A060', '#F2C080', '#F8DCA8'], 0, 48)
    disc(cv, 70, 22, 8, '#FFF0C0', '#F8E08A')
    for k, (y0, amp, col, lt) in enumerate(((50, 4, '#D9A860', '#E8BC78'), (58, 5, '#E0B470', '#EEC888'))):
        for x in range(WW):
            top = int(y0 + amp * math.sin(x * 0.08 + k * 2))
            for y in range(top, HH): cv.px(x, y, col)
            cv.px(x, top, lt)
    for cx in (16, 22, 28):   # караван-силуэты
        cy = 49 + (cx % 3)
        for x in range(cx - 2, cx + 3): cv.px(x, cy, '#8A6038')
        cv.px(cx - 1, cy - 1, '#8A6038'); cv.px(cx + 2, cy - 2, '#8A6038'); cv.px(cx + 3, cy - 2, '#8A6038')
        cv.px(cx - 2, cy + 1, '#8A6038'); cv.px(cx + 2, cy + 1, '#8A6038')
    for px_ in (84,):   # оазис
        for y in range(40, 58): cv.px(px_ + (58 - y) // 6, y, '#8A6038')
        for dx in range(-6, 7):
            cv.px(px_ + 3 + dx, 40 + abs(dx) // 2, '#4E8E6A'); cv.px(px_ + 3 + dx, 41 + abs(dx) // 2, '#3F7A5A')
    ground(cv, 72, ['#E8C080', '#E0B470', '#D4A460'], rnd, ['#C99A5A', '#F2D49A'])


# ---------------- сакура ----------------
@register('Сакура')
def sakura(cv, rnd):
    grad(cv, ['#F4D8E0', '#F8E8EC', '#FAF0EE'], 0, 56)
    disc(cv, 20, 14, 6, '#E07A7A')
    for x in range(40, 58):   # тории
        cv.px(x, 30, '#C4473F'); cv.px(x, 31, '#C4473F')
    for x in range(41, 57): cv.px(x, 34, '#C4473F')
    cv.px(39, 29, '#C4473F'); cv.px(58, 29, '#C4473F')
    for y in range(31, 56): cv.px(43, y, '#C4473F'); cv.px(54, y, '#C4473F')
    for x, top, crown in ((10, 30, 12), (84, 26, 13)):
        for y in range(top, 64): cv.px(x, y, '#5A3A3A'); cv.px(x + 1, y, '#5A3A3A')
        for c, (dx, dy, r) in zip(['#F4B8CC', '#E8A0B8', '#F8D0DC'] * 2,
                                   ((0, 0, crown), (-6, 4, crown - 3), (6, 3, crown - 3), (0, -4, crown - 4))):
            blob(cv, x + dx, top + dy, r, r * 0.75, c, rnd, 0.3)
    grad(cv, ['#8FC09A', '#7AB088'], 56, 66)
    ground(cv, 66, ['#9FD0A8', '#8FC09A', '#7AB088'], rnd, ['#F4B8CC'])


def _petals(cv, rnd, hp):
    for _ in range(45):
        x, y = rnd.randrange(WW), rnd.randrange(70)
        if (x, y) not in hp: cv.px(x, y, rnd.choice(['#F4B8CC', '#E8A0B8']))
sakura.post = _petals


# ---------------- джунгли ----------------
@register('Джунгли')
def jungle(cv, rnd):
    grad(cv, ['#3F7A5A', '#4E8E6A', '#2E5A46'], 0, 76)
    for _ in range(14):
        blob(cv, rnd.randrange(WW), rnd.randrange(10, 60), rnd.randint(6, 12), rnd.randint(4, 8),
             rnd.choice(['#2E6650', '#3A7A5E', '#245040']), rnd, 0.3)
    for k in range(10):
        x = rnd.randrange(WW)
        for y in range(0, rnd.randint(20, 50)):
            cv.px(x + int(2 * math.sin(y * 0.3)), y, '#5A8A3A')
            if y % 6 == 0: cv.px(x + 1 + int(2 * math.sin(y * 0.3)), y, '#81B29A')
    for cx, cy in ((10, 60), (86, 58), (24, 68), (74, 68)):   # большие листья
        for i in range(10):
            for j in range(-3 + abs(i - 5) // 2, 4 - abs(i - 5) // 2):
                cv.px(cx + j, cy - i, '#5FA37E' if j < 0 else '#4E8E6A')
    for x, y, c in ((20, 20, '#E0473F'), (78, 14, '#5A9ADA')):   # попугаи
        cv.rect(x, y, x + 2, y + 3, c); cv.px(x + 3, y + 1, '#F2CC8F'); cv.px(x + 1, y + 4, '#F2CC8F'); cv.px(x + 1, y + 1, K)
    ground(cv, 76, ['#4A3A26', '#3A2E1E'], rnd, ['#5FA37E'])
    for _ in range(25):
        cv.px(rnd.randrange(WW), rnd.randrange(30, 70), rnd.choice(['#E8607A', '#F2CC8F']))


# ---------------- подводный мир ----------------
@register('Подводный мир')
def underwater(cv, rnd):
    grad(cv, ['#5AB0D8', '#3D8FC0', '#2E6E9E', '#1E4E7A'], 0, 76)
    for x in range(0, WW, 7):
        for y in range(0, 30):
            if (y + x) % 9 < 2 and y < 20 + (x % 11): cv.px(x + y // 4, y, '#8FD0F0')
    for k in range(8):
        x = rnd.randrange(WW); h = rnd.randint(14, 30)
        for y in range(76 - h, 77): cv.px(x + int(1.5 * math.sin(y * 0.4 + k)), y, '#4FA88A')
    for cx, col in ((12, '#E8607A'), (84, '#E8943A'), (22, '#B794E0'), (76, '#E07A5F')):
        for i in range(9):
            cv.px(cx, 76 - i, col); cv.px(cx - i // 3, 76 - i - 1, col); cv.px(cx + i // 3, 76 - i - 2, col)
    for x, y, c in ((16, 30, '#F2CC8F'), (80, 24, '#E8783A'), (60, 16, '#8FD0F0'), (28, 46, '#E8607A')):
        cv.rect(x, y, x + 3, y + 1, c); cv.px(x + 4, y - 1, c); cv.px(x + 4, y + 2, c); cv.px(x + 4, y, c); cv.px(x + 4, y + 1, c)
        cv.px(x, y, K)
    ground(cv, 76, ['#E8D4A0', '#D9C08A', '#C9AC78'], rnd, ['#F4E8C8', '#B89A60'])
    disc(cv, 70, 82, 2, '#E8A0A8'); cv.px(69, 81, '#F4C6D4')


def _bubbles(cv, rnd, hp):
    for _ in range(20):
        x, y = rnd.randrange(WW), rnd.randrange(70)
        if (x, y) in hp: continue
        cv.px(x, y, '#C8EEFA'); cv.px(x + 1, y - 1, '#8FD0F0')
underwater.post = _bubbles


# ---------------- подсолнухи ----------------
@register('Подсолнухи')
def sunflowers(cv, rnd):
    grad(cv, ['#5A9ADA', '#8FC0E8', '#C8E2F0'], 0, 50)
    cloud(cv, 12, 12, 16); cloud(cv, 64, 8, 18)
    grad(cv, ['#6FA858', '#5A9048', '#4E803E'], 48, 78)
    for row, (y, r, n) in enumerate(((52, 1, 30), (60, 2, 16), (70, 3, 9))):
        for i in range(n):
            x = int((i + 0.5 + (row % 2) * 0.5) * WW / n)
            for yy in range(y, y + 6 + row * 4): cv.px(x, yy, '#4E8E3A')
            disc(cv, x, y, r + 1, '#F2C83A'); disc(cv, x, y, max(1, r - 1), '#6B4430')
            if r >= 2: cv.px(x - r - 1, y + 3, '#5FA37E'); cv.px(x + r + 1, y + 4, '#5FA37E')
    ground(cv, 78, ['#5A9048', '#4E803E'], rnd)


# ---------------- замок ----------------
@register('Сказочный замок')
def castle(cv, rnd):
    grad(cv, ['#6A4A8A', '#C06A7A', '#F2A070', '#F8D09A'], 0, 56)
    disc(cv, 18, 40, 7, '#FFE0A0')
    for x0, top, w in ((38, 18, 6), (52, 12, 6), (64, 20, 6), (44, 28, 22)):
        for y in range(top, 58):
            for x in range(x0, x0 + w): cv.px(x, y, '#B8B0C8' if x < x0 + w - 2 else '#9890B0')
        if w <= 6:
            for k in range(5):
                for x in range(x0 + k // 2 - 1, x0 + w - k // 2 + 1): cv.px(x, top - 5 + k, '#5A3A8A')
            cv.px(x0 + w // 2, top - 7, '#5A3A8A'); cv.px(x0 + w // 2 + 1, top - 7, '#E0473F'); cv.px(x0 + w // 2 + 2, top - 7, '#E0473F')
            cv.px(x0 + 2, top + 4, '#F2CC8F'); cv.px(x0 + 2, top + 5, '#F2CC8F')
        else:
            for x in range(x0, x0 + w, 2): cv.px(x, top - 1, '#B8B0C8')
    for y in range(48, 58):
        for x in range(53, 58): cv.px(x, y, '#3A2A3A')
    for x in range(WW):
        top = 56 + int(4 * math.sin(x * 0.06 + 0.5) + 2 * math.cos(x * 0.15))
        for y in range(top, HH): cv.px(x, y, '#5FA37E' if y < top + 3 else '#4E8E6A')
    ground(cv, 74, ['#5FA37E', '#4E8E6A', '#3F7A5A'], rnd, ['#F2CC8F', '#E8A0B8', '#F4F1DE'])
    for x in range(44, 64):
        for y in range(58, 74):
            if abs(x - 55 - (y - 58) * 0.4) < 1 + (y - 58) * 0.15: cv.px(x, y, '#D9C7A3')


# ---------------- костёр в лесу ----------------
@register('Костёр в лесу')
def campfire(cv, rnd):
    grad(cv, ['#0C0E22', '#141834', '#1E2448'], 0, 66)
    stars(cv, rnd, 50, 30)
    moon(cv, 14, 10, 4)
    for x in range(0, WW, 6):
        h = rnd.randint(18, 34)
        for k in range(h):
            for dx in range(-(k // 3), k // 3 + 1): cv.px(x + dx, 70 - h + k, '#0E1A1A')
    ground(cv, 70, ['#2A2420', '#221C18'], rnd)
    for k in range(10):   # палатка
        for x in range(78 - k, 79 + k): cv.px(x, 64 + k, '#E07A5F' if x < 78 else '#B8604A')
    for y in range(68, 74): cv.px(78, y, '#3A2420')
    cx, cy = 16, 80
    for r, c in ((10, '#3A2A28'), (7, '#4A342A')):
        for x in range(cx - r, cx + r + 1):
            for y in range(cy - r // 3, cy + r // 3 + 1):
                if ((x - cx) / r) ** 2 + ((y - cy) / (r / 3)) ** 2 <= 1: cv.px(x, y, c)
    for i in range(-3, 4): cv.px(cx + i, cy + 1, '#6B4430'); cv.px(cx + i, cy, '#8A5A3B') if abs(i) < 3 else None
    for y in range(cy - 7, cy):
        w = (cy - y) // 2
        for x in range(cx - 3 + w // 2, cx + 4 - w // 2):
            cv.px(x, y, '#F8E08A' if abs(x - cx) < 1 else ('#E8943A' if abs(x - cx) < 2 else '#E0473F'))


# снежная ночь из первой волны — тоже в списке
from bg import scene_b as _snow
_snow.title = 'Снежная ночь'
SCENES.insert(0, _snow)
