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


def inked(im):
    """画了东西的地方（不是奶油色纸）= True。纸：亮、不怎么饱和。稍微膨胀一圈，字别贴着线。"""
    a = np.asarray(im.convert("RGB").resize((PX // 4, PX // 4)), dtype=np.int16)
    mx, mn = a.max(axis=2), a.min(axis=2)
    ink = (mx < 200) | ((mx - mn) > 45)
    img = Image.fromarray((ink * 255).astype(np.uint8)).filter(ImageFilter.MaxFilter(9)).resize((PX, PX))
    return np.asarray(img) > 127


def fit(lines, font, width):
    """按字宽折行：旁白本来就短，超宽的行再拆。英文按单词拆，不把一个词劈成两半。"""
    out = []
    d = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    NO_START = "，。！？、；：」』）…—,.!?;:)\"”’"      # 这些不放行首
    for ln in lines:
        latin = any("a" <= c.lower() <= "z" for c in ln)
        units = [w + " " for w in ln.split(" ")] if latin else list(ln)
        cur = ""
        for u in units:
            if u.strip() and u.strip()[0] in NO_START and cur:
                cur += u                          # 标点跟着上一个字走，宁可稍微超一点
                continue
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
    # 候选位置：左/中/右 × 从上到下 7 档，字块再试三种宽度（整宽、2/3、1/2——窄一点、行多一点，
    # 才塞得进空角）。按「这块里有多少不是纸的像素」挑：只看梯度的话，平涂的大脸梯度很低，
    # 字会被放到脸上（英文版好几页盖住了眼睛）。
    ink = inked(im)
    full = PX - 2 * SAFE - 80
    cands = []
    for frac in (1.0, 0.66, 0.5):
        ls = lines if frac == 1.0 else fit(text.split("\n"), font, int(full * frac))
        if len(ls) * lh + 70 > PX * 0.45:
            continue
        ws = [d.textlength(l, font=font) for l in ls]
        w, h = int(max(ws)) + 110, lh * len(ls) + 70
        xs = {"左": SAFE + 20, "中": (PX - w) // 2, "右": PX - SAFE - 20 - w}
        top, bottom = SAFE + 20, PX - SAFE - 20 - h
        for i in range(7):
            y = top + (bottom - top) * i // 6
            for xk, x in xs.items():
                cover = float(ink[y:y + h, x:x + w].mean())
                # 同样空时：靠上下边更像书；整宽排版优先（行少好念）
                score = cover + (0.0 if i in (0, 6) else 0.03) + (0.0 if frac == 1.0 else 0.02)
                cands.append((score, cover, f"{i}{xk}{'' if frac == 1.0 else frac}", x, y, w, h, ls, ws))
    _, cover, where, x0, y0, w, h, lines, widths = min(cands, key=lambda c: c[0])
    busy = busyness(im, (x0, y0, x0 + w, y0 + h))
    if cover > 0.04 or busy > BUSY or title:
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


def band_page(src_im, text, size, font_path):
    """图上方、字在下面一条纸上：早期那几本画面没给字留空，字压在图上会盖住他的脸、压在黑夜空上看不清。
    图缩成正方形放在上部居中，左右留纸；下面的纸条按字的行数定高。"""
    while True:                                # 字条最多占三成，超了就缩字，别把图挤小
        font = ImageFont.truetype(font_path, size)
        lines = fit(text.split("\n"), font, PX - 2 * SAFE - 80)
        lh = int(size * 1.45)
        band = lh * len(lines) + 2 * SAFE
        if band <= PX * 0.3 or size <= MIN_BODY:
            break
        size -= 6
    side = PX - band - SAFE                    # 图的边长
    page = Image.new("RGB", (PX, PX), PAPER)
    pic = src_im.convert("RGB").resize((side, side), Image.LANCZOS).filter(
        ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
    page.paste(pic, ((PX - side) // 2, SAFE))
    d = ImageDraw.Draw(page)
    y0 = SAFE + side + (band - lh * len(lines)) // 2 - SAFE // 3
    for i, l in enumerate(lines):
        w = d.textlength(l, font=font)
        d.text(((PX - w) / 2, y0 + i * lh), l, font=font, fill=INK)
    return page


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
        if st.get("image_dir"):              # 早期 5 本：图上字下
            im = band_page(Image.open(os.path.join(src, f"page_{p['n']:02d}.png")), p[text], body, font)
            im.save(os.path.join(dst, f"{p['n']:02d}.jpg"), quality=95, dpi=(300, 300))
            pages.append(im)
            report.append(f"p{p['n']:02d} band")
            continue
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
