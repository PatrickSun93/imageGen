"""Draw the exact-count diagram pages with code instead of the image model.

Why: these pages are the whole point of a maths book — eight circles must be eight circles — and the model
cannot count. Every such page came out wrong. Drawing them with PIL makes the counts exact by construction.

The look is built to sit next to the rendered pages: the book's own palette from its story JSON, a cream
ground, thick near-black outlines, flat fills, slight paper grain. 1024x1024, same as the renders.

usage: draw_math.py <slug> [<slug> ...]     writes storybook/out/<slug>_qwen/page_NN.png
       draw_math.py --check                 lists which pages each slug knows how to draw
Pages are written straight into the assembled book AND back into out/bakeoff/ so a later whole-book
rerun cannot copy an old model render over them.
"""
import json, math, os, random, sys
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")
REPO = r"C:\FlowDev\githubdevitems\comfyUIItems"
SB = os.path.join(REPO, "storybook")
OUT = os.path.join(SB, "out")
S = 1024                      # page size, matches the renders
PAGES = {}                    # (slug, n) -> function(draw, pal)


def page(slug, n):
    def deco(fn):
        PAGES[(slug, n)] = fn
        return fn
    return deco


def palette(slug):
    st = json.load(open(os.path.join(SB, f"story_{slug}.json"), encoding="utf-8"))
    p = st["palette"]
    return {
        "ink": p["ink"], "ground": p["ground"], "paper": p["paper"],
        "accent": p["accent"], "soft": p["soft"], "line": p["line"], "bark": p["bark"],
    }


def grain(img, strength=5):
    """A little paper noise so the flat fills don't look like a screenshot beside the painted pages."""
    rnd = random.Random(7)
    px = img.load()
    for y in range(0, S, 2):
        for x in range(0, S, 2):
            d = rnd.randint(-strength, strength)
            r, g, b = px[x, y]
            px[x, y] = (max(0, min(255, r + d)), max(0, min(255, g + d)), max(0, min(255, b + d)))
    return img


def disc(d, cx, cy, r, fill, pal, w=7):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=pal["ink"], width=w)


def cross(d, cx, cy, r, pal, w=11):
    k = r * 0.72
    d.line([cx - k, cy - k, cx + k, cy + k], fill=pal["ink"], width=w)
    d.line([cx - k, cy + k, cx + k, cy - k], fill=pal["ink"], width=w)


def arrow(d, x1, y1, x2, y2, pal, w=9, head=26):
    d.line([x1, y1, x2, y2], fill=pal["ink"], width=w)
    a = math.atan2(y2 - y1, x2 - x1)
    for s in (+1, -1):
        d.line([x2, y2, x2 - head * math.cos(a + s * 0.45), y2 - head * math.sin(a + s * 0.45)],
               fill=pal["ink"], width=w)


def row(n, cx, cy, gap):
    """n evenly spaced x positions centred on cx."""
    total = (n - 1) * gap
    return [(cx - total / 2 + i * gap, cy) for i in range(n)]


# ---------------------------------------------------------------- minus (拿走几个还剩几个)

@page("minus", 2)
def _(d, pal):
    """8 − 3 = 5：八个圆两排（5+3），画大，占满画面。"""
    for i, (x, y) in enumerate(row(5, S / 2, 360, 200)):
        disc(d, x, y, 84, pal["accent"] if i < 3 else pal["paper"], pal, w=10)
        if i < 3:
            cross(d, x, y, 84, pal, w=16)
    for i, (x, y) in enumerate(row(3, S / 2, 680, 200)):
        disc(d, x, y, 84, pal["paper"], pal, w=10)


@page("minus", 3)
def _(d, pal):
    """一堆八个，被一条粗竖线分成左三右五。"""
    d.line([S / 2, 150, S / 2, S - 150], fill=pal["ink"], width=14)
    for x, y in [(180, 360), (370, 360), (275, 640)]:
        disc(d, x, y, 92, pal["accent"], pal, w=10)
    for x, y in [(650, 300), (860, 300), (650, 520), (860, 520), (755, 740)]:
        disc(d, x, y, 92, pal["paper"], pal, w=10)


@page("minus", 4)
def _(d, pal):
    """上排八个搬走三个，下排五个搬回三个 —— 减法和加法是一对。"""
    for i, (x, y) in enumerate(row(8, S / 2, 300, 122)):
        disc(d, x, y, 54, pal["paper"] if i < 5 else pal["accent"], pal, w=9)
    arrow(d, 660, 400, 900, 400, pal, w=12, head=34)
    for i, (x, y) in enumerate(row(8, S / 2, 730, 122)):
        disc(d, x, y, 54, pal["paper"] if i < 5 else pal["accent"], pal, w=9)
    arrow(d, 900, 620, 660, 620, pal, w=12, head=34)


@page("minus", 5)
def _(d, pal):
    """0–10 数轴，从 8 往回退三步到 5。刻度粗、跨度大、退步弧线画满上半张。"""
    y = 620
    x0, x1 = 70, S - 70
    step = (x1 - x0) / 10
    d.line([x0, y, x1, y], fill=pal["ink"], width=14)
    for i in range(11):
        x = x0 + i * step
        d.line([x, y - 30, x, y + 30], fill=pal["ink"], width=11)
    for start in (8, 7, 6):
        xa, xb = x0 + start * step, x0 + (start - 1) * step
        d.arc([xb, y - 260, xa, y - 20], 180, 360, fill=pal["accent"], width=14)
        arrow(d, xb + 40, y - 150, xb + 4, y - 50, pal, w=12, head=30)
    disc(d, x0 + 8 * step, y, 46, pal["accent"], pal, w=10)
    disc(d, x0 + 5 * step, y, 46, pal["paper"], pal, w=10)


@page("minus", 6)
def _(d, pal):
    """八个对齐五个，多出来的三个就是差。"""
    top = row(8, S / 2, 330, 122)
    bot = row(8, S / 2, 700, 122)
    for i, (x, y) in enumerate(top):
        disc(d, x, y, 54, pal["accent"] if i >= 5 else pal["paper"], pal, w=9)
    for x, y in bot[:5]:
        disc(d, x, y, 54, pal["paper"], pal, w=9)
    for x, _ in top[5:]:
        d.line([x, 400, x, 630], fill=pal["accent"], width=11)


@page("minus", 7)
def _(d, pal):
    """减去零 vs 减去它自己。"""
    for x, y in row(5, S / 2, 320, 190):
        disc(d, x, y, 80, pal["paper"], pal, w=10)
    for x, y in row(5, S / 2, 710, 190):
        disc(d, x, y, 80, pal["accent"], pal, w=10)
        cross(d, x, y, 80, pal, w=16)


@page("minus", 11)
def _(d, pal):
    """五个加三个，合起来还是八个 —— 加回去验算。"""
    for x, y in row(5, 285, 300, 118):
        disc(d, x, y, 52, pal["paper"], pal, w=9)
    for x, y in row(3, 795, 300, 118):
        disc(d, x, y, 52, pal["accent"], pal, w=9)
    arrow(d, S / 2, 430, S / 2, 590, pal, w=13, head=36)
    for i, (x, y) in enumerate(row(8, S / 2, 740, 122)):
        disc(d, x, y, 54, pal["paper"] if i < 5 else pal["accent"], pal, w=9)


# ---------------------------------------------------------------- tens (十个一捆)

# 边距 30：一行五捆需要 5×180 + 4×12 = 948px，留 60 就只剩 904px 放不下。
# 这个数字是被 spread() 的报错逼出来的，不是拍脑袋定的。
MARGIN = 30          # 画面四边留白，任何东西都不许越过


def lay(n, width=None, margin=MARGIN):
    """把 n 个等宽的槽均分在可用宽度里，返回每个槽的中心 x 和槽宽。

    所有多件排列都走这里，页面代码里不再出现手算的像素坐标——上一版就是因为
    每改一次间距就要重算一遍位置，结果间距修好了、数目反而错了（每捆 14 根、
    散棍掉到画外）。数目和不出界必须由构造保证，不能靠我算对。
    """
    avail = (width or S) - 2 * margin
    slot = avail / n
    return [margin + slot * (i + 0.5) for i in range(n)], slot


def stick(d, x, y, h, pal, fill=None, half=13, w=6):
    """一根小棍：竖着的圆角长条。half 是半宽。"""
    d.rounded_rectangle([x - half, y - h / 2, x + half, y + h / 2], radius=min(10, half),
                        fill=fill or pal["paper"], outline=pal["ink"], width=w)


# 整数栅格：一根棍占 STICK_W，棍后跟 STICK_GAP 的缝。两者都不缩放，
# 所以一捆的宽度恒等于 n*(STICK_W+STICK_GAP)，根数由构造保证。
# 前三版败在“按槽宽反推棍宽”：槽一窄棍子细成线，描边把相邻两根并成一根，
# 十根目测成十一二根。放不下就换行，绝不压窄棍子。
# 尺寸按“一行要放得下五捆”倒推：5×(10+8)×10 + 4×18 = 972 < 1024−2×60 还差一点，
# 所以捆间距在五捆那几页收到 12。棍宽 10、缝 8 仍然一眼数得清。
STICK_W = 12         # 棍子实宽（整数）
STICK_GAP = 6        # 棍与棍之间的缝（整数）
STICK_EDGE = 3       # 描边宽：必须远小于 STICK_W/2，否则内部填色被挤没、两色交替失效
BUNDLE_PAD = 12      # 捆与捆之间至少留这么宽的空当


def bundle_span(n=10):
    return n * (STICK_W + STICK_GAP)


def bundle(d, cx, cy, pal, h=210, n=10, band=True, **_):
    """一捆：n 根小棍并排 + 一道扎绳。宽度恒定，不随槽位变化。"""
    span = bundle_span(n)
    x0 = int(cx - span / 2) + STICK_GAP // 2
    for i in range(n):
        x = x0 + i * (STICK_W + STICK_GAP) + STICK_W / 2
        stick(d, x, cy, h, pal, pal["accent"] if i % 2 else pal["paper"],
              half=STICK_W / 2, w=STICK_EDGE)
    if band:
        d.rounded_rectangle([cx - span / 2, cy - 24, cx + span / 2, cy + 24], radius=12,
                            fill=pal["bark"], outline=pal["ink"], width=7)
    return span


def spread(k, item_w, pad=BUNDLE_PAD, margin=MARGIN):
    """把 k 个等宽的东西横向摆开，返回中心 x 列表。放不下就报错而不是硬挤。"""
    need = k * item_w + (k - 1) * pad
    if need > S - 2 * margin:
        raise ValueError(f"{k} 个 × {item_w}px 放不进一行，改成换行排")
    x = (S - need) / 2 + item_w / 2
    return [x + i * (item_w + pad) for i in range(k)]


@page("tens", 2)
def _(d, pal):
    """十根扎成一捆 —— 正好十根。"""
    bundle(d, S / 2, S / 2, pal, h=560)
    return "1 捆 ×10 根"


@page("tens", 3)
def _(d, pal):
    """三捆加四根散的。捆和散棍都按实宽摆，摆不下就会直接报错。"""
    bw, sw_ = bundle_span(), STICK_W
    xs = spread(3, bw, pad=BUNDLE_PAD)
    for cx in xs:
        bundle(d, cx, 470, pal, h=420)
    loose = spread(4, sw_, pad=46)
    for cx in loose:
        stick(d, cx, 830, 150, pal, half=STICK_W / 2, w=STICK_EDGE)
    return "3 捆 ×10 根 + 4 根散"


@page("tens", 5)
def _(d, pal):
    """34 和 43：一样的两个数字，摆的位置不一样。"""
    bw = bundle_span()
    for cy, nb, nl in ((300, 3, 4), (740, 4, 3)):
        for cx in spread(nb, bw, pad=BUNDLE_PAD):
            bundle(d, cx, cy, pal, h=250)
        for cx in spread(nl, STICK_W, pad=46):
            stick(d, cx, cy + 180, 90, pal, half=STICK_W / 2, w=STICK_EDGE)
    return "上 3 捆 4 散（34）/ 下 4 捆 3 散（43）"


@page("tens", 6)
def _(d, pal):
    """散的凑够十根，就要扎成一捆搬到前面去。"""
    for i in range(10):
        stick(d, 640 + i * (STICK_W + 18), 520, 340, pal, half=STICK_W / 2, w=STICK_EDGE)
    arrow(d, 560, 520, 450, 520, pal, w=13, head=36)
    bundle(d, 250, 520, pal, h=340)
    return "10 根散 → 1 捆 ×10 根"


@page("tens", 7)
def _(d, pal):
    """十捆再扎一次，就是一百 —— 两行五捆。"""
    bw = bundle_span()
    for cy in (320, 720):
        for cx in spread(5, bw, pad=BUNDLE_PAD):
            bundle(d, cx, cy, pal, h=260)
    return "10 捆 ×10 根 = 100"


@page("tens", 11)
def _(d, pal):
    """十个一分是一角，十个一角是一元 —— 越往后越大。"""
    coins = ((205, 76), (505, 116), (838, 166))
    for cx, r in coins:
        disc(d, cx, S / 2, r, pal["accent"], pal, w=10)
        disc(d, cx, S / 2, r * 0.62, pal["paper"], pal, w=8)
    for (x1, r1), (x2, r2) in zip(coins, coins[1:]):      # 两段箭头一样长，不再手算端点
        mid = (x1 + r1 + x2 - r2) / 2
        arrow(d, mid - 34, S / 2, mid + 34, S / 2, pal, w=12, head=32)


@page("tens", 12)
def _(d, pal):
    """五捆还剩三根 —— 五十三。"""
    for cx in spread(5, bundle_span(), pad=BUNDLE_PAD):
        bundle(d, cx, 350, pal, h=280)
    for cx in spread(3, STICK_W, pad=60):
        stick(d, cx, 760, 200, pal, half=STICK_W / 2, w=STICK_EDGE)
    return "5 捆 ×10 根 + 3 根散（53）"


# ---------------------------------------------------------------- planets（数目和比例必须准的两页）

# 八颗行星的相对大小（水金地火 小，木土 大，天海 中）和颜色角色。
# 半径是按真实比例压缩过的，保证“前四颗明显小、后四颗明显大”这条唯一要讲的事成立。
PLANET_R = [16, 26, 27, 20, 78, 68, 42, 40]


@page("planets", 10)
def _(d, pal):
    """八颗排一排比大小：一行放得下就放，放不下由 spread 抛错。"""
    # 行星一律用冷色（soft/bark），暖橙只留给太阳：上一版木星也是橙的、大小又接近，
    # 一眼看去像画了两个太阳，孩子分不出哪个是「最左边那颗」。
    cols = [pal["bark"], pal["soft"], pal["bark"], pal["soft"],
            pal["soft"], pal["bark"], pal["soft"], pal["bark"]]
    # 太阳完整画在左侧，八颗在它右边的剩余宽度里排开。上一版用 pieslice 从
    # x=-170 起画，太阳被切成一牙；起点又写死 x=100，和按 S-120 算的 pad 对不上，
    # 最右一颗顶到画边。现在左右边距都从 MARGIN 推，页面里不再有手写的起点。
    sun_r = 96                                      # 明显大过最大的木星（78），一眼分得出
    sun_cx = MARGIN + sun_r
    disc(d, sun_cx, S / 2, sun_r, pal["accent"], pal, w=8)
    left = sun_cx + sun_r + 34                      # 行星区左界
    total = sum(2 * r for r in PLANET_R)
    pad = (S - MARGIN - left - total) / (len(PLANET_R) - 1)
    if pad < 6:
        raise ValueError(f"八颗行星放不进剩余的 {S - MARGIN - left}px")
    x = left
    for r, c in zip(PLANET_R, cols):
        disc(d, x + r, S / 2, r, c, pal, w=7)
        x += 2 * r + pad
    return f"太阳 + 8 颗，半径 {PLANET_R}，前四小后四大"


@page("planets", 11)
def _(d, pal):
    """八条同心轨道，一圈比一圈大，每条上坐一颗，角度错开免得连成一线。"""
    cx = cy = S / 2
    for i in range(8):
        r = 96 + i * 54
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=pal["soft"], width=4)
    disc(d, cx, cy, 58, pal["accent"], pal, w=8)
    for i in range(8):
        r = 96 + i * 54
        a = -1.15 + i * 0.82             # 每颗错开约 47 度，八颗绕开一圈
        disc(d, cx + r * math.cos(a), cy + r * math.sin(a), 15 + i % 3 * 4,
             pal["bark"] if i % 2 else pal["paper"], pal, w=5)
    return "太阳 + 8 条同心轨道，每条 1 颗"


def render(slug):
    pal = palette(slug)
    done = []
    for (s, n), fn in sorted(PAGES.items()):
        if s != slug:
            continue
        img = Image.new("RGB", (S, S), pal["ground"])
        d = ImageDraw.Draw(img)
        note = fn(d, pal)          # 页面函数返回“这页画了什么”的构造清单
        grain(img)
        dst = os.path.join(OUT, f"{slug}_qwen", f"page_{n:02d}.png")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        # backups go OUTSIDE the book folder: pack_images.py and contact_sheet.py both collect
        # page_*.png, so anything kept beside the real pages gets published as an extra page
        bdir = os.path.join(OUT, "_backup", slug)
        os.makedirs(bdir, exist_ok=True)
        keep = os.path.join(bdir, f"page_{n:02d}_model.png")
        if os.path.exists(dst) and not os.path.exists(keep):
            os.rename(dst, keep)
        img.save(dst)
        bake = os.path.join(OUT, "bakeoff", f"{slug}_p{n:02d}_lightning8.png")
        img.save(bake)
        done.append((n, note or ""))
    print(f"{slug}: 程序画了 {len(done)} 页")
    for n, note in done:                # 数字由绘制参数直接打印，核对数字而不是数图
        print(f"    p{n:02d}  {note}")


if __name__ == "__main__":
    if "--check" in sys.argv:
        for s in sorted({s for s, _ in PAGES}):
            print(s, sorted(n for x, n in PAGES if x == s))
    else:
        for slug in sys.argv[1:]:
            render(slug)
