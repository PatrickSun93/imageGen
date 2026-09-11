#!/usr/bin/env python3
"""把一本书的 10 页拼成一张联系表，审图用。

用法: python contact_sheet.py <图片目录> [输出文件]
例:   python contact_sheet.py sea_win
      → sea_win_sheet.png
"""
import sys, glob, os
from PIL import Image, ImageDraw

src = sys.argv[1].rstrip("/\\")
out = sys.argv[2] if len(sys.argv) > 2 else f"{os.path.basename(src)}_sheet.png"

files = sorted(glob.glob(os.path.join(src, "page_*.png")))
if not files:
    sys.exit(f"{src} 里没有 page_*.png")

CELL, COLS, LABEL = 420, 5, 26
rows = (len(files) + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * CELL, rows * (CELL + LABEL)), "white")
draw = ImageDraw.Draw(sheet)

for i, f in enumerate(files):
    im = Image.open(f).convert("RGB").resize((CELL, CELL), Image.LANCZOS)
    x, y = (i % COLS) * CELL, (i // COLS) * (CELL + LABEL)
    sheet.paste(im, (x, y))
    draw.text((x + 6, y + CELL + 7), os.path.basename(f)[:-4], fill="black")

sheet.save(out)
print(f"{out}  {sheet.size[0]}×{sheet.size[1]}  共 {len(files)} 页")
