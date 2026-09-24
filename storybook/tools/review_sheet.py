"""审图联系表：一本书 32 页分两张，每张 16 页配旁白。usage: review_sheet.py <slug>..."""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
SP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'out', '_review'); os.makedirs(SP, exist_ok=True)
f = ImageFont.truetype('msyh.ttc', 17); T = 380; TX = 120
for slug in sys.argv[1:]:
    st = json.load(open(f'story_{slug}.json', encoding='utf-8'))
    for half in (0, 1):
        ns = range(1 + 16 * half, 17 + 16 * half)
        c = Image.new('RGB', (T * 4, (T + TX) * 4), 'white'); d = ImageDraw.Draw(c)
        for i, n in enumerate(ns):
            x, y = (i % 4) * T, (i // 4) * (T + TX)
            fn = f'out/bakeoff/{slug}_p{n:02d}_lightning8.png'
            fn = fn if os.path.exists(fn) else fn.replace('bakeoff/', 'bakeoff/_old/')
            im = Image.open(fn).convert('RGB').resize((T, T)) if os.path.exists(fn) else Image.new('RGB', (T, T), 'grey'); c.paste(im, (x, y))
            if '_old' in fn: d.rectangle((x, y, x + T - 1, y + T - 1), outline='red', width=6)
            d.multiline_text((x + 8, y + T + 4), f"{n} " + st['pages'][n - 1]['zh'].replace('\n', ''), fill='black', font=f, spacing=2) if len(st['pages'][n-1]['zh']) < 22 else \
            d.multiline_text((x + 8, y + T + 4), f"{n} " + st['pages'][n - 1]['zh'], fill='black', font=f, spacing=2)
        c.save(f'{SP}/rv_{slug}_{half}.jpg', quality=80)
print('ok')
