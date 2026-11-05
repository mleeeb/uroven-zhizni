"""Домашние животные (маски 16x16): хорёк, собака, барашек, мини-свинка."""
FERRET = [
    "................",
    "................",
    "................",
    "..O..O..........",
    "..OOOO..........",
    ".OMMMMO.........",
    ".OEWWEO.........",
    ".OWWNWO.........",
    "..OWWOOOOOOO....",
    "..OOOOOOOOOOO...",
    "..OOWWOOOOOOOO..",
    "..OOWWOOOOOOOO..",
    "...OOOOOOOOOOOD.",
    "...DD.DD.DD.DD.D",
    "................",
    "................",
]
FERRET_PAL = {'O': '#D9C7A3', 'M': '#6B4A30', 'W': '#F4F1DE', 'E': '#0C0E22', 'N': '#E8A0A8', 'D': '#6B4A30'}

DOG = [
    "................",
    "..DD......DD....",
    ".DDDOOOOOODDD...",
    ".DDOOOOOOOODD...",
    ".DDOEOOOOEODD...",
    "..DOOOOOOOOD....",
    "...OOWWWWOO.....",
    "...OWWNNWWO.....",
    "....OWWWWO......",
    "...OORRRROO..O..",
    "..OOOOGOOOOO.O..",
    "..OOOOOOOOOOOO..",
    "..OOOOOOOOOOO...",
    "..OOOOOOOOOOO...",
    "..WW.WW...WW.WW.",
    "................",
]
DOG_PAL = {'O': '#B8864A', 'D': '#8A5A30', 'W': '#F4E8C8', 'E': '#0C0E22', 'N': '#1E1A22', 'R': '#C4473F', 'G': '#F2CC8F'}

LAMB = [
    "................",
    "....WWWWWW......",
    "...WWwWWwWW.....",
    "..LWDDDDDDWL....",
    "..LWDEDDEDWL....",
    "...WDDDDDDW.....",
    "...WWDNNDWW.....",
    "..WWWWDDWWWWW...",
    ".WWwWWWWWWwWWW..",
    ".WWWWWwWWWWWWW..",
    ".WWwWWWWWWWwWW..",
    ".WWWWWWWwWWWWW..",
    "..WWwWWWWWWwW...",
    "..DD.DD...DD.DD.",
    "..DD.DD...DD.DD.",
    "................",
]
LAMB_PAL = {'W': '#F4F1DE', 'w': '#D9D6C4', 'D': '#3A3646', 'E': '#F4F1DE', 'N': '#E8A0A8', 'L': '#3A3646'}

PIG = [
    "................",
    "................",
    "................",
    "...P......P.....",
    "...PP....PP.....",
    "..PPPPPPPPPP....",
    "..PPEPPPPEPP....",
    "..PPPSSSSPPP....",
    "..PPPSNNSPPP....",
    ".PPPPPSSPPPPP...",
    ".PPPPPPPPPPPPP.Q",
    ".PpPPPPPPPPPpPQ.",
    ".PPPPPPPPPPPPP..",
    "..PPPPPPPPPPP...",
    "..pp.pp...pp.pp.",
    "................",
]
PIG_PAL = {'P': '#F2B8C0', 'p': '#D8909A', 'S': '#E8A0A8', 'N': '#B86070', 'E': '#0C0E22', 'Q': '#D8909A'}

PETS3 = [('Хорёк', FERRET, FERRET_PAL), ('Собака', DOG, DOG_PAL), ('Барашек', LAMB, LAMB_PAL), ('Мини-свинка', PIG, PIG_PAL)]
