"""Просмотр каталога: python3 cat_preview.py head [scale]"""
import sys
from PIL import Image, ImageDraw, ImageFont
from outfit import CATALOG, compose
import w_head, w_small, w_top, w_low, w_folk, w_fest, w_extra, w_folk2  # noqa

LOOK_M = dict(skin=0, hair=1, shirt=0)
LOOK_F = dict(skin=1, hair=4, shirt=2)
F = ImageFont.truetype('/home/claude/src/app/src/main/assets/www/fonts/IBMPlexMono-Medium.ttf', 14)


def render(slot, scale=4, cols=6, ids=None):
    its = [v for v in CATALOG.values() if v['slot'] == slot] if not ids else [CATALOG[i] for i in ids]
    cw, ch = 32 * scale * 2 + 8, 44 * scale + 22
    rows = (len(its) + cols - 1) // cols
    out = Image.new('RGBA', (cols * (cw + 12) + 12, rows * (ch + 12) + 12), '#1B1E3A')
    d = ImageDraw.Draw(out)
    for i, it in enumerate(its):
        x, y = 12 + (i % cols) * (cw + 12), 12 + (i // cols) * (ch + 12)
        d.rectangle([x, y, x + cw, y + ch], fill='#151833')
        for j, (sex, look) in enumerate((('m', LOOK_M), ('f', LOOK_F))):
            if it['only'] and it['only'] != sex: continue
            cv = compose(sex, **look, **{it['slot']: it['id']})
            im = cv.image(scale)
            out.paste(im, (x + j * (32 * scale + 8), y), im)
        d.text((x + 4, y + ch - 18), it['name'], font=F, fill='#F4F1DE')
    return out


if __name__ == '__main__':
    slot = sys.argv[1]
    sc = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    render(slot, sc).save(f'cat_{slot}.png')
