"""审图用：一本书一张联系表 + 旁白清单。usage: sheet.py <slug> [slug...]"""
import base64, glob, io, json, os, re, sys
from PIL import Image, ImageDraw
SB = r"C:\FlowDev\githubdevitems\comfyUIItems\storybook"
SP = os.path.join(SB, "out", "_review"); os.makedirs(SP, exist_ok=True)
sys.stdout.reconfigure(encoding="utf-8")

ALIAS={"ants_flux":"ants_moving","rafflesia":"_art_rafflesia"}

def page_images(slug, npages):
    slug = ALIAS.get(slug, slug)
    for d in (f"{SB}/out/{slug}_qwen", f"{SB}/out/{slug}", f"{SB}/out/_backup/{slug}"):
        if len(glob.glob(f"{d}/page_*.png")) >= npages:
            return [Image.open(f"{d}/page_{i:02d}.png") for i in range(1, npages + 1)]
    j = f"{SB}/out/web_{slug}/images_b64.json"
    if os.path.exists(j):
        data = json.load(open(j, encoding="utf-8"))
        vals = [data[k] for k in sorted(data)] if isinstance(data, dict) else data
        out = []
        for v in vals:
            if isinstance(v, dict): v = v.get("b64") or v.get("data") or ""
            out.append(Image.open(io.BytesIO(base64.b64decode(re.sub(r"^data:[^,]+,", "", v)))))
        return out[:npages]
    raise SystemExit(f"{slug}: 找不到页图")

for slug in sys.argv[1:]:
    st = json.load(open(f"{SB}/story_{slug}.json", encoding="utf-8"))
    pages = st["pages"]; ims = page_images(slug, len(pages))
    T, C = 330, 6
    R = (len(ims) + C - 1) // C
    c = Image.new("RGB", (C * T, R * (T + 16)), "white"); d = ImageDraw.Draw(c)
    for i, im in enumerate(ims):
        im = im.convert("RGB"); im.thumbnail((T, T))
        x, y = (i % C) * T, (i // C) * (T + 16) + 16
        c.paste(im, (x, y)); d.text((x + 3, y - 14), f"p{i+1}", fill="red")
    p = f"{SP}/sheet_{slug}.jpg"; c.save(p, quality=80)
    print(f"== {slug} | {st['title']} | {st.get('subtitle','')} | {len(pages)} 页")
    for pg in pages:
        zh = re.sub(r"\s+", " ", pg["zh"])
        print(f"p{pg['n']}: {zh}")
    print(p, "\n")
