"""Питомцы 16x16 (рисуются масками) и сцена «герой + питомец»."""
from px32 import Canvas, base, K

CAT = [
    "................",
    "..O.......O.....",
    "..OO.....OO.....",
    "..OPO...OPO.....",
    "..OOOoOoOOO.....",
    ".OOOOOOOOOOO....",
    ".OOGEOOOGEOO....",
    ".OoOOOPOOOoO....",
    ".OOOWWWWWOOO....",
    "..OOOWWWOOO.....",
    "..OOOWWWOOO..o..",
    ".OOOOWWWOOOO..O.",
    ".OoOOWWWOOoO..O.",
    ".OOoOOWOOoOO.OO.",
    ".OOWWOOOWWOOOO..",
    "..WW.....WW.....",
]
CAT_PAL = {'O': '#E39B52', 'o': '#B8733A', 'W': '#F4F1DE', 'P': '#E8A0A8', 'G': '#9FD3A8', 'E': '#0C0E22'}

DRAGON = [
    "....H....H......",
    "....HH..HH......",
    "...GGGGGGGG.....",
    "..GGGGgGGGGG....",
    "..GGEGGGGEGG....",
    "..GGEGGGGEGG....",
    "W.GGGGGGGGGG.W..",
    "WW.GgGGGGgG.WW..",
    "WWW.GGGGGG.WWW..",
    "WWwGGBBBBGGwWW..",
    ".WwGGbbbbGGwW...",
    "..WGGBBBBGGW....",
    "...GGbbbbGG..gg.",
    "...GgBBBBgGGGg..",
    "..GGGGGGGGGG....",
    "..HH.H..H.HH....",
]
DRAGON_PAL = {'G': '#5FA37E', 'g': '#417A5C', 'B': '#F2CC8F', 'b': '#C9A15F', 'H': '#F4F1DE',
              'E': '#0C0E22', 'W': '#8FB3E0', 'w': '#6F93C0'}


def pet_canvas(mask, pal):
    cv = Canvas(18, 17)
    for y, row in enumerate(mask):
        for x, ch in enumerate(row):
            if ch != '.': cv.px(x + 1, y, pal[ch])
    cv.outline()
    return cv


def with_pet(hero: Canvas, pet: Canvas, gap=0):
    """Герой слева, питомец справа у ног."""
    sc = Canvas(hero.w + pet.w + gap, hero.h)
    for y in range(hero.h):
        for x in range(hero.w): sc.g[y][x] = hero.g[y][x]
    oy = hero.h - pet.h
    for y in range(pet.h):
        for x in range(pet.w):
            c = pet.g[y][x]
            if c != '.': sc.px(hero.w + gap + x - 2, oy + y, c)
    return sc
