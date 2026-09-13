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
