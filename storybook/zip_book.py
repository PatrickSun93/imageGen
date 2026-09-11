"""book_done.py <slug>: zip page_01..10 as storybook/out/<slug>.zip and write a numbered contact sheet."""
import sys, os, zipfile
from PIL import Image, ImageDraw, ImageFont
ROOT = r"C:\FlowDev\githubdevitems\comfyUIItems"
slug, sheet_dir = sys.argv[1], sys.argv[2]
src = os.path.join(ROOT, "storybook", "out", slug + "_lora")
pages = [os.path.join(src, f"page_{n:02d}.png") for n in range(1, 11)]
missing = [p for p in pages if not os.path.exists(p)]
if missing: sys.exit(f"missing: {missing}")
dst = os.path.join(ROOT, "storybook", "out", slug + ".zip")
with zipfile.ZipFile(dst, "w", zipfile.ZIP_STORED) as z:
    for p in pages: z.write(p, os.path.basename(p))
S = 420
sheet = Image.new("RGB", (S * 5, S * 2), "white")
d = ImageDraw.Draw(sheet); f = ImageFont.truetype("arialbd.ttf", 34)
for i, p in enumerate(pages):
    x, y = (i % 5) * S, (i // 5) * S
    sheet.paste(Image.open(p).convert("RGB").resize((S - 6, S - 6), Image.LANCZOS), (x + 3, y + 3))
    d.rectangle([x + 6, y + 6, x + 56, y + 48], fill="white"); d.text((x + 12, y + 8), str(i + 1), fill="red", font=f)
out = os.path.join(sheet_dir, f"sheet_{slug}.png"); sheet.save(out)
print(dst, round(os.path.getsize(dst) / 1048576, 1), "MB;", "sheet", out)
