# -*- coding: utf-8 -*-
"""把一本书做成印刷文件：10 寸方款照片书/绘本。

  输出 out/print_<slug>/
    00_cover.jpg          封面（书名压在第 1 页的图上，放在最空的那一条）
    01.jpg … 32.jpg       内页，旁白排在画面上最空的那一条
    <slug>_print.pdf      上面这些按顺序合成一个 PDF
    check_sheet.jpg       全书缩略图，给人一眼看画风是不是一致

尺寸：10 寸成品 254mm + 四边各 3mm 出血 = 260mm，300dpi → 3071 像素。
字离裁切线至少 5mm（出血 3mm + 5mm = 约 95 像素，取 110）。

放大：1024 → 3071 用 LANCZOS 加一点锐化。这个画风是平涂色块加细线，
这样放大不会糊得明显；以后装了超分模型可以换掉 upscale()。

字放哪儿：按字块的实际大小，在上/下 × 左/中/右六个位置里算「忙不忙」
（亮度梯度的平均值），放在最空的那一个。要是那一块也不空，
字后面垫一块半透明的纸色圆角底，保证四岁孩子也看得清。

usage: make_print.py <slug> [<slug> ...]
"""
import json, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
SB = os.path.dirname(os.path.abspath(__file__))
PX = 3071                     # 260mm @ 300dpi
SAFE = 110                    # 出血 + 安全边
FONT = r"C:\Windows\Fonts\Dengb.ttf"
FONT_EN = r"C:\Windows\Fonts\georgiab.ttf"   # 英文版用 Georgia 粗体，书的感觉
BODY_PT = 28                  # 成品上 28pt，一个字约 1 厘米，孩子跟着看也清楚
BODY = int(BODY_PT / 72 * 300)
BODY_EN = int(24 / 72 * 300)  # 英文句子比中文长，28pt 的字块会压到角色，24pt 仍比一般绘本大
INK = (46, 40, 30)
PAPER = (246, 241, 228)
MIN_BODY = int(20 / 72 * 300)
BUSY = 7.0                   # 梯度均值超过这个，就垫底


def upscale(im):
    im = im.convert("RGB").resize((PX, PX), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))


def busyness(im, box):
    a = np.asarray(im.crop(box).convert("L").resize((256, 80)), dtype=np.float32)
    return float(np.abs(np.diff(a, axis=0)).mean() + np.abs(np.diff(a, axis=1)).mean())


def fit(lines, font, width):
    """按字宽折行：旁白本来就短，超宽的行再拆。英文按单词拆，不把一个词劈成两半。"""
    out = []
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    for ln in lines:
        units = [w + " " for w in ln.split(" ")] if " " in ln else list(ln)
        cur = ""
        for u in units:
            if d.textlength((cur + u).rstrip(), font=font) > width and cur:
                out.append(cur.rstrip()); cur = u
            else:
                cur += u
        out.append(cur.rstrip())
    return out


def place_text(im, text, size, title=False, font_path=FONT):
    """在六个位置（上/下 × 左/中/右）里挑最空的一块放字：按字块实际大小算，
    不再整条居中——居中会压在龙头上（第一版第 21、32 页就是）。"""
    # 字多的页（蚂蚁那本英文有七行长句）字块会盖住半个画面：超过画面三分之一高就缩小字号，最小 20pt
    while True:
        font = ImageFont.truetype(font_path, size)
        lines = fit(text.split("\n"), font, PX - 2 * SAFE - 80)
        lh = int(size * 1.55)
        if title or lh * len(lines) + 70 <= PX // 3 or size <= MIN_BODY:
            break
        size -= 6
    d = ImageDraw.Draw(im, "RGBA")
    widths = [d.textlength(l, font=font) for l in lines]
    w, h = int(max(widths)) + 110, lh * len(lines) + 70
    xs = {"左": SAFE + 20, "中": (PX - w) // 2, "右": PX - SAFE - 20 - w}
    ys = {"上": SAFE + 20, "下": PX - SAFE - 20 - h}
    if title:
        # 书名块大，只放上下两条常常压住主角（龙轮到了吗的封面压住了那个秋千），
        # 所以书名多一排居中的候选位置，左中右都能放
        ys["中"] = (PX - h) // 2
    cands = []
    for yk, y in ys.items():
        for xk, x in xs.items():
            score = busyness(im, (x, y, x + w, y + h)) * (1.0 if yk == "上" else 1.1)
            cands.append((score, yk + xk, x, y))
    busy, where, x0, y0 = min(cands)
    if busy > BUSY or title:
        d.rounded_rectangle((x0, y0, x0 + w, y0 + h), radius=60, fill=PAPER + (225,))
    for i, l in enumerate(lines):
        d.text((x0 + (w - widths[i]) / 2, y0 + 45 + i * lh), l, font=font, fill=INK)
    return where, busy


def title_size(text, font_path):
    """书名从正文的 1.7 倍往下缩，缩到每行都不用折行为止（英文书名长，折行会把一个词甩到下一行）。"""
    size = int(BODY * 1.7)
    while size > BODY:
        f = ImageFont.truetype(font_path, size)
        if all(f.getlength(l) <= PX - 2 * SAFE - 80 - 110 for l in text.split("\n")):
            break
        size -= 8
    return size


def build(slug):
    st = json.load(open(os.path.join(SB, f"story_{slug}.json"), encoding="utf-8"))
    # 英文版 story_<slug>_en.json 用中文版的图（image_slug），旁白在每页的 "en" 里
    # 早期那几本的成书图不在 <slug>_qwen 里，英文版用 image_dir 指到从已发布网页导出的图
    src = os.path.join(SB, "out", st.get("image_dir") or f"{st.get('image_slug', slug)}_qwen")
    en = st.get("lang") == "en"
    text, font, body = st.get("text_key", "zh"), (FONT_EN if en else FONT), (BODY_EN if en else BODY)
    dst = os.path.join(SB, "out", f"print_{slug}")
    os.makedirs(dst, exist_ok=True)
    pages, report = [], []
    cover = upscale(Image.open(os.path.join(src, "page_01.png")))
    title = st["title"] + "\n" + st.get("subtitle", "")
    place_text(cover, title, title_size(title, font), title=True, font_path=font)
    cover.save(os.path.join(dst, "00_cover.jpg"), quality=95, dpi=(300, 300))
    pages.append(cover)
    for p in st["pages"]:
        im = upscale(Image.open(os.path.join(src, f"page_{p['n']:02d}.png")))
        where, busy = place_text(im, p[text], body, font_path=font)
        im.save(os.path.join(dst, f"{p['n']:02d}.jpg"), quality=95, dpi=(300, 300))
        pages.append(im)
        report.append(f"p{p['n']:02d} {where} {busy:.1f}{' 垫底' if busy > BUSY else ''}")
    pdf = os.path.join(dst, f"{slug}_print.pdf")
    pages[0].save(pdf, save_all=True, append_images=pages[1:], resolution=300)
    # 缩略图：一眼看全书画风是否一致
    T = 300
    cols = 6
    rows = (len(pages) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * T, rows * T), "white")
    for i, im in enumerate(pages):
        sheet.paste(im.resize((T, T)), ((i % cols) * T, (i // cols) * T))
    sheet.save(os.path.join(dst, "check_sheet.jpg"), quality=85)
    print(f"{slug}: {len(pages)} 页（含封面）→ {pdf}  {os.path.getsize(pdf) // 1048576} MB")
    print("  " + " | ".join(report))


if __name__ == "__main__":
    for s in sys.argv[1:]:
        build(s)
