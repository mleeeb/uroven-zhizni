"""Фон «Снежная ночь с ёлкой»: вариант А (квадрат за героем) и Б (вся карточка)."""
import math
import random
from px32 import Canvas, base, K

SKY = ['#10132A', '#141834', '#191D3D', '#1F2448', '#262C54']
STAR, STAR_D = '#F4F1DE', '#8A8BA8'
MOON, MOON_D = '#F2CC8F', '#D9B176'
SNOW, SNOW_M, SNOW_D = '#EDEBDD', '#C9CBDD', '#9FA3C4'
FAR, FAR_TIP = '#12152E', '#6A70A0'
NEAR, NEAR_TIP = '#202650', '#6A70A0'
TREE = ['#1F4A3B', '#2A6150', '#3A7D64']
TREE_EDGE = '#0F2A22'
LIGHTS = ['#F2CC8F', '#E07A5F', '#8FB3E0', '#B794E0']


def sky(cv, horizon):
    n = len(SKY)
    for y in range(cv.h):
        t = min(1, y / max(1, horizon)) * (n - 1)
        i = int(t); f = t - i
        for x in range(cv.w):
            c = SKY[min(i, n - 1)]
            # упорядоченный дизеринг между полосами
            if i + 1 < n and f > 0.5 and (x + y) % 2 == 0: c = SKY[i + 1]
            if i + 1 < n and f > 0.8: c = SKY[i + 1]
            cv.px(x, y, c)


def stars(cv, rnd, n, ymax, avoid=()):
    for _ in range(n):
        x, y = rnd.randrange(cv.w), rnd.randrange(ymax)
        if any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in avoid): continue
        cv.px(x, y, STAR if rnd.random() < 0.45 else STAR_D)


def twinkle(cv, x, y):
    cv.px(x, y, STAR)
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)): cv.px(x + dx, y + dy, STAR_D)


def moon(cv, cx, cy, r=4):
    for y in range(cy - r - 2, cy + r + 3):
        for x in range(cx - r - 2, cx + r + 3):
            d = math.hypot(x - cx, y - cy)
            if r + 0.5 < d <= r + 1.8 and (x + y) % 2 == 0: cv.px(x, y, '#2F355F')
    for y in range(cy - r, cy + r + 1):
        for x in range(cx - r, cx + r + 1):
            if math.hypot(x - cx, y - cy) <= r + 0.3:
                cut = math.hypot(x - (cx + 2), y - (cy - 1)) <= r - 0.6
                if not cut: cv.px(x, y, MOON if x < cx - 1 or y > cy + 1 else MOON_D)


def firs(cv, rnd, y_base, color, tip, hmin, hmax, step, fill_to=None):
    """Полоса ёлок-силуэтов с заснеженными макушками."""
    x = -2
    while x < cv.w + 2:
        h = rnd.randint(hmin, hmax)
        for k in range(h):
            half = (k + 1) // 2
            for dx in range(-half, half + 1):
                cv.px(x + dx, y_base - h + k, color)
        cv.px(x, y_base - h, tip)
        if h > 8:
            cv.px(x - 1, y_base - h + 4, tip); cv.px(x - 2, y_base - h + 7, tip)
        x += step + rnd.randint(-1, 1)
    for yy in range(y_base, fill_to or y_base + 1):
        for xx in range(cv.w): cv.px(xx, yy, color)


def field(cv, y0, rnd):
    """Ночное снежное поле: темнее вдали, светлее у ног."""
    cols = ['#343A68', '#424978', '#525A88', '#646C98']
    n = cv.h - y0
    for y in range(y0, cv.h):
        t = (y - y0) / max(1, n) * (len(cols) - 1)
        i = int(t); f = t - i
        for x in range(cv.w):
            c = cols[i]
            if i + 1 < len(cols) and f > 0.5 and (x + y) % 2 == 0: c = cols[i + 1]
            cv.px(x, y, c)
    for _ in range(cv.w):
        x, y = rnd.randrange(cv.w), rnd.randrange(y0 + 1, cv.h)
        cv.px(x, y, '#A9AECE')


def hills(cv, rnd, y0, color, light, amp, freq, phase):
    for x in range(cv.w):
        top = int(y0 + amp * math.sin(x * freq + phase))
        for y in range(top, cv.h): cv.px(x, y, color)
        cv.px(x, top, light)


def ground(cv, y0, rnd):
    for x in range(cv.w):
        top = y0 + (1 if math.sin(x * 0.45) > 0.55 else 0) - (1 if math.sin(x * 0.21 + 1) > 0.8 else 0)
        for y in range(top, cv.h):
            cv.px(x, y, SNOW if y < top + 2 else SNOW_M)
        cv.px(x, top, '#FFFFFF' if x % 7 == 3 else SNOW)
    for _ in range(cv.w // 3):
        x, y = rnd.randrange(cv.w), rnd.randrange(y0 + 3, cv.h)
        cv.px(x, y, SNOW_D); cv.px(x + 1, y, SNOW_D)


def tree(cv, cx, top, bottom, half_max, rnd):
    """Нарядная ёлка: ярусы, снег на лапах, гирлянда, шары, звезда."""
    pts = {}
    tiers = 4
    h = bottom - top
    for t in range(tiers):
        y0 = top + 3 + int(h * t / tiers * 0.92)
        y1 = top + 3 + int(h * (t + 1) / tiers)
        w0 = 1 + int(half_max * t / tiers * 0.55)
        w1 = int(half_max * (t + 1) / tiers)
        for y in range(y0, y1 + 1):
            f = (y - y0) / max(1, y1 - y0)
            half = int(w0 + (w1 - w0) * f)
            for dx in range(-half, half + 1):
                shade = 1 if dx < -half // 3 else (0 if dx > half // 3 else 1)
                if dx < -half * 0.55: shade = 2
                pts[(cx + dx, y)] = TREE[shade]
        # снег на кончиках яруса
        yb = y1
        for dx in range(-w1, w1 + 1):
            if abs(dx) > w1 - 3 or (dx + t) % 4 == 0: pts[(cx + dx, yb)] = SNOW if dx < 0 else SNOW_M
    # ствол
    for y in range(bottom, bottom + 3):
        for dx in (-1, 0, 1): pts[(cx + dx, y)] = '#5A3E2B'
    # контур
    edge = set()
    for (x, y) in pts:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            n = (x + dx, y + dy)
            if n not in pts: edge.add(n)
    for (x, y) in edge: cv.px(x, y, TREE_EDGE)
    for (x, y), c in pts.items(): cv.px(x, y, c)
    # гирлянда: диагонали из огоньков
    for t in range(tiers):
        y0 = top + 3 + int(h * t / tiers * 0.92) + 2
        y1 = top + 3 + int(h * (t + 1) / tiers) - 1
        for i, y in enumerate(range(y0, y1, 2)):
            f = (y - top) / h
            half = int(half_max * f * 0.85)
            x = cx - half + int((y - y0) / max(1, (y1 - y0)) * half * 2)
            if (x, y) in pts: cv.px(x, y, LIGHTS[(i + t) % 4])
    # шары
    for _ in range(int(h * 0.5)):
        y = rnd.randint(top + 6, bottom - 1)
        f = (y - top) / h
        half = int(half_max * f * 0.8)
        if half < 2: continue
        x = cx + rnd.randint(-half, half)
        if (x, y) in pts and pts[(x, y)] in TREE: cv.px(x, y, rnd.choice(LIGHTS))
    # звезда
    sy = top + 1
    for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)): cv.px(cx + dx, sy + dy, '#F2CC8F')
    cv.px(cx, sy, '#FFF6D8')
    for dx, dy in ((2, 0), (-2, 0), (0, -2)): cv.px(cx + dx, sy + dy, '#C9A15F')


def house(cv, x0, y_base):
    """Домик с горящим окном."""
    w, hh = 12, 7
    for y in range(y_base - hh, y_base):
        for x in range(x0 + 1, x0 + w - 1): cv.px(x, y, '#4A3426' if (y % 2) else '#56402F')
    for k in range(6):   # крыша
        for x in range(x0 - 1 + k, x0 + w + 1 - k):
            cv.px(x, y_base - hh - 1 - k, SNOW if k < 2 or x in (x0 - 1 + k, x0 + w - k) else SNOW_M)
    for y in range(y_base - 5, y_base - 2):
        for x in range(x0 + 4, x0 + 8): cv.px(x, y, '#F2CC8F')
    cv.px(x0 + 5, y_base - 4, '#E8A65A'); cv.px(x0 + 6, y_base - 4, '#E8A65A')
    for x in range(x0 + 4, x0 + 8): cv.px(x, y_base - 6, '#3A2A1F')
    cv.px(x0 + 9, y_base - hh - 4, '#4A3426'); cv.px(x0 + 9, y_base - hh - 5, '#4A3426')   # труба
    for i, (dx, dy) in enumerate(((10, 7), (11, 9), (10, 11))):
        cv.px(x0 + dx, y_base - hh - dy + 2, '#5A6090')


def snowfall(cv, rnd, n, ymax, protect):
    for _ in range(n):
        x, y = rnd.randrange(cv.w), rnd.randrange(ymax)
        if (x, y) in protect: continue
        cv.px(x, y, '#E8E6DA' if rnd.random() < 0.6 else '#A9ABC6')


def paste(cv, hero, ox, oy):
    pts = set()
    for y in range(hero.h):
        for x in range(hero.w):
            c = hero.g[y][x]
            if c != '.': cv.px(ox + x, oy + y, c); pts.add((ox + x, oy + y))
    return pts


def scene_a(hero, seed=7):
    rnd = random.Random(seed)
    cv = Canvas(52, 52)
    sky(cv, 34)
    stars(cv, rnd, 26, 28)
    twinkle(cv, 6, 6); twinkle(cv, 45, 22)
    moon(cv, 44, 8, 4)
    firs(cv, rnd, 36, FAR, FAR_TIP, 5, 10, 4)
    field(cv, 36, rnd)
    tree(cv, 26, 0, 43, 25, rnd)
    ground(cv, 44, rnd)
    hp = paste(cv, hero, 10, 2)
    snowfall(cv, rnd, 30, 42, hp)
    return cv


def scene_b(hero, seed=11):
    rnd = random.Random(seed)
    cv = Canvas(96, 88)
    sky(cv, 28)
    stars(cv, rnd, 55, 28)
    for xy in ((8, 8), (28, 18), (66, 4), (60, 22), (40, 6)): twinkle(cv, *xy)
    moon(cv, 84, 9, 5)
    firs(cv, rnd, 31, FAR, FAR_TIP, 5, 12, 5)
    field(cv, 31, rnd)
    house(cv, 4, 32)
    house(cv, 78, 33)
    tree(cv, 48, 24, 78, 26, rnd)
    ground(cv, 78, rnd)
    hp = paste(cv, hero, 32, 35)
    snowfall(cv, rnd, 60, 76, hp)
    return cv
