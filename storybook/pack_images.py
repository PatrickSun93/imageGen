#!/usr/bin/env python3
"""把一本书的 PNG 压成 JPEG 并转 base64，供 build_web.py 内嵌。

用法: python pack_images.py <图片目录> <网页目录> [质量]
例:   python pack_images.py sea_win web_sea
      → web_sea/images_b64.json
"""
import sys, os, io, glob, json, base64
from PIL import Image

sys.stdout.reconfigure(encoding="utf-8")   # the summary lines are Chinese; Windows consoles default to cp1252

src     = sys.argv[1].rstrip("/\\")
webdir  = sys.argv[2].rstrip("/\\")
quality = int(sys.argv[3]) if len(sys.argv) > 3 else 82
LIMIT   = 16 * 1024 * 1024        # Artifact 上限

files = sorted(glob.glob(os.path.join(src, "page_*.png")))
if not files:
    sys.exit(f"{src} 里没有 page_*.png")
os.makedirs(webdir, exist_ok=True)

out, total = {}, 0
for f in files:
    n = str(int(os.path.basename(f).split("_")[1].split(".")[0]))
    buf = io.BytesIO()
    Image.open(f).convert("RGB").save(
        buf, "JPEG", quality=quality, optimize=True, progressive=True)
    total += buf.tell()
    out[n] = base64.b64encode(buf.getvalue()).decode()

path = os.path.join(webdir, "images_b64.json")
json.dump(out, open(path, "w"))
b64 = os.path.getsize(path)
print(f"{len(files)} 页  JPEG {total/1024/1024:.2f} MB  →  base64 {b64/1024/1024:.2f} MB")
print(f"写入 {path}")
if b64 > LIMIT * 0.8:
    print(f"⚠️  接近 Artifact 的 16 MB 上限，考虑降质量：python pack_images.py {src} {webdir} 72")
