"""Питомцы, волна 2 (маски 16x16, рисуются pets.pet_canvas)."""
CORGI = [
    "................",
    "..O.......O.....",
    "..OO.....OO.....",
    "..OOOOOOOOO.....",
    ".OOOWWWWWOOO....",
    ".OOEWWWWWEOO....",
    ".OOWWWNWWWOO....",
    "..OWWWWWWWO.....",
    "...OOWWWOO......",
    "..OOOWWWOOOO..O.",
    ".OOOOWWWOOOOOOO.",
    ".OOOOWWWOOOOOO..",
    ".OOOOOOOOOOOO...",
    ".OOOOOOOOOOOO...",
    ".WW.WW....WW.WW.",
    "................",
]
CORGI_PAL = {'O': '#E8943A', 'W': '#F4F1DE', 'E': '#0C0E22', 'N': '#3A281C'}

OWL = [
    "................",
    "...O.......O....",
    "...OO.....OO....",
    "...OOOOOOOOO....",
    "..OWWWOOOWWWO...",
    "..OWEWOOOWEWO...",
    "..OWWWOYOWWWO...",
    "..OOOOOYOOOOO...",
    "..OoBBBBBBBoO...",
    "..OoBbBBbBBoO...",
    "..OoBBBBBBBoO...",
    "..OoBbBBBbBoO...",
    "...OBBBBBBBO....",
    "....OOOOOOO.....",
    "....YY...YY.....",
    "GGGGGGGGGGGGGGGG",
]
OWL_PAL = {'O': '#8A6A48', 'o': '#6B4A30', 'W': '#F4F1DE', 'E': '#0C0E22', 'Y': '#E8A03A', 'B': '#D9C7A3', 'b': '#B09A74',
           'G': '#5A3E2B'}

HAMSTER = [
    "................",
    "................",
    "................",
    "................",
    "....P.....P.....",
    "...PPO...OPP....",
    "..OOOOOOOOOOO...",
    "..OOEOOOOOEOO...",
    ".OOOOOONOOOOOO..",
    ".OWWOOOOOOOWWO..",
    ".OWWWWWWWWWWWO..",
    ".OOWWWWWWWWWOO..",
    "..OOWWWWWWWOO...",
    "...OOOOOOOOO....",
    "...PP.....PP....",
    "................",
]
HAMSTER_PAL = {'O': '#E8B46A', 'W': '#F8ECD8', 'E': '#0C0E22', 'N': '#E8A0A8', 'P': '#E8A0A8'}

FOX = [
    "................",
    ".O.........O....",
    ".OO.......OO....",
    ".OKO.....OKO....",
    ".OOOOOOOOOOO....",
    "OOOEOOOOOEOOO...",
    "OWWWOOOOOWWWO...",
    ".WWWWWNWWWWW....",
    "..WWWWWWWWW.....",
    "...OOWWWOO......",
    "..OOOWWWOOO..OO.",
    "..OOOWWWOOO.OOOO",
    "..OOOOOOOOO.OOWW",
    "..OOOOOOOOOOOWW.",
    "..KK.KK.KK.KK...",
    "................",
]
FOX_PAL = {'O': '#D9643A', 'W': '#F4F1DE', 'E': '#0C0E22', 'N': '#1E1A22', 'K': '#3A2420'}

PETS2 = [('Корги', CORGI, CORGI_PAL), ('Сова', OWL, OWL_PAL), ('Хомяк', HAMSTER, HAMSTER_PAL), ('Лисёнок', FOX, FOX_PAL)]
