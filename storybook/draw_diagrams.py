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
from PIL import Image, ImageDraw, ImageFont

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


# ---------------------------------------------------------------- 通用图元
# 按这次重审里的错法频次挑的：
#   panel2   「对比两格画成一样」——磁铁同极相斥、电路断/通、四冲程、翅膀上下拍、冰与水
#   ngon     「六边形一律画成八边形」——蜂房、雪花、形状各中一次
#   hex_tile 「铺满不留缝」说不清
#   wave      吸 4 呼 6、声速 vs 光速这类长短关系

def panel2(d, pal, gap=44, top=150):
    """左右两格等大的对比框，返回两个 (cx, cy, w, h)；内容由调用方画。

    两格永远等大、等高、并排，差别只能来自画进去的内容 —— 这样「两格画成一样」
    这种错法在构造上就不可能出现（要么内容不同，要么是调用方自己写错）。
    """
    w = (S - 2 * MARGIN - gap) / 2
    h = S - top - MARGIN
    cy = top + h / 2
    boxes = []
    for i in range(2):
        cx = MARGIN + w / 2 + i * (w + gap)
        d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                            radius=18, fill=pal["paper"], outline=pal["ink"], width=6)
        boxes.append((cx, cy, w, h))
    return boxes


def ngon(d, cx, cy, r, n, pal, fill=None, w=6, rot=0.0):
    """正 n 边形。边数由参数保证，不靠模型数。"""
    pts = [(cx + r * math.cos(rot + 2 * math.pi * i / n),
            cy + r * math.sin(rot + 2 * math.pi * i / n)) for i in range(n)]
    d.polygon(pts, fill=fill or pal["paper"])
    for a, b in zip(pts, pts[1:] + pts[:1]):      # polygon 的 outline 不支持 width
        d.line([a, b], fill=pal["ink"], width=w)
    return pts


def hex_tile(d, cx, cy, r, pal, rings=2, fill=None, w=5, box=None):
    """正六边形蜂窝：一圈一圈铺开，边对边不留缝。返回铺了几格。

    box 给了 (w, h) 就按它反推半径，保证整片落在框内 —— 上一版写死 r=44、rings=2，
    结果蜂窝铺出了右框还压到左框上。凡是往 panel2 的框里塞东西，尺寸都必须由框反推。
    """
    if box:
        # 横向极值：q+s/2 最大 1.5*rings，再加自身半宽 0.5 → 总宽 r*√3*(3*rings+1)
        # 纵向极值：s 最大 rings，步距 1.5r，再加自身半高 r → 总高 r*(3*rings+2)
        bw, bh = box
        r = min(bw / (math.sqrt(3) * (3 * rings + 1)), bh / (3 * rings + 2)) * 0.94
    dx, dy = r * math.sqrt(3), r * 1.5
    cells = {(0, 0)}
    for ring in range(1, rings + 1):
        for q in range(-ring, ring + 1):
            cells |= {(q, -ring), (q, ring)}
        for s in range(-ring + 1, ring):
            cells |= {(-ring, s), (ring, s)}
    for q, s in sorted(cells):
        ngon(d, cx + dx * (q + s / 2), cy + dy * s, r, 6, pal,
             fill=fill, w=w, rot=math.pi / 2)
    return len(cells)


def wave(d, x0, x1, cy, pal, rise=1, fall=1, cycles=2, amp=90, w=10):
    """呼吸波：rise/fall 是上升段与下降段的相对长度（吸 4 呼 6 就传 4 和 6）。"""
    span = (x1 - x0) / cycles
    up = span * rise / (rise + fall)
    for c in range(cycles):
        x = x0 + c * span
        d.arc([x, cy - amp, x + 2 * up, cy + amp], 180, 360, fill=pal["accent"], width=w)
        d.arc([x + up, cy - amp, x + up + 2 * (span - up), cy + amp], 0, 180,
              fill=pal["soft"], width=w)


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


# ---------------------------------------------------------------- magnet（磁铁为什么吸铁）

def bar_magnet(d, cx, cy, w, h, pal, flip=False):
    """条形磁铁：一半 accent 一半 soft，两极颜色分明。flip 把红端换到左边。"""
    a, b = (pal["soft"], pal["accent"]) if not flip else (pal["accent"], pal["soft"])
    d.rectangle([cx - w / 2, cy - h / 2, cx, cy + h / 2], fill=a)
    d.rectangle([cx, cy - h / 2, cx + w / 2, cy + h / 2], fill=b)
    d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2],
                outline=pal["ink"], width=6)


@page("magnet", 4)
def _(d, pal):
    """异极相吸 vs 同极相斥 —— 两格的箭头方向必须相反。"""
    (lx, ly, lw, _), (rx, ry, rw, _) = panel2(d, pal)
    bw, bh = lw * 0.36, 84
    off = lw * 0.23                       # 两块磁铁各自的中心偏移
    ay = ly - bh / 2 - 54                 # 箭头贴在磁铁上方，一眼看出是这两块之间的事
    # 左：蓝端对红端，两支箭头相向（吸）
    bar_magnet(d, lx - off, ly, bw, bh, pal, flip=False)
    bar_magnet(d, lx + off, ly, bw, bh, pal, flip=True)
    arrow(d, lx - off - 10, ay, lx - 26, ay, pal, w=9, head=22)
    arrow(d, lx + off + 10, ay, lx + 26, ay, pal, w=9, head=22)
    # 右：两个红端相对，两支箭头背离（推）
    bar_magnet(d, rx - off, ry, bw, bh, pal, flip=False)
    bar_magnet(d, rx + off, ry, bw, bh, pal, flip=False)
    arrow(d, rx - 26, ay, rx - off - 10, ay, pal, w=9, head=22)
    arrow(d, rx + 26, ay, rx + off + 10, ay, pal, w=9, head=22)
    return "左格异极相吸（两箭头相向）/ 右格同极相斥（两箭头背离）"


@page("magnet", 6)
def _(d, pal):
    """磁区：左格乱七八糟，右格全部转成同一个方向。"""
    rnd = random.Random(11)
    (lx, ly, lw, lh), (rx, ry, rw, rh) = panel2(d, pal)
    for gx, gy, w_, h_, aligned in ((lx, ly, lw, lh, False), (rx, ry, rw, rh, True)):
        cols, rows = 5, 6
        for i in range(cols):
            for j in range(rows):
                x = gx - w_ / 2 + w_ * (i + 0.5) / cols
                y = gy - h_ / 2 + h_ * (j + 0.5) / rows
                a = 0.0 if aligned else rnd.uniform(0, 2 * math.pi)
                dx, dy = 34 * math.cos(a), 34 * math.sin(a)
                arrow(d, x - dx / 2, y - dy / 2, x + dx / 2, y + dy / 2, pal, w=6, head=14)
    return "左 30 个乱向箭头 / 右 30 个全部朝右"


@page("magnet", 3)
def _(d, pal):
    """一头北极一头南极：两端颜色分明，再各点一簇铁屑表示那里力气最大。"""
    bar_magnet(d, S / 2, S / 2, 620, 180, pal)
    rnd = random.Random(3)
    for side in (-1, +1):                       # 两端各撒一簇铁屑，中间不撒
        for _ in range(26):
            x = S / 2 + side * rnd.uniform(250, 360)
            y = S / 2 + rnd.uniform(-160, 160)
            a = rnd.uniform(0, math.pi)
            d.line([x - 14 * math.cos(a), y - 14 * math.sin(a),
                    x + 14 * math.cos(a), y + 14 * math.sin(a)], fill=pal["ink"], width=5)
    return "1 条磁铁，左半 soft（北）右半 accent（南），两端各 26 根铁屑、中间没有"


@page("magnet", 7)
def _(d, pal):
    """磁铁吸起一根钉子，钉子自己又吸起第二根 —— 必须是一条链。"""
    bar_magnet(d, S / 2, 210, 420, 110, pal)
    x = S / 2
    for i, y in enumerate((330, 560)):
        d.rounded_rectangle([x - 22, y, x + 22, y + 190], radius=10,
                            fill=pal["soft"], outline=pal["ink"], width=6)
        d.ellipse([x - 46, y - 26, x + 46, y + 26], fill=pal["bark"], outline=pal["ink"], width=6)
    return "磁铁 → 钉子1 → 钉子2，挂成一条链"


@page("magnet", 9)
def _(d, pal):
    """地球的磁力线：从北极出来、鼓到两侧、再回到南极。

    上一版画成三个同心椭圆，闭合成环 —— 看上去还是「给地球套了几个环」，
    和模型原本画成土星环是同一个概念错误。磁力线必须是开口弧线：两端收拢到
    两极，中间鼓出去，左右各一族。
    """
    # 磁力线画了四版都被读成「环」（模型画土星环、同心椭圆、眼睛形闭环、尖角橄榄形），
    # 于是退成最朴素的画法：地球 + 地轴 + 一根指向北极的指南针。五岁孩子本来也看不懂
    # 磁力线，而「指南针总是指着南北」是他能理解的，磁力线交给旁白讲。
    cx, cy, R = S / 2, S / 2 + 20, 210
    d.line([cx, cy - R - 120, cx, cy + R + 120], fill=pal["ink"], width=10)
    disc(d, cx, cy, R, pal["bark"], pal, w=9)
    for py, col in ((cy - R, pal["accent"]), (cy + R, pal["paper"])):
        disc(d, cx, py, 20, col, pal, w=6)
    # 指南针：表盘压在地球右下方，针笔直指向上（北）
    nx, ny, nr = cx + R * 0.72, cy + R * 0.72, 104
    disc(d, nx, ny, nr, pal["paper"], pal, w=8)
    d.polygon([(nx, ny - nr * 0.72), (nx - 20, ny), (nx + 20, ny)], fill=pal["accent"])
    d.polygon([(nx, ny + nr * 0.72), (nx - 20, ny), (nx + 20, ny)], fill=pal["paper"])
    for pts in (((nx, ny - nr * 0.72), (nx - 20, ny), (nx + 20, ny)),
                ((nx, ny + nr * 0.72), (nx - 20, ny), (nx + 20, ny))):
        for a, b in zip(pts, pts[1:] + pts[:1]):
            d.line([a, b], fill=pal["ink"], width=5)
    disc(d, nx, ny, 12, pal["ink"], pal, w=3)
    return "1 个地球 + 1 根地轴（两极各 1 个记号）+ 1 个指南针，针指向北"


@page("magnet", 10)
def _(d, pal):
    """指南针：一根针，一半红一半白。"""
    cx, cy, R = S / 2, S / 2, 300
    disc(d, cx, cy, R, pal["paper"], pal, w=10)
    for i in range(12):
        a = i * math.pi / 6
        d.line([cx + (R - 34) * math.cos(a), cy + (R - 34) * math.sin(a),
                cx + (R - 12) * math.cos(a), cy + (R - 12) * math.sin(a)],
               fill=pal["ink"], width=6)
    d.polygon([(cx, cy - 210), (cx - 34, cy), (cx + 34, cy)], fill=pal["accent"])
    d.polygon([(cx, cy + 210), (cx - 34, cy), (cx + 34, cy)], fill=pal["paper"])
    for pts in (((cx, cy - 210), (cx - 34, cy), (cx + 34, cy)),
                ((cx, cy + 210), (cx - 34, cy), (cx + 34, cy))):
        for a, b in zip(pts, pts[1:] + pts[:1]):
            d.line([a, b], fill=pal["ink"], width=6)
    disc(d, cx, cy, 20, pal["ink"], pal, w=4)
    return "1 个表盘 + 1 根针，上半 accent 下半 paper"


# ---------------------------------------------------------------- power / ice / bird（对比两格）

@page("power", 10)
def _(d, pal):
    """断开 vs 接通：左格缺一段、灯暗，右格闭合、灯亮。"""
    for (cx, cy, w_, h_), closed in zip(panel2(d, pal), (False, True)):
        lw_, lh_ = w_ * 0.62, h_ * 0.42
        x0, x1 = cx - lw_ / 2, cx + lw_ / 2
        y0, y1 = cy - lh_ / 2 + 40, cy + lh_ / 2 + 40
        d.line([x0, y0, x1, y0], fill=pal["ink"], width=9)
        d.line([x0, y0, x0, y1], fill=pal["ink"], width=9)
        d.line([x1, y0, x1, y1], fill=pal["ink"], width=9)
        if closed:
            d.line([x0, y1, x1, y1], fill=pal["ink"], width=9)
        else:
            d.line([x0, y1, cx - 46, y1], fill=pal["ink"], width=9)
            d.line([cx + 46, y1, x1, y1], fill=pal["ink"], width=9)
        disc(d, cx, y0 - 4, 52, pal["accent"] if closed else pal["soft"], pal, w=7)
        if closed:
            for i in range(8):
                a = i * math.pi / 4
                d.line([cx + 66 * math.cos(a), y0 - 4 + 66 * math.sin(a),
                        cx + 96 * math.cos(a), y0 - 4 + 96 * math.sin(a)],
                       fill=pal["accent"], width=7)
    return "左格回路有缺口、灯暗 / 右格回路闭合、灯亮有光线"


@page("ice", 4)
def _(d, pal):
    """冰里的分子排成整齐格子，而且比水里挨得更紧。"""
    (lx, ly, lw, lh), (rx, ry, rw, rh) = panel2(d, pal)
    for cx, cy, w_, h_, n, jitter in ((lx, ly, lw, lh, 7, 0.0), (rx, ry, rw, rh, 6, 0.34)):
        rnd = random.Random(5)
        r = min(w_ / (2 * n), h_ / (2 * n)) * 0.9
        for j in range(n):
            for i in range(n):
                jx = rnd.uniform(-jitter, jitter) * 2 * r
                jy = rnd.uniform(-jitter, jitter) * 2 * r
                disc(d, cx + (i - (n - 1) / 2) * 2 * r + jx,
                     cy + (j - (n - 1) / 2) * 2 * r + jy, r - 3, pal["soft"], pal, w=4)
    return "左 49 个排成整齐格子（冰）/ 右 36 个挤散（水）"


@page("bird", 7)
def _(d, pal):
    """下拍羽毛合严，上抬羽毛张开 —— 两格的羽毛间距必须不同。"""
    for (cx, cy, w_, h_), tight in zip(panel2(d, pal), (True, False)):
        n, span = 9, w_ * 0.72
        gap = span / n * (0.55 if tight else 1.0)
        for i in range(n):
            x = cx - (n - 1) * gap / 2 + i * gap
            d.line([x, cy - h_ * 0.22, x, cy + h_ * 0.22], fill=pal["ink"], width=14)
        arrow(d, cx, cy - h_ * 0.34, cx, cy - h_ * 0.34 + (70 if tight else -70), pal, w=10, head=26)
    return "左 9 根羽毛合严、箭头向下 / 右 9 根张开、箭头向上"


@page("hiccup", 10)
def _(d, pal):
    """吸气数到四，吐气数到六 —— 上升段必须明显短于下降段。"""
    wave(d, MARGIN + 30, S - MARGIN - 30, S / 2, pal, rise=4, fall=6, cycles=2, amp=150, w=14)
    return "2 个周期，上升段:下降段 = 4:6"


# ---------------------------------------------------------------- fish / sound / power（流向与长短）

def fish_body(d, cx, cy, L, pal, fill=None):
    """一条侧看的鱼。返回 (嘴 x, 鳃盖 x, 鳃盖后缘 y 上沿, 身高)。

    鳃盖必须明显靠近头部（头长约占身长两成），否则出水口看起来在肚子中间；
    再给腹部加一块浅色，让「上背下腹」分得开 —— 上一版通体一色，鳃盖线几乎看不见。
    """
    h = L * 0.46
    d.ellipse([cx - L / 2, cy - h / 2, cx + L / 2, cy + h / 2],
              fill=fill or pal["soft"], outline=pal["ink"], width=7)
    d.chord([cx - L / 2, cy - h / 2, cx + L / 2, cy + h / 2], 12, 168,
            fill=pal["paper"], outline=pal["ink"], width=5)          # 浅色腹部
    tail = [(cx + L / 2 - 6, cy), (cx + L / 2 + L * 0.26, cy - h * 0.42),
            (cx + L / 2 + L * 0.26, cy + h * 0.42)]
    d.polygon(tail, fill=fill or pal["soft"])
    for a, b in zip(tail, tail[1:] + tail[:1]):
        d.line([a, b], fill=pal["ink"], width=7)
    gill = cx - L * 0.30                                             # 头长约两成，鳃盖靠前
    d.arc([gill - 46, cy - h / 2 + 4, gill + 46, cy + h / 2 - 4], 250, 110,
          fill=pal["ink"], width=8)
    disc(d, cx - L / 2 + 30, cy - h * 0.18, 10, pal["ink"], pal, w=2)
    return cx - L / 2, gill, cy - h * 0.30, h


@page("fish", 4)
def _(d, pal):
    """水从嘴进、从鳃出。出水箭头从鳃盖处斜向后上方，不从肚子底下穿出。"""
    cy = S / 2 + 30
    mouth, gill, gy, h = fish_body(d, S / 2 + 40, cy, 560, pal)
    arrow(d, mouth - 230, cy, mouth + 6, cy, pal, w=12, head=32)      # 进：一直画到嘴边
    arrow(d, gill + 10, gy, gill - 60, gy - 200, pal, w=12, head=32)  # 出：从鳃向后上方斜出
    return "1 条鱼 + 进水箭头（画到嘴边）+ 出水箭头（自鳃盖斜向上）"


@page("fish", 7)
def _(d, pal):
    """一直喝水、一直从鳃吐出去：一条粗路径贯穿头部，两端各一个箭头。"""
    cy = S / 2 + 30
    mouth, gill, gy, h = fish_body(d, S / 2 + 40, cy, 560, pal)
    pts = [(mouth - 210, cy), (mouth + 20, cy), (gill + 20, cy - h * 0.10), (gill - 10, gy)]
    d.line(pts, fill=pal["accent"], width=14, joint="curve")
    arrow(d, mouth - 210, cy, mouth - 120, cy, pal, w=12, head=30)
    arrow(d, gill - 10, gy, gill - 80, gy - 190, pal, w=12, head=30)
    return "1 条鱼 + 1 条贯穿头部的粗路径，进口在嘴、出口在鳃，两端各 1 个箭头"


@page("sound", 7)
def _(d, pal):
    """声音快，光更快得多 —— 两支箭头长短必须差出量级。"""
    x0 = MARGIN + 40
    for y, frac, col in ((S / 2 - 120, 0.22, pal["soft"]), (S / 2 + 120, 1.0, pal["accent"])):
        x1 = x0 + (S - 2 * MARGIN - 80) * frac
        d.line([x0, y, x1, y], fill=col, width=18)
        arrow(d, x1 - 40, y, x1, y, pal, w=14, head=38)
        disc(d, x0, y, 20, col, pal, w=6)
    return "上：声音，短箭头（22%）/ 下：光，长箭头（100%）"


@page("power", 9)
def _(d, pal):
    """电要走成一个圈：从插座出去、穿过台灯、再回插座。走向由箭头说清楚。"""
    cx, cy = S / 2, S / 2 + 30
    w_, h_ = 520, 340
    x0, x1, y0, y1 = cx - w_ / 2, cx + w_ / 2, cy - h_ / 2, cy + h_ / 2
    for seg in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)),
                ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
        d.line([seg[0], seg[1]], fill=pal["ink"], width=10)
    # 插座画成方块，台灯画成圆，各占回路一边
    d.rounded_rectangle([x0 - 58, cy - 62, x0 + 58, cy + 62], radius=14,
                        fill=pal["bark"], outline=pal["ink"], width=8)
    for dy in (-24, 24):
        d.line([x0 - 18, cy + dy, x0 + 18, cy + dy], fill=pal["ink"], width=8)
    disc(d, cx, y0, 56, pal["accent"], pal, w=8)
    for i, (ax, ay, bx, by) in enumerate((
            (cx - 120, y0, cx - 40, y0), (x1, cy - 80, x1, cy + 20),
            (cx + 120, y1, cx + 40, y1), (x0, cy + 120, x0, cy + 70))):
        arrow(d, ax, ay, bx, by, pal, w=9, head=24)
    return "1 个闭合回路 + 插座（方）+ 台灯（圆）+ 4 个同向箭头"


# ---------------------------------------------------------------- 只用已验证图元的一批
# （对比两格、正多边形、等分圆、长短箭头、计数栅格。生物剖面那类留到最后集中处理。）

@page("snow", 7)
def _(d, pal):
    """六片雪花，片片不同：枝杈数和长短由参数错开，六个角是共同点。"""
    rnd = random.Random(21)
    spots = [(S * 0.25, S * 0.28), (S * 0.5, S * 0.22), (S * 0.75, S * 0.28),
             (S * 0.25, S * 0.72), (S * 0.5, S * 0.78), (S * 0.75, S * 0.72)]
    for k, (cx, cy) in enumerate(spots):
        R = 118
        branches = 2 + k % 3                       # 每片枝杈数不同
        for i in range(6):                         # 永远六个角
            a = math.pi / 2 + i * math.pi / 3
            d.line([cx, cy, cx + R * math.cos(a), cy + R * math.sin(a)],
                   fill=pal["ink"], width=8)
            for j in range(branches):
                t = 0.35 + j * 0.22
                bx, by = cx + R * t * math.cos(a), cy + R * t * math.sin(a)
                ln = 40 - j * 8 + (k % 2) * 10
                for s in (+1, -1):
                    d.line([bx, by, bx + ln * math.cos(a + s * 1.0),
                            by + ln * math.sin(a + s * 1.0)], fill=pal["ink"], width=6)
    return "6 片雪花，每片 6 个角，枝杈数 2/3/4 各不相同"


@page("half", 3)
def _(d, pal):
    """从中间切 = 对，切歪了 = 错。两格必须一个打勾一个打叉。"""
    (lx, ly, lw, lh), (rx, ry, rw, rh) = panel2(d, pal)
    R = min(lw, lh) * 0.30
    # 左：正中切开，打勾
    disc(d, lx, ly - 40, R, pal["accent"], pal, w=9)
    d.line([lx, ly - 40 - R, lx, ly - 40 + R], fill=pal["ink"], width=10)
    for a, b in (((lx - 60, ly + 210), (lx - 16, ly + 254)), ((lx - 16, ly + 254), (lx + 66, ly + 168))):
        d.line([a, b], fill=pal["ink"], width=16)
    # 右：切偏了，打叉
    disc(d, rx, ry - 40, R, pal["accent"], pal, w=9)
    d.line([rx + R * 0.45, ry - 40 - R * 0.9, rx + R * 0.45, ry - 40 + R * 0.9],
           fill=pal["ink"], width=10)
    cross(d, rx, ry + 210, 56, pal, w=16)
    return "左格正中切开 + 勾 / 右格切偏 + 叉"


@page("half", 9)
def _(d, pal):
    """两个半圆合起来就是一个整圆。"""
    # 两个半圆要留出「还没合上」的缝，否则贴在一起就读成一个整圆或哑铃。
    # 上一版三个图元挤在右半张、中间还被短横连住，看着像哑铃。
    # 两个半圆必须「面对面紧挨着、只差一道缝」，让人一眼看出合起来正好是个圆。
    # 上一版把两个半圆拉得太开，中间那个又被箭头连到整圆上，读成了「一个半圆变整圆」。
    R, gap = 128, 26
    cy = S / 2
    # 左半圆凸面朝左，它的左边缘是 lx-R = pair_cx - gap/2 - 2R，
    # 所以这一对的中心至少要放在 MARGIN + 2R + gap/2 才不出界。
    pair_cx = MARGIN + 2 * R + gap / 2 + 24
    # pieslice(90,270) 画的是凸面朝左的那半块，它的平边正好落在圆心 x 上；
    # pieslice(270,90) 的平边也落在自己的圆心 x 上。所以两块「面对面只差一道缝」时，
    # 两个圆心只相隔 gap，而不是 2R —— 按 2R 摆会在中间空出整整一个半圆的宽度。
    lx = pair_cx - gap / 2                     # 左半圆（凸面朝左，平边在右）
    rx = pair_cx + gap / 2                     # 右半圆（平边在左，凸面朝右）
    d.pieslice([lx - R, cy - R, lx + R, cy + R], 90, 270,
               fill=pal["accent"], outline=pal["ink"], width=9)
    d.pieslice([rx - R, cy - R, rx + R, cy + R], 270, 90,
               fill=pal["soft"], outline=pal["ink"], width=9)
    wx = S - MARGIN - R - 40                   # 合拢后的整圆
    mid = (rx + R + wx - R) / 2
    arrow(d, mid - 56, cy, mid + 56, cy, pal, w=12, head=32)
    d.pieslice([wx - R, cy - R, wx + R, cy + R], 90, 270,
               fill=pal["accent"], outline=pal["ink"], width=9)
    d.pieslice([wx - R, cy - R, wx + R, cy + R], 270, 90,
               fill=pal["soft"], outline=pal["ink"], width=9)
    return "左边 2 个半圆面对面（只差一道缝）+ 1 个箭头 → 右边 1 个完整圆"


@page("count", 8)
def _(d, pal):
    """彩虹七色：七条，一条不多一条不少。"""
    bands = ["#c0392b", "#e67e22", "#f1c40f", "#27ae60", "#2980b9", "#4b3fa0", "#7d3c98"]
    cx, cy = S / 2, S * 0.82
    for i, col in enumerate(bands):
        R = 380 - i * 46
        d.arc([cx - R, cy - R, cx + R, cy + R], 180, 360, fill=col, width=40)
    return f"{len(bands)} 条彩虹色带（红橙黄绿蓝靛紫）"


@page("plus", 8)
def _(d, pal):
    """三根手指加两根手指：左手竖三根，右手竖两根。"""
    for cx, up in ((S * 0.28, 3), (S * 0.72, 2)):
        palm_y = S * 0.70
        d.rounded_rectangle([cx - 110, palm_y - 60, cx + 110, palm_y + 120], radius=40,
                            fill=pal["paper"], outline=pal["ink"], width=8)
        for i in range(5):
            x = cx - 80 + i * 40
            h = 200 if i < up else 46
            d.rounded_rectangle([x - 16, palm_y - 60 - h, x + 16, palm_y - 20], radius=16,
                                fill=pal["accent"] if i < up else pal["soft"],
                                outline=pal["ink"], width=6)
    d.line([S / 2 - 46, S * 0.55, S / 2 + 46, S * 0.55], fill=pal["ink"], width=14)
    d.line([S / 2, S * 0.55 - 46, S / 2, S * 0.55 + 46], fill=pal["ink"], width=14)
    return "左手 3 根竖起 + 右手 2 根竖起，中间一个加号"


# ---------------------------------------------------------------- car（安全：从哪一侧下车）

@page("car", 11)
def _(d, pal):
    """俯视：人行道在上、马路在下，只有靠人行道那一侧的后门开着。

    这页交给模型画了两轮，两轮都把四扇门全开、其中两扇正对着驶来的自行车 ——
    比原稿更危险。「哪一侧」是纯空间关系，模型讲不清，改由程序保证：
    车身是一个闭合矩形，只有上边缘开一块门板，自行车固定在下方马路上。
    """
    # 人行道（上）与马路（下）
    d.rectangle([0, 0, S, 250], fill=pal["soft"])
    d.rectangle([0, 250, S, 262], fill=pal["ink"])
    d.rectangle([0, 700, S, 712], fill=pal["ink"])
    d.rectangle([0, 712, S, S], fill=pal["bark"])
    for x in range(60, S, 150):                       # 马路中线
        d.rectangle([x, 880, x + 80, 894], fill=pal["paper"])

    # 车身：俯视轮廓。上一版是个圆角矩形加两个白方块，被读成手提箱 ——
    # 五岁孩子要先认出这是车，所以补上收窄的车头车尾、四个轮子、梯形风挡。
    cx, cy = S / 2, 470
    bw, bh = 660, 290
    for wx_ in (cx - bw * 0.30, cx + bw * 0.30):      # 四个轮子，露在车身外
        for wy in (cy - bh / 2 - 6, cy + bh / 2 + 6):
            d.rounded_rectangle([wx_ - 42, wy - 20, wx_ + 42, wy + 20], radius=12,
                                fill=pal["ink"])
    d.polygon([(cx - bw / 2, cy - bh / 2 + 54), (cx - bw / 2 + 76, cy - bh / 2),
               (cx + bw / 2 - 76, cy - bh / 2), (cx + bw / 2, cy - bh / 2 + 54),
               (cx + bw / 2, cy + bh / 2 - 54), (cx + bw / 2 - 76, cy + bh / 2),
               (cx - bw / 2 + 76, cy + bh / 2), (cx - bw / 2, cy + bh / 2 - 54)],
              fill=pal["accent"])
    pts = [(cx - bw / 2, cy - bh / 2 + 54), (cx - bw / 2 + 76, cy - bh / 2),
           (cx + bw / 2 - 76, cy - bh / 2), (cx + bw / 2, cy - bh / 2 + 54),
           (cx + bw / 2, cy + bh / 2 - 54), (cx + bw / 2 - 76, cy + bh / 2),
           (cx - bw / 2 + 76, cy + bh / 2), (cx - bw / 2, cy + bh / 2 - 54)]
    for a, b in zip(pts, pts[1:] + pts[:1]):
        d.line([a, b], fill=pal["ink"], width=9)
    for sx, sw in ((cx - bw * 0.30, 96), (cx + bw * 0.30, 96)):   # 前后风挡，梯形
        d.polygon([(sx - sw / 2, cy - bh / 2 + 30), (sx + sw / 2, cy - bh / 2 + 30),
                   (sx + sw / 2 - 16, cy + bh / 2 - 30), (sx - sw / 2 + 16, cy + bh / 2 - 30)],
                  fill=pal["paper"], outline=pal["ink"])
    # 唯一开着的门：靠人行道那一侧（上边缘）。门板用浅色并在车身上留出同宽的缺口，
    # 才看得出「这扇门开了」——上一版门板和车身同色，读成车顶上多了个盒子。
    door_x = cx + 30
    d.rectangle([door_x - 86, cy - bh / 2 - 4, door_x + 86, cy - bh / 2 + 16],
                fill=pal["ground"])                                   # 车身上的门洞
    # 门板沿车身上缘的一条边斜着翻出（梯形，靠车一端宽、外端窄），
    # 上一版是平移到车外的方块，读成车顶行李箱。
    hinge_x = door_x - 86
    d.polygon([(hinge_x, cy - bh / 2 + 8), (hinge_x + 172, cy - bh / 2 + 8),
               (hinge_x + 128, cy - bh / 2 - 104), (hinge_x + 18, cy - bh / 2 - 104)],
              fill=pal["paper"])
    pts = [(hinge_x, cy - bh / 2 + 8), (hinge_x + 172, cy - bh / 2 + 8),
           (hinge_x + 128, cy - bh / 2 - 104), (hinge_x + 18, cy - bh / 2 - 104)]
    for a, b in zip(pts, pts[1:] + pts[:1]):
        d.line([a, b], fill=pal["ink"], width=8)
    disc(d, hinge_x + 8, cy - bh / 2 + 6, 10, pal["ink"], pal, w=2)    # 铰链点

    # 自行车：下方马路上，在车尾后方
    bx, by = cx - 250, 840
    for off in (-58, 58):
        disc(d, bx + off, by, 46, None, pal, w=8)
    d.line([bx - 58, by, bx - 10, by - 60, bx + 58, by], fill=pal["ink"], width=8)
    d.line([bx - 10, by - 60, bx + 20, by - 62], fill=pal["ink"], width=8)
    return "1 辆车（车身闭合）+ 1 扇朝人行道开的门 + 1 辆在马路侧的自行车"


# ---------------------------------------------------------------- traffic（安全：走在斑马线上）

@page("traffic", 9)
def _(d, pal):
    """俯视：三个孩子都在斑马线上，两辆车停在停止线后，交警站在路边。

    这页交给模型画了两轮，两轮都把孩子塞进车道、斑马线空着，交警还站在线中央挡路。
    「谁在线上、车停在哪」是纯位置关系，改由程序保证。
    """
    # 这本调色板的 bark 是绿色，上一版拿它铺马路，路面成了草地；改用中性灰。
    ROAD = "#6f7378"
    d.rectangle([0, 0, S, 190], fill=pal["soft"])          # 上方人行道
    d.rectangle([0, 190, S, 834], fill=ROAD)               # 马路
    d.rectangle([0, 834, S, S], fill=pal["soft"])          # 下方人行道

    zx, zw = 250, 300                                      # 斑马线带，往左挪出车位
    for i in range(7):
        y = 210 + i * 88
        d.rectangle([zx, y, zx + zw, y + 54], fill=pal["paper"])

    # 停止线：与斑马线垂直（竖着的一道），画在两辆车的前方
    stop_x = zx + zw + 70
    d.rectangle([stop_x, 210, stop_x + 16, 814], fill=pal["paper"])
    for k, (bx, by) in enumerate(((stop_x + 60, 300), (stop_x + 60, 560))):
        d.rounded_rectangle([bx, by, bx + 230, by + 130], radius=28,
                            fill=pal["accent"] if k == 0 else pal["ink"],
                            outline=pal["ink"], width=7)

    for i, cy_ in enumerate((330, 500, 670)):              # 三个孩子，全在斑马线上
        cxk = zx + zw / 2 + (i - 1) * 78
        disc(d, cxk, cy_, 30, pal["accent"], pal, w=7)
        d.rounded_rectangle([cxk - 26, cy_ + 30, cxk + 26, cy_ + 104], radius=18,
                            fill=pal["soft"], outline=pal["ink"], width=6)

    gx = zx - 130                                          # 交警站在路边，不挡斑马线
    disc(d, gx, 520, 32, pal["paper"], pal, w=7)
    d.rounded_rectangle([gx - 28, 552, gx + 28, 640], radius=18,
                        fill=pal["paper"], outline=pal["ink"], width=6)
    d.line([gx, 560, gx, 470], fill=pal["ink"], width=8)
    ngon(d, gx, 442, 44, 8, pal, fill=pal["accent"], w=6)  # 八角停牌
    return "3 个孩子全在斑马线上 + 2 辆车停在停止线后 + 1 个交警在路边"


# ---------------------------------------------------------------- ice / snow / sound / bee（下一批）

@page("ice", 8)
def _(d, pal):
    """水珠挂在杯子外面，不是杯里的水漏出来 —— 珠子必须全在杯壁之外。"""
    cx, cy = S / 2, S / 2 + 30
    gw, gh = 300, 420
    d.rounded_rectangle([cx - gw / 2, cy - gh / 2, cx + gw / 2, cy + gh / 2], radius=26,
                        fill=pal["paper"], outline=pal["ink"], width=10)
    d.rectangle([cx - gw / 2 + 14, cy - 60, cx + gw / 2 - 14, cy + gh / 2 - 14],
                fill=pal["soft"])                                  # 杯里的水
    d.line([cx - gw / 2 + 14, cy - 60, cx + gw / 2 - 14, cy - 60], fill=pal["ink"], width=6)
    rnd = random.Random(9)
    for _ in range(18):                                            # 水珠：全部贴在杯壁外侧
        side = rnd.choice((-1, 1))
        x = cx + side * (gw / 2 + rnd.uniform(14, 44))
        y = cy + rnd.uniform(-gh / 2 + 40, gh / 2 - 30)
        disc(d, x, y, rnd.uniform(11, 19), pal["soft"], pal, w=4)
    return "1 个杯子 + 18 颗水珠，全在杯壁外侧"


@page("ice", 9)
def _(d, pal):
    """冰化要吸热：箭头一律从周围指向冰块。"""
    cx, cy = S / 2, S / 2 + 20
    gw, gh = 320, 400
    d.rounded_rectangle([cx - gw / 2, cy - gh / 2, cx + gw / 2, cy + gh / 2], radius=26,
                        fill=pal["paper"], outline=pal["ink"], width=10)
    d.rectangle([cx - gw / 2 + 14, cy - 110, cx + gw / 2 - 14, cy + gh / 2 - 14],
                fill=pal["soft"])
    # 冰块要泡在水里（水面在 cy-110），上一版画在 cy-190 骑上了杯口。
    icy = cy + 20
    d.rounded_rectangle([cx - 74, icy - 70, cx + 74, icy + 70], radius=16,
                        fill=pal["paper"], outline=pal["ink"], width=8)
    for a in range(8):                                             # 八支箭头，起点都在杯外
        ang = a * math.pi / 4
        r0, r1 = 330, 190
        arrow(d, cx + r0 * math.cos(ang), icy + r0 * math.sin(ang) * 0.70,
              cx + r1 * math.cos(ang), icy + r1 * math.sin(ang) * 0.70,
              pal, w=8, head=22)
    return "1 块泡在水里的冰 + 8 支箭头，全部由杯外指向冰"


@page("snow", 3)
def _(d, pal):
    """一粒灰尘上冻出一颗小冰晶 —— 六个角，但很小，还没长成雪花。"""
    cx, cy = S / 2, S / 2
    disc(d, cx, cy, 16, pal["accent"], pal, w=5)                   # 中心那粒灰尘
    for i in range(6):
        a = math.pi / 2 + i * math.pi / 3
        d.line([cx, cy, cx + 90 * math.cos(a), cy + 90 * math.sin(a)],
               fill=pal["ink"], width=9)
    d.ellipse([cx - 200, cy - 200, cx + 200, cy + 200], outline=pal["soft"], width=5)
    return "1 粒灰尘 + 6 根短枝（还没长成完整雪花）"


@page("sound", 10)
def _(d, pal):
    """太空里没有空气，所以没有声音：一个火箭，周围什么波纹都没有。"""
    # 这本是浅色调色板，上一版直接用它当底，「太空」完全没出来，火箭还像座小房子。
    SPACE = "#151a2c"
    d.rectangle([0, 0, S, S], fill=SPACE)
    rnd = random.Random(4)
    for _ in range(90):
        r = rnd.choice((2, 2, 3, 4))
        x, y = rnd.uniform(20, S - 20), rnd.uniform(20, S - 20)
        d.ellipse([x - r, y - r, x + r, y + r], fill=pal["paper"])
    cx, cy = S / 2, S / 2 + 30
    d.polygon([(cx, cy - 250), (cx - 52, cy - 90), (cx + 52, cy - 90)], fill=pal["accent"])
    d.rounded_rectangle([cx - 52, cy - 90, cx + 52, cy + 150], radius=16,
                        fill=pal["paper"], outline=pal["ink"], width=7)
    for s in (-1, 1):                                              # 两片尾翼，细长火箭
        d.polygon([(cx + s * 52, cy + 60), (cx + s * 122, cy + 160),
                   (cx + s * 52, cy + 150)], fill=pal["accent"])
    disc(d, cx, cy - 10, 30, pal["soft"], pal, w=6)
    return "深色太空底 + 1 枚带尾翼的火箭 + 90 颗星，周围没有任何波纹"


@page("bee", 11)
def _(d, pal):
    """一只工蜂一辈子只做一小勺的十二分之一：勺子分十二格，只填一格。"""
    # 上一版圆盘大、柄细长，读成了棒棒糖。勺子要「盘小柄粗、柄从盘边平滑伸出」。
    cx, cy = S / 2, S / 2 - 40
    R = 140
    d.rounded_rectangle([cx - 44, cy + R - 40, cx + 44, cy + R + 250], radius=44,
                        fill=pal["paper"], outline=pal["ink"], width=8)   # 粗勺柄，先画在盘下
    for i in range(12):
        a0, a1 = i * 30 - 90, (i + 1) * 30 - 90
        d.pieslice([cx - R, cy - R, cx + R, cy + R], a0, a1,
                   fill=pal["accent"] if i == 0 else pal["paper"],
                   outline=pal["ink"], width=5)
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=pal["ink"], width=9)
    return "1 个分成 12 格的勺子（盘小柄粗），只有 1 格是满的"


# ---------------------------------------------------------------- 第五批新书：camo / post / doctor / share

@page("camo", 3)
def _(d, pal):
    """条纹配条纹，斑点配斑点，远看就糊成一片。"""
    for (cx, cy, w_, h_), stripes in zip(panel2(d, pal), (True, False)):
        rnd = random.Random(31 if stripes else 32)
        if stripes:
            for i in range(14):
                x = cx - w_ / 2 + w_ * (i + 0.5) / 14
                d.line([x, cy - h_ / 2 + 10, x, cy + h_ / 2 - 10], fill=pal["soft"], width=22)
            for i in range(6):
                x = cx - w_ * 0.22 + w_ * 0.44 * i / 5
                d.line([x, cy - 150, x, cy + 150], fill=pal["ink"], width=20)
        else:
            for _ in range(40):
                gx = cx + rnd.uniform(-w_ / 2 + 30, w_ / 2 - 30)
                gy = cy + rnd.uniform(-h_ / 2 + 30, h_ / 2 - 30)
                disc(d, gx, gy, 26, pal["soft"], pal, w=3)
            for _ in range(12):
                gx = cx + rnd.uniform(-w_ * 0.24, w_ * 0.24)
                gy = cy + rnd.uniform(-150, 150)
                disc(d, gx, gy, 24, pal["ink"], pal, w=3)
    return "左格：14 条背景竖纹 + 6 条动物竖纹 / 右格：40 个背景斑点 + 12 个动物斑点"


@page("camo", 4)
def _(d, pal):
    """色素袋张开或收拢，颜色就变了。"""
    for (cx, cy, w_, h_), spread in zip(panel2(d, pal), (False, True)):
        cols, rows = 5, 5
        for i in range(cols):
            for j in range(rows):
                gx = cx - w_ * 0.30 + w_ * 0.60 * i / (cols - 1)
                gy = cy - h_ * 0.30 + h_ * 0.60 * j / (rows - 1)
                disc(d, gx, gy, 46 if spread else 16, pal["accent"], pal, w=5)
    return "左格 25 个收拢的小色素袋 / 右格 25 个张开的大色素袋"


@page("camo", 6)
def _(d, pal):
    """同一只动物，三种花样等于三句话。"""
    xs, slot = lay(3)
    cy = S / 2
    rnd = random.Random(9)
    for k, cx in enumerate(xs):
        body = [(cx - 130, cy + 90), (cx - 90, cy - 70), (cx + 90, cy - 70), (cx + 130, cy + 90)]
        fill = (pal["ink"], pal["accent"], pal["paper"])[k]
        d.polygon(body, fill=fill)
        for a, b in zip(body, body[1:] + body[:1]):
            d.line([a, b], fill=pal["ink"], width=8)
        if k == 2:
            for _ in range(9):
                gx = cx + rnd.uniform(-90, 90)
                gy = cy + rnd.uniform(-50, 60)
                disc(d, gx, gy, 20, pal["accent"], pal, w=4)
    return "3 个相同轮廓：全深 / 全鲜艳 / 带 9 块斑，三种「说法」"


@page("camo", 8)
def _(d, pal):
    """没毒的长得像有毒的，鸟就不敢碰。"""
    for (cx, cy, w_, h_), warn in zip(panel2(d, pal), (True, False)):
        for s in (-1, 1):
            wing = [(cx, cy), (cx + s * 190, cy - 150), (cx + s * 210, cy + 40), (cx, cy + 90)]
            d.polygon(wing, fill=pal["accent"])
            for a, b in zip(wing, wing[1:] + wing[:1]):
                d.line([a, b], fill=pal["ink"], width=7)
            for k in range(3):
                disc(d, cx + s * (70 + k * 55), cy - 60 + k * 40, 18, pal["paper"], pal, w=4)
        d.rounded_rectangle([cx - 18, cy - 60, cx + 18, cy + 110], radius=14,
                            fill=pal["ink"])
        if warn:
            tri = [(cx, cy - 260), (cx - 60, cy - 160), (cx + 60, cy - 160)]
            d.polygon(tri, fill=pal["accent"])
            for a, b in zip(tri, tri[1:] + tri[:1]):
                d.line([a, b], fill=pal["ink"], width=7)
    return "两只花纹完全相同的蝴蝶，左边多 1 个警告三角（有毒）"


@page("camo", 10)
def _(d, pal):
    """结构色磨碎就没了。"""
    for (cx, cy, w_, h_), whole in zip(panel2(d, pal), (True, False)):
        if whole:
            quill = [(cx, cy - h_ * 0.34), (cx, cy + h_ * 0.34)]
            d.line(quill, fill=pal["ink"], width=12)
            for i in range(16):
                t = i / 15
                y = cy - h_ * 0.32 + h_ * 0.62 * t
                span = 150 * math.sin(math.pi * t) + 30
                for s in (-1, 1):
                    d.line([cx, y, cx + s * span, y - 26], fill=pal["accent"], width=6)
        else:
            rnd = random.Random(17)
            for _ in range(80):
                gx = cx + rnd.uniform(-w_ * 0.26, w_ * 0.26)
                gy = cy + rnd.uniform(-60, 120)
                disc(d, gx, gy, 7, pal["soft"], pal, w=1)
    return "左格：1 根完整羽毛（32 条细纹）/ 右格：80 粒磨碎的粉末"


@page("post", 2)
def _(d, pal):
    """信封上三块地方：邮票、寄信人、收信人。"""
    cx, cy = S / 2, S / 2
    w_, h_ = S - 2 * MARGIN - 80, 520
    d.rounded_rectangle([cx - w_ / 2, cy - h_ / 2, cx + w_ / 2, cy + h_ / 2], radius=16,
                        fill=pal["paper"], outline=pal["ink"], width=9)
    d.rounded_rectangle([cx + w_ / 2 - 170, cy - h_ / 2 + 30, cx + w_ / 2 - 40, cy - h_ / 2 + 160],
                        radius=8, fill=pal["accent"], outline=pal["ink"], width=7)
    for i in range(2):
        d.line([cx - w_ / 2 + 50, cy - h_ / 2 + 60 + i * 40,
                cx - w_ / 2 + 260, cy - h_ / 2 + 60 + i * 40], fill=pal["soft"], width=12)
    for i in range(3):
        d.line([cx - 140, cy + 30 + i * 48, cx + 260, cy + 30 + i * 48],
               fill=pal["ink"], width=14)
    return "1 个信封 + 右上邮票 + 左上 2 行寄信人 + 中间 3 行收信人"


@page("post", 3)
def _(d, pal):
    """地址从大写到小：城市、街道、门牌。"""
    cx, cy = S / 2, S / 2
    for i, frac in enumerate((1.0, 0.66, 0.34)):
        w_ = (S - 2 * MARGIN) * frac
        h_ = 460 * frac
        d.rounded_rectangle([cx - w_ / 2, cy - h_ / 2, cx + w_ / 2, cy + h_ / 2], radius=18,
                            fill=pal["paper"] if i else pal["ground"],
                            outline=pal["ink"], width=9)
    return "3 个逐层缩小的嵌套方框：城市 / 街道 / 门牌"


@page("post", 5)
def _(d, pal):
    """分拣中心按方向分成几堆。"""
    cx, cy = MARGIN + 220, S / 2
    d.rounded_rectangle([cx - 140, cy - 150, cx + 140, cy + 150], radius=22,
                        fill=pal["soft"], outline=pal["ink"], width=9)
    for k, dy in enumerate((-210, -70, 70, 210)):
        arrow(d, cx + 160, cy, S - MARGIN - 220, cy + dy, pal, w=10, head=26)
        d.rounded_rectangle([S - MARGIN - 200, cy + dy - 50, S - MARGIN - 40, cy + dy + 50],
                            radius=14, fill=pal["paper"], outline=pal["ink"], width=7)
    return "1 个分拣中心 + 4 支箭头 + 4 堆信"


@page("post", 8)
def _(d, pal):
    """一层层分下去，最后落到一户人家。"""
    cx, cy = S / 2, S / 2
    steps = ((S - 2 * MARGIN, 420), (620, 300), (340, 180), (150, 90))
    for i, (w_, h_) in enumerate(steps):
        d.rounded_rectangle([cx - w_ / 2, cy - h_ / 2, cx + w_ / 2, cy + h_ / 2], radius=16,
                            fill=pal["accent"] if i == len(steps) - 1 else pal["paper"],
                            outline=pal["ink"], width=8)
    return "4 层逐步缩小的区域，最里一层填成强调色（那一户）"


@page("post", 10)
def _(d, pal):
    """信箱上的小红旗竖起来，表示有信要寄。"""
    cx = S / 2
    base = S - MARGIN - 120
    d.rounded_rectangle([cx - 30, base - 360, cx + 30, base], radius=12,
                        fill=pal["soft"], outline=pal["ink"], width=8)
    d.pieslice([cx - 170, base - 520, cx + 170, base - 280], 180, 360,
               fill=pal["paper"], outline=pal["ink"], width=9)
    d.rectangle([cx - 170, base - 400, cx + 170, base - 340], fill=pal["paper"],
                outline=pal["ink"], width=9)
    d.line([cx + 180, base - 300, cx + 180, base - 480], fill=pal["ink"], width=10)
    flag = [(cx + 186, base - 480), (cx + 300, base - 450), (cx + 186, base - 420)]
    d.polygon(flag, fill=pal["accent"])
    for a, b in zip(flag, flag[1:] + flag[:1]):
        d.line([a, b], fill=pal["ink"], width=6)
    return "1 个路边信箱 + 1 面竖起来的小红旗"


@page("doctor", 4)
def _(d, pal):
    """听诊器：圆片、管子、两个耳塞。"""
    cx = S / 2
    disc(d, cx, S - MARGIN - 200, 110, pal["soft"], pal, w=10)
    disc(d, cx, S - MARGIN - 200, 66, pal["paper"], pal, w=7)
    d.line([cx, S - MARGIN - 310, cx, S / 2 - 60], fill=pal["ink"], width=14)
    for s in (-1, 1):
        pts = [(cx, S / 2 - 60), (cx + s * 120, S / 2 - 200), (cx + s * 150, MARGIN + 170)]
        d.line(pts, fill=pal["ink"], width=14, joint="curve")
        disc(d, cx + s * 150, MARGIN + 150, 34, pal["accent"], pal, w=7)
    return "1 个听诊器：1 个圆片 + 1 条管子 + 2 个耳塞"


@page("doctor", 6)
def _(d, pal):
    """张大嘴说「啊」，舌头压下去才看得见后面。"""
    cx, cy = S / 2, S / 2 + 20
    d.ellipse([cx - 300, cy - 220, cx + 300, cy + 220], fill=pal["accent"],
              outline=pal["ink"], width=10)
    d.pieslice([cx - 230, cy - 40, cx + 230, cy + 260], 180, 360,
               fill=pal["soft"], outline=pal["ink"], width=8)
    d.ellipse([cx - 90, cy - 150, cx + 90, cy - 40], fill=pal["paper"],
              outline=pal["ink"], width=7)
    arrow(d, cx + 330, cy - 260, cx + 110, cy - 120, pal, w=10, head=26)
    return "1 张张开的嘴 + 压低的舌头 + 后方 1 个亮区 + 1 支光束箭头"


@page("doctor", 8)
def _(d, pal):
    """疫苗先让身体认识病菌。"""
    for (cx, cy, w_, h_), armed in zip(panel2(d, pal), (False, True)):
        shield = [(cx, cy - 170), (cx + 140, cy - 90), (cx + 110, cy + 140),
                  (cx, cy + 190), (cx - 110, cy + 140), (cx - 140, cy - 90)]
        d.polygon(shield, fill=pal["paper"])
        for a, b in zip(shield, shield[1:] + shield[:1]):
            d.line([a, b], fill=pal["ink"], width=8)
        if armed:
            rnd = random.Random(23)
            for _ in range(6):
                a = rnd.uniform(0, 2 * math.pi)
                gx, gy = cx + 250 * math.cos(a), cy + 250 * math.sin(a)
                disc(d, gx, gy, 26, pal["accent"], pal, w=5)
                arrow(d, gx, gy, cx + 330 * math.cos(a), cy + 330 * math.sin(a),
                      pal, w=7, head=20)
    return "左格：1 面盾牌 / 右格：同样的盾牌 + 6 个被弹开的病菌"


@page("doctor", 10)
def _(d, pal):
    """可以先问一句：这个会不会疼？"""
    cx, cy = S / 2, S / 2
    small = [(cx - 330, cy - 150), (cx - 60, cy - 150), (cx - 60, cy + 20),
             (cx - 130, cy + 20), (cx - 170, cy + 90), (cx - 180, cy + 20),
             (cx - 330, cy + 20)]
    big = [(cx + 40, cy - 60), (cx + 340, cy - 60), (cx + 340, cy + 190),
           (cx + 180, cy + 190), (cx + 130, cy + 260), (cx + 120, cy + 190),
           (cx + 40, cy + 190)]
    for pts, fill in ((small, pal["paper"]), (big, pal["accent"])):
        d.polygon(pts, fill=fill)
        for a, b in zip(pts, pts[1:] + pts[:1]):
            d.line([a, b], fill=pal["ink"], width=8)
    return "2 个对话框：左边小的（孩子问）/ 右边大的（医生答）"


def share_box(d, pal, cx, cy, half_w, half_h, n, cols=1):
    """一个装 n 个圆的框。圆的半径由框宽反推，保证不压在框线上。

    share 整本 10 页都用这个版式，所以半径必须由框反推 —— 写死半径会让圆
    穿出盒子（p7 第一版就是这样）。
    """
    d.rounded_rectangle([cx - half_w, cy - half_h, cx + half_w, cy + half_h],
                        radius=20, fill=pal["paper"], outline=pal["ink"], width=8)
    rows = math.ceil(n / cols)
    r = min(half_w / cols, half_h / rows) * 0.72
    # 列距和行距都要再收一点，否则圆心正好落在半宽/半高处、圆会贴着框壁
    # （p7 两列时两个圆几乎顶到左右边线）。0.78 留出一圈明显的内边距。
    pitch_x = 2 * half_w / cols * 0.78
    pitch_y = 2 * half_h / rows * 0.78
    for i in range(n):
        col, row = i % cols, i // cols
        x = cx + (col - (cols - 1) / 2) * pitch_x
        y = cy + (row - (rows - 1) / 2) * pitch_y
        disc(d, x, y, r, pal["accent"], pal, w=7)
    return r


@page("share", 2)
def _(d, pal):
    """六块分给三个人，每人两块。"""
    xs, slot = lay(3)
    for cx in xs:
        share_box(d, pal, cx, S / 2, slot * 0.36, 150, 2, cols=2)
    return "3 个框，每框 2 个圆（共 6 个）"


@page("share", 3)
def _(d, pal):
    """一个一个发，发两轮。"""
    xs, slot = lay(3)
    for row, cy in enumerate((S / 2 - 160, S / 2 + 160)):
        for cx in xs:
            disc(d, cx, cy, 58, pal["accent"], pal, w=8)
            arrow(d, cx, cy - 110 if row == 0 else cy - 110, cx, cy - 64, pal, w=8, head=22)
    return "2 轮 ×3 个圆，每个圆上方 1 支发放箭头"


@page("share", 4)
def _(d, pal):
    """六除以三等于二。"""
    for i, cx in enumerate([MARGIN + 90 + i * 96 for i in range(6)]):
        disc(d, cx, S / 2 - 180, 42, pal["accent"], pal, w=7)
    xs, slot = lay(3)
    for cx in xs:
        share_box(d, pal, cx, S / 2 + 180, slot * 0.32, 120, 2, cols=2)
    return "上排 6 个圆 → 下排 3 个框各 2 个圆"


@page("share", 5)
def _(d, pal):
    """六个人分六块，每人一块。"""
    xs, slot = lay(6)
    for cx in xs:
        share_box(d, pal, cx, S / 2, slot * 0.38, 120, 1, cols=1)
    return "6 个框，每框 1 个圆"


@page("share", 6)
def _(d, pal):
    """两个人分六块，每人三块。"""
    xs, slot = lay(2)
    for cx in xs:
        share_box(d, pal, cx, S / 2, slot * 0.34, 220, 3, cols=1)
    return "2 个框，每框 3 个圆"


@page("share", 7)
def _(d, pal):
    """七块分给三个人，还剩一块。"""
    xs, slot = lay(3)
    for cx in xs:
        share_box(d, pal, cx, S / 2 - 60, slot * 0.34, 140, 2, cols=2)
    disc(d, S / 2, S - MARGIN - 160, 62, pal["soft"], pal, w=9)
    return "3 个框各 2 个圆 + 框外单独 1 个圆（余数）"


@page("share", 8)
def _(d, pal):
    """剩下那块切成三份。"""
    cx, cy, R = S / 2, S / 2, 280
    for i in range(3):
        a0 = i * 120 - 90
        d.pieslice([cx - R, cy - R, cx + R, cy + R], a0, a0 + 120,
                   fill=pal["accent"] if i == 0 else pal["paper"],
                   outline=pal["ink"], width=9)
    return "1 个圆分成 3 块等大扇形（各 120 度）"


@page("share", 9)
def _(d, pal):
    """绳子从正中剪，水倒到一样高。"""
    x0, x1 = MARGIN + 60, S - MARGIN - 60
    y = S / 2 - 200
    d.rounded_rectangle([x0, y - 30, x1, y + 30], radius=16, fill=pal["accent"],
                        outline=pal["ink"], width=8)
    d.line([(x0 + x1) / 2, y - 80, (x0 + x1) / 2, y + 80], fill=pal["ink"], width=12)
    for cx in (S / 2 - 200, S / 2 + 200):
        d.rounded_rectangle([cx - 90, S / 2 + 40, cx + 90, S / 2 + 320], radius=18,
                            fill=pal["paper"], outline=pal["ink"], width=8)
        d.rectangle([cx - 76, S / 2 + 150, cx + 76, S / 2 + 306], fill=pal["soft"])
    return "1 根绳子 + 正中 1 道剪线 + 2 个水位相同的杯子"


@page("share", 10)
def _(d, pal):
    """一个玩具轮流玩，时间也能平分。"""
    cx, cy, R = S / 2, S / 2, 290
    d.pieslice([cx - R, cy - R, cx + R, cy + R], -90, 90, fill=pal["accent"],
               outline=pal["ink"], width=9)
    d.pieslice([cx - R, cy - R, cx + R, cy + R], 90, 270, fill=pal["paper"],
               outline=pal["ink"], width=9)
    return "1 个圆分成 2 个等大半圆，一深一浅"


@page("share", 11)
def _(d, pal):
    """一个人分，另一个人先挑。"""
    xs, slot = lay(2)
    cy = S / 2 + 40
    for cx in xs:
        share_box(d, pal, cx, cy, slot * 0.32, 180, 3, cols=1)
    d.rounded_rectangle([xs[0] - 40, MARGIN + 60, xs[0] + 40, MARGIN + 200], radius=18,
                        fill=pal["soft"], outline=pal["ink"], width=7)
    arrow(d, xs[1], MARGIN + 90, xs[1], cy - 180, pal, w=11, head=28)
    return "2 个各 3 个圆的框 + 左边 1 只分的手 + 右边 1 支挑的箭头"


# ---------------------------------------------------------------- 第五批新书：rock / paper / plastic / sleepwin

def layer_stack(d, pal, cx, cy, w, n=8, h=52, shades=None):
    """一摞水平地层，从上到下颜色略有差别。返回每层的中心 y。"""
    shades = shades or [pal["paper"], pal["soft"], pal["bark"], pal["line"]]
    ys = []
    for i in range(n):
        y = cy - n * h / 2 + i * h
        d.rectangle([cx - w / 2, y, cx + w / 2, y + h],
                    fill=shades[i % len(shades)], outline=pal["ink"], width=5)
        ys.append(y + h / 2)
    return ys


@page("rock", 3)
def _(d, pal):
    """泥沙一层一层铺上去，压成石头。"""
    layer_stack(d, pal, S / 2, S / 2, S - 2 * MARGIN - 80, n=8, h=64)
    return "8 层水平地层，颜色依次交替"


@page("rock", 4)
def _(d, pal):
    """越下面的越老，越上面的越新。"""
    w = S - 2 * MARGIN - 220
    ys = layer_stack(d, pal, S / 2 - 60, S / 2, w, n=8, h=60)
    x = S / 2 - 60 + w / 2 + 70
    arrow(d, x, ys[0] - 40, x, ys[-1] + 40, pal, w=12, head=30)
    d.rectangle([S / 2 - 60 - w / 2, ys[-1] - 30, S / 2 - 60 + w / 2, ys[-1] + 30],
                outline=pal["accent"], width=10)
    return "8 层地层 + 1 支自上而下的箭头 + 最下一层加粗描边（最老）"


@page("rock", 5)
def _(d, pal):
    """地壳一挤，平平的层就被折成弯的。"""
    cx, cy = S / 2, S / 2 + 40
    w = S - 2 * MARGIN - 200
    for i in range(6):
        pts = []
        for k in range(41):
            t = k / 40
            x = cx - w / 2 + t * w
            y = cy - 150 + i * 56 - 130 * math.sin(math.pi * t)
            pts.append((x, y))
        d.line(pts, fill=pal["ink"] if i % 2 else pal["accent"], width=18, joint="curve")
    arrow(d, MARGIN, cy, MARGIN + 150, cy, pal, w=12, head=30)
    arrow(d, S - MARGIN, cy, S - MARGIN - 150, cy, pal, w=12, head=30)
    return "6 条拱起的地层 + 左右各 1 支向内挤压的箭头"


@page("rock", 7)
def _(d, pal):
    """不同深度的层里，埋着不同的化石。"""
    w = S - 2 * MARGIN - 120
    ys = layer_stack(d, pal, S / 2, S / 2, w, n=7, h=68)
    d.ellipse([S / 2 - 190, ys[1] - 26, S / 2 - 130, ys[1] + 26], fill=pal["accent"],
              outline=pal["ink"], width=5)
    d.polygon([(S / 2 + 30, ys[3] - 28), (S / 2 + 90, ys[3]), (S / 2 + 30, ys[3] + 28)],
              fill=pal["accent"])
    d.rounded_rectangle([S / 2 - 60, ys[5] - 16, S / 2 + 60, ys[5] + 16], radius=14,
                        fill=pal["accent"], outline=pal["ink"], width=5)
    return "7 层地层 + 3 个化石分别埋在第 2、4、6 层"


@page("rock", 9)
def _(d, pal):
    """碎成沙，被带走，又压成新的石头。"""
    cx, cy, R = S / 2, S / 2, 270
    for i in range(3):
        a0 = i * 120 - 80
        d.arc([cx - R, cy - R, cx + R, cy + R], a0, a0 + 78, fill=pal["accent"], width=16)
        a_end, a_pre = math.radians(a0 + 78), math.radians(a0 + 64)
        arrow(d, cx + R * math.cos(a_pre), cy + R * math.sin(a_pre),
              cx + R * math.cos(a_end), cy + R * math.sin(a_end), pal, w=10, head=26)
    spots = [(cx, cy - R), (cx + R * 0.87, cy + R * 0.5), (cx - R * 0.87, cy + R * 0.5)]
    disc(d, spots[0][0], spots[0][1], 62, pal["bark"], pal, w=8)
    rnd = random.Random(2)
    for _ in range(30):
        # 先定中心再加半径。上一版对左上角和右下角各自独立取随机数，
        # 常常算出 x1 < x0，PIL 直接抛 ValueError。
        gx = spots[1][0] + rnd.uniform(-60, 60)
        gy = spots[1][1] + rnd.uniform(-40, 40)
        d.ellipse([gx - 6, gy - 6, gx + 6, gy + 6], fill=pal["bark"])
    layer_stack(d, pal, spots[2][0], spots[2][1], 150, n=4, h=26)
    return "1 个三段循环 + 巨石 / 沙粒 / 新地层 三个符号"


@page("paper", 3)
def _(d, pal):
    """木屑加水，搅成纸浆。"""
    for (cx, cy, w_, h_), pulp in zip(panel2(d, pal), (False, True)):
        d.pieslice([cx - w_ * 0.30, cy - 60, cx + w_ * 0.30, cy + 240], 0, 180,
                   fill=pal["paper"], outline=pal["ink"], width=9)
        if pulp:
            d.pieslice([cx - w_ * 0.25, cy + 10, cx + w_ * 0.25, cy + 190], 0, 180,
                       fill=pal["soft"])
        else:
            rnd = random.Random(6)
            for _ in range(26):
                x = cx + rnd.uniform(-w_ * 0.22, w_ * 0.22)
                y = cy + rnd.uniform(20, 170)
                d.rectangle([x - 14, y - 10, x + 14, y + 10], fill=pal["bark"],
                            outline=pal["ink"], width=3)
    return "左格：26 块木屑 / 右格：一碗纸浆"


@page("paper", 4)
def _(d, pal):
    """纸浆倒在细网上，水从网眼漏下去。"""
    cy = S / 2 - 40
    x0, x1 = MARGIN + 60, S - MARGIN - 60
    d.rectangle([x0, cy, x1, cy + 26], fill=pal["soft"], outline=pal["ink"], width=7)
    for x in range(int(x0) + 30, int(x1) - 20, 46):     # 网眼
        d.line([x, cy, x, cy + 26], fill=pal["ink"], width=5)
    d.rectangle([x0 + 20, cy - 40, x1 - 20, cy], fill=pal["paper"],
                outline=pal["ink"], width=6)
    for i, x in enumerate(range(int(x0) + 60, int(x1) - 40, 120)):
        d.ellipse([x - 14, cy + 80 + (i % 2) * 50, x + 14, cy + 120 + (i % 2) * 50],
                  fill=pal["soft"], outline=pal["ink"], width=4)
    return "1 张细网 + 网上 1 层纸浆 + 网下若干滴落的水"


@page("paper", 5)
def _(d, pal):
    """压干、烘干，就是一张纸。"""
    xs, slot = lay(3)
    cy = S / 2
    d.rounded_rectangle([xs[0] - 130, cy - 50, xs[0] + 130, cy + 50], radius=16,
                        fill=pal["soft"], outline=pal["ink"], width=8)
    d.rounded_rectangle([xs[1] - 130, cy - 30, xs[1] + 130, cy + 30], radius=12,
                        fill=pal["soft"], outline=pal["ink"], width=8)
    disc(d, xs[1], cy - 110, 76, pal["bark"], pal, w=8)
    d.rounded_rectangle([xs[2] - 130, cy - 16, xs[2] + 130, cy + 16], radius=8,
                        fill=pal["paper"], outline=pal["ink"], width=8)
    return "3 个阶段：湿层 → 滚筒压 → 干燥的薄纸"


@page("paper", 7)
def _(d, pal):
    """旧纸泡开，重新做成新纸。"""
    cx, cy, R = S / 2, S / 2, 260
    for i in range(3):
        a0 = i * 120 - 80
        d.arc([cx - R, cy - R, cx + R, cy + R], a0, a0 + 78, fill=pal["accent"], width=16)
        a_end, a_pre = math.radians(a0 + 78), math.radians(a0 + 64)
        arrow(d, cx + R * math.cos(a_pre), cy + R * math.sin(a_pre),
              cx + R * math.cos(a_end), cy + R * math.sin(a_end), pal, w=10, head=26)
    spots = [(cx, cy - R), (cx + R * 0.87, cy + R * 0.5), (cx - R * 0.87, cy + R * 0.5)]
    for k, (sx, sy) in enumerate(spots):
        if k == 1:
            d.pieslice([sx - 70, sy - 50, sx + 70, sy + 90], 0, 180, fill=pal["soft"],
                       outline=pal["ink"], width=7)
        else:
            d.rounded_rectangle([sx - 60, sy - 76, sx + 60, sy + 76], radius=10,
                                fill=pal["paper"], outline=pal["ink"], width=7)
    return "1 个三段循环 + 旧纸 / 纸浆 / 新纸 三个符号"


@page("paper", 10)
def _(d, pal):
    """砍一棵，补种一棵。"""
    for row, cy in enumerate((S / 2 - 180, S / 2 + 180)):
        xs, slot = lay(5)
        for k, cx in enumerate(xs):
            if row == 0 and k == 2:
                d.rounded_rectangle([cx - 18, cy + 40, cx + 18, cy + 110], radius=8,
                                    fill=pal["bark"], outline=pal["ink"], width=6)
            elif row == 1 and k == 2:
                d.line([cx, cy + 110, cx, cy + 40], fill=pal["bark"], width=10)
                disc(d, cx, cy + 20, 34, pal["accent"], pal, w=6)
            else:
                d.rounded_rectangle([cx - 18, cy + 40, cx + 18, cy + 110], radius=8,
                                    fill=pal["bark"], outline=pal["ink"], width=6)
                disc(d, cx, cy - 20, 72, pal["accent"], pal, w=7)
    return "上排 5 棵（第 3 棵只剩树桩）/ 下排 5 棵（第 3 棵是小树苗）"


@page("plastic", 12)
def _(d, pal):
    """回收桶：桶身要有明确的回收标志，不是普通垃圾桶。"""
    ground = S - MARGIN - 150
    d.line([0, ground, S, ground], fill=pal["ink"], width=10)
    cx = S / 2
    bw = 360
    d.rounded_rectangle([cx - bw / 2, ground - 520, cx + bw / 2, ground - 30], radius=30,
                        fill=pal["accent"], outline=pal["ink"], width=10)
    d.rounded_rectangle([cx - bw / 2 - 18, ground - 590, cx + bw / 2 + 18, ground - 500],
                        radius=24, fill=pal["ink"])
    # 三箭头回收标志
    R = 110
    for i in range(3):
        a0 = i * 120 - 90
        d.arc([cx - R, ground - 300 - R, cx + R, ground - 300 + R], a0 + 8, a0 + 86,
              fill=pal["paper"], width=22)
        a_end, a_pre = math.radians(a0 + 86), math.radians(a0 + 68)
        arrow(d, cx + R * math.cos(a_pre), ground - 300 + R * math.sin(a_pre),
              cx + R * math.cos(a_end), ground - 300 + R * math.sin(a_end),
              pal, w=14, head=34)
    return "1 个回收桶 + 桶身 1 个三箭头回收标志"


@page("plastic", 3)
def _(d, pal):
    """树叶会被吃掉，最后变回土。"""
    xs, slot = lay(3)
    cy = S / 2
    d.ellipse([xs[0] - 110, cy - 80, xs[0] + 110, cy + 80], fill=pal["accent"],
              outline=pal["ink"], width=8)
    d.pieslice([xs[1] - 110, cy - 80, xs[1] + 110, cy + 80], 200, 90, fill=pal["accent"],
               outline=pal["ink"], width=8)
    rnd = random.Random(8)
    for _ in range(40):
        x = xs[2] + rnd.uniform(-110, 110)
        y = cy + rnd.uniform(20, 80)
        disc(d, x, y, 9, pal["bark"], pal, w=2)
    return "3 个阶段：整片叶 → 被啃掉一半 → 一堆土粒"


@page("plastic", 4)
def _(d, pal):
    """小虫子认识树叶，不认识塑料。"""
    for (cx, cy, w_, h_), leaf in zip(panel2(d, pal), (True, False)):
        rnd = random.Random(12 if leaf else 13)
        if leaf:
            d.ellipse([cx - 130, cy - 90, cx + 130, cy + 90], fill=pal["accent"],
                      outline=pal["ink"], width=8)
            for _ in range(14):
                a = rnd.uniform(0, 2 * math.pi)
                disc(d, cx + 150 * math.cos(a), cy + 110 * math.sin(a), 12,
                     pal["ink"], pal, w=2)
        else:
            d.rounded_rectangle([cx - 70, cy - 150, cx + 70, cy + 150], radius=26,
                                fill=pal["paper"], outline=pal["ink"], width=8)
            for _ in range(14):
                a = rnd.uniform(0, 2 * math.pi)
                disc(d, cx + 250 * math.cos(a), cy + 200 * math.sin(a), 12,
                     pal["ink"], pal, w=2)
    return "左格：叶子 + 14 个贴着它的小点 / 右格：瓶子 + 14 个远离它的小点"


@page("plastic", 6)
def _(d, pal):
    """碎成看不见的小片，可它还是塑料。"""
    xs, slot = lay(4)
    cy = S / 2
    rnd = random.Random(15)
    for k, cx in enumerate(xs):
        if k == 0:
            # 上一版整瓶画成纯圆角矩形，看不出是瓶子；补上瓶身、瓶颈、瓶盖。
            d.rounded_rectangle([cx - 60, cy - 90, cx + 60, cy + 140], radius=24,
                                fill=pal["paper"], outline=pal["ink"], width=8)
            d.rounded_rectangle([cx - 26, cy - 150, cx + 26, cy - 80], radius=10,
                                fill=pal["paper"], outline=pal["ink"], width=8)
            d.rounded_rectangle([cx - 32, cy - 178, cx + 32, cy - 142], radius=8,
                                fill=pal["accent"], outline=pal["ink"], width=7)
        elif k == 1:
            d.rounded_rectangle([cx - 58, cy - 90, cx + 58, cy - 10], radius=18,
                                fill=pal["paper"], outline=pal["ink"], width=8)
            d.rounded_rectangle([cx - 26, cy - 150, cx + 26, cy - 96], radius=10,
                                fill=pal["paper"], outline=pal["ink"], width=8)
            d.rounded_rectangle([cx - 50, cy + 20, cx + 50, cy + 140], radius=20,
                                fill=pal["paper"], outline=pal["ink"], width=8)
        elif k == 2:
            for _ in range(9):
                x = cx + rnd.uniform(-70, 70)
                y = cy + rnd.uniform(-120, 120)
                d.rectangle([x - 16, y - 12, x + 16, y + 12], fill=pal["paper"],
                            outline=pal["ink"], width=4)
        else:
            for _ in range(60):
                x = cx + rnd.uniform(-80, 80)
                y = cy + rnd.uniform(-130, 130)
                disc(d, x, y, 5, pal["paper"], pal, w=1)
    return "4 个阶段：整瓶 → 裂成两段 → 9 块碎片 → 60 粒微塑料"


@page("plastic", 8)
def _(d, pal):
    """干净的塑料可以熔化，做成新东西。"""
    cx, cy, R = S / 2, S / 2, 260
    for i in range(3):
        a0 = i * 120 - 80
        d.arc([cx - R, cy - R, cx + R, cy + R], a0, a0 + 78, fill=pal["accent"], width=16)
        a_end, a_pre = math.radians(a0 + 78), math.radians(a0 + 64)
        arrow(d, cx + R * math.cos(a_pre), cy + R * math.sin(a_pre),
              cx + R * math.cos(a_end), cy + R * math.sin(a_end), pal, w=10, head=26)
    spots = [(cx, cy - R), (cx + R * 0.87, cy + R * 0.5), (cx - R * 0.87, cy + R * 0.5)]
    d.rounded_rectangle([spots[0][0] - 42, spots[0][1] - 76, spots[0][0] + 42, spots[0][1] + 76],
                        radius=18, fill=pal["paper"], outline=pal["ink"], width=7)
    rnd = random.Random(21)
    for _ in range(14):
        x = spots[1][0] + rnd.uniform(-60, 60)
        y = spots[1][1] + rnd.uniform(-50, 50)
        d.rectangle([x - 12, y - 9, x + 12, y + 9], fill=pal["paper"],
                    outline=pal["ink"], width=3)
    d.polygon([(spots[2][0] - 70, spots[2][1] + 60), (spots[2][0] - 40, spots[2][1] - 50),
               (spots[2][0] + 40, spots[2][1] - 50), (spots[2][0] + 70, spots[2][1] + 60)],
              fill=pal["accent"])
    return "1 个三段循环 + 瓶子 / 碎片 / 新衣服 三个符号"


@page("plastic", 10)
def _(d, pal):
    """自带杯子、布袋子，不要一次性的。"""
    xs, slot = lay(3)
    cy = S / 2
    d.rounded_rectangle([xs[0] - 70, cy - 90, xs[0] + 70, cy + 110], radius=22,
                        fill=pal["paper"], outline=pal["ink"], width=8)
    d.rounded_rectangle([xs[0] - 50, cy - 130, xs[0] + 50, cy - 90], radius=16,
                        fill=pal["accent"], outline=pal["ink"], width=7)
    d.rounded_rectangle([xs[1] - 90, cy - 50, xs[1] + 90, cy + 120], radius=14,
                        fill=pal["accent"], outline=pal["ink"], width=8)
    d.arc([xs[1] - 60, cy - 140, xs[1] + 60, cy - 20], 180, 360, fill=pal["ink"], width=10)
    d.rounded_rectangle([xs[2] - 16, cy - 130, xs[2] + 16, cy + 130], radius=12,
                        fill=pal["paper"], outline=pal["ink"], width=7)
    d.line([xs[2] - 110, cy - 130, xs[2] + 110, cy + 130], fill=pal["accent"], width=22)
    return "3 个符号：自带杯 / 布袋 / 一次性吸管（划掉）"


@page("sleepwin", 3)
def _(d, pal):
    """冬眠时心跳和呼吸都慢下来。"""
    for cy, freq, col in ((S / 2 - 150, 9, pal["accent"]), (S / 2 + 150, 3, pal["soft"])):
        pts = []
        for i in range(241):
            t = i / 240
            x = MARGIN + 40 + t * (S - 2 * MARGIN - 80)
            y = cy - 90 * math.sin(t * freq * 2 * math.pi)
            pts.append((x, y))
        d.line(pts, fill=col, width=12, joint="curve")
    return "上条 9 个波峰（平时）/ 下条 3 个波峰（冬眠）"


@page("sleepwin", 4)
def _(d, pal):
    """身体调慢了，用的力气就少。"""
    base = S - MARGIN - 160
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    for cx, h, col in ((S / 2 - 220, 520, pal["accent"]), (S / 2 + 220, 150, pal["soft"])):
        d.rounded_rectangle([cx - 110, base - h, cx + 110, base], radius=18,
                            fill=col, outline=pal["ink"], width=8)
    return "2 根柱子站在同一条线上：左高（平时）/ 右矮（冬眠）"


@page("sleepwin", 6)
def _(d, pal):
    """土拨鼠体温降得多，熊降得少。"""
    for (cx, cy, w_, h_), deep in zip(panel2(d, pal), (True, False)):
        bw, bh = 66, h_ * 0.62
        d.rounded_rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2],
                            radius=32, fill=pal["paper"], outline=pal["ink"], width=8)
        fill_h = bh * (0.18 if deep else 0.68)
        d.rounded_rectangle([cx - bw / 2 + 12, cy + bh / 2 - fill_h,
                             cx + bw / 2 - 12, cy + bh / 2 - 12],
                            radius=24, fill=pal["accent"])
        disc(d, cx, cy + bh / 2, 54, pal["accent"], pal, w=8)
    return "左格液柱很低（真冬眠）/ 右格液柱只略低（熊）"


@page("sleepwin", 9)
def _(d, pal):
    """醒一次要花掉好多存下来的力气。"""
    x0, x1 = MARGIN + 60, S - MARGIN - 60
    cy = S / 2
    n = 10
    seg = (x1 - x0) / n
    for i in range(n):
        x = x0 + i * seg
        d.rectangle([x, cy - 90, x + seg - 10, cy + 90],
                    fill=pal["accent"] if i >= 3 else pal["paper"],
                    outline=pal["ink"], width=6)
        if i < 3:
            cross(d, x + (seg - 10) / 2, cy, 56, pal, w=12)
    return "10 格存粮，前 3 格被划掉（醒来用掉的）"


@page("sleepwin", 10)
def _(d, pal):
    """天暖起来，它们自己就醒了。"""
    cx = S / 2 - 120
    bw, bh = 70, 480
    d.rounded_rectangle([cx - bw / 2, S / 2 - bh / 2, cx + bw / 2, S / 2 + bh / 2],
                        radius=34, fill=pal["paper"], outline=pal["ink"], width=9)
    d.rounded_rectangle([cx - bw / 2 + 14, S / 2 - bh / 2 + 90,
                         cx + bw / 2 - 14, S / 2 + bh / 2 - 14],
                        radius=26, fill=pal["accent"])
    disc(d, cx, S / 2 + bh / 2, 58, pal["accent"], pal, w=9)
    arrow(d, cx + 170, S / 2 + 160, cx + 170, S / 2 - 200, pal, w=14, head=36)
    return "1 支体温计（液柱升高）+ 1 支向上的箭头"


# ---------------------------------------------------------------- trash p1（模型四次都塞人进来，改程序画）

@page("trash", 1)
def _(d, pal):
    """三个一样的桶站在地上，只有盖子颜色不同 —— 画面里不会有人。

    这页交给模型画了四次：三个孩子 → 擦成一张脸 → 擦成一块肉色斑 → 又是三个孩子。
    场景里写明「只有三个桶、地面和墙」也没用。桶就是圆角矩形加盖子加轮子，
    几何极简，改程序画，顺便保证画面里绝不会出现人。
    """
    ground = S - MARGIN - 150
    d.rectangle([0, ground, S, S], fill=pal["ground"])
    d.line([0, ground, S, ground], fill=pal["ink"], width=10)
    # 正文写的是蓝、绿、黑三色盖子，而这本调色板里没有绿，accent 又是蓝，
    # 上一版拿 soft 当第一个盖子画成了灰。这里直接写死三个色值。
    lids = ["#2f6fb0", "#3f9e4d", "#20242a"]                 # 蓝 / 绿 / 黑，对应正文
    xs, slot = lay(3)
    bw = min(slot * 0.66, 240)
    for cx, lid in zip(xs, lids):
        top = ground - 520
        d.rounded_rectangle([cx - bw / 2, top + 60, cx + bw / 2, ground - 40], radius=26,
                            fill=pal["paper"], outline=pal["ink"], width=9)
        d.rounded_rectangle([cx - bw / 2 - 14, top, cx + bw / 2 + 14, top + 70], radius=22,
                            fill=lid, outline=pal["ink"], width=9)
        for dx in (-bw * 0.30, bw * 0.30):                   # 两个轮子
            disc(d, cx + dx, ground - 20, 32, pal["ink"], pal, w=4)
    return "3 个等大的桶站在地上，盖子分别是蓝 / 绿 / 黑，画面里没有人"


# ---------------------------------------------------------------- 第五批新书：wind / thunder / rainbow / glass

def flow_arrows(d, pal, pts_from, pts_to, w=10, head=26):
    """成组的同向箭头，用来画气流、热流这类「一进一出」。"""
    for (x1, y1), (x2, y2) in zip(pts_from, pts_to):
        arrow(d, x1, y1, x2, y2, pal, w=w, head=head)


@page("wind", 3)
def _(d, pal):
    """太阳晒热地面，热空气往上升。"""
    base = S - MARGIN - 160
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    disc(d, S - MARGIN - 180, MARGIN + 160, 90, pal["accent"], pal, w=8)
    xs = [S / 2 - 200, S / 2, S / 2 + 200]
    flow_arrows(d, pal, [(x, base - 40) for x in xs], [(x, base - 460) for x in xs])
    return "1 条地面 + 1 个太阳 + 3 支向上的箭头"


@page("wind", 4)
def _(d, pal):
    """热空气升上去，旁边的冷空气补进来 —— 这一进一出就是风。"""
    base = S - MARGIN - 160
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    xs = [S / 2 - 140, S / 2, S / 2 + 140]
    flow_arrows(d, pal, [(x, base - 40) for x in xs], [(x, base - 420) for x in xs])
    arrow(d, MARGIN + 40, base - 120, S / 2 - 230, base - 120, pal, w=11, head=28)
    arrow(d, S - MARGIN - 40, base - 120, S / 2 + 230, base - 120, pal, w=11, head=28)
    return "3 支向上的箭头（热空气）+ 左右各 1 支向内的箭头（冷空气补进来）"


@page("wind", 5)
def _(d, pal):
    """海陆风：白天从海吹向陆，晚上反过来。"""
    for (cx, cy, w_, h_), day in zip(panel2(d, pal), (True, False)):
        mid = cx
        d.rectangle([cx - w_ / 2 + 8, cy + 40, mid, cy + h_ / 2 - 8], fill=pal["soft"])
        d.polygon([(mid, cy + h_ / 2 - 8), (mid, cy + 40),
                   (cx + w_ / 2 - 8, cy - 20), (cx + w_ / 2 - 8, cy + h_ / 2 - 8)],
                  fill=pal["bark"])
        if day:
            arrow(d, cx - w_ * 0.32, cy - 60, cx + w_ * 0.28, cy - 60, pal, w=11, head=28)
        else:
            arrow(d, cx + w_ * 0.28, cy - 60, cx - w_ * 0.32, cy - 60, pal, w=11, head=28)
    return "左格箭头由海指向陆（白天）/ 右格箭头由陆指向海（晚上）"


@page("wind", 7)
def _(d, pal):
    """北风是从北边吹来的。"""
    cx, cy, R = S / 2, S / 2, 300
    disc(d, cx, cy, R, pal["paper"], pal, w=10)
    for i in range(4):
        a = math.radians(i * 90 - 90)
        d.line([cx + (R - 60) * math.cos(a), cy + (R - 60) * math.sin(a),
                cx + (R - 14) * math.cos(a), cy + (R - 14) * math.sin(a)],
               fill=pal["ink"], width=12)
    arrow(d, cx, cy - R - 150, cx, cy - 60, pal, w=14, head=36)
    return "1 个四向罗盘 + 1 支自北向中心的粗箭头"


@page("wind", 9)
def _(d, pal):
    """台风是又急又转的大风，要待在屋里。"""
    cx, cy = S / 2 - 120, S / 2
    pts = []
    for i in range(260):
        t = i / 260
        a = t * 3.2 * 2 * math.pi
        r = 330 * (1 - t * 0.88)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.line(pts, fill=pal["accent"], width=16, joint="curve")
    hx = S - MARGIN - 170
    d.polygon([(hx - 120, S / 2 + 60), (hx, S / 2 - 60), (hx + 120, S / 2 + 60)],
              fill=pal["paper"])
    d.rectangle([hx - 95, S / 2 + 60, hx + 95, S / 2 + 250], fill=pal["paper"],
                outline=pal["ink"], width=8)
    for a, b in (((hx - 120, S / 2 + 60), (hx, S / 2 - 60)), ((hx, S / 2 - 60), (hx + 120, S / 2 + 60))):
        d.line([a, b], fill=pal["ink"], width=8)
    return "1 个卷 3.2 圈的螺旋（台风）+ 1 间关着的房子"


@page("thunder", 3)
def _(d, pal):
    """云里上下攒了两种电。"""
    cx, cy = S / 2, S / 2
    d.ellipse([cx - 380, cy - 220, cx + 380, cy + 220], fill=pal["soft"],
              outline=pal["ink"], width=9)
    rnd = random.Random(5)
    for _ in range(18):
        x = cx + rnd.uniform(-300, 300)
        y = cy + rnd.uniform(-160, -40)
        disc(d, x, y, 16, pal["paper"], pal, w=4)
    for _ in range(18):
        x = cx + rnd.uniform(-300, 300)
        y = cy + rnd.uniform(40, 160)
        d.rectangle([x - 14, y - 14, x + 14, y + 14], fill=pal["accent"],
                    outline=pal["ink"], width=4)
    return "1 朵云 + 上方 18 个圆 + 下方 18 个方（两种电）"


@page("thunder", 4)
def _(d, pal):
    """电跳过去，就是闪电。"""
    cx = S / 2
    d.ellipse([cx - 340, MARGIN + 60, cx + 340, MARGIN + 320], fill=pal["soft"],
              outline=pal["ink"], width=9)
    base = S - MARGIN - 120
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    pts = [(cx, MARGIN + 320), (cx - 90, MARGIN + 480), (cx + 40, MARGIN + 500),
           (cx - 60, base)]
    d.line(pts, fill=pal["accent"], width=20, joint="curve")
    return "1 朵云 + 1 道折线闪电 + 1 条地面"


@page("thunder", 5)
def _(d, pal):
    """空气一胀一缩，就响了。"""
    for (cx, cy, w_, h_), expand in zip(panel2(d, pal), (True, False)):
        R = min(w_, h_) * (0.34 if expand else 0.20)
        disc(d, cx, cy, R, pal["accent"] if expand else pal["soft"], pal, w=9)
        for i in range(8):
            a = i * math.pi / 4
            if expand:
                arrow(d, cx + (R + 20) * math.cos(a), cy + (R + 20) * math.sin(a),
                      cx + (R + 130) * math.cos(a), cy + (R + 130) * math.sin(a),
                      pal, w=8, head=22)
            else:
                arrow(d, cx + (R + 150) * math.cos(a), cy + (R + 150) * math.sin(a),
                      cx + (R + 30) * math.cos(a), cy + (R + 30) * math.sin(a),
                      pal, w=8, head=22)
    return "左格大圆 + 8 支向外箭头（胀）/ 右格小圆 + 8 支向内箭头（缩）"


@page("thunder", 6)
def _(d, pal):
    """光一秒三十万公里，声音一秒三百多米。"""
    x0 = MARGIN + 40
    full = S - 2 * MARGIN - 80
    for cy, frac, col in ((S / 2 - 120, 1.0, pal["accent"]), (S / 2 + 120, 0.06, pal["soft"])):
        d.rounded_rectangle([x0, cy - 40, x0 + full * frac, cy + 40], radius=20,
                            fill=col, outline=pal["ink"], width=8)
    d.line([x0, S / 2 - 200, x0, S / 2 + 200], fill=pal["ink"], width=8)
    return "上条铺满整幅（光）/ 下条只有 6%（声音），左端对齐"


@page("thunder", 9)
def _(d, pal):
    """待在屋里最安全，别在大树下、别在空地上。"""
    xs, slot = lay(3)
    cy = S / 2
    hx = xs[0]
    d.polygon([(hx - 110, cy + 40), (hx, cy - 80), (hx + 110, cy + 40)], fill=pal["paper"])
    d.rectangle([hx - 88, cy + 40, hx + 88, cy + 220], fill=pal["paper"],
                outline=pal["ink"], width=8)
    for a, b in (((hx - 110, cy + 40), (hx, cy - 80)), ((hx, cy - 80), (hx + 110, cy + 40))):
        d.line([a, b], fill=pal["ink"], width=8)
    tx = xs[1]
    d.rectangle([tx - 22, cy - 20, tx + 22, cy + 220], fill=pal["bark"],
                outline=pal["ink"], width=7)
    disc(d, tx, cy - 90, 110, pal["soft"], pal, w=8)
    fx = xs[2]
    d.line([fx - 140, cy + 200, fx + 140, cy + 200], fill=pal["ink"], width=10)
    for x, y in ((tx, cy + 60), (fx, cy + 60)):
        d.line([x - 150, y - 180, x + 150, y + 180], fill=pal["accent"], width=22)
    return "3 个符号：房子（好）/ 大树（划掉）/ 空地（划掉）"


@page("rainbow", 9)
def _(d, pal):
    """双彩虹：外面那条淡一些，颜色还是反的——紫在外，红在里。

    模型画的版本里两条弧颜色顺序一样，正文说的「反过来」没画出来。
    """
    bands = ["#c0392b", "#e67e22", "#f1c40f", "#27ae60", "#2980b9", "#4b3fa0", "#7d3c98"]
    cx, cy = S / 2, S - MARGIN - 40
    for i, col in enumerate(bands):                       # 内弧：红在最外
        r = 330 - i * 34
        d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=col, width=30)
    for i, col in enumerate(reversed(bands)):             # 外弧：紫在最外，且更淡
        r = 500 - i * 26
        d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=col, width=16)
    return "2 条彩虹：内弧红在外紫在内（粗）/ 外弧紫在外红在内（细），顺序相反"


@page("rainbow", 2)
def _(d, pal):
    """白光穿过三棱镜，分成七色。"""
    cy = S / 2
    d.line([MARGIN, cy - 60, S / 2 - 60, cy - 20], fill=pal["ink"], width=12)
    d.polygon([(S / 2 - 40, cy - 180), (S / 2 - 150, cy + 150), (S / 2 + 70, cy + 150)],
              fill=pal["paper"])
    pts = [(S / 2 - 40, cy - 180), (S / 2 - 150, cy + 150), (S / 2 + 70, cy + 150)]
    for a, b in zip(pts, pts[1:] + pts[:1]):
        d.line([a, b], fill=pal["ink"], width=9)
    bands = ["#c0392b", "#e67e22", "#f1c40f", "#27ae60", "#2980b9", "#4b3fa0", "#7d3c98"]
    for i, col in enumerate(bands):
        d.line([S / 2 + 60, cy + 20, S - MARGIN, cy - 60 + i * 46], fill=col, width=12)
    return "1 束白光 + 1 个三棱镜 + 7 条分开的彩色光"


@page("rainbow", 3)
def _(d, pal):
    """光进水里会拐个弯，这叫折射。"""
    cy = S / 2
    d.rectangle([MARGIN, cy, S - MARGIN, S - MARGIN], fill=pal["soft"])
    d.line([MARGIN, cy, S - MARGIN, cy], fill=pal["ink"], width=10)
    hit = (S / 2, cy)
    d.line([MARGIN + 80, cy - 340, hit[0], hit[1]], fill=pal["ink"], width=12)
    d.line([hit[0], hit[1], S - MARGIN - 200, S - MARGIN - 40], fill=pal["accent"], width=12)
    for i in range(9):                                  # 原方向用虚线示意
        t0, t1 = i / 9, i / 9 + 0.05
        x0 = hit[0] + (hit[0] - (MARGIN + 80)) * t0
        y0 = hit[1] + (hit[1] - (cy - 340)) * t0
        x1 = hit[0] + (hit[0] - (MARGIN + 80)) * t1
        y1 = hit[1] + (hit[1] - (cy - 340)) * t1
        d.line([x0, y0, x1, y1], fill=pal["soft"], width=6)
    return "1 条入射光 + 1 条折射后的光 + 1 条虚线（原方向）"


@page("rainbow", 4)
def _(d, pal):
    """光在一颗水滴里拐弯、反射、再拐弯出来。"""
    cx, cy, R = S / 2 + 60, S / 2, 300
    disc(d, cx, cy, R, pal["paper"], pal, w=10)
    entry = (cx - R * 0.62, cy - R * 0.62)
    back = (cx + R * 0.86, cy + R * 0.10)
    d.line([MARGIN, cy - R, entry[0], entry[1]], fill=pal["ink"], width=11)
    d.line([entry[0], entry[1], back[0], back[1]], fill=pal["ink"], width=11)
    bands = ["#c0392b", "#e67e22", "#f1c40f", "#27ae60", "#2980b9", "#4b3fa0", "#7d3c98"]
    for i, col in enumerate(bands):
        d.line([back[0], back[1], MARGIN + 40, cy + 160 + i * 34], fill=col, width=8)
    return "1 颗水滴 + 入射 1 条 + 内部反射 1 条 + 出射 7 条彩色光"


@page("rainbow", 6)
def _(d, pal):
    """彩虹总在太阳的对面。"""
    disc(d, MARGIN + 140, MARGIN + 160, 100, pal["accent"], pal, w=8)
    cx = S / 2 + 40
    d.rounded_rectangle([cx - 40, S / 2 - 40, cx + 40, S / 2 + 200], radius=24,
                        fill=pal["soft"], outline=pal["ink"], width=8)
    disc(d, cx, S / 2 - 90, 52, pal["soft"], pal, w=8)
    bands = ["#c0392b", "#e67e22", "#f1c40f", "#27ae60", "#2980b9", "#4b3fa0", "#7d3c98"]
    for i, col in enumerate(bands):
        r = 300 - i * 26
        d.arc([S - MARGIN - 2 * r, S / 2 + 120 - r, S - MARGIN, S / 2 + 120 + r],
              180, 360, fill=col, width=20)
    return "左边 1 个太阳 + 中间 1 个背对太阳的人 + 右边 1 条七色彩虹"


@page("rainbow", 8)
def _(d, pal):
    """颜色顺序不变：红在最外，紫在最里。"""
    bands = ["#c0392b", "#e67e22", "#f1c40f", "#27ae60", "#2980b9", "#4b3fa0", "#7d3c98"]
    cx, cy = S / 2, S - MARGIN - 60
    for i, col in enumerate(bands):
        r = 420 - i * 52
        d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=col, width=44)
    return "7 条同心弧，最外红、最内紫"


@page("glass", 6)
def _(d, pal):
    """玻璃为什么透明：里面排得乱，可挨得紧，光直接穿过去。

    模型画的版本里三条光线汇聚到方块内部就停住了，没有穿出去。
    """
    cx, cy = S / 2, S / 2
    w_, h_ = 420, 460
    d.rounded_rectangle([cx - w_ / 2, cy - h_ / 2, cx + w_ / 2, cy + h_ / 2], radius=18,
                        fill=pal["paper"], outline=pal["ink"], width=9)
    rnd = random.Random(29)
    for _ in range(70):                                   # 排得乱但挨得紧
        gx = cx + rnd.uniform(-w_ / 2 + 30, w_ / 2 - 30)
        gy = cy + rnd.uniform(-h_ / 2 + 30, h_ / 2 - 30)
        disc(d, gx, gy, 12, pal["soft"], pal, w=3)
    for dy in (-140, 0, 140):                             # 三条光线一直穿到画面右缘
        d.line([MARGIN, cy + dy, S - MARGIN, cy + dy], fill=pal["accent"], width=12)
        arrow(d, S - MARGIN - 120, cy + dy, S - MARGIN, cy + dy, pal, w=12, head=30)
    return "1 块玻璃（70 个乱排的小颗粒）+ 3 条从左穿到右的光线，每条末端 1 个箭头"


@page("glass", 10)
def _(d, pal):
    """回收玻璃更省火：第二支温度计要明显更低。"""
    for (cx, cy, w_, h_), hot in zip(panel2(d, pal), (True, False)):
        bw, bh = 70, h_ * 0.66
        d.rounded_rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2],
                            radius=34, fill=pal["paper"], outline=pal["ink"], width=9)
        fill_h = bh * (0.84 if hot else 0.34)
        d.rounded_rectangle([cx - bw / 2 + 14, cy + bh / 2 - fill_h,
                             cx + bw / 2 - 14, cy + bh / 2 - 14],
                            radius=26, fill=pal["accent"])
        disc(d, cx, cy + bh / 2, 56, pal["accent"], pal, w=9)
    return "左格液柱 84%（烧沙子）/ 右格液柱 34%（烧碎玻璃），差别明显"


@page("glass", 3)
def _(d, pal):
    """沙子烧到很热就熔化，变成会流动的液体。"""
    for (cx, cy, w_, h_), molten in zip(panel2(d, pal), (False, True)):
        d.pieslice([cx - w_ * 0.32, cy - 40, cx + w_ * 0.32, cy + 260], 0, 180,
                   fill=pal["paper"], outline=pal["ink"], width=9)
        if molten:
            d.pieslice([cx - w_ * 0.26, cy + 20, cx + w_ * 0.26, cy + 200], 0, 180,
                       fill=pal["accent"])
        else:
            rnd = random.Random(9)
            for _ in range(70):
                x = cx + rnd.uniform(-w_ * 0.24, w_ * 0.24)
                y = cy + rnd.uniform(40, 180)
                disc(d, x, y, 7, pal["bark"], pal, w=2)
    return "左格：一碗散沙粒 / 右格：一碗流动的熔液"


@page("glass", 4)
def _(d, pal):
    """用长管子蘸一团，往里吹气。"""
    cy = S / 2
    d.rounded_rectangle([MARGIN + 40, cy - 22, S - MARGIN - 260, cy + 22], radius=18,
                        fill=pal["soft"], outline=pal["ink"], width=8)
    disc(d, S - MARGIN - 180, cy, 150, pal["accent"], pal, w=9)
    arrow(d, MARGIN - 10, cy, MARGIN + 120, cy, pal, w=12, head=30)
    return "1 根长管 + 管端 1 团熔玻璃 + 1 支吹入的箭头"


@page("glass", 5)
def _(d, pal):
    """一边吹一边转，慢慢鼓成空心的杯子。"""
    xs, slot = lay(3)
    cy = S / 2
    # 上一版第三个画成了方框，整排读作「甜甜圈变相框」。第三个改成侧视杯形：
    # 上沿开口、杯壁两侧收进去、杯底平 —— 一眼看得出是在吹一只杯子。
    for k, cx in enumerate(xs):
        R = 90 + k * 36
        if k == 0:
            disc(d, cx, cy, R, pal["accent"], pal, w=9)
        elif k == 1:
            disc(d, cx, cy, R, pal["accent"], pal, w=9)
            disc(d, cx, cy, R * 0.46, pal["ground"], pal, w=6)
        else:
            top, bot = cy - R, cy + R
            outer = [(cx - R * 0.76, top), (cx + R * 0.76, top),
                     (cx + R * 0.60, bot), (cx - R * 0.60, bot)]
            d.polygon(outer, fill=pal["accent"])
            for a, b in zip(outer, outer[1:] + outer[:1]):
                d.line([a, b], fill=pal["ink"], width=9)
            inner = [(cx - R * 0.60, top + 26), (cx + R * 0.60, top + 26),
                     (cx + R * 0.44, bot - 34), (cx - R * 0.44, bot - 34)]
            d.polygon(inner, fill=pal["ground"])
            for a, b in zip(inner, inner[1:] + inner[:1]):
                d.line([a, b], fill=pal["ink"], width=6)
    return "3 个阶段：实心团 → 中间鼓出空心 → 侧视杯形（开口在上、杯壁收进去）"


@page("glass", 7)
def _(d, pal):
    """玻璃硬得脆，一摔就碎，碎片很锋利。"""
    cx = S / 2 - 220
    d.rounded_rectangle([cx - 90, S / 2 - 180, cx + 90, S / 2 + 180], radius=26,
                        fill=pal["paper"], outline=pal["ink"], width=9)
    rnd = random.Random(4)
    for _ in range(9):
        px = S / 2 + 160 + rnd.uniform(-140, 200)
        py = S / 2 + rnd.uniform(-180, 180)
        a = rnd.uniform(0, math.pi)
        size = rnd.uniform(40, 90)
        pts = [(px, py),
               (px + size * math.cos(a), py + size * math.sin(a)),
               (px + size * 0.6 * math.cos(a + 1.6), py + size * 0.6 * math.sin(a + 1.6))]
        d.polygon(pts, fill=pal["paper"])
        for p, q in zip(pts, pts[1:] + pts[:1]):
            d.line([p, q], fill=pal["ink"], width=6)
    return "左边 1 只完整的杯子 + 右边 9 块带尖角的碎片"


@page("glass", 9)
def _(d, pal):
    """玻璃可以一直回收。"""
    cx, cy, R = S / 2, S / 2, 280
    for i in range(3):
        a0 = i * 120 - 80
        d.arc([cx - R, cy - R, cx + R, cy + R], a0, a0 + 80, fill=pal["accent"], width=16)
        a_end = math.radians(a0 + 80)
        a_pre = math.radians(a0 + 66)
        arrow(d, cx + R * math.cos(a_pre), cy + R * math.sin(a_pre),
              cx + R * math.cos(a_end), cy + R * math.sin(a_end), pal, w=10, head=26)
    spots = [(cx, cy - R), (cx + R * 0.87, cy + R * 0.5), (cx - R * 0.87, cy + R * 0.5)]
    d.rounded_rectangle([spots[0][0] - 34, spots[0][1] - 70, spots[0][0] + 34, spots[0][1] + 70],
                        radius=16, fill=pal["paper"], outline=pal["ink"], width=7)
    for dx in (-30, 0, 30):
        d.polygon([(spots[1][0] + dx, spots[1][1] - 30), (spots[1][0] + dx + 26, spots[1][1] + 24),
                   (spots[1][0] + dx - 18, spots[1][1] + 20)], fill=pal["paper"])
    d.pieslice([spots[2][0] - 60, spots[2][1] - 50, spots[2][0] + 60, spots[2][1] + 70],
               0, 180, fill=pal["accent"], outline=pal["ink"], width=7)
    return "1 个三段循环箭头 + 瓶子 / 碎片 / 熔炉 三个符号"


# ---------------------------------------------------------------- 第五批新书：hungry / fever / print / year

@page("hungry", 3)
def _(d, pal):
    """食物拆成很小的糖，顺着血跑遍全身。"""
    cy = S / 2
    d.ellipse([MARGIN, cy - 90, MARGIN + 220, cy + 90], fill=pal["paper"],
              outline=pal["ink"], width=9)
    arrow(d, MARGIN + 250, cy, MARGIN + 380, cy, pal, w=11, head=28)
    rnd = random.Random(3)
    for _ in range(40):
        x = rnd.uniform(MARGIN + 420, S - MARGIN)
        y = cy + rnd.uniform(-170, 170)
        disc(d, x, y, rnd.uniform(8, 15), pal["accent"], pal, w=3)
    return "1 个盘子 + 1 支箭头 + 40 粒小糖散开"


@page("hungry", 4)
def _(d, pal):
    """血糖吃过饭高一点，过几小时降下来。"""
    x0, x1 = MARGIN + 40, S - MARGIN - 40
    base = S / 2 + 150
    d.line([x0, base, x1, base], fill=pal["ink"], width=8)
    pts = [(x0, base - 40), (x0 + 150, base - 40), (x0 + 300, base - 330),
           (x0 + 520, base - 240), (x1, base - 70)]
    d.line(pts, fill=pal["accent"], width=14, joint="curve")
    d.ellipse([x0 + 110, base - 90, x0 + 190, base - 10], fill=pal["paper"],
              outline=pal["ink"], width=7)
    return "1 条曲线：先平、吃饭后升高、然后慢慢降下来"


@page("hungry", 5)
def _(d, pal):
    """血糖降下来，身体给大脑发信号。"""
    x0, x1 = MARGIN + 40, S - MARGIN - 40
    base = S / 2 + 220
    pts = [(x0, base - 300), (x0 + 300, base - 240), (x1 - 120, base - 70)]
    d.line(pts, fill=pal["accent"], width=14, joint="curve")
    low = (x1 - 120, base - 70)
    disc(d, low[0], low[1], 20, pal["accent"], pal, w=5)
    brain = (S / 2 + 60, MARGIN + 170)
    d.ellipse([brain[0] - 150, brain[1] - 110, brain[0] + 150, brain[1] + 110],
              fill=pal["paper"], outline=pal["ink"], width=9)
    arrow(d, low[0], low[1] - 40, brain[0] + 40, brain[1] + 120, pal, w=10, head=26)
    return "1 条下降的曲线 + 1 个低点 + 1 支指向大脑的箭头"


@page("hungry", 7)
def _(d, pal):
    """吃太快，大脑来不及收到「饱了」。"""
    for (cx, cy, w_, h_), fast in zip(panel2(d, pal), (True, False)):
        R = min(w_, h_) * 0.26
        disc(d, cx, cy - 60, R, pal["paper"], pal, w=9)
        d.pieslice([cx - R, cy - 60 - R, cx + R, cy - 60 + R], -90,
                   -90 + (60 if fast else 220), fill=pal["accent"])
        d.ellipse([cx - 90, cy + 170, cx + 90, cy + 250], fill=pal["paper"],
                  outline=pal["ink"], width=8)
    return "左格：短扇形（吃得快）/ 右格：长扇形（吃得慢），各配 1 个碗"


@page("hungry", 9)
def _(d, pal):
    """米饭面包慢慢放糖，能撑得久。"""
    x0, x1 = MARGIN + 260, S - MARGIN - 40
    base = S / 2 + 150
    d.ellipse([MARGIN, base - 110, MARGIN + 200, base + 40], fill=pal["paper"],
              outline=pal["ink"], width=9)
    d.line([x0, base - 60, x1, base - 250], fill=pal["accent"], width=14)
    for i in range(6):
        t = i / 5
        disc(d, x0 + t * (x1 - x0), base - 60 - t * 190, 14, pal["accent"], pal, w=4)
    return "1 个饭碗 + 1 条缓慢上升的斜线 + 6 粒均匀分布的糖"


@page("fever", 3)
def _(d, pal):
    """白细胞围上去。"""
    cx, cy = S / 2, S / 2
    disc(d, cx, cy, 150, pal["paper"], pal, w=10)
    for i in range(6):
        a = i * math.pi / 3
        gx, gy = cx + 300 * math.cos(a), cy + 300 * math.sin(a)
        disc(d, gx, gy, 36, pal["accent"], pal, w=6)
        for k in range(8):                      # 病菌的小刺
            b = k * math.pi / 4
            d.line([gx + 36 * math.cos(b), gy + 36 * math.sin(b),
                    gx + 52 * math.cos(b), gy + 52 * math.sin(b)],
                   fill=pal["ink"], width=5)
        arrow(d, cx + 170 * math.cos(a), cy + 170 * math.sin(a),
              cx + 250 * math.cos(a), cy + 250 * math.sin(a), pal, w=8, head=22)
    return "1 个白细胞 + 6 个带刺的病菌 + 6 支由内向外的箭头"


@page("fever", 4)
def _(d, pal):
    """病菌怕热，白细胞在热一点时跑得更快。"""
    for (cx, cy, w_, h_), high in zip(panel2(d, pal), (False, True)):
        bw, bh = 62, h_ * 0.62
        d.rounded_rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2],
                            radius=30, fill=pal["paper"], outline=pal["ink"], width=8)
        fill_h = bh * (0.42 if not high else 0.80)
        d.rounded_rectangle([cx - bw / 2 + 12, cy + bh / 2 - fill_h,
                             cx + bw / 2 - 12, cy + bh / 2 - 12],
                            radius=22, fill=pal["accent"])
        disc(d, cx, cy + bh / 2, 52, pal["accent"], pal, w=8)
    return "左格体温计液柱低 / 右格液柱明显更高"


@page("fever", 5)
def _(d, pal):
    """大脑把目标温度调高一格。"""
    cx, cy, R = S / 2, S / 2 + 30, 280
    disc(d, cx, cy, R, pal["paper"], pal, w=10)
    for i in range(11):
        a = math.radians(180 + i * 18)
        d.line([cx + (R - 44) * math.cos(a), cy + (R - 44) * math.sin(a),
                cx + (R - 12) * math.cos(a), cy + (R - 12) * math.sin(a)],
               fill=pal["ink"], width=8)
    # 上一版两根指针都在上方、夹角太小，「从低调到高」读不出方向。
    # 旧指针放在左下（低），新指针放在右上（高），中间一段粗弧 + 箭头标出转向。
    a_old = math.radians(180 + 1 * 18)          # 左下，接近最低刻度
    a_new = math.radians(180 + 8 * 18)          # 右上，接近最高刻度
    d.line([cx, cy, cx + (R - 70) * math.cos(a_old), cy + (R - 70) * math.sin(a_old)],
           fill=pal["soft"], width=14)
    d.line([cx, cy, cx + (R - 70) * math.cos(a_new), cy + (R - 70) * math.sin(a_new)],
           fill=pal["accent"], width=24)
    rr = R - 150
    d.arc([cx - rr, cy - rr, cx + rr, cy + rr], 180 + 1 * 18, 180 + 8 * 18,
          fill=pal["accent"], width=14)
    a_tip = math.radians(180 + 8 * 18)
    a_pre = math.radians(180 + 7 * 18)
    arrow(d, cx + rr * math.cos(a_pre), cy + rr * math.sin(a_pre),
          cx + rr * math.cos(a_tip), cy + rr * math.sin(a_tip), pal, w=12, head=30)
    disc(d, cx, cy, 18, pal["ink"], pal, w=3)
    return "1 个刻度盘 + 旧指针（浅，偏低）+ 新指针（深，偏高）+ 1 段带箭头的弧"


@page("fever", 6)
def _(d, pal):
    """打赢了，开关调回来，出汗降温。"""
    cx, cy, R = S / 2, S / 2 - 20, 250
    disc(d, cx, cy, R, pal["paper"], pal, w=10)
    for i in range(11):
        a = math.radians(180 + i * 18)
        d.line([cx + (R - 40) * math.cos(a), cy + (R - 40) * math.sin(a),
                cx + (R - 12) * math.cos(a), cy + (R - 12) * math.sin(a)],
               fill=pal["ink"], width=7)
    a_new = math.radians(180 + 4 * 18)
    d.line([cx, cy, cx + (R - 70) * math.cos(a_new), cy + (R - 70) * math.sin(a_new)],
           fill=pal["accent"], width=18)
    for k, x in enumerate((cx - 140, cx, cx + 140)):
        y = cy + R + 120 + (k % 2) * 40
        d.pieslice([x - 26, y - 34, x + 26, y + 26], 0, 180, fill=pal["soft"],
                   outline=pal["ink"], width=5)
        d.polygon([(x - 26, y - 4), (x, y - 56), (x + 26, y - 4)], fill=pal["soft"])
    return "1 个刻度盘（指针回到低位）+ 3 滴汗"


@page("fever", 8)
def _(d, pal):
    """多喝水、多睡觉、吃清淡。"""
    xs, slot = lay(3)
    cy = S / 2
    d.rounded_rectangle([xs[0] - 60, cy - 130, xs[0] + 60, cy + 130], radius=20,
                        fill=pal["paper"], outline=pal["ink"], width=8)
    d.rectangle([xs[0] - 48, cy - 20, xs[0] + 48, cy + 118], fill=pal["soft"])
    d.rounded_rectangle([xs[1] - 150, cy + 10, xs[1] + 150, cy + 130], radius=24,
                        fill=pal["paper"], outline=pal["ink"], width=8)
    d.rounded_rectangle([xs[1] - 150, cy - 60, xs[1] - 40, cy + 20], radius=18,
                        fill=pal["soft"], outline=pal["ink"], width=6)
    d.pieslice([xs[2] - 130, cy - 90, xs[2] + 130, cy + 130], 0, 180,
               fill=pal["paper"], outline=pal["ink"], width=8)
    return "3 个并排符号：水杯 / 床 / 碗"


@page("print", 3)
def _(d, pal):
    """三种花样：圈、拐弯、尖顶。"""
    xs, slot = lay(3)
    cy = S / 2
    R = min(slot * 0.40, 200)
    for k, cx in enumerate(xs):
        d.ellipse([cx - R * 0.78, cy - R, cx + R * 0.78, cy + R],
                  fill=pal["paper"], outline=pal["ink"], width=8)
        for i in range(6):
            t = (i + 1) / 7
            rx, ry = R * 0.70 * t, R * 0.88 * t
            if k == 0:                                   # 同心圈
                d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=pal["ink"], width=6)
            elif k == 1:                                 # 拐个弯
                d.arc([cx - rx - 30, cy - ry, cx + rx - 30, cy + ry], 250, 110,
                      fill=pal["ink"], width=6)
            else:                                        # 帐篷尖顶
                d.line([cx - rx, cy + ry * 0.6, cx, cy - ry * 0.9], fill=pal["ink"], width=6)
                d.line([cx, cy - ry * 0.9, cx + rx, cy + ry * 0.6], fill=pal["ink"], width=6)
    return "3 个指纹：同心圈 / 拐弯 / 尖顶，各 6 条纹"


@page("print", 4)
def _(d, pal):
    """皮肤被挤一下、拉一下，线就定下来了。"""
    cx, cy = S / 2, S / 2
    R = 260
    d.ellipse([cx - R * 0.78, cy - R, cx + R * 0.78, cy + R],
              fill=pal["paper"], outline=pal["ink"], width=9)
    for i in range(7):
        t = (i + 1) / 8
        rx, ry = R * 0.70 * t, R * 0.88 * t
        d.arc([cx - rx, cy - ry, cx + rx, cy + ry], 200, 160, fill=pal["ink"], width=6)
    for a_deg in (20, 160, 270):
        a = math.radians(a_deg)
        arrow(d, cx + (R + 150) * math.cos(a) * 0.78, cy + (R + 150) * math.sin(a),
              cx + (R + 20) * math.cos(a) * 0.78, cy + (R + 20) * math.sin(a),
              pal, w=9, head=24)
    return "1 个指纹 + 3 支由外向内挤压的箭头"


@page("print", 5)
def _(d, pal):
    """长大只是整个变大，花样不变。"""
    for cx, R in ((S / 2 - 250, 150), (S / 2 + 250, 240)):
        d.ellipse([cx - R * 0.78, S / 2 - R, cx + R * 0.78, S / 2 + R],
                  fill=pal["paper"], outline=pal["ink"], width=8)
        for i in range(6):
            t = (i + 1) / 7
            rx, ry = R * 0.70 * t, R * 0.88 * t
            d.ellipse([cx - rx, S / 2 - ry, cx + rx, S / 2 + ry],
                      outline=pal["ink"], width=6)
    return "2 个同样花样的指纹，右边整体更大"


@page("print", 7)
def _(d, pal):
    """十根手指，十个不一样的花样。"""
    rnd = random.Random(11)
    for row_i in range(2):
        for col in range(5):
            cx = MARGIN + 110 + col * ((S - 2 * MARGIN - 220) / 4)
            cy = S / 2 - 180 + row_i * 360
            R = 96
            d.ellipse([cx - R * 0.78, cy - R, cx + R * 0.78, cy + R],
                      fill=pal["paper"], outline=pal["ink"], width=6)
            kind = (row_i * 5 + col) % 3
            for i in range(4):
                t = (i + 1) / 5
                rx, ry = R * 0.70 * t, R * 0.88 * t
                if kind == 0:
                    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=pal["ink"], width=4)
                elif kind == 1:
                    d.arc([cx - rx - 14, cy - ry, cx + rx - 14, cy + ry], 250, 110,
                          fill=pal["ink"], width=4)
                else:
                    d.line([cx - rx, cy + ry * 0.6, cx, cy - ry * 0.9], fill=pal["ink"], width=4)
                    d.line([cx, cy - ry * 0.9, cx + rx, cy + ry * 0.6], fill=pal["ink"], width=4)
    return "10 个指纹，排成 2 行 5 列，三种花样轮换"


@page("print", 9)
def _(d, pal):
    """手指碰过的地方留下看不见的指纹。"""
    cx, cy = S / 2, S / 2 + 40
    d.rounded_rectangle([cx - 170, cy - 220, cx + 170, cy + 220], radius=40,
                        fill=pal["paper"], outline=pal["ink"], width=9)
    for k, (dx, dy) in enumerate(((-70, -110), (20, 10), (-30, 130))):
        R = 62
        d.ellipse([cx + dx - R * 0.78, cy + dy - R, cx + dx + R * 0.78, cy + dy + R],
                  outline=pal["soft"], width=5)
        for i in range(3):
            t = (i + 1) / 4
            d.ellipse([cx + dx - R * 0.70 * t, cy + dy - R * 0.88 * t,
                       cx + dx + R * 0.70 * t, cy + dy + R * 0.88 * t],
                      outline=pal["soft"], width=4)
    return "1 只杯子 + 3 个淡色指纹印"


@page("year", 2)
def _(d, pal):
    """一年十二个月。"""
    for r in range(3):
        for c in range(4):
            x = MARGIN + 40 + c * ((S - 2 * MARGIN - 80) / 4)
            y = MARGIN + 120 + r * 250
            w_ = (S - 2 * MARGIN - 80) / 4 - 24
            d.rounded_rectangle([x, y, x + w_, y + 190], radius=14,
                                fill=pal["paper"], outline=pal["ink"], width=7)
    return "12 个等大格子，排成 3 行 4 列"


@page("year", 3)
def _(d, pal):
    """每月的天数：二月最短。"""
    # 柱宽和间距要分开算：上一版用 step-16 当宽度、又加了 8 的左偏移，
    # 矮柱两侧留出视觉空隙，十二根看着像十一根加一根。
    n = 12
    gap = 10
    avail = S - 2 * MARGIN
    bw = (avail - gap * (n - 1)) / n
    base = S - MARGIN - 120
    for i in range(n):
        h = 420 if i != 1 else 300
        x = MARGIN + i * (bw + gap)
        d.rounded_rectangle([x, base - h, x + bw, base], radius=8,
                            fill=pal["accent"] if i == 1 else pal["paper"],
                            outline=pal["ink"], width=6)
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=8)
    return f"12 根等宽柱子（宽 {bw:.0f}、间距 {gap}），第 2 根明显更矮"


@page("year", 5)
def _(d, pal):
    """十二个月分成四季，每季三个月。"""
    n = 12
    step = (S - 2 * MARGIN) / n
    cols = [pal["accent"], pal["soft"], pal["bark"], pal["line"]]
    for i in range(n):
        x = MARGIN + step * i + 6
        d.rounded_rectangle([x, S / 2 - 160, x + step - 12, S / 2 + 160], radius=12,
                            fill=cols[i // 3], outline=pal["ink"], width=6)
    return "12 个格子，按每 3 个一组分成 4 种颜色"


@page("year", 7)
def _(d, pal):
    """夏天白天长，夜里短。"""
    base = S / 2
    d.rounded_rectangle([MARGIN, base - 120, S - MARGIN - 260, base - 20], radius=24,
                        fill=pal["accent"], outline=pal["ink"], width=8)
    d.rounded_rectangle([MARGIN, base + 20, MARGIN + 260, base + 120], radius=24,
                        fill=pal["ink"], outline=pal["ink"], width=8)
    return "上条长（白天）/ 下条短（夜里），左端对齐"


@page("year", 9)
def _(d, pal):
    """冬天白天短，夜里长。"""
    base = S / 2
    d.rounded_rectangle([MARGIN, base - 120, MARGIN + 260, base - 20], radius=24,
                        fill=pal["accent"], outline=pal["ink"], width=8)
    d.rounded_rectangle([MARGIN, base + 20, S - MARGIN - 260, base + 120], radius=24,
                        fill=pal["ink"], outline=pal["ink"], width=8)
    return "上条短（白天）/ 下条长（夜里），左端对齐"


@page("year", 10)
def _(d, pal):
    """日历每行七格。"""
    cols, rows = 7, 5
    w_ = (S - 2 * MARGIN) / cols
    h_ = 150
    top = S / 2 - rows * h_ / 2
    for r in range(rows):
        for c in range(cols):
            d.rectangle([MARGIN + c * w_, top + r * h_,
                         MARGIN + (c + 1) * w_, top + (r + 1) * h_],
                        fill=pal["paper"], outline=pal["ink"], width=5)
    return "1 个 7 列 5 行的日历格"


# ---------------------------------------------------------------- 第五批新书：eye / ear（感官剖面）

@page("eye", 2)
def _(d, pal):
    """有光才看得见：亮房间看得清椅子，暗房间几乎看不见。

    这页交给模型画了两次，两次都把并排的两格理解成「一本摊开的书的两页」。
    它本质就是一个亮/暗对比，交给 panel2 才靠谱。
    """
    (lx, ly, lw, lh), (rx, ry, rw, rh) = panel2(d, pal)
    d.rectangle([rx - rw / 2 + 6, ry - rh / 2 + 6, rx + rw / 2 - 6, ry + rh / 2 - 6],
                fill=pal["ink"])                                  # 右格：关了灯
    for (cx, cy, w_, h_), lit in (((lx, ly, lw, lh), True), ((rx, ry, rw, rh), False)):
        col = pal["ink"] if lit else pal["soft"]
        seat_y = cy + h_ * 0.16
        d.rounded_rectangle([cx - 110, seat_y, cx + 110, seat_y + 34], radius=10,
                            fill=pal["accent"] if lit else None, outline=col, width=8)
        d.line([cx - 96, seat_y + 34, cx - 96, seat_y + 180], fill=col, width=10)
        d.line([cx + 96, seat_y + 34, cx + 96, seat_y + 180], fill=col, width=10)
        d.line([cx - 96, seat_y, cx - 96, seat_y - 190], fill=col, width=10)
        d.line([cx + 96, seat_y, cx + 96, seat_y - 190], fill=col, width=10)
        for k in range(3):
            y = seat_y - 40 - k * 52
            d.line([cx - 96, y, cx + 96, y], fill=col, width=8)
        if lit:
            bulb = (cx + w_ * 0.30, cy - h_ * 0.30)
            disc(d, bulb[0], bulb[1], 46, pal["accent"], pal, w=8)
            for i in range(8):
                a = i * math.pi / 4
                d.line([bulb[0] + 60 * math.cos(a), bulb[1] + 60 * math.sin(a),
                        bulb[0] + 100 * math.cos(a), bulb[1] + 100 * math.sin(a)],
                       fill=pal["accent"], width=7)
    return "左格：亮着的灯 + 看得清的椅子 / 右格：全黑 + 只剩轮廓的椅子"


@page("eye", 5)
def _(d, pal):
    """视网膜：眼球剖面，后壁上铺着一层膜。

    模型把这页画成了「脸上一只装饰性的大眼睛」，没有剖面也没有后壁那层膜。
    """
    cx, cy, R = S / 2, S / 2, 320
    disc(d, cx, cy, R, pal["paper"], pal, w=10)
    # 后壁那层膜：右侧一段加厚的弧
    d.arc([cx - R, cy - R, cx + R, cy + R], -70, 70, fill=pal["accent"], width=34)
    # 前面的角膜与晶状体
    d.arc([cx - R, cy - R, cx + R, cy + R], 130, 230, fill=pal["soft"], width=18)
    d.ellipse([cx - R * 0.86, cy - 90, cx - R * 0.52, cy + 90],
              fill=pal["soft"], outline=pal["ink"], width=8)
    for dy in (-120, 0, 120):
        d.line([cx - R - 130, cy + dy, cx - R * 0.72, cy + dy * 0.55],
               fill=pal["ink"], width=8)
        d.line([cx - R * 0.52, cy + dy * 0.30, cx + R * 0.92, cy - dy * 0.55],
               fill=pal["ink"], width=8)
    return "1 个眼球剖面 + 后壁 1 层加厚的膜（视网膜）+ 3 条穿过晶状体的光线"


@page("eye", 3)
def _(d, pal):
    """瞳孔：亮的地方缩小，暗的地方张大。"""
    for (cx, cy, w_, h_), small in zip(panel2(d, pal), (True, False)):
        R = min(w_, h_) * 0.32
        disc(d, cx, cy, R, pal["paper"], pal, w=9)
        disc(d, cx, cy, R * 0.52, pal["soft"], pal, w=7)
        disc(d, cx, cy, R * (0.16 if small else 0.38), pal["ink"], pal, w=4)
    return "左格瞳孔小（亮处）/ 右格瞳孔大（暗处），虹膜和眼白相同"


@page("eye", 4)
def _(d, pal):
    """晶状体把散开的光聚到一点。"""
    cx, cy = S / 2, S / 2
    d.ellipse([cx - 70, cy - 190, cx + 70, cy + 190], fill=pal["paper"],
              outline=pal["ink"], width=9)
    focus = cx + 320
    for dy in (-150, 0, 150):
        d.line([MARGIN, cy + dy, cx - 40, cy + dy], fill=pal["ink"], width=8)
        d.line([cx + 40, cy + dy * 0.72, focus, cy], fill=pal["ink"], width=8)
    disc(d, focus, cy, 16, pal["accent"], pal, w=4)
    return "1 片晶状体 + 3 条入射光 + 3 条汇聚到 1 个点的出射光"


@page("eye", 6)
def _(d, pal):
    """落在视网膜上的像是倒过来的。"""
    cy = S / 2
    lx, rx = MARGIN + 150, S - MARGIN - 150
    d.rounded_rectangle([lx - 26, cy - 150, lx + 26, cy + 60], radius=10,
                        fill=pal["accent"], outline=pal["ink"], width=7)
    d.ellipse([lx - 20, cy - 200, lx + 20, cy - 140], fill=pal["accent"])
    d.ellipse([S / 2 - 46, cy - 150, S / 2 + 46, cy + 150], fill=pal["paper"],
              outline=pal["ink"], width=8)
    d.rounded_rectangle([rx - 26, cy - 60, rx + 26, cy + 150], radius=10,
                        fill=pal["accent"], outline=pal["ink"], width=7)
    d.ellipse([rx - 20, cy + 140, rx + 20, cy + 200], fill=pal["accent"])
    for dy, dy2 in ((-170, 170), (60, -60)):
        d.line([lx, cy + dy, rx, cy + dy2], fill=pal["ink"], width=6)
    return "左边 1 支正立的蜡烛 → 穿过晶状体 → 右边 1 支倒立的蜡烛，2 条交叉光线"


@page("eye", 8)
def _(d, pal):
    """两只眼睛看到的稍稍不同，合起来才知道远近。"""
    cy = S - MARGIN - 160
    lx, rx = S / 2 - 210, S / 2 + 210
    for cx in (lx, rx):
        d.ellipse([cx - 90, cy - 54, cx + 90, cy + 54], fill=pal["paper"],
                  outline=pal["ink"], width=8)
        disc(d, cx, cy, 30, pal["ink"], pal, w=4)
    tx, ty = S / 2, MARGIN + 150
    d.rounded_rectangle([tx - 70, ty - 60, tx + 70, ty + 90], radius=18,
                        fill=pal["accent"], outline=pal["ink"], width=8)
    for cx in (lx, rx):
        d.line([cx, cy - 60, tx, ty + 90], fill=pal["ink"], width=7)
    return "2 只眼睛 + 1 个杯子 + 2 条成明显夹角的视线"


@page("eye", 9)
def _(d, pal):
    """看远处晶状体变薄，看近处变厚。"""
    for (cx, cy, w_, h_), thin in zip(panel2(d, pal), (True, False)):
        half = w_ * (0.06 if thin else 0.15)
        d.ellipse([cx - half, cy - h_ * 0.28, cx + half, cy + h_ * 0.28],
                  fill=pal["paper"], outline=pal["ink"], width=9)
        if thin:
            for k in (-1, 0, 1):
                d.line([cx - w_ * 0.40, cy + k * 60, cx + w_ * 0.40, cy + k * 60],
                       fill=pal["ink"], width=6)
        else:
            for k in (-1, 0, 1):
                d.line([cx - w_ * 0.40, cy + k * 110, cx + w_ * 0.40, cy + k * 30],
                       fill=pal["ink"], width=6)
    return "左格晶状体薄、光线平行（看远）/ 右格晶状体厚、光线发散（看近）"


@page("ear", 2)
def _(d, pal):
    """外耳、中耳、内耳，三段。"""
    w_ = (S - 2 * MARGIN) / 3
    for k, col in enumerate((pal["paper"], pal["soft"], pal["bark"])):
        x = MARGIN + k * w_
        d.rectangle([x, S / 2 - 240, x + w_, S / 2 + 240], fill=col,
                    outline=pal["ink"], width=8)
    return "3 段等宽区域，颜色依次不同（外耳 / 中耳 / 内耳）"


@page("ear", 4)
def _(d, pal):
    """耳道尽头是一张薄薄的耳膜。"""
    cy = S / 2
    x0, x1 = MARGIN + 60, S - MARGIN - 240
    d.rectangle([x0, cy - 110, x1, cy + 110], fill=pal["paper"],
                outline=pal["ink"], width=8)
    d.line([x1, cy - 110, x1, cy + 110], fill=pal["accent"], width=24)
    arrow(d, x0 - 10, cy, x0 + 160, cy, pal, w=10, head=26)
    return "1 条耳道 + 尽头 1 张绷紧的耳膜 + 1 支入射箭头"


@page("ear", 5)
def _(d, pal):
    """声音大，耳膜抖得厉害；声音小，只轻轻动一下。"""
    for (cx, cy, w_, h_), loud in zip(panel2(d, pal), (True, False)):
        x1 = cx + w_ * 0.22
        d.rectangle([cx - w_ * 0.36, cy - 80, x1, cy + 80], fill=pal["paper"],
                    outline=pal["ink"], width=7)
        bulge = 70 if loud else 16
        d.arc([x1 - bulge, cy - 80, x1 + bulge, cy + 80], 270, 90,
              fill=pal["accent"], width=18)
        for i in range(3 if loud else 1):
            r = 40 + i * 34
            d.arc([cx - w_ * 0.36 - r, cy - r, cx - w_ * 0.36 + r, cy + r], 300, 60,
                  fill=pal["ink"], width=7)
    return "左格：3 道声波、耳膜鼓得远 / 右格：1 道声波、耳膜几乎不动"


@page("ear", 6)
def _(d, pal):
    """三块小骨头一个推一个，把抖动放大。"""
    cy = S / 2
    xs = [MARGIN + 180 + i * 250 for i in range(3)]
    for i, x in enumerate(xs):
        d.rounded_rectangle([x - 70, cy - 40 - i * 12, x + 70, cy + 40 + i * 12],
                            radius=26, fill=pal["paper"], outline=pal["ink"], width=8)
    for i in range(2):
        arrow(d, xs[i] + 74, cy, xs[i + 1] - 74, cy, pal, w=8 + i * 4, head=22 + i * 6)
    return "3 块小骨依次相接 + 2 支箭头，后一支更粗（放大）"


@page("ear", 7)
def _(d, pal):
    """内耳是一根卷起来的管子，像蜗牛。"""
    cx, cy = S / 2, S / 2
    pts = []
    for i in range(220):
        t = i / 220
        a = t * 2.5 * 2 * math.pi
        r = 340 * (1 - t * 0.86)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.line(pts, fill=pal["accent"], width=26, joint="curve")
    return "1 条螺旋，卷 2.5 圈（耳蜗）"


@page("ear", 8)
def _(d, pal):
    """水一晃，小毛就跟着弯。"""
    base = S / 2 + 160
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    n = 22
    step = (S - 2 * MARGIN) / n
    for i in range(n):
        x = MARGIN + step * (i + 0.5)
        bend = 44 if 6 <= i <= 14 else 0          # 波下面的那一段弯倒
        d.line([x, base, x + bend, base - 120], fill=pal["ink"], width=8)
    pts = [(MARGIN + step * (i + 0.5), base - 210 + 46 * math.sin(i / 2.2))
           for i in range(n)]
    d.line(pts, fill=pal["accent"], width=12, joint="curve")
    return "22 根小毛，其中 9 根在波下方弯倒 + 1 条起伏的波"


# ---------------------------------------------------------------- 第五批新书：more（比多少）
# 整本讲一一对应，数目全部由构造保证。用的都是今天验证过的图元：lay / disc / row。

def pair_rows(d, pal, top_n, bot_n, cy=None, r=54, link=False, mark_extra=False):
    """两排圆，从左边同一起点开始一一对应。返回 (上排 x 列表, 下排 x 列表)。

    对齐是这本书的全部要点，所以两排共用同一个步距、同一个左起点 —— 不各自居中。
    """
    cy = cy or S / 2
    n = max(top_n, bot_n)
    step = min(2 * r + 26, (S - 2 * MARGIN) / n)
    x0 = MARGIN + step / 2
    xs = [x0 + i * step for i in range(n)]
    for i in range(top_n):
        extra = mark_extra and i >= bot_n
        disc(d, xs[i], cy - 110, r, pal["accent"] if extra else pal["paper"], pal, w=9)
    for i in range(bot_n):
        disc(d, xs[i], cy + 110, r, pal["soft"], pal, w=9)
    if link:
        for i in range(min(top_n, bot_n)):
            d.line([xs[i], cy - 110 + r, xs[i], cy + 110 - r], fill=pal["ink"], width=7)
    return xs[:top_n], xs[:bot_n]


@page("more", 2)
def _(d, pal):
    """一个对一个地摆好，就能比出来。"""
    pair_rows(d, pal, 5, 5, link=True)
    return "上排 5 个 + 下排 5 个，一一对应"


@page("more", 3)
def _(d, pal):
    """刚好配完，谁也没剩下 —— 一样多。"""
    pair_rows(d, pal, 4, 4, r=62, link=True)
    return "上排 4 个 + 下排 4 个，全部配对，没有剩余"


@page("more", 4)
def _(d, pal):
    """上面剩下两个，上面就比下面多两个。"""
    pair_rows(d, pal, 6, 4, link=True, mark_extra=True)
    return "上排 6 个 + 下排 4 个，多出的 2 个标成强调色"


@page("more", 5)
def _(d, pal):
    """多和少是比出来的：三个比两个多，比十个少。"""
    groups = (2, 3, 10)
    box_w = (S - 2 * MARGIN - 2 * 30) / 3
    for k, n in enumerate(groups):
        bx = MARGIN + k * (box_w + 30)
        d.rounded_rectangle([bx, S / 2 - 210, bx + box_w, S / 2 + 210], radius=18,
                            fill=pal["paper"], outline=pal["ink"], width=6)
        cols = 2 if n <= 4 else 3
        r = min(box_w / (2 * cols) - 10, 46)
        for i in range(n):
            cx = bx + box_w / 2 + ((i % cols) - (cols - 1) / 2) * 2 * r
            cy = S / 2 - 120 + (i // cols) * 2 * r
            disc(d, cx, cy, r - 4, pal["accent"], pal, w=6)
    return "三个框：2 个 / 3 个 / 10 个"


@page("more", 6)
def _(d, pal):
    """一眼就看得出：一堆挤满，一堆稀疏。"""
    (lx, ly, lw, lh), (rx, ry, rw, rh) = panel2(d, pal)
    rnd = random.Random(7)
    for i in range(20):
        cx = lx + (i % 5 - 2) * lw * 0.17
        cy = ly + (i // 5 - 1.5) * lh * 0.20
        disc(d, cx, cy, 34, pal["accent"], pal, w=6)
    for i, (dx, dy) in enumerate(((-0.22, -0.18), (0.16, 0.02), (-0.06, 0.22))):
        disc(d, rx + dx * rw, ry + dy * rh, 34, pal["accent"], pal, w=6)
    return "左格 20 个（挤满）/ 右格 3 个（稀疏）"


@page("more", 7)
def _(d, pal):
    """摆得开看着像更多，其实一样多 —— 两排都是六个。"""
    cy = S / 2
    wide = [MARGIN + 70 + i * ((S - 2 * MARGIN - 140) / 5) for i in range(6)]
    tight = [S / 2 - 2.5 * 92 + i * 92 for i in range(6)]
    for x in wide:
        disc(d, x, cy - 130, 44, pal["accent"], pal, w=8)
    for x in tight:
        disc(d, x, cy + 130, 44, pal["accent"], pal, w=8)
    return "上排 6 个（摆得开）/ 下排 6 个（挤在一起），数目相同"


@page("more", 8)
def _(d, pal):
    """三个大的不一定比五个小的多 —— 数的是个数。"""
    for x in [S / 2 - 220, S / 2, S / 2 + 220]:
        disc(d, x, S / 2 - 140, 92, pal["accent"], pal, w=9)
    for i in range(5):
        disc(d, MARGIN + 110 + i * 200, S / 2 + 160, 46, pal["soft"], pal, w=8)
    return "上排 3 个大的 / 下排 5 个小的"


@page("more", 9)
def _(d, pal):
    """比长短要从同一头开始。"""
    x0 = MARGIN + 40
    for cy, w_ in ((S / 2 - 90, S - 2 * MARGIN - 120), (S / 2 + 90, (S - 2 * MARGIN - 120) * 0.58)):
        d.rounded_rectangle([x0, cy - 36, x0 + w_, cy + 36], radius=18,
                            fill=pal["accent"], outline=pal["ink"], width=8)
    d.line([x0, S / 2 - 190, x0, S / 2 + 190], fill=pal["ink"], width=8)
    return "两条横条，左端对齐在同一条竖线上，上长下短"


@page("more", 10)
def _(d, pal):
    """比高矮要站在同一块地上。"""
    base = S - MARGIN - 80
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    for cx, h in ((S / 2 - 190, 420), (S / 2 + 190, 600)):
        d.rounded_rectangle([cx - 80, base - h, cx + 80, base], radius=18,
                            fill=pal["accent"], outline=pal["ink"], width=8)
    return "两条竖条站在同一条地平线上，右边明显更高"


@page("more", 11)
def _(d, pal):
    """两队一个对一个，哪队拖出来一截，哪队更长。"""
    pair_rows(d, pal, 7, 5, r=44, link=True, mark_extra=True)
    return "上排 7 个 + 下排 5 个，多出的 2 个标成强调色并伸出下排末端"


# ---------------------------------------------------------------- 第五批新书：clock（钟面）

def clock_face(d, cx, cy, R, pal, ticks=12, minute_ticks=False,
               hour=None, minute=None, second=None, wedge_to=None):
    """一个钟面。刻度数、指针角度全部由参数算出，读者能数得清、对得上。

    hour/minute 用「几点几分」而不是角度：时针角 = (hour%12 + minute/60) * 30 度，
    分针角 = minute * 6 度 —— 半点时时针自然落在两个数字中间，不用手调。
    """
    disc(d, cx, cy, R, pal["paper"], pal, w=10)
    # 钟面必须写出 1–12：正文通篇说「短针指 3」「短针在 6 和 7 中间」，
    # 只有刻度线的话孩子对不上。字体用 Arial Black（今天已确认可用）。
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/ariblk.ttf", int(R * 0.20))
    except Exception:
        font = None
    if font is not None:
        for i in range(1, 13):
            a = math.radians(i * 30 - 90)
            nx, ny = cx + (R - 74) * math.cos(a), cy + (R - 74) * math.sin(a)
            d.text((nx, ny), str(i), font=font, fill=pal["ink"], anchor="mm")
    if minute_ticks:
        for i in range(60):
            a = math.radians(i * 6 - 90)
            long_ = (i % 5 == 0)
            r0 = R - (34 if long_ else 18)
            d.line([cx + r0 * math.cos(a), cy + r0 * math.sin(a),
                    cx + (R - 8) * math.cos(a), cy + (R - 8) * math.sin(a)],
                   fill=pal["ink"], width=9 if long_ else 5)
    else:
        for i in range(ticks):
            a = math.radians(i * (360 / ticks) - 90)
            d.line([cx + (R - 36) * math.cos(a), cy + (R - 36) * math.sin(a),
                    cx + (R - 8) * math.cos(a), cy + (R - 8) * math.sin(a)],
                   fill=pal["ink"], width=10)
    if wedge_to is not None:                       # 从十二点起量到某一分钟的扇形
        d.pieslice([cx - R * 0.62, cy - R * 0.62, cx + R * 0.62, cy + R * 0.62],
                   -90, wedge_to * 6 - 90, fill=pal["accent"])
    def hand(angle_deg, length, width):
        a = math.radians(angle_deg - 90)
        d.line([cx, cy, cx + length * math.cos(a), cy + length * math.sin(a)],
               fill=pal["ink"], width=width)
    # 时针短而粗、分针长而细。上一版两者的长度写反了（hour 画长、minute 画短），
    # 于是「三点整」看起来成了时针指 12、分针指 3 —— 角度全对，针却认错了。
    # 构造清单写着「时针指 3」反而掩盖了它：程序画保证得了角度，保证不了参数映射。
    # 第三版。前两版长度确实是「时针短分针长」，但时针只到半径一半、离圆心太近，
    # 视觉重心全落在那根几乎顶到边的细长针上，一眼读成「长针指 3」。
    # 这一版把差别压在「粗」上：时针拉长到 0.62R 但明显更粗，分针细到 12。
    if minute is not None:
        hand(minute * 6, R * 0.86, 12)        # 分针：最长、最细
    if hour is not None:
        hand((hour % 12 + (minute or 0) / 60) * 30, R * 0.62, 34)   # 时针：稍短、很粗
    if second is not None:
        hand(second * 6, R * 0.86, 7)
    disc(d, cx, cy, 16, pal["ink"], pal, w=3)
    return R


@page("clock", 2)
def _(d, pal):
    """十二个数字围成一圈 —— 先只画刻度，不画针。"""
    clock_face(d, S / 2, S / 2, 380, pal, ticks=12)
    return "1 个钟面 + 12 个刻度，没有指针"


@page("clock", 3)
def _(d, pal):
    """短针叫时针，走得很慢。"""
    clock_face(d, S / 2, S / 2, 380, pal, ticks=12, hour=12)
    return "1 个钟面 + 只有 1 根短的时针，指向正上"


@page("clock", 4)
def _(d, pal):
    """长针叫分针，一圈六十分钟。"""
    clock_face(d, S / 2, S / 2, 360, pal, ticks=12, minute=0)
    cx, cy, R = S / 2, S / 2, 360
    for i in range(10):                            # 一圈的走向，用一串小箭头表示
        a0 = math.radians(i * 36 - 84)
        a1 = math.radians(i * 36 - 60)
        arrow(d, cx + (R + 46) * math.cos(a0), cy + (R + 46) * math.sin(a0),
              cx + (R + 46) * math.cos(a1), cy + (R + 46) * math.sin(a1), pal, w=6, head=16)
    return "1 个钟面 + 只有 1 根长的分针 + 外圈 10 个同向箭头"


@page("clock", 5)
def _(d, pal):
    """分针走完一圈，时针才挪一格。"""
    for (cx, cy, w_, h_), t in zip(panel2(d, pal), ((12, 0), (1, 0))):
        clock_face(d, cx, cy, min(w_, h_) * 0.40, pal, ticks=12, hour=t[0], minute=t[1])
    return "左格 12:00 / 右格 1:00，时针挪了 1 格、分针回到原处"


@page("clock", 6)
def _(d, pal):
    """整点：短针指 3，长针指 12。"""
    clock_face(d, S / 2, S / 2, 380, pal, ticks=12, hour=3, minute=0)
    return "1 个钟面，时针指 3、分针指 12（三点整）"


@page("clock", 7)
def _(d, pal):
    """半点：长针指下面，短针在两个数字中间。"""
    clock_face(d, S / 2, S / 2, 380, pal, ticks=12, hour=3, minute=30)
    return "1 个钟面，分针指 6、时针在 3 和 4 中间（三点半）"


@page("clock", 8)
def _(d, pal):
    """一圈六十个小格，每五个一大格。"""
    clock_face(d, S / 2, S / 2, 380, pal, minute_ticks=True)
    return "1 个钟面 + 60 个小刻度，每第 5 个加粗"


@page("clock", 9)
def _(d, pal):
    """长针走到第一个数字，是五分钟。"""
    clock_face(d, S / 2, S / 2, 380, pal, minute_ticks=True, minute=5, wedge_to=5)
    return "1 个钟面，分针指 5 分处 + 从 12 点量过来的扇形"


@page("clock", 10)
def _(d, pal):
    """还有一根更细的秒针。"""
    clock_face(d, S / 2, S / 2, 380, pal, minute_ticks=True, hour=10, minute=8, second=40)
    return "1 个钟面 + 时针、分针、秒针三根，指向各不相同"


@page("clock", 11)
def _(d, pal):
    """先看短针在几和几之间，再看长针走了几格。"""
    clock_face(d, S / 2, S / 2, 380, pal, minute_ticks=True, hour=7, minute=20)
    return "1 个钟面，时针在 7 和 8 之间、分针指 20 分处"


# ---------------------------------------------------------------- A 类最后一批（meteor / sky / sundial / crab / power / fish）

@page("meteor", 3)
def _(d, pal):
    """太空里的小石头绕着太阳跑 —— 一条环带，不是地上的路。"""
    cx, cy = S / 2, S / 2
    disc(d, cx, cy, 92, pal["accent"], pal, w=9)
    rnd = random.Random(13)
    for i in range(26):                                   # 石头沿一条宽环带分布
        a = rnd.uniform(0, 2 * math.pi)
        r = rnd.uniform(280, 400)
        disc(d, cx + r * math.cos(a), cy + r * math.sin(a) * 0.86,
             rnd.uniform(9, 18), pal["bark"], pal, w=4)
    d.ellipse([cx - 400, cy - 344, cx + 400, cy + 344], outline=pal["soft"], width=5)
    d.ellipse([cx - 280, cy - 240, cx + 280, cy + 240], outline=pal["soft"], width=5)
    return "1 个太阳 + 26 块石头分布在一条环带上"


@page("meteor", 5)
def _(d, pal):
    """石头冲进空气，前面的空气被挤得又热又亮 —— 亮的在石头前方。"""
    # 上一版把发亮弧画成一道拱悬在石头上方，像彩虹；正文说亮的在石头「前面」。
    # 石头自右上飞向左下，发亮楔形就贴在它左下方的行进前侧。
    cx, cy = S / 2 + 40, S / 2 - 20
    d.line([0, 760, S, 700], fill=pal["soft"], width=6)                 # 空气层顶界
    ang = math.radians(215)                                             # 行进方向：左下
    for i in range(5):                                                   # 五道弧，越靠前越大
        k = 0.5 + i * 0.22
        r = 90 * k
        px, py = cx + (60 + i * 26) * math.cos(ang), cy + (60 + i * 26) * math.sin(ang)
        d.arc([px - r, py - r, px + r, py + r],
              math.degrees(ang) - 70, math.degrees(ang) + 70,
              fill=pal["accent"], width=11)
    disc(d, cx, cy, 46, pal["bark"], pal, w=8)
    arrow(d, cx + 230, cy - 190, cx + 80, cy - 66, pal, w=10, head=26)  # 来向
    return "1 块石头（居中）+ 行进前方 5 道发亮弧 + 1 支来向箭头"


@page("meteor", 8)
def _(d, pal):
    """地球穿过一条布满尘粒的路，于是看到许多流星。"""
    cx, cy = S / 2 - 120, S / 2
    band_y = cy + 40
    rnd = random.Random(17)
    for _ in range(120):                                                 # 尘带：一条斜向的带
        t = rnd.uniform(0, 1)
        x = 200 + t * (S - 120)
        y = band_y + (t - 0.5) * 160 + rnd.uniform(-26, 26)
        disc(d, x, y, rnd.uniform(2, 5), pal["soft"], pal, w=1)
    disc(d, cx, cy, 130, pal["bark"], pal, w=9)
    for i in range(5):                                                   # 迎着尘带的一侧有流星条纹
        y = cy - 90 + i * 46
        d.line([cx + 120, y, cx + 190, y - 26], fill=pal["accent"], width=7)
    arrow(d, cx - 230, cy, cx - 150, cy, pal, w=10, head=26)
    return "1 个地球 + 1 条尘带 + 迎面 5 道流星条纹 + 1 支行进箭头"


@page("meteor", 10)
def _(d, pal):
    """彗尾总是背着太阳。"""
    sx, sy = MARGIN + 110, S / 2
    disc(d, sx, sy, 96, pal["accent"], pal, w=9)
    hx, hy = S - MARGIN - 300, S / 2 - 60
    disc(d, hx, hy, 54, pal["paper"], pal, w=8)
    rnd = random.Random(23)
    for _ in range(90):                                                  # 尾巴：从彗核背离太阳方向铺开
        t = rnd.uniform(0, 1)
        spread_ = 26 + t * 120
        x = hx + t * 300
        y = hy + rnd.uniform(-spread_, spread_) * 0.7
        disc(d, x, y, rnd.uniform(2, 6), pal["soft"], pal, w=1)
    arrow(d, hx + 70, hy - 150, hx + 250, hy - 200, pal, w=8, head=22)
    return "1 个太阳（左）+ 1 个彗核 + 1 条朝右背离太阳的尾巴"


@page("sky", 4)
def _(d, pal):
    """蓝光被撞得到处跑，红光几乎直直穿过去。"""
    for (cx, cy, w_, h_), scatter in zip(panel2(d, pal), (True, False)):
        col = pal["accent"] if not scatter else pal["soft"]
        disc(d, cx, cy, 26, pal["ink"], pal, w=5)
        arrow(d, cx - w_ * 0.40, cy, cx - 40, cy, pal, w=9, head=24)
        if scatter:
            for i in range(7):                                           # 撞散：多方向射出
                a = -1.2 + i * 0.4
                arrow(d, cx + 30 * math.cos(a), cy + 30 * math.sin(a),
                      cx + 170 * math.cos(a), cy + 170 * math.sin(a), pal, w=7, head=20)
        else:
            arrow(d, cx + 40, cy, cx + w_ * 0.40, cy, pal, w=9, head=24)
    return "左格：1 支入射 + 7 支散开（蓝光）/ 右格：1 支入射 + 1 支直穿（红光）"


@page("sky", 10)
def _(d, pal):
    """月亮上没有空气，太阳照着天也是黑的。"""
    d.rectangle([0, 0, S, S], fill="#12141c")
    rnd = random.Random(31)
    for _ in range(70):
        x, y = rnd.uniform(20, S - 20), rnd.uniform(20, 620)
        r = rnd.choice((2, 2, 3))
        d.ellipse([x - r, y - r, x + r, y + r], fill=pal["paper"])
    disc(d, S / 2 + 230, 220, 90, pal["accent"], pal, w=8)               # 太阳当空
    d.pieslice([-200, 620, S + 200, S + 500], 180, 360,
               fill=pal["soft"], outline=pal["ink"], width=8)            # 月面
    rnd2 = random.Random(5)
    for _ in range(9):
        x = rnd2.uniform(60, S - 60)
        y = rnd2.uniform(700, 900)
        r = rnd2.uniform(18, 46)
        d.ellipse([x - r, y - r * 0.5, x + r, y + r * 0.5],
                  outline=pal["ink"], width=5)
    return "黑天 + 70 颗星 + 1 个太阳 + 1 片带 9 个环形坑的月面"


@page("sundial", 7)
def _(d, pal):
    """八点、九点、十点各画一个记号 —— 三个记号必须都在。"""
    gy = 700
    d.rectangle([0, gy, S, S], fill=pal["bark"])
    d.line([0, gy, S, gy], fill=pal["ink"], width=8)
    cx = S / 2 + 120
    d.rounded_rectangle([cx - 16, gy - 340, cx + 16, gy], radius=10,
                        fill=pal["paper"], outline=pal["ink"], width=8)  # 直立的棍子
    for i, (dx, ln) in enumerate(((-430, 300), (-300, 210), (-190, 140))):
        d.line([cx, gy + 20, cx + dx, gy + 20 + ln * 0.30],
               fill=pal["soft"], width=9)                                # 三条影子
        d.ellipse([cx + dx - 22, gy + 20 + ln * 0.30 - 22,
                   cx + dx + 22, gy + 20 + ln * 0.30 + 22],
                  fill=pal["accent"], outline=pal["ink"], width=6)       # 三个记号
    return "1 根直立的棍子 + 3 条影子 + 3 个记号"


@page("sundial", 9)
def _(d, pal):
    """阴天没有影子：一朵云遮住太阳，棍子脚下什么都没有。"""
    gy = 700
    d.rectangle([0, gy, S, S], fill=pal["bark"])
    d.line([0, gy, S, gy], fill=pal["ink"], width=8)
    cx = S / 2
    d.rounded_rectangle([cx - 16, gy - 340, cx + 16, gy], radius=10,
                        fill=pal["paper"], outline=pal["ink"], width=8)
    for dx, dy, r in ((-150, 0, 90), (-30, -40, 110), (110, 0, 86), (0, 30, 100)):
        disc(d, cx + dx, 250 + dy, r, pal["soft"], pal, w=7)             # 一朵厚云
    return "1 根直立的棍子 + 1 朵遮住天空的云，地上没有影子"


@page("sundial", 10)
def _(d, pal):
    """夏天太阳走得高，冬天走得低 —— 两条弧高低必须差得出来。"""
    gy = 760
    d.line([0, gy, S, gy], fill=pal["ink"], width=8)
    d.arc([MARGIN, gy - 620, S - MARGIN, gy + 620], 180, 360,
          fill=pal["accent"], width=14)                                  # 夏：高
    d.arc([MARGIN + 120, gy - 250, S - MARGIN - 120, gy + 250], 180, 360,
          fill=pal["soft"], width=14)                                    # 冬：低
    disc(d, S / 2, gy - 620, 40, pal["accent"], pal, w=7)
    disc(d, S / 2, gy - 250, 36, pal["soft"], pal, w=7)
    return "1 条地平线 + 1 条高弧（夏）+ 1 条低弧（冬）"


@page("crab", 9)
def _(d, pal):
    """一队寄居蟹，每只都背着壳，旧壳留给小的。"""
    xs, slot = lay(5)
    for i, cx in enumerate(xs):
        R = 88 - i * 12
        disc(d, cx, S / 2, R, pal["paper"], pal, w=8)                    # 壳
        for k in range(3):                                               # 壳上的螺旋
            rr = R * (0.72 - k * 0.22)
            d.arc([cx - rr, S / 2 - rr, cx + rr, S / 2 + rr], 20, 300,
                  fill=pal["ink"], width=5)
        for s in (-1, 1):                                                # 露出的脚
            d.line([cx + s * R * 0.6, S / 2 + R * 0.7,
                    cx + s * (R + 40), S / 2 + R + 30], fill=pal["ink"], width=7)
    return "5 只寄居蟹排成一队，壳一只比一只小，每只都背着壳"


@page("power", 8)
def _(d, pal):
    """电表在前、配电箱在后：一进一出，顺序不能反。"""
    cy = S / 2
    mx, bx = MARGIN + 200, S - MARGIN - 240
    d.rounded_rectangle([mx - 110, cy - 130, mx + 110, cy + 130], radius=20,
                        fill=pal["paper"], outline=pal["ink"], width=9)  # 电表
    disc(d, mx, cy - 20, 58, pal["soft"], pal, w=7)
    d.rounded_rectangle([bx - 120, cy - 160, bx + 120, cy + 160], radius=20,
                        fill=pal["bark"], outline=pal["ink"], width=9)   # 配电箱
    arrow(d, MARGIN - 10, cy, mx - 120, cy, pal, w=10, head=26)          # 进线
    arrow(d, mx + 120, cy, bx - 130, cy, pal, w=10, head=26)             # 表→箱
    for i, dy in enumerate((-90, 0, 90)):                                # 箱→三路
        arrow(d, bx + 130, cy + dy, S - MARGIN + 10, cy + dy, pal, w=9, head=24)
    return "进线 → 电表 → 配电箱 → 3 路出线，箭头全部同向"


# ---------------------------------------------------------------- 生物剖面与过程图（批量写，抽样验收）

def seed_halves(d, cx, cy, R, pal, gap=18):
    """一颗豆子剖开：两片厚子叶面对面，中间一道缝，缝里一个小芽。"""
    d.pieslice([cx - gap / 2 - R, cy - R, cx - gap / 2 + R, cy + R], 90, 270,
               fill=pal["paper"], outline=pal["ink"], width=8)
    d.pieslice([cx + gap / 2 - R, cy - R, cx + gap / 2 + R, cy + R], 270, 90,
               fill=pal["paper"], outline=pal["ink"], width=8)
    return cx, cy


@page("sprout", 2)
def _(d, pal):
    """剖开一颗豆子：里面是两片厚子叶，不是一荚好几颗。"""
    cx, cy = S / 2, S / 2
    seed_halves(d, cx, cy, 230, pal, gap=26)
    d.line([cx, cy - 80, cx, cy + 120], fill=pal["accent"], width=12)   # 中间的小芽
    d.line([cx, cy - 80, cx - 44, cy - 140], fill=pal["accent"], width=10)
    d.line([cx, cy - 80, cx + 44, cy - 140], fill=pal["accent"], width=10)
    return "1 颗豆子剖开 = 2 片子叶 + 1 个小芽"


@page("sprout", 3)
def _(d, pal):
    """两片子叶中间藏着小芽：上面长茎叶，下面长根。"""
    cx, cy = S / 2, S / 2
    seed_halves(d, cx, cy, 210, pal, gap=150)
    d.line([cx, cy - 140, cx, cy + 60], fill=pal["accent"], width=14)
    d.line([cx, cy - 140, cx - 50, cy - 200], fill=pal["accent"], width=11)
    d.line([cx, cy - 140, cx + 50, cy - 200], fill=pal["accent"], width=11)
    for i, dx in enumerate((-46, 0, 46)):                               # 三条根往下
        d.line([cx, cy + 60, cx + dx, cy + 230], fill=pal["bark"], width=9)
    return "2 片子叶 + 中间 1 个芽（上 2 片叶 / 下 3 条根）"


@page("sprout", 6)
def _(d, pal):
    """最先钻出来的是根：只有根，还没有叶子。"""
    gy = 420
    d.rectangle([0, gy, S, S], fill=pal["bark"])
    d.line([0, gy, S, gy], fill=pal["ink"], width=8)
    cx = S / 2
    seed_halves(d, cx, gy + 90, 84, pal, gap=12)
    d.line([cx, gy + 174, cx, gy + 400], fill=pal["paper"], width=14)   # 一条主根向下
    for dx, dy in ((-60, 330), (60, 350)):
        d.line([cx, gy + 260, cx + dx, gy + dy], fill=pal["paper"], width=9)
    return "1 颗豆子在土里 + 1 条主根 + 2 条侧根，地面上什么都没有"


@page("sprout", 7)
def _(d, pal):
    """弯着腰像个钩子，用背顶开土 —— 芽还没出土。"""
    gy = 380
    d.rectangle([0, gy, S, S], fill=pal["bark"])
    d.line([0, gy, S, gy], fill=pal["ink"], width=8)
    cx = S / 2
    pts = [(cx, gy + 380), (cx, gy + 200), (cx - 30, gy + 90), (cx - 110, gy + 70)]
    d.line(pts, fill=pal["paper"], width=16, joint="curve")
    d.line([cx, gy + 380, cx, gy + 470], fill=pal["paper"], width=10)
    return "1 株弯成钩形的芽，钩顶仍在土面以下"


@page("sprout", 8)
def _(d, pal):
    """钻出地面，举起两片厚子叶。"""
    gy = 620
    d.rectangle([0, gy, S, S], fill=pal["bark"])
    d.line([0, gy, S, gy], fill=pal["ink"], width=8)
    cx = S / 2
    d.line([cx, gy, cx, gy - 240], fill=pal["accent"], width=14)
    for s in (-1, 1):
        d.ellipse([cx + s * 20 - (0 if s > 0 else 150), gy - 300,
                   cx + s * 20 + (150 if s > 0 else 0), gy - 200],
                  fill=pal["paper"], outline=pal["ink"], width=8)
    return "1 根茎 + 2 片厚子叶（地面之上）"


@page("sprout", 10)
def _(d, pal):
    """真叶长出来，两片子叶变黄、掉下来。"""
    gy = 660
    d.rectangle([0, gy, S, S], fill=pal["bark"])
    d.line([0, gy, S, gy], fill=pal["ink"], width=8)
    cx = S / 2
    d.line([cx, gy, cx, gy - 380], fill=pal["accent"], width=14)
    for s in (-1, 1):                                                   # 上方两片绿真叶
        d.ellipse([cx + s * 24 - (0 if s > 0 else 140), gy - 430,
                   cx + s * 24 + (140 if s > 0 else 0), gy - 340],
                  fill=pal["accent"], outline=pal["ink"], width=7)
    for s in (-1, 1):                                                   # 下方两片黄子叶
        d.ellipse([cx + s * 20 - (0 if s > 0 else 110), gy - 190,
                   cx + s * 20 + (110 if s > 0 else 0), gy - 120],
                  fill=pal["bark"], outline=pal["ink"], width=7)
    return "上 2 片绿真叶 + 下 2 片黄子叶"


@page("sprout", 11)
def _(d, pal):
    """光从一边来，茎就朝那边弯。"""
    gy = 700
    d.rectangle([0, gy, S, S], fill=pal["bark"])
    d.line([0, gy, S, gy], fill=pal["ink"], width=8)
    for i in range(4):                                                  # 左侧射来的光线
        y = 200 + i * 90
        arrow(d, 60, y, 300, y + 30, pal, w=8, head=22)
    cx = 660
    pts = [(cx, gy), (cx - 40, gy - 180), (cx - 140, gy - 300)]
    d.line(pts, fill=pal["accent"], width=16, joint="curve")
    d.ellipse([cx - 250, gy - 350, cx - 100, gy - 270],
              fill=pal["paper"], outline=pal["ink"], width=8)
    return "4 支自左射来的光 + 1 株朝左弯的茎"


@page("hiccup", 2)
def _(d, pal):
    """膈肌是胸腔下面一块平平的、像伞一样的肉。"""
    # 正面对称构图（方框 + 两个圆 + 一道横弧）无论怎么配色都读成人脸，已经错两次。
    # 换成侧视剖面：身体侧着朝左，肺在上方、膈肌是一道横贯身体的弧 —— 对称性一破，
    # 脸就不成立了。这和 magnet p9 退成指南针是同一个判断：参数调不动时，问题在构图。
    # 第三次了。正面对称读成脸，侧视剖面读成歪盒子 —— 扁平几何画不出「立体结构」。
    # 退成最朴素的画法：一个竖向躯干轮廓，上部一片肺，中间一条明显的横线标出膈肌。
    # 同 magnet p9 退成指南针、bee p11 接受勺子：信息到位就不再追求「像解剖图」。
    cx, cy = S / 2, S / 2
    d.rounded_rectangle([cx - 200, cy - 340, cx + 200, cy + 340], radius=100,
                        fill=pal["paper"], outline=pal["ink"], width=10)
    d.ellipse([cx - 130, cy - 280, cx + 130, cy - 80],
              fill=pal["soft"], outline=pal["ink"], width=8)             # 肺，在上
    d.line([cx - 205, cy + 20, cx + 205, cy + 20], fill=pal["accent"], width=30)  # 膈肌，一条横线
    return "1 个躯干轮廓 + 上部 1 片肺 + 中间 1 条横线（膈肌）"


@page("hiccup", 3)
def _(d, pal):
    """吸气时膈肌下拉、肺变大；呼气时膈肌上顶、肺变小。"""
    for (cx, cy, w_, h_), inhale in zip(panel2(d, pal), (True, False)):
        lung_h = 190 if inhale else 120
        for s in (-1, 1):
            d.ellipse([cx + s * 22 - (0 if s > 0 else 130), cy - 200,
                       cx + s * 22 + (130 if s > 0 else 0), cy - 200 + lung_h],
                      fill=pal["soft"], outline=pal["ink"], width=7)
        dy = 90 if inhale else 0
        d.arc([cx - 170, cy + dy - 40, cx + 170, cy + dy + 140], 180, 360,
              fill=pal["accent"], width=16)
        arrow(d, cx, cy + dy + 180, cx, cy + dy + (250 if inhale else 110), pal, w=10, head=26)
    return "左格：膈肌下拉、肺大、箭头向下 / 右格：膈肌上顶、肺小、箭头向上"


@page("hiccup", 5)
def _(d, pal):
    """声门啪地关上，空气撞在关着的门上 —— 这是喉咙，不是胃。"""
    cx, cy = S / 2, S / 2
    d.rounded_rectangle([cx - 130, cy - 330, cx + 130, cy + 330], radius=40,
                        fill=pal["paper"], outline=pal["ink"], width=9)  # 气管
    d.line([cx - 130, cy, cx + 130, cy], fill=pal["accent"], width=22)   # 关闭的声门
    arrow(d, cx, cy + 260, cx, cy + 60, pal, w=12, head=32)              # 空气自下撞上来
    return "1 条气管 + 1 道关闭的声门 + 1 支自下而上的箭头"


@page("bird", 4)
def _(d, pal):
    """鸟的骨头是空心的，里面有细细的支架。"""
    cx, cy = S / 2, S / 2
    d.rounded_rectangle([cx - 330, cy - 90, cx + 330, cy + 90], radius=90,
                        fill=pal["paper"], outline=pal["ink"], width=10)
    for i in range(7):                                                   # 内部斜撑
        x = cx - 260 + i * 87
        d.line([x, cy - 70, x + 60, cy + 70], fill=pal["soft"], width=8)
        d.line([x + 60, cy - 70, x, cy + 70], fill=pal["soft"], width=8)
    return "1 段空心骨 + 7 组交叉支架"


@page("bird", 5)
def _(d, pal):
    """机翼上面拱起、下面平直。"""
    cx, cy = S / 2, S / 2
    # 上一版只用 d.line 画轮廓，翼面是空心梯形；气流又飘在离翼很远的上方。
    # 改成填充实心翼面，气流贴着上表面走。
    # 翼面用 soft（深褐）填充时和黑描边糊成一团，下缘的直线也被盖住，
    # 「上拱下平」看不出来。改成浅色翼面 + 最后单独压一条深色下缘线。
    pts = [(cx - 320, cy), (cx - 180, cy - 110), (cx + 60, cy - 120), (cx + 320, cy)]
    d.polygon(pts, fill=pal["paper"])
    for a, b in zip(pts, pts[1:] + pts[:1]):
        d.line([a, b], fill=pal["ink"], width=8)
    d.line([cx - 320, cy, cx + 320, cy], fill=pal["ink"], width=16)      # 平直的下缘，压在最上层
    for i in range(3):                                                   # 紧贴上表面的气流
        y = cy - 160 - i * 46
        arrow(d, cx - 330, y, cx + 330, y - 10, pal, w=7, head=20)
    arrow(d, cx, cy + 180, cx, cy + 44, pal, w=12, head=30)              # 升力向上
    return "1 个浅色翼面（上拱、下缘一条粗直线）+ 上方 3 支贴面气流 + 1 支升力箭头"


@page("bird", 9)
def _(d, pal):
    """三种翅膀：又长又窄、又短又圆、很尖。"""
    shapes = (((-1, 0), (0.0, -0.30), (0.9, -0.16), (1, 0)),            # 长窄
              ((-1, 0), (-0.2, -0.62), (0.5, -0.40), (1, 0)),           # 短圆
              ((-1, 0), (0.3, -0.50), (0.8, -0.06), (1, 0)))            # 尖
    for k, sh in enumerate(shapes):
        cx = MARGIN + 170 + k * 300
        cy = S / 2 + 80
        pts = [(cx + x * 150, cy + y * 300) for x, y in sh]
        d.line(pts + [pts[0]], fill=pal["ink"], width=10, joint="curve")
    return "3 种翅形：长窄 / 短圆 / 尖"


@page("rocket", 6)
def _(d, pal):
    """烧完一段就扔掉一段：下面那一级正在脱开。"""
    cx = S / 2
    d.polygon([(cx, 120), (cx - 70, 300), (cx + 70, 300)], fill=pal["accent"])
    d.rounded_rectangle([cx - 70, 300, cx + 70, 520], radius=14,
                        fill=pal["paper"], outline=pal["ink"], width=8)
    d.rounded_rectangle([cx - 70, 620, cx + 70, 860], radius=14,
                        fill=pal["soft"], outline=pal["ink"], width=8)   # 脱开的一级，有明显间隙
    arrow(d, cx + 150, 660, cx + 150, 860, pal, w=10, head=26)
    return "上段火箭 + 下段已脱开（中间 100px 间隙）+ 1 支下落箭头"


@page("rocket", 7)
def _(d, pal):
    """最上面那一小截飞上去：只有小小的返回舱，没有整枚火箭。"""
    cx, cy = S / 2, S / 2
    d.polygon([(cx, cy - 200), (cx - 120, cy + 60), (cx + 120, cy + 60)], fill=pal["accent"])
    for a, b in (((cx, cy - 200), (cx - 120, cy + 60)), ((cx - 120, cy + 60), (cx + 120, cy + 60)),
                 ((cx + 120, cy + 60), (cx, cy - 200))):
        d.line([a, b], fill=pal["ink"], width=9)
    disc(d, cx, cy - 40, 44, pal["paper"], pal, w=7)                     # 舷窗
    return "1 个小返回舱（圆锥 + 1 个舷窗），没有箭体和尾焰"


@page("rocket", 10)
def _(d, pal):
    """返回舱冲进大气层，外面烧得通红 —— 它在往下掉。"""
    cx = S / 2
    d.arc([cx - 460, 180, cx + 460, 620], 0, 180, fill=pal["soft"], width=14)  # 大气层弧
    d.polygon([(cx, 620), (cx - 110, 400), (cx + 110, 400)], fill=pal["accent"])
    for a, b in (((cx, 620), (cx - 110, 400)), ((cx - 110, 400), (cx + 110, 400)),
                 ((cx + 110, 400), (cx, 620))):
        d.line([a, b], fill=pal["ink"], width=9)
    arrow(d, cx, 700, cx, 880, pal, w=12, head=32)                        # 向下
    return "1 道大气层弧 + 1 个尖端朝下的返回舱 + 1 支向下箭头"


# ---------------------------------------------------------------- 数学书剩下的计数与等分页

@page("minus", 8)
def _(d, pal):
    """三块饼干拿不走五块：三个圆，五个叉，有两个叉底下没有圆。"""
    xs, slot = lay(5)
    for i, cx in enumerate(xs):
        if i < 3:
            disc(d, cx, 560, 74, pal["accent"], pal, w=10)
        cross(d, cx, 560, 74, pal, w=14)
    return "3 个圆 + 5 个叉，最后 2 个叉下面没有圆"


@page("minus", 9)
def _(d, pal):
    """十三减五：一捆十根加三根散的，从捆里抽走五根。"""
    # 上一版三组东西各摆各的：捆没传 slot 退回默认宽度、三散棍甩在最右、
    # 抽出的五根孤零零在下方。改成「捆 + 紧贴其右的三根散」为一组居左，
    # 抽出的五根在其正下方，中间一支箭头连起来。
    bw = bundle_span()
    left = MARGIN + 40
    bundle(d, left + bw / 2, 400, pal, h=300)
    sx = left + bw + 40
    for i in range(3):
        stick(d, sx + i * 44, 400, 300, pal, half=STICK_W / 2, w=STICK_EDGE)
    arrow(d, left + bw / 2, 580, left + bw / 2, 690, pal, w=11, head=28)
    for i in range(5):                                  # 抽走的五根，正下方，同为强调色
        stick(d, left + bw / 2 + (i - 2) * 46, 830, 220, pal, pal["accent"],
              half=STICK_W / 2, w=STICK_EDGE)
    return "1 捆 ×10 根 + 紧邻 3 根散 → 下方抽出 5 根"


@page("tens", 4)
def _(d, pal):
    """三捆四根，写成 34：捆在左、散在右，位置对应十位和个位。"""
    bw = bundle_span()
    for cx in spread(3, bw, pad=BUNDLE_PAD):
        bundle(d, cx - 120, 460, pal, h=300)
    for i, cx in enumerate(spread(4, STICK_W, pad=52)):
        stick(d, cx + 300, 460, 300, pal, half=STICK_W / 2, w=STICK_EDGE)
    d.line([S / 2 + 60, 200, S / 2 + 60, 760], fill=pal["soft"], width=6)
    return "左边 3 捆（十位）+ 右边 4 根散（个位），中间一条分隔线"


@page("plus", 2)
def _(d, pal):
    """一加一等于二：左边一个，右边一个，合起来两个。"""
    disc(d, 180, S / 2, 88, pal["accent"], pal, w=10)
    d.line([320, S / 2, 420, S / 2], fill=pal["ink"], width=16)      # 加号
    d.line([370, S / 2 - 50, 370, S / 2 + 50], fill=pal["ink"], width=16)
    disc(d, 560, S / 2, 88, pal["accent"], pal, w=10)
    d.line([690, S / 2 - 26, 790, S / 2 - 26], fill=pal["ink"], width=14)  # 等号
    d.line([690, S / 2 + 26, 790, S / 2 + 26], fill=pal["ink"], width=14)
    for i, cx in enumerate((890, 890)):
        disc(d, cx, S / 2 - 92 + i * 184, 76, pal["accent"], pal, w=10)
    return "1 个 + 1 个 = 2 个"


@page("plus", 5)
def _(d, pal):
    """二加三等于五。"""
    # 上一版把 2 个、加号、3 个硬塞进一行，圆挤成一条、加号压在圆上、最右一个出画。
    # 改成：上行用 lay(7) 分槽 —— 槽 0,1 放两个，槽 2 放加号，槽 3,4,5 放三个；
    # 下行五个统一同色，表示「合起来就是 5 个」，不再按来源分色。
    xs, _ = lay(7)
    for cx in xs[:2]:
        disc(d, cx, 320, 68, pal["accent"], pal, w=9)
    px = xs[2]
    d.line([px - 46, 320, px + 46, 320], fill=pal["ink"], width=16)
    d.line([px, 274, px, 366], fill=pal["ink"], width=16)
    for cx in xs[3:6]:
        disc(d, cx, 320, 68, pal["accent"], pal, w=9)
    d.line([S / 2 - 64, 540, S / 2 + 64, 540], fill=pal["ink"], width=14)
    d.line([S / 2 - 64, 594, S / 2 + 64, 594], fill=pal["ink"], width=14)
    xs5, _ = lay(5)
    for cx in xs5:
        disc(d, cx, 800, 68, pal["accent"], pal, w=9)
    return "上行 2 个 + 3 个（中间加号）/ 下行 5 个同色"


@page("plus", 9)
def _(d, pal):
    """五块饼干吃掉两块：五个圆，前两个划掉。"""
    xs, _ = lay(5)
    for i, cx in enumerate(xs):
        disc(d, cx, S / 2, 82, pal["accent"] if i < 2 else pal["paper"], pal, w=10)
        if i < 2:
            cross(d, cx, S / 2, 82, pal, w=16)
    return "5 个圆，前 2 个划掉，剩 3 个"


@page("plus", 10)
def _(d, pal):
    """减号就是短短的一横 —— 只有一条。"""
    d.line([S / 2 - 180, S / 2, S / 2 + 180, S / 2], fill=pal["ink"], width=34)
    return "1 条横线（减号）"


@page("plus", 12)
def _(d, pal):
    """加起来一共十块：两排各五个。"""
    for cy in (380, 660):
        xs, _ = lay(5)
        for cx in xs:
            disc(d, cx, cy, 78, pal["accent"], pal, w=10)
    return "2 排 ×5 个 = 10 个"


@page("half", 5)
def _(d, pal):
    """五颗糖分两个人：左二右二，中间剩一颗。"""
    for cx in (200, 340):
        disc(d, cx, S / 2, 76, pal["accent"], pal, w=10)
    for cx in (684, 824):
        disc(d, cx, S / 2, 76, pal["soft"], pal, w=10)
    disc(d, S / 2, S / 2, 76, pal["paper"], pal, w=10)
    return "左 2 颗 + 右 2 颗 + 中间剩 1 颗 = 5 颗"


@page("half", 6)
def _(d, pal):
    """分给三个人，每人三分之一 —— 三块必须一样大。"""
    cx, cy, R = S / 2, S / 2, 270
    for i in range(3):
        a0, a1 = i * 120 - 90, (i + 1) * 120 - 90
        d.pieslice([cx - R, cy - R, cx + R, cy + R], a0, a1,
                   fill=pal["accent"] if i == 0 else pal["paper"],
                   outline=pal["ink"], width=9)
    return "1 个圆分成 3 块等大的扇形（每块 120 度）"


# ---------------------------------------------------------------- seasons / water / moon / teeth

@page("seasons", 3)
def _(d, pal):
    """地球斜着转：只有一根倾斜的地轴，不是两根交叉的杆。"""
    cx, cy, R = S / 2, S / 2, 230
    tilt = 0.41                                        # 约 23.5 度
    dx, dy = math.sin(tilt), -math.cos(tilt)
    d.line([cx - dx * (R + 150), cy - dy * (R + 150),
            cx + dx * (R + 150), cy + dy * (R + 150)], fill=pal["ink"], width=12)
    disc(d, cx, cy, R, pal["soft"], pal, w=9)
    for s in (-1, 1):                                  # 两极记号
        disc(d, cx + s * dx * R, cy + s * dy * R, 18, pal["accent"], pal, w=5)
    d.line([cx - R, cy, cx + R, cy], fill=pal["paper"], width=6)   # 赤道，帮助看出倾斜
    return "1 个地球 + 1 根倾斜地轴（约 23 度）+ 两极各 1 个记号"


@page("seasons", 4)
def _(d, pal):
    """一个太阳、两个地球：半年北边朝太阳，半年南边朝太阳。"""
    sun_cx = S / 2
    disc(d, sun_cx, S / 2, 96, pal["accent"], pal, w=9)
    tilt = 0.41
    dx, dy = math.sin(tilt), -math.cos(tilt)
    # 两个地球的地轴必须「一直歪向同一个方向」，所以 dx,dy 对两边完全一致，
    # side 只决定位置。上一版让 side 同时控制了倾斜符号，两根地轴歪成了八字。
    for side in (-1, 1):
        cx = sun_cx + side * 330
        R = 120
        d.line([cx - dx * (R + 70), S / 2 - dy * (R + 70),
                cx + dx * (R + 70), S / 2 + dy * (R + 70)], fill=pal["ink"], width=9)
        disc(d, cx, S / 2, R, pal["soft"], pal, w=8)
        # 朝着太阳的那一极标红：左边地球在太阳左侧，朝阳的是它的右半；
        # 地轴恒定歪向右上，于是左边亮北极（+），右边亮南极（-）。
        lit = 1 if side < 0 else -1
        disc(d, cx + lit * dx * R, S / 2 + lit * dy * R, 18, pal["accent"], pal, w=5)
    return "1 个太阳 + 2 个地球，两根地轴同向倾斜，朝太阳的那一极各标 1 个记号"


@page("water", 7)
def _(d, pal):
    """雨落下来：一部分顺坡流走，一部分渗进土里 —— 两种箭头方向必须分开。"""
    d.polygon([(0, 620), (S, 380), (S, S), (0, S)], fill=pal["bark"])
    d.line([(0, 620), (S, 380)], fill=pal["ink"], width=9)
    for i in range(6):                                  # 地表径流：顺坡向下
        x = 120 + i * 150
        y = 620 - (x / S) * 240
        arrow(d, x, y - 30, x + 90, y + 6, pal, w=8, head=22)
    for i in range(5):                                  # 下渗：垂直向下
        x = 180 + i * 170
        y = 620 - (x / S) * 240
        arrow(d, x, y + 40, x, y + 190, pal, w=8, head=22)
    return "1 条斜坡 + 6 支顺坡箭头（流走）+ 5 支垂直箭头（渗下去）"


@page("moon", 7)
def _(d, pal):
    """月亮绕地球转：一条轨道，箭头只指一个方向。"""
    cx, cy, R = S / 2, S / 2, 300
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=pal["soft"], width=6)
    disc(d, cx, cy, 110, pal["bark"], pal, w=9)
    for i in range(4):                                  # 四个箭头，全部逆时针同向
        a = i * math.pi / 2 + 0.3
        a2 = a + 0.34
        arrow(d, cx + R * math.cos(a), cy + R * math.sin(a),
              cx + R * math.cos(a2), cy + R * math.sin(a2), pal, w=9, head=24)
    disc(d, cx + R, cy, 46, pal["paper"], pal, w=7)
    return "1 个地球 + 1 条轨道 + 1 个月亮 + 4 个同向箭头"


@page("teeth", 4)
def _(d, pal):
    """上面十颗，下面十颗 —— 数目由构造保证。"""
    # 牙齿画成上宽下窄的梯形（像真牙），两排各自收成一道颌弧；
    # 上一版用圆角方块、弧张得太开，两端还叠在一起，读成两串珠子。
    cx = S / 2
    for cy, up in ((S / 2 - 40, True), (S / 2 + 40, False)):
        R = 300
        for i in range(10):
            a = math.pi * (0.10 + 0.80 * i / 9)
            ang = -a if up else a
            x = cx + R * math.cos(ang)
            y = cy + R * math.sin(ang) * 0.52
            w0, w1, h = 30, 21, 34                      # 冠宽、根宽、高
            top, bot = (y - h, y + h) if up else (y + h, y - h)
            pts = [(x - w0, top), (x + w0, top), (x + w1, bot), (x - w1, bot)]
            d.polygon(pts, fill=pal["paper"])
            for p, q in zip(pts, pts[1:] + pts[:1]):
                d.line([p, q], fill=pal["ink"], width=6)
    return "上颌 10 颗 + 下颌 10 颗（梯形牙冠）"


# ---------------------------------------------------------------- bee / snow（六边形）

@page("bee", 8)
def _(d, pal):
    """圆形之间留缝，六边形一个挨一个不留缝。"""
    (lx, ly, lw, lh), (rx, ry, rw, rh) = panel2(d, pal)
    cols = 5
    r = min(lw / (2 * cols), lh / (2 * cols)) * 0.92     # 半径由框反推，5×5 必然落在框内
    for j in range(cols):
        for i in range(cols):
            disc(d, lx + (i - (cols - 1) / 2) * 2 * r, ly + (j - (cols - 1) / 2) * 2 * r,
                 r - 3, pal["accent"], pal, w=5)
    n = hex_tile(d, rx, ry, 0, pal, rings=2, fill=pal["accent"], box=(rw, rh))
    return f"左 {cols * cols} 个圆（留缝）/ 右 {n} 个正六边形（不留缝）"


@page("snow", 6)
def _(d, pal):
    """雪花是六个角：板状和枝状各画一个，边数由 ngon 保证。"""
    ngon(d, S / 2 - 230, S / 2, 170, 6, pal, fill=pal["paper"], w=8, rot=math.pi / 2)
    cx, cy = S / 2 + 230, S / 2
    for i in range(6):
        a = math.pi / 2 + i * math.pi / 3
        x2, y2 = cx + 170 * math.cos(a), cy + 170 * math.sin(a)
        d.line([cx, cy, x2, y2], fill=pal["ink"], width=10)
        for t, ln in ((0.5, 52), (0.75, 36)):
            bx, by = cx + 170 * t * math.cos(a), cy + 170 * t * math.sin(a)
            for s in (+1, -1):
                d.line([bx, by, bx + ln * math.cos(a + s * 1.0),
                        by + ln * math.sin(a + s * 1.0)], fill=pal["ink"], width=7)
    return "左 1 个正六边形板 / 右 1 片六个角的枝状雪花"


# ---------------------------------------------------------------- 复审第二轮打回的 12 页（2026-09-13）
# 这批页重画过一次，第二次审还是错，错法全落在模型的老毛病上：
#   纸底纹    wind p8 画在撕边纸上、sleepwin p7 画在卷边旧纸上、doctor p7 浮在纸卡上
#   乱码字    post p4 告示牌、post p9 信箱铭牌、paper p9 两页假手写
#   摊开的书  paper p6 / paper p9 / doctor p5（paper 这本讲的就是纸，主体本身招书）
#   确数      thunder p7 该竖三根手指画了五根
#   比例      doctor p2 成年医生画成穿白大褂的小孩
# 都是「奶油底上摆一两个东西」的示意图。按 4.2b 交给程序：程序不会写字，
# 不会自带纸底纹，手指有几根由参数决定。

def finger(d, x, top, bottom, pal, half=30, w=10, fill=None):
    """一根手指：先填进掌里，再只描「左边—顶弧—右边」这个 U 形。

    直接画整个圆角矩形会在掌面上留一条横线（指根被自己的描边切断）。
    """
    d.rounded_rectangle([x - half, top, x + half, bottom], radius=half,
                        fill=fill or pal["paper"])
    d.arc([x - half, top, x + half, top + 2 * half], 180, 360, fill=pal["ink"], width=w)
    for s in (-1, 1):
        d.line([x + s * half, top + half, x + s * half, bottom], fill=pal["ink"], width=w)


@page("post", 4)
def _(d, pal):
    """邮筒里的信被收走，装进大袋子。铭牌一律不画 —— 模型两次都在那儿写乱码。"""
    ground = S - MARGIN - 130
    d.line([MARGIN, ground, S - MARGIN, ground], fill=pal["ink"], width=10)
    bx, bw = MARGIN + 250, 230
    d.rounded_rectangle([bx - bw / 2, ground - 540, bx + bw / 2, ground], radius=28,
                        fill=pal["accent"], outline=pal["ink"], width=10)
    d.pieslice([bx - bw / 2 - 14, ground - 640, bx + bw / 2 + 14, ground - 460], 180, 360,
               fill=pal["accent"], outline=pal["ink"], width=10)
    d.rounded_rectangle([bx - 76, ground - 450, bx + 76, ground - 408], radius=10,
                        fill=pal["ink"])                                  # 投信口
    sx = S - MARGIN - 280
    d.rounded_rectangle([sx - 190, ground - 330, sx + 190, ground], radius=70,
                        fill=pal["soft"], outline=pal["ink"], width=10)   # 鼓起来的袋身
    d.rounded_rectangle([sx - 92, ground - 430, sx + 92, ground - 300], radius=26,
                        fill=pal["soft"], outline=pal["ink"], width=10)   # 袋口
    d.line([sx - 96, ground - 330, sx + 96, ground - 330], fill=pal["ink"], width=10)
    for dx in (-44, 44):                                                  # 露出来的信封角
        d.rounded_rectangle([sx + dx - 46, ground - 500, sx + dx + 46, ground - 410],
                            radius=8, fill=pal["paper"], outline=pal["ink"], width=7)
    return "1 个邮筒（圆顶 + 1 条投信口）+ 1 个扎着口的邮袋，露出 2 个信封角；画面里没有字"


@page("post", 9)
def _(d, pal):
    """邮递员的车，和门口一排信箱。"""
    ground = S - MARGIN - 110
    d.line([MARGIN, ground, S - MARGIN, ground], fill=pal["ink"], width=10)
    x1, x2, R = MARGIN + 170, MARGIN + 400, 100
    for wx in (x1, x2):
        disc(d, wx, ground - R, R, pal["ground"], pal, w=12)
        disc(d, wx, ground - R, 24, pal["soft"], pal, w=6)
    seat, head = ((x1 + x2) / 2 - 10, ground - R - 180), (x2, ground - R - 160)
    for a, b in ((( x1, ground - R), seat), (seat, (x2, ground - R)),
                 (seat, head), (head, (x2, ground - R)), ((x1, ground - R), (x2, ground - R))):
        d.line([a, b], fill=pal["ink"], width=11)
    d.line([head, (x2 + 70, ground - R - 190)], fill=pal["ink"], width=11)     # 车把
    d.rounded_rectangle([x2 - 40, ground - R - 300, x2 + 110, ground - R - 175], radius=14,
                        fill=pal["soft"], outline=pal["ink"], width=8)         # 车筐
    for dx in (-6, 34, 74):                                                    # 筐里的信
        d.rounded_rectangle([x2 + dx - 26, ground - R - 350, x2 + dx + 26, ground - R - 290],
                            radius=6, fill=pal["paper"], outline=pal["ink"], width=6)
    bx0, bx1 = S - MARGIN - 400, S - MARGIN
    by0, by1 = ground - 450, ground - 150
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=16, fill=pal["soft"],
                        outline=pal["ink"], width=9)
    for leg in (bx0 + 40, bx1 - 70):
        d.rectangle([leg, by1, leg + 30, ground], fill=pal["ink"])
    bw_, bh_ = (bx1 - bx0 - 80) / 3, (by1 - by0 - 60) / 2
    for r_ in range(2):
        for c_ in range(3):
            cx_ = bx0 + 20 + c_ * (bw_ + 20) + bw_ / 2
            cy_ = by0 + 20 + r_ * (bh_ + 20) + bh_ / 2
            d.rounded_rectangle([cx_ - bw_ / 2, cy_ - bh_ / 2, cx_ + bw_ / 2, cy_ + bh_ / 2],
                                radius=10, fill=pal["paper"], outline=pal["ink"], width=7)
            d.rounded_rectangle([cx_ - bw_ * 0.30, cy_ - 12, cx_ + bw_ * 0.30, cy_ + 12],
                                radius=6, fill=pal["ink"])
    return "1 辆邮车（2 个轮子 + 1 个装 3 封信的筐）+ 1 组 6 个信箱（每个 1 条投信口）；画面里没有字"


@page("paper", 2)
def _(d, pal):
    """树干里那些很细的丝：从中心射向外圈，不是一圈一圈的年轮。"""
    cx, cy, R = S / 2, S / 2, 360
    disc(d, cx, cy, R, pal["paper"], pal, w=11)
    n = 60
    for i in range(n):
        a = 2 * math.pi * i / n
        d.line([cx + R * 0.12 * math.cos(a), cy + R * 0.12 * math.sin(a),
                cx + (R - 14) * math.cos(a), cy + (R - 14) * math.sin(a)],
               fill=pal["bark"] if i % 2 else pal["soft"], width=6)
    disc(d, cx, cy, R * 0.12, pal["soft"], pal, w=8)
    return f"1 个树干横截面 + {n} 条从中心射向外圈的细丝（整幅没有一个同心圆）"


@page("paper", 6)
def _(d, pal):
    """三种纸：软的、硬的、滑的。"""
    xs, slot = lay(3)
    cy = S / 2
    w_, h_ = min(slot * 0.70, 240), 400
    x = xs[0]                                                   # 抽纸：两边起皱
    pts = [(x - w_ / 2 + 20 * math.sin(i / 12 * 6 * math.pi), cy - h_ / 2 + i / 12 * h_)
           for i in range(13)]
    pts += [(x + w_ / 2 + 20 * math.sin((1 - i / 12) * 6 * math.pi), cy + h_ / 2 - i / 12 * h_)
            for i in range(13)]
    d.polygon(pts, fill=pal["paper"])
    d.line(pts + [pts[0]], fill=pal["ink"], width=7, joint="curve")
    x = xs[1]                                                   # 纸箱：侧面露出瓦楞
    d.rectangle([x - w_ / 2, cy - h_ / 2, x + w_ / 2, cy + h_ / 2],
                fill=pal["soft"], outline=pal["ink"], width=8)
    fy0, fy1 = cy + h_ / 2 - 96, cy + h_ / 2 - 24
    d.rectangle([x - w_ / 2, fy0, x + w_ / 2, fy1], fill=pal["paper"],
                outline=pal["ink"], width=6)
    step = 40
    flutes = int((w_ - 12) // step)
    for k in range(flutes):
        sx = x - w_ / 2 + 6 + k * step
        d.arc([sx, fy0 + 5, sx + step, fy1 - 5], 180, 360, fill=pal["ink"], width=6)
    x = xs[2]                                                   # 照片纸：一道斜高光
    d.rectangle([x - w_ / 2, cy - h_ / 2, x + w_ / 2, cy + h_ / 2],
                fill=pal["paper"], outline=pal["ink"], width=8)
    d.polygon([(x - w_ / 2 + 18, cy + h_ / 2 - 18), (x + w_ / 2 - 96, cy - h_ / 2 + 18),
               (x + w_ / 2 - 18, cy - h_ / 2 + 18), (x - w_ / 2 + 96, cy + h_ / 2 - 18)],
              fill=pal["ground"])
    return f"3 张纸样并排：1 张两边起皱的软纸 / 1 张露出 {flutes} 道瓦楞的硬纸板 / 1 张带斜高光的滑纸"


@page("paper", 9)
def _(d, pal):
    """一张纸的正面和反面，两面都写了。字迹只画成线条，不写字。"""
    boxes = panel2(d, pal)
    for (cx, cy, w_, h_), back in zip(boxes, (False, True)):
        for i in range(5):
            y = cy - h_ * 0.26 + i * h_ * 0.13
            short = 90 if i == 4 else 0
            d.line([cx - w_ * 0.32, y, cx + w_ * 0.32 - short, y], fill=pal["soft"], width=15)
        if back:                                                # 背面：折起来的一角
            k = 90
            d.polygon([(cx + w_ / 2 - k, cy - h_ / 2), (cx + w_ / 2, cy - h_ / 2),
                       (cx + w_ / 2, cy - h_ / 2 + k)], fill=pal["ground"])
            d.line([cx + w_ / 2 - k, cy - h_ / 2, cx + w_ / 2, cy - h_ / 2 + k],
                   fill=pal["ink"], width=7)
    (ax, _, aw, ah) = boxes[0]
    top = boxes[0][1] - ah / 2
    d.arc([ax, top - 150, boxes[1][0], top + 30], 180, 360, fill=pal["ink"], width=10)
    arrow(d, boxes[1][0] - 40, top - 58, boxes[1][0], top - 10, pal, w=10, head=26)
    return "左格：正面 5 行字迹 / 右格：背面 5 行字迹 + 折角，上方 1 支「翻过来」的弧形箭头（字迹是线条，不是字）"


@page("wind", 8)
def _(d, pal):
    """风能帮我们做事：帆船、风车、种子。直接画在底色上，不铺纸。"""
    xs, slot = lay(3)
    cy = S / 2
    x = xs[0]
    d.line([x - 160, cy + 160, x + 160, cy + 160], fill=pal["ink"], width=10)
    hull = [(x - 130, cy + 66), (x + 130, cy + 66), (x + 84, cy + 158), (x - 84, cy + 158)]
    d.polygon(hull, fill=pal["soft"])
    for a, b in zip(hull, hull[1:] + hull[:1]):
        d.line([a, b], fill=pal["ink"], width=8)
    d.line([x, cy + 60, x, cy - 210], fill=pal["ink"], width=10)
    sail = [(x + 12, cy - 200), (x + 140, cy + 40), (x + 12, cy + 40)]
    d.polygon(sail, fill=pal["accent"])
    for a, b in zip(sail, sail[1:] + sail[:1]):
        d.line([a, b], fill=pal["ink"], width=8)
    x = xs[1]
    tower = [(x - 36, cy + 220), (x + 36, cy + 220), (x + 16, cy - 120), (x - 16, cy - 120)]
    d.polygon(tower, fill=pal["paper"])
    for a, b in zip(tower, tower[1:] + tower[:1]):
        d.line([a, b], fill=pal["ink"], width=8)
    hub = (x, cy - 130)
    for i in range(3):
        a = math.radians(i * 120 - 90)
        blade = [(hub[0] + 28 * math.cos(a + 1.9), hub[1] + 28 * math.sin(a + 1.9)),
                 (hub[0] + 180 * math.cos(a), hub[1] + 180 * math.sin(a)),
                 (hub[0] + 28 * math.cos(a - 1.9), hub[1] + 28 * math.sin(a - 1.9))]
        d.polygon(blade, fill=pal["accent"])
        for p, q in zip(blade, blade[1:] + blade[:1]):
            d.line([p, q], fill=pal["ink"], width=7)
    disc(d, hub[0], hub[1], 28, pal["paper"], pal, w=7)
    x = xs[2]
    px, py, fluff = x + 10, cy - 60, 12
    for i in range(fluff):
        a = math.radians(i * 360 / fluff)
        d.line([px, py, px + 96 * math.cos(a), py + 96 * math.sin(a)],
               fill=pal["soft"], width=6)
    d.line([px, py, px - 30, cy + 160], fill=pal["ink"], width=8, joint="curve")
    disc(d, px - 30, cy + 160, 20, pal["accent"], pal, w=6)
    d.arc([x - 150, cy + 40, x + 190, cy + 300], 200, 330, fill=pal["soft"], width=8)
    return f"3 个并排的小图：1 条帆船（1 面帆）/ 1 座风车（3 片叶）/ 1 颗蒲公英种子（{fluff} 根绒毛）；底色上没有纸边"


@page("thunder", 7)
def _(d, pal):
    """数一数：竖起来的手指正好三根，由 slots 决定。

    上一版把掌、指、拇指当成几个圆角矩形分开画，深色填充又和这本的夜色底几乎同色，
    看着像散落的药丸。这版整只手是一条闭合轮廓，一次画完 —— 内部不会再有接缝。
    """
    cx, cy = S / 2, S / 2 + 90
    ptop, pbot, wrist = cy - 150, cy + 150, 862
    half, gap = 30, 72
    slots = [cx - 108, cx - 36, cx + 36, cx + 108]
    tips = [232, 232, 232, 408]          # 前三根竖起来，小指收着

    def cap(l, r, top, steps=14):
        """指尖的半圆，从左侧顶点走到右侧顶点。"""
        hw = (r - l) / 2
        mx, my = (l + r) / 2, top + hw
        return [(mx + hw * math.cos(a), my + hw * math.sin(a))
                for a in (math.pi + math.pi * i / steps for i in range(steps + 1))]

    pts = [(cx - 92, wrist), (cx - 92, pbot), (cx - 160, pbot), (cx - 160, 712)]
    pts += [(cx - 160 + 130 * math.cos(a), 651 + 61 * math.sin(a))      # 伸出去的拇指
            for a in (math.pi / 2 + math.pi * i / 14 for i in range(15))]
    pts += [(cx - 160, 590), (cx - 160, ptop)]
    for x, tip in zip(slots, tips):
        pts.append((x - half, ptop))
        pts += cap(x - half, x + half, tip)
        pts.append((x + half, ptop))
    pts += [(cx + 160, ptop), (cx + 160, pbot), (cx + 92, pbot), (cx + 92, wrist)]
    d.polygon(pts, fill=pal["soft"])
    d.line(pts + [pts[0]], fill=pal["ink"], width=10, joint="curve")
    up = sum(1 for t in tips if t < ptop - 100)
    return (f"1 只手，外轮廓一笔画完：{up} 根竖起的手指（等宽 {half * 2}px、等距 {gap}px）"
            f"+ 1 根收起的小指 + 1 根伸出去的拇指；掌和指之间没有横线")


@page("doctor", 2)
def _(d, pal):
    """医生是大人：身高按 6.7 个头画，靠比例而不是靠画风保证。"""
    cx = S / 2
    d.rectangle([cx - 190, 700, cx + 190, 736], fill=pal["soft"], outline=pal["ink"], width=8)
    for lx in (cx - 170, cx + 140):
        d.rectangle([lx, 736, lx + 30, 900], fill=pal["soft"], outline=pal["ink"], width=7)
    coat = [(cx - 150, 320), (cx + 150, 320), (cx + 120, 700), (cx - 120, 700)]
    for s in (-1, 1):                                            # 手臂：先粗描边再填色
        pts = [(cx + s * 140, 350), (cx + s * 190, 520), (cx + s * 120, 660)]
        d.line(pts, fill=pal["ink"], width=62, joint="curve")
        d.line(pts, fill=pal["paper"], width=46, joint="curve")
    d.polygon(coat, fill=pal["paper"])
    for a, b in zip(coat, coat[1:] + coat[:1]):
        d.line([a, b], fill=pal["ink"], width=9)
    for s in (-1, 1):
        d.line([cx + s * 62, 325, cx, 430], fill=pal["ink"], width=8)      # 翻领
        d.line([cx + s * 70, 336, cx + s * 24, 520], fill=pal["ink"], width=10,
               joint="curve")                                              # 听诊器管
        disc(d, cx + s * 120, 660, 28, pal["soft"], pal, w=7)              # 手
    disc(d, cx + 24, 556, 36, pal["accent"], pal, w=8)                     # 听诊器圆片
    for by in (480, 570):
        disc(d, cx, by, 12, pal["soft"], pal, w=5)
    for s in (-1, 1):                                                      # 腿
        d.line([cx + s * 70, 700, cx + s * 90, 840], fill=pal["ink"], width=76, joint="curve")
        d.line([cx + s * 70, 700, cx + s * 90, 840], fill=pal["soft"], width=60, joint="curve")
        d.rounded_rectangle([cx + s * 90 - 54, 846, cx + s * 90 + 54, 900], radius=18,
                            fill=pal["ink"])
    d.rectangle([cx - 18, 262, cx + 18, 322], fill=pal["paper"], outline=pal["ink"], width=8)
    head_r = 54
    disc(d, cx, 215, head_r, pal["paper"], pal, w=9)
    d.pieslice([cx - head_r - 4, 152, cx + head_r + 4, 258], 180, 360, fill=pal["ink"])
    for s in (-1, 1):
        disc(d, cx + s * 26, 224, 17, pal["ground"], pal, w=6)             # 眼镜
    d.line([cx - 9, 224, cx + 9, 224], fill=pal["ink"], width=6)
    d.arc([cx - 22, 238, cx + 22, 268], 0, 180, fill=pal["ink"], width=6)
    ratio = round((900 - (215 - head_r)) / (2 * head_r), 1)
    return f"1 位坐在凳子上的成年医生：身高 {ratio} 个头（小孩只有 4~5 个）+ 眼镜 + 白大褂 + 脖子上 1 个听诊器"


@page("doctor", 5)
def _(d, pal):
    """听诊器的金属圆片：中间没有孔，所以不会变成光盘。"""
    cx, cy = S / 2, S / 2 + 20
    disc(d, cx, cy, 300, pal["soft"], pal, w=12)
    disc(d, cx, cy, 244, pal["paper"], pal, w=9)
    d.arc([cx - 200, cy - 200, cx + 200, cy + 200], 186, 250, fill=pal["ground"], width=22)
    d.rounded_rectangle([cx - 44, cy - 400, cx + 44, cy - 286], radius=20,
                        fill=pal["soft"], outline=pal["ink"], width=9)      # 接管子的那截
    return "1 个金属圆片：1 圈外沿 + 1 块平面 + 1 道高光 + 上方 1 截管口；中间没有孔（不是光盘）"


@page("doctor", 7)
def _(d, pal):
    """创可贴本身，直接画在底色上 —— 不放在任何纸卡上。"""
    cx, cy = S / 2, S / 2
    bw, bh = 640, 230
    d.rounded_rectangle([cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2], radius=56,
                        fill=pal["accent"], outline=pal["ink"], width=10)
    d.rounded_rectangle([cx - 120, cy - 84, cx + 120, cy + 84], radius=14,
                        fill=pal["paper"], outline=pal["ink"], width=8)     # 药垫
    holes = 0
    for s in (-1, 1):
        for r_ in range(2):
            for c_ in range(3):
                hx = cx + s * (170 + c_ * 58)
                hy = cy - 40 + r_ * 80
                disc(d, hx, hy, 11, pal["ink"], pal, w=0)
                holes += 1
    return f"1 张创可贴：中间 1 块药垫 + 左右共 {holes} 个小孔；直接画在底色上，没有纸卡"


@page("doctor", 11)
def _(d, pal):
    """三件事：按时吃药、多喝水、早点睡。"""
    xs, slot = lay(3)
    cy = S / 2
    x = xs[0]                                                   # 药瓶：不透明 + 十字标
    d.rounded_rectangle([x - 96, cy - 150, x + 96, cy + 210], radius=22,
                        fill=pal["soft"], outline=pal["ink"], width=9)
    d.rounded_rectangle([x - 70, cy - 230, x + 70, cy - 140], radius=14,
                        fill=pal["accent"], outline=pal["ink"], width=9)
    for rx in range(-50, 51, 25):
        d.line([x + rx, cy - 222, x + rx, cy - 150], fill=pal["ink"], width=5)
    d.rounded_rectangle([x - 74, cy - 70, x + 74, cy + 140], radius=10,
                        fill=pal["paper"], outline=pal["ink"], width=7)
    d.rectangle([x - 16, cy - 30, x + 16, cy + 100], fill=pal["accent"])
    d.rectangle([x - 58, cy + 12, x + 58, cy + 58], fill=pal["accent"])
    x = xs[1]                                                   # 一杯水：杯口敞开
    cup = [(x - 92, cy - 170), (x + 92, cy - 170), (x + 66, cy + 190), (x - 66, cy + 190)]
    d.polygon(cup, fill=pal["paper"])
    d.polygon([(x - 78, cy - 40), (x + 78, cy - 40), (x + 66, cy + 190), (x - 66, cy + 190)],
              fill=pal["accent"])
    for a, b in zip(cup, cup[1:]):
        d.line([a, b], fill=pal["ink"], width=9)
    d.line([cup[3], cup[0]], fill=pal["ink"], width=9)
    d.line([x - 78, cy - 40, x + 78, cy - 40], fill=pal["ink"], width=7)
    x = xs[2]                                                   # 一张床：侧面
    d.rectangle([x - 130, cy - 150, x - 96, cy + 130], fill=pal["soft"],
                outline=pal["ink"], width=8)
    d.rounded_rectangle([x - 130, cy - 10, x + 140, cy + 90], radius=14,
                        fill=pal["paper"], outline=pal["ink"], width=9)
    d.rounded_rectangle([x - 112, cy - 78, x - 16, cy - 6], radius=18,
                        fill=pal["accent"], outline=pal["ink"], width=8)
    for lx in (x - 122, x + 108):
        d.rectangle([lx, cy + 90, lx + 26, cy + 180], fill=pal["soft"],
                    outline=pal["ink"], width=7)
    return "3 个符号：1 个带十字标的药瓶（瓶身不透明）/ 1 杯水（杯口敞开）/ 1 张带枕头的床"


@page("sleepwin", 7)
def _(d, pal):
    """池塘剖面：冰在上面，青蛙和乌龟都埋在泥里。"""
    ice0, ice1 = 300, 370
    mud0 = S - MARGIN - 230
    d.rectangle([MARGIN, ice1, S - MARGIN, mud0], fill=pal["soft"])          # 水
    d.rectangle([MARGIN, ice0, S - MARGIN, ice1], fill=pal["paper"],
                outline=pal["ink"], width=8)                                 # 冰
    for cxk in range(MARGIN + 120, S - MARGIN - 60, 170):
        d.line([cxk, ice0 + 8, cxk + 26, ice1 - 8], fill=pal["ink"], width=5)
    d.rectangle([MARGIN, mud0, S - MARGIN, S - MARGIN], fill=pal["bark"],
                outline=pal["ink"], width=8)                                 # 泥
    fx, fy = S / 2 - 190, mud0 + 110                                         # 青蛙
    d.ellipse([fx - 110, fy - 60, fx + 110, fy + 60], fill=pal["accent"],
              outline=pal["ink"], width=8)
    for s in (-1, 1):
        disc(d, fx + s * 52, fy - 58, 30, pal["accent"], pal, w=8)
        disc(d, fx + s * 52, fy - 62, 10, pal["ink"], pal, w=0)
        d.line([fx + s * 96, fy + 20, fx + s * 140, fy + 54], fill=pal["ink"], width=12)
    tx, ty = S / 2 + 190, mud0 + 110                                         # 乌龟
    # 头要先画、壳后画压住头根，否则头会变成飘在壳边上的一个球（上一版就是）
    disc(d, tx + 132, ty - 30, 38, pal["accent"], pal, w=8)
    disc(d, tx + 148, ty - 38, 9, pal["ink"], pal, w=0)
    d.pieslice([tx - 130, ty - 110, tx + 130, ty + 110], 180, 360,
               fill=pal["paper"], outline=pal["ink"], width=8)
    d.line([tx - 130, ty, tx + 130, ty], fill=pal["ink"], width=8)
    for k in range(-1, 2):
        d.line([tx + k * 62, ty - 4, tx + k * 40, ty - 96], fill=pal["ink"], width=6)
    for s in (-1, 1):
        d.rounded_rectangle([tx + s * 96 - 26, ty - 6, tx + s * 96 + 26, ty + 46], radius=12,
                            fill=pal["accent"], outline=pal["ink"], width=7)
    return "1 个池塘剖面：1 层冰（4 道裂纹）+ 1 池水 + 1 层泥，泥里埋着 1 只青蛙和 1 只乌龟"


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
        # 成品目录的后缀不统一：新书是 _qwen，早期 LoRA 书是 _lora / _qwen_lora。
        # 写死 _qwen 会在一个本不存在的目录里凭空建出单页（crab 就这么中过招，
        # 连带把它的 index.html 打包成了 0 字节）。这里按实际存在的目录挑。
        book_dir = next((os.path.join(OUT, f"{slug}{sfx}") for sfx in
                         ("_qwen", "_qwen_lora", "_lora")
                         if os.path.isdir(os.path.join(OUT, f"{slug}{sfx}"))),
                        os.path.join(OUT, f"{slug}_qwen"))
        dst = os.path.join(book_dir, f"page_{n:02d}.png")
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
