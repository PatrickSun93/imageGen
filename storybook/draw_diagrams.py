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
