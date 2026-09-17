# -*- coding: utf-8 -*-
"""第七批示意图页（3/5）：那时候的地球、加州、第一个发现、名字、云、雾、冰雹、龙卷风。"""
from draw_diagrams import (S, MARGIN, page, asset, place, halo, lie_flat, poly, disc, arrow,
                           cross, lay, panel2, hbar, footprint, bands, flow_arrows, cmp_len,
                           cmp_height, cmp_count, bars, timeline, steps, magnify)
from PIL import ImageColor
import math, random


# ---------------------------------------------------------------- 这一批自己的图元
# 手册硬规矩：任何首尾相接的曲线都会被读成一个环。所以画气流一律用 arc_arrow ——
# 一段**开口**的弧，起点画一个圆点，终点带一个箭头尖，段与段之间留缺口。
# 上升气流、下沉气流、打转、冰雹在云里翻滚，全部由它和直箭头拼出来。

def arc_arrow(d, pal, cx, cy, rx, ry, a0, a1, w=10, head=26, col=None, dot=True):
    """一段开口的弧线箭头：起点一个圆点，终点一个箭头尖，中间不闭合。

    返回 (起点, 终点)，方便下一段对着它留缺口。
    """
    n = 48
    pts = []
    for i in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * i / n)
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    d.line(pts, fill=col or pal["ink"], width=w, joint="curve")
    if dot:
        disc(d, pts[0][0], pts[0][1], w * 0.9 + 5, pal["accent"], pal, w=0)
    arrow(d, pts[-2][0], pts[-2][1], pts[-1][0], pts[-1][1], pal, w=w, head=head)
    return pts[0], pts[-1]


def gap_arrow(d, pal, x1, y1, x2, y2, r1, r2, w=11, head=30):
    """两个圆之间的箭头：两端各让开自己的半径，箭头不插进圆里。"""
    a = math.atan2(y2 - y1, x2 - x1)
    arrow(d, x1 + r1 * math.cos(a), y1 + r1 * math.sin(a),
          x2 - r2 * math.cos(a), y2 - r2 * math.sin(a), pal, w=w, head=head)


def fit(a, max_w, max_h):
    """返回一个宽度，使素材缩放后同时不超过 max_w 和 max_h。

    只按 w= 摆位是个坑：素材的长宽比是模型给的，我不知道。同一句 place(w=340)，
    横着的素材乖乖待在框里，竖着的就顶穿了框顶。凡是往框里塞素材，两边都要卡。
    """
    aw, ah = a.size
    s = min(max_w / aw, max_h / ah)
    return aw * s


def rgb(c):
    """调色板里存的是 "#2b2820" 这样的字符串，halo() 要的是 (r, g, b)。"""
    return ImageColor.getrgb(c)


def scaled_h(a, w_):
    """素材缩到宽 w_ 以后的高度 —— 先算出来才好定它该摆在哪个 y。"""
    return a.height * w_ / a.width


def half_at(a, frac):
    """量素材在相对高度 frac（0=顶、1=底）那一行上的半宽和中心，都按素材宽度取比例。

    龙卷风这种上粗下细的柱子，绕着它画的旋转弧得贴住它**那一层**的粗细。柱子长什么样
    是模型定的，程序不知道，所以别猜——直接从素材自己的 alpha 上量一行。
    """
    w_, h_ = a.size
    y = max(0, min(h_ - 1, int(h_ * frac)))
    bb = a.getchannel("A").crop((0, y, w_, y + 1)).getbbox()
    if not bb:
        return 0.08, 0.5
    return (bb[2] - bb[0]) / 2.0 / w_, (bb[0] + bb[2]) / 2.0 / w_


def rings(d, cx, cy, r, n, pal, w=6):
    """n 圈同心圆，由外往里画，两色交替 —— 圈数由参数保证，数得清。"""
    for k in range(n):
        disc(d, cx, cy, r * (n - k) / n, pal["paper"] if k % 2 else pal["soft"], pal, w=w)
    return n


def blob(d, cx, cy, rx, ry, pal, fill=None, seed=1, n=15, w=8):
    """一块不规则的陆地。同一个 seed 出来的形状永远一样。"""
    rnd = random.Random(seed)
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        k = 0.72 + rnd.random() * 0.46
        pts.append((cx + rx * k * math.cos(a), cy + ry * k * math.sin(a)))
    poly(d, pts, pal, fill if fill is not None else pal["bark"], w)
    return pts


def wordblock(d, cx, cy, w_, h_, pal):
    """名字里的一块：一个空的圆角框，内容由调用方往里画（不写字）。"""
    d.rounded_rectangle([cx - w_ / 2, cy - h_ / 2, cx + w_ / 2, cy + h_ / 2], radius=22,
                        fill=pal["paper"], outline=pal["ink"], width=8)


def dashed_v(d, x, y0, y1, pal, seg=16, w=5, col=None):
    """一条竖着的虚线，用来标空当。"""
    n = 0
    y = y0
    while y < y1:
        d.line([x, y, x, min(y + seg, y1)], fill=col or pal["line"], width=w)
        y += seg * 2
        n += 1
    return n


# ---------------------------------------------------------------- oldworld（那时候的地球）
# 素材：1 蕨丛 / 2 针叶树 / 3 长脖子恐龙 / 4 小花

@page("oldworld", 3)
def _(d, pal, img):
    """草是很晚才来的，等它铺满地面，恐龙已经走光了 —— 两格里恐龙和草永远不同框。"""
    n_grass = 6
    g = asset("oldworld", 5)
    step = gw = gh = 0
    for (cx, cy, w_, h_), dino in zip(panel2(d, pal), (True, False)):
        base = cy + h_ / 2 - 60
        d.line([cx - w_ / 2 + 20, base, cx + w_ / 2 - 20, base], fill=pal["ink"], width=9)
        if dino:
            place(img, asset("oldworld", 3), cx, base, h=300, anchor="bottom")
        else:
            step = (w_ - 90) / n_grass
            for i in range(n_grass):
                gx = cx - w_ / 2 + 45 + step * (i + 0.5)
                gw, gh = place(img, g, gx, base + 8, w=fit(g, step * 1.7, 210),
                               anchor="bottom")
    return (f"两格等大：左格 1 只长脖子恐龙站在光地上（高 300px，0 丛草）/ "
            f"右格 {n_grass} 丛草（素材5，各 {gw}×{gh}px），根都扎在同一条地线上、"
            f"间距 {step:.0f}px，相邻两丛的叶子交叠成一片草地（0 只恐龙）")


@page("oldworld", 5)
def _(d, pal, img):
    """针叶树最高，长脖子恐龙够它的顶 —— 脚底同一条地线，高度由参数定死。"""
    tree_h, dino_h = 780, 340
    base = S - MARGIN - 130
    note = cmp_height(img, d, pal, "oldworld",
                      [(2, tree_h, S / 2 + 230), (3, dino_h, S / 2 - 260)], base=base)
    for hh in (tree_h, dino_h):                    # 两条水平的高度线，比高矮一眼看到头
        d.line([MARGIN, base - hh, S - MARGIN, base - hh], fill=pal["line"], width=5)
    return note + f"；另加 2 条水平高度线（{tree_h}px 和 {dino_h}px），树比恐龙高 {tree_h - dino_h}px"


@page("oldworld", 7)
def _(d, pal, img):
    """恐龙住了一亿年，地上才开出第一批小花 —— 花的刻度落在时间线很靠后的地方。"""
    y = S / 2 + 80
    note = timeline(img, d, pal, "oldworld",
                    [(0.15, 3, "恐龙住下来"), (0.85, 4, "第一批小花")], y=y)
    x0, x1 = MARGIN + 50, S - MARGIN - 50
    a, b = 0.15, 0.80
    hbar(d, x0 + (x1 - x0) * a, y + 110, (x1 - x0) * (b - a), 70, pal, pal["soft"])
    return note + f"；线下 1 根横条盖住 {a * 100:.0f}%~{b * 100:.0f}%（恐龙住的那一亿年），花的刻度在它右边"


@page("oldworld", 9)
def _(d, pal):
    """最早所有陆地连成一整块，后来才裂成好几块。"""
    n_piece = 5
    for (cx, cy, w_, h_), whole in zip(panel2(d, pal), (True, False)):
        if whole:
            blob(d, cx, cy, w_ * 0.40, h_ * 0.28, pal, seed=3, n=17)
        else:
            spots = [(-0.26, -0.20, 0.17, 0.12), (0.22, -0.24, 0.15, 0.10),
                     (-0.28, 0.12, 0.14, 0.11), (0.18, 0.10, 0.16, 0.12),
                     (-0.02, 0.32, 0.13, 0.09)]
            for k, (fx, fy, rx, ry) in enumerate(spots):
                blob(d, cx + w_ * fx, cy + h_ * fy, w_ * rx, h_ * ry, pal, seed=11 + k, n=13)
    return f"两格等大：左格 1 整块陆地 / 右格 {n_piece} 块分开的陆地，块与块之间都留着空当"


@page("oldworld", 11)
def _(d, pal, img):
    """那时候地球转得快，一天比现在短一点。"""
    spins = (3, 1)
    fracs = (0.86, 1.00)
    el = asset("oldworld", 6)
    ew = fit(el, 300, 300)                 # 两格用同一个宽度，地球必定一样大
    aw = ah = 0
    for (cx, cy, w_, h_), n_spin, frac in zip(panel2(d, pal), spins, fracs):
        ey = cy - 150
        aw, ah = place(img, el, cx, ey, w=ew)
        rx, ry = aw / 2 + 58, ah / 2 + 58   # 弧箭头贴着地球自己的外框转，不写死半径
        for k in range(n_spin):
            a0 = -90 + 360 * k / n_spin + 10
            arc_arrow(d, pal, cx, ey, rx, ry, a0, a0 + 360 / n_spin - 34, w=9, head=24)
        x0 = cx - w_ / 2 + 34
        full = w_ - 68
        hbar(d, x0, cy + 250, full * frac, 76, pal, pal["accent"] if frac < 1 else pal["soft"])
        d.line([x0, cy + 180, x0, cy + 320], fill=pal["ink"], width=8)
    return (f"两格等大，两格的地球是同一个素材缩到同一个尺寸（素材6，各 {aw}×{ah}px）："
            f"左格（那时候）地球外面 {spins[0]} 段旋转弧箭头、一天的横条占格宽 {fracs[0] * 100:.0f}% / "
            f"右格（现在）{spins[1]} 段、横条占 {fracs[1] * 100:.0f}%；两条横条都从各自格子的左端起算")


# ---------------------------------------------------------------- california（加州有没有恐龙）
# 素材：1 菊石 / 2 海生爬行动物 / 3 鸭嘴龙 / 4 剑齿虎

@page("california", 2)
def _(d, pal, img):
    """别处的恐龙骨头一堆一堆，加州的一只手都数得过来。"""
    many, few = 24, 4
    b = asset("california", 5)
    cols, rows_ = 4, 6
    mw = mh = fw = fh = 0
    for (cx, cy, w_, h_), lots in zip(panel2(d, pal), (True, False)):
        if lots:
            sx, sy = (w_ - 80) / cols, (h_ - 230) / rows_
            bw = fit(b, sx * 0.94, sy * 0.84)
            for r_ in range(rows_):
                for c_ in range(cols):
                    mw, mh = place(img, b, cx - (cols - 1) * sx / 2 + c_ * sx,
                                   cy - (rows_ - 1) * sy / 2 + r_ * sy, w=bw)
        else:
            sy = 170
            bw = fit(b, w_ * 0.74, sy * 0.80)
            for k in range(few):
                fw, fh = place(img, b, cx, cy - (few - 1) * sy / 2 + k * sy, w=bw)
    return (f"两格等大，两格都是同一根化石腿骨（素材5）：左格 {many} 根（{rows_} 行 ×{cols}，"
            f"各 {mw}×{mh}px）/ 右格 {few} 根（1 列，各 {fw}×{fh}px），一根一根数得清")


@page("california", 5)
def _(d, pal, img):
    """菊石小的像纽扣，大的比盘子还宽 —— 同一个素材缩成两种大小。

    以前小的只有 70px 高、大的 430px，小的那颗缩得看不出是个壳。现在按画面能容下的
    上限反推：大的先顶到 700px 高（宽度另卡在 430px 以内，横着的素材才不会顶穿边距），
    小的按定死的比例跟着放大，两颗都比原来大一大截。
    """
    el = asset("california", 1)
    ratio = el.width / el.height
    big = min(700, 600 / ratio)                    # 高和宽两头都卡住
    small = big * 0.29
    xs = MARGIN + 50 + small * ratio / 2
    xb = S - MARGIN - 50 - big * ratio / 2
    note = cmp_height(img, d, pal, "california", [(1, small, xs), (1, big, xb)])
    return note + f"；同一个菊石素材缩成两种大小，大的是小的 {big / small:.1f} 倍"


@page("california", 7)
def _(d, pal, img):
    """沧龙、鱼龙、菊石都住在水里，恐龙住在陆地上 —— 三样在水里，一样在陆上。"""
    n_water = 3
    sizes = []
    for (cx, cy, w_, h_), water in zip(panel2(d, pal), (True, False)):
        if water:
            top = cy - h_ / 2 + 110                # 水面抬高 60px，三层各分到更高的槽
            d.rectangle([cx - w_ / 2 + 8, top, cx + w_ / 2 - 8, cy + h_ / 2 - 8], fill=pal["soft"])
            for i in range(9):                                  # 水面的波纹
                wx = cx - w_ / 2 + 10 + i * (w_ - 20) / 9
                d.arc([wx, top - 22, wx + (w_ - 20) / 9, top + 22], 180, 360,
                      fill=pal["ink"], width=7)
            slot = (cy + h_ / 2 - 20 - top) / 3
            for a, mw, k in ((2, 430, 0.5), (2, 340, 1.5), (1, 260, 2.5)):
                el = asset("california", a)
                sizes.append(place(img, el, cx, top + slot * k,
                                   w=fit(el, mw, slot * 0.90)))
        else:
            base = cy + h_ / 2 - 70
            d.line([cx - w_ / 2 + 20, base, cx + w_ / 2 - 20, base], fill=pal["ink"], width=9)
            dw, dh = place(img, asset("california", 3), cx, base, w=400, anchor="bottom")
    return (f"两格等大：左格水面以下 {n_water} 样（2 只海生爬行动物 + 1 个菊石，上下分三层不叠，"
            f"各 {' / '.join(f'{a}×{b}px' for a, b in sizes)}）/ "
            f"右格陆地上 1 只恐龙（{dw}×{dh}px）站在地线上")


@page("california", 9)
def _(d, pal, img):
    """恐龙走了六千多万年，沥青坑里那些骨头才四万年 —— 骨头的刻度紧贴着现在这一端。"""
    t_bone = 1 - 40000 / 66000000
    y = S / 2 + 80
    note = timeline(img, d, pal, "california",
                    [(0.0, None, "恐龙走了"), (t_bone, None, "沥青坑里的骨头")], y=y)
    x0, x1 = MARGIN + 50, S - MARGIN - 50
    for tx, ax, a in ((x0, MARGIN + 190, 3), (x0 + (x1 - x0) * t_bone, S - MARGIN - 190, 4)):
        place(img, asset("california", a), ax, y - 46, w=280, anchor="bottom")
        d.line([ax, y - 42, tx, y - 28], fill=pal["line"], width=5)
    return note + f"；两个刻度一个贴最左、一个在 {t_bone * 100:.2f}%（几乎贴着最右），各用 1 条引线接到上面的素材"


@page("california", 11)
def _(d, pal, img):
    """坑里挖出来的，狼最多；剑齿虎的两颗牙特别长。"""
    fw, fs = 0.95, 0.14
    boxes = panel2(d, pal)
    cx, cy, w_, h_ = boxes[0]
    x0, full = cx - w_ / 2 + 30, w_ - 60
    hbar(d, x0, cy - 90, full * fw, 80, pal, pal["accent"])
    hbar(d, x0, cy + 90, full * fs, 80, pal, pal["soft"])
    d.line([x0, cy - 160, x0, cy + 160], fill=pal["ink"], width=8)
    cx, cy, w_, h_ = boxes[1]
    aw, ah = place(img, asset("california", 4), cx, cy + 230, w=380, anchor="bottom")
    tx = cx - aw / 2 + aw * 0.16
    ty = cy + 230 - ah + ah * 0.34
    d.ellipse([tx - aw * 0.12, ty - ah * 0.16, tx + aw * 0.12, ty + ah * 0.16],
              outline=pal["accent"], width=12)
    return (f"两格等大：左格 2 根左端对齐的横条（狼 {fw * 100:.0f}% / 剑齿虎 {fs * 100:.0f}%）/ "
            f"右格 1 只剑齿虎（宽 {aw}px）+ 1 个圈住它两颗长牙的圈")


# ---------------------------------------------------------------- firstfind（谁第一个发现恐龙）
# 素材：1 化石牙 / 2 鬣蜥 / 3 禽龙 / 4 碎石块

@page("firstfind", 4)
def _(d, pal, img):
    """扁扁的一颗牙，边上一排小锯齿。"""
    n_saw = 11
    tw, th = place(img, lie_flat(asset("firstfind", 1)), S / 2, 330, w=620)
    hx = S / 2 - tw * 0.26
    d.ellipse([hx - 110, 330 - 92, hx + 110, 330 + 92], outline=pal["accent"], width=12)
    arrow(d, hx, 330 + 104, hx, 700, pal, w=10, head=28)
    y = 800
    x0, x1 = MARGIN + 200, S - MARGIN - 200
    d.line([x0, y, x1, y], fill=pal["ink"], width=10)
    step = (x1 - x0) / n_saw
    for i in range(n_saw):
        sx = x0 + step * i
        poly(d, [(sx, y), (sx + step * 0.5, y - 70), (sx + step, y)], pal, pal["accent"], 5)
    return (f"1 颗横躺的牙（素材1，宽 {tw}px 高 {th}px）+ 1 个圈住带齿那条边的圈 + "
            f"1 支向下的箭头 + 下面放大的 {n_saw} 个小锯齿，一个一个数得清")


@page("firstfind", 6)
def _(d, pal, img):
    """他见到一只鬣蜥，嘴里的牙跟那颗一模一样。"""
    boxes = panel2(d, pal)
    cx, cy, w_, h_ = boxes[0]
    place(img, lie_flat(asset("firstfind", 1)), cx, cy, w=w_ * 0.84)
    cx, cy, w_, h_ = boxes[1]
    aw, ah = place(img, asset("firstfind", 2), cx, cy, w=w_ * 0.90)
    mx = cx - aw / 2 + aw * 0.07
    my = cy - ah / 2 + ah * 0.34
    d.ellipse([mx - aw * 0.11, my - ah * 0.16, mx + aw * 0.11, my + ah * 0.16],
              outline=pal["accent"], width=12)
    return f"两格等大：左格 1 颗化石牙（宽 {w_ * 0.84:.0f}px）/ 右格 1 只鬣蜥（宽 {aw}px）+ 1 个圈住它嘴的圈"


@page("firstfind", 7)
def _(d, pal, img):
    """那一颗牙是鬣蜥牙的二十倍 —— 下面正好二十颗小牙首尾相接，和上面一样长。

    旁白点名了「二十倍」，二十颗就一颗都不能少。可二十颗首尾相接等于上面那一颗，
    每颗必然只有四十来个像素，整排看上去就是一条锯齿线 —— 这一页以前最糟就糟在这儿。
    所以照着 cloud 7 那套两级放大来：等长那一排照旧（二十倍是靠它成立的），再把正中间
    那一颗单独框出来、引到下面的框里放大十几倍，一颗小牙到底长什么样这才看得见。
    """
    n_small = 20
    a = lie_flat(asset("firstfind", 1))
    span = fit(a, 900, 420)                       # 高度也卡住：横躺的牙太高会撞下面那排
    cx = S / 2
    by = MARGIN + scaled_h(a, span) / 2           # 大牙顶着上边距摆，下面才腾得出两层
    bw, bh = place(img, a, cx, by, w=span)
    unit = span / n_small
    x0 = cx - span / 2
    sy = 505
    sw = sh = 0
    for i in range(n_small):
        sw, sh = place(img, a, x0 + unit * (i + 0.5), sy, w=unit)
    for x in (x0, x0 + span):                     # 两端的对齐线，等长是看这个
        for seg in range(5):
            y = by + bh / 2 + 14 + seg * 18
            d.line([x, y, x, y + 9], fill=pal["line"], width=5)
    i0 = n_small // 2                             # 框正中间那一颗，引线才不歪
    mx0, mx1 = x0 + unit * i0, x0 + unit * (i0 + 1)
    d.rectangle([mx0, sy - sh / 2 - 12, mx1, sy + sh / 2 + 12], outline=pal["accent"], width=6)
    bx0, bx1, by0, by1 = 230, 794, 600, 960
    d.line([mx0, sy + sh / 2 + 12, bx0, by0], fill=pal["line"], width=6)
    d.line([mx1, sy + sh / 2 + 12, bx1, by0], fill=pal["line"], width=6)
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=20, fill=pal["paper"],
                        outline=pal["ink"], width=9)
    mw, mh = place(img, a, (bx0 + bx1) / 2, (by0 + by1) / 2,
                   w=fit(a, bx1 - bx0 - 50, by1 - by0 - 50))
    return (f"上面 1 颗化石牙（素材1，{bw}×{bh}px）；下面 {n_small} 颗同一个素材缩小的小牙首尾相接，"
            f"每颗 {sw}×{sh}px，合计 {unit * n_small:.0f}px —— 和上面那一颗正好等长（两端各 1 排对齐线），"
            f"所以大的是小的 {n_small} 倍；正中间第 {i0 + 1} 颗被 1 个方框框住，2 条引线接到下面的框，"
            f"框里把同一颗放大到 {mw}×{mh}px（{mw / unit:.0f} 倍），一颗小牙长什么样这才看得清")


@page("firstfind", 9)
def _(d, pal, img):
    """那根尖骨头，他不知道该搁哪儿，就插在了鼻子上。"""
    base = S - MARGIN - 110
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    aw, ah = place(img, asset("firstfind", 3), S / 2, base, h=560, anchor="bottom")
    nx = S / 2 - aw / 2 + aw * 0.05          # 鼻尖，量的是禽龙素材自己的外框
    ny = base - ah + ah * 0.16
    sp = asset("firstfind", 5)
    spw = fit(sp, 90, 150)
    sw, sh = place(img, sp, nx, ny + 28, w=spw, anchor="bottom")
    halo(img, sp, nx, ny + 28, w=spw, color=rgb(pal["accent"]), grow=16, width=11,
         anchor="bottom")
    return (f"1 只禽龙站在地线上（高 {ah}px）+ 鼻子上 1 根尖骨头（素材5，{sw}×{sh}px，尖朝上）"
            f"+ 1 圈沿着这根骨头自己的轮廓描出来的强调线")


@page("firstfind", 10)
def _(d, pal, img):
    """那根尖骨头不长在鼻子上，长在大拇指上。"""
    # 两个落点是量着禽龙素材自己的外框定的：鼻尖在它宽 5% / 高 16% 处，
    # 前掌在宽 33% / 高 90% 处。以前是 (0.06, 0.30) 和 (0.30, 0.64)——一个落在脖子上，
    # 一个落在胸口，都不是骨刺该长的地方；画成小三角还看不出来，换成真骨刺就露馅了。
    spots = ((0.05, 0.16), (0.33, 0.90))
    sp = asset("firstfind", 5)
    spw = fit(sp, 62, 104)
    widths = []
    sw = sh = 0
    for (cx, cy, w_, h_), spot, nose in zip(panel2(d, pal), spots, (True, False)):
        base = cy + h_ / 2 - 70
        d.line([cx - w_ / 2 + 20, base, cx + w_ / 2 - 20, base], fill=pal["ink"], width=9)
        aw, ah = place(img, asset("firstfind", 3), cx, base, w=w_ * 0.92, anchor="bottom")
        widths.append(aw)
        sx = cx - aw / 2 + aw * spot[0]
        sy = base - ah + ah * spot[1]
        sw, sh = place(img, sp, sx, sy + 20, w=spw, anchor="bottom")
        if nose:
            cross(d, sx, sy + 20 - sh / 2, sh * 0.78, pal)
        else:
            halo(img, sp, sx, sy + 20, w=spw, color=rgb(pal["accent"]), grow=14, width=10,
                 anchor="bottom")
    return (f"两格等大，同一只禽龙（宽各 {widths[0]}px）站在各自的地线上，"
            f"两格用同一根尖骨头素材（素材5，各 {sw}×{sh}px）："
            "左格它插在鼻子上、被 1 个大叉划掉 / 右格它长在大拇指上、"
            "被 1 圈沿它自己轮廓描出来的强调线圈住")


@page("firstfind", 11)
def _(d, pal, img):
    """欧文把这些大家伙归成一类 —— 一个框圈住三只大的，小蜥蜴留在框外。"""
    top, bot = 170, 700
    d.rounded_rectangle([MARGIN + 30, top, S - MARGIN - 30, bot], radius=30,
                        fill=pal["paper"], outline=pal["ink"], width=10)
    base = bot - 60
    d.line([MARGIN + 70, base, S - MARGIN - 70, base], fill=pal["ink"], width=8)
    n_in = 0
    for x, w in ((230, 200), (512, 260), (794, 200)):
        place(img, asset("firstfind", 3), x, base, w=w, anchor="bottom")
        n_in += 1
    place(img, asset("firstfind", 2), S / 2, 960, w=210, anchor="bottom")
    return f"1 个大框：框里 {n_in} 只大家伙站在同一条地线上（宽 200/260/200px），框外下面 1 只小蜥蜴"


# ---------------------------------------------------------------- dinonames（恐龙的名字是怎么来的）
# 素材：1 三角龙 / 2 霸王龙 / 3 迅猛龙 / 4 腕龙
# 名字一律画成「几个词块 + 一支向下的箭头 + 那只恐龙」，几页长一个样，看多了就懂规矩。

def _name_blocks(d, pal, glyphs, top=70, h=230):
    """把一个名字拆成几块，横排。glyphs 是 [画法函数, ...]，块数就是名字的段数。

    块里画什么（素材还是图元）由调用方决定，但**几块、多宽、隔多远、中间有没有加号**
    一律由这里算：lay() 把整幅宽均分成 len(glyphs) 个槽，块宽是槽宽的 0.80，
    所以相邻两块之间永远留着槽宽的 0.20，两块之间正中画一个「＋」，最后一支向下的
    箭头落在整排的正中间。换成素材以后，词与词的排列还是程序说了算。
    """
    n = len(glyphs)
    xs, slot = lay(n)
    bw = slot * 0.80
    cy = top + h / 2
    for gx, g in zip(xs, glyphs):
        wordblock(d, gx, cy, bw, h, pal)
        g(gx, cy, bw, h)
    for i in range(n - 1):                        # 块与块之间一个加号，读成「拼起来」
        mx = (xs[i] + xs[i + 1]) / 2
        d.line([mx - 22, cy, mx + 22, cy], fill=pal["ink"], width=9)
        d.line([mx, cy - 22, mx, cy + 22], fill=pal["ink"], width=9)
    arrow(d, S / 2, top + h + 20, S / 2, top + h + 130, pal, w=12, head=32)
    return n, top + h + 150


@page("dinonames", 2)
def _(d, pal, img):
    """名字是拼出来的：前一半说它的样子，后面那个「龙」原本是蜥蜴。"""
    y0, y1 = 250, 560
    d.rounded_rectangle([MARGIN + 50, y0, S - MARGIN - 50, y1], radius=28,
                        fill=pal["paper"], outline=pal["ink"], width=10)
    d.line([S / 2, y0, S / 2, y1], fill=pal["ink"], width=10)
    el = asset("dinonames", 1)
    aw, ah = place(img, el, (MARGIN + 50 + S / 2) / 2, (y0 + y1) / 2,
                   w=fit(el, 330, y1 - y0 - 40))
    lz = asset("dinonames", 5)
    lw, lh = place(img, lz, (S - MARGIN - 50 + S / 2) / 2, (y0 + y1) / 2,
                   w=fit(lz, 330, y1 - y0 - 40))
    return (f"1 个名字拆成左右两半（1 个大框 + 中间 1 条竖线，两半等宽）："
            f"左半 1 只恐龙的样子（素材1，{aw}×{ah}px）/ 右半 1 只蜥蜴（素材5，{lw}×{lh}px）")


@page("dinonames", 4)
def _(d, pal, img):
    """三、角、脸 —— 拆成三块，合起来就是「长着三只角的脸」。"""
    n_dot = 3
    size = {}

    def g_three(gx, gy, gw, gh):                  # 「三」是个数目，这块只能由程序画
        for k in range(n_dot):
            disc(d, gx - (n_dot - 1) * 37 + k * 74, gy, 26, pal["accent"], pal, w=6)

    def g_horn(gx, gy, gw, gh):
        a = asset("dinonames", 6)
        size["角"] = place(img, a, gx, gy, w=fit(a, gw * 0.62, gh * 0.82))

    def g_face(gx, gy, gw, gh):
        a = asset("dinonames", 7)
        size["脸"] = place(img, a, gx, gy, w=fit(a, gw * 0.86, gh * 0.82))

    n, ytop = _name_blocks(d, pal, [g_three, g_horn, g_face])
    base = S - MARGIN - 40
    el = asset("dinonames", 1)
    aw, ah = place(img, el, S / 2, base, w=fit(el, 640, base - ytop - 20), anchor="bottom")
    hx = S / 2 - aw / 2 + aw * 0.16
    hy = base - ah + ah * 0.32
    d.ellipse([hx - aw * 0.15, hy - ah * 0.22, hx + aw * 0.15, hy + ah * 0.22],
              outline=pal["accent"], width=12)
    return (f"名字拆成 {n} 个等宽的词块，横着一排、块与块之间 {n - 1} 个加号："
            f"第 1 块 {n_dot} 个点（＝三，数目由程序保证）/ 第 2 块 1 只兽角（素材6，"
            f"{size['角'][0]}×{size['角'][1]}px）/ 第 3 块 1 张三只角的脸（素材7，"
            f"{size['脸'][0]}×{size['脸'][1]}px）；下面 1 支向下的箭头 + "
            f"1 只三角龙（宽 {aw}px）+ 1 个圈住它脸上那几只角的圈")


@page("dinonames", 6)
def _(d, pal, img):
    """暴君、蜥蜴、王 —— 三块，合起来是「暴君蜥蜴之王」。"""
    size = {}

    def g_tyrant(gx, gy, gw, gh):
        a = asset("dinonames", 9)
        size["暴君"] = place(img, a, gx, gy, w=fit(a, gw * 0.88, gh * 0.82))

    def g_lizard(gx, gy, gw, gh):
        a = asset("dinonames", 5)
        size["蜥蜴"] = place(img, a, gx, gy, w=fit(a, gw * 0.88, gh * 0.82))

    def g_king(gx, gy, gw, gh):
        a = asset("dinonames", 8)
        size["王"] = place(img, a, gx, gy, w=fit(a, gw * 0.72, gh * 0.82))

    n, ytop = _name_blocks(d, pal, [g_tyrant, g_lizard, g_king])
    base = S - MARGIN - 40
    el = asset("dinonames", 2)
    aw, ah = place(img, el, S / 2, base, w=fit(el, 560, base - ytop - 20), anchor="bottom")
    return (f"名字拆成 {n} 个等宽的词块，横着一排、块与块之间 {n - 1} 个加号："
            f"第 1 块 1 排长在张开的颌上的大牙（素材9，{size['暴君'][0]}×{size['暴君'][1]}px，＝暴君）/ "
            f"第 2 块 1 只蜥蜴（素材5，{size['蜥蜴'][0]}×{size['蜥蜴'][1]}px）/ "
            f"第 3 块 1 顶王冠（素材8，{size['王'][0]}×{size['王'][1]}px，＝王）；"
            f"下面 1 支向下的箭头 + 1 只霸王龙（宽 {aw}px）")


@page("dinonames", 8)
def _(d, pal, img):
    """快 + 贼 —— 两块，合起来是「跑得快的贼」。"""
    n_dash = 3
    size = {}

    def g_fast(gx, gy, gw, gh):                   # 「快」是速度线，本来就该程序画
        for k in range(n_dash):
            yy = gy - (n_dash - 1) * 28 + k * 56
            arrow(d, gx - gw * 0.30, yy, gx + gw * 0.30, yy, pal, w=10, head=26)

    def g_thief(gx, gy, gw, gh):
        a = asset("dinonames", 10)
        ex, ey = gx - gw * 0.12, gy + gh * 0.14
        ew, eh = place(img, a, ex, ey, w=fit(a, gw * 0.46, gh * 0.46))
        size["贼"] = (ew, eh)
        arrow(d, ex + ew * 0.45, ey - eh * 0.28, gx + gw * 0.34, gy - gh * 0.30,
              pal, w=10, head=26)            # 蛋被叼着往外走 —— 这才是「贼」

    n, ytop = _name_blocks(d, pal, [g_fast, g_thief])
    base = S - MARGIN - 40
    el = asset("dinonames", 3)
    aw, ah = place(img, el, S / 2, base, w=fit(el, 560, base - ytop - 20), anchor="bottom")
    return (f"名字拆成 {n} 个等宽的词块，横着一排、块与块之间 {n - 1} 个加号："
            f"第 1 块 {n_dash} 支向右的箭头（＝快，数目由程序保证）/ "
            f"第 2 块 1 枚带斑点的恐龙蛋（素材10，{size['贼'][0]}×{size['贼'][1]}px）"
            f"被 1 支斜着往外的箭头拽走（＝贼）；下面 1 支向下的箭头 + 1 只迅猛龙（宽 {aw}px）")


@page("dinonames", 10)
def _(d, pal, img):
    """有些名字里藏着地名 —— 在哪儿挖出来的。"""
    dots = ((-0.22, -0.40), (0.26, 0.55))
    for (cx, cy, w_, h_), (fx, fy), a, seed in zip(panel2(d, pal), dots, (4, 1), (21, 22)):
        my = cy - 200
        blob(d, cx, my, w_ * 0.38, 120, pal, fill=pal["soft"], seed=seed, n=15)
        dx, dy = cx + w_ * fx, my + 120 * fy
        disc(d, dx, dy, 26, pal["accent"], pal, w=7)
        arrow(d, dx, dy + 44, dx, cy + 60, pal, w=10, head=26)
        base = cy + h_ / 2 - 60
        d.line([cx - w_ / 2 + 20, base, cx + w_ / 2 - 20, base], fill=pal["ink"], width=9)
        place(img, asset("dinonames", a), cx, base, w=340, anchor="bottom")
    return ("两格等大：每格 1 块地图 + 1 个地点圆点 + 1 支从圆点指下来的箭头 + "
            "1 只站在地线上的恐龙（宽各 340px），两格的圆点落在地图上不同的位置")


@page("dinonames", 11)
def _(d, pal, img):
    """有些名字里藏着人名 —— 记着是谁第一个把它从石头里挖出来。"""
    boxes = panel2(d, pal)
    cx, cy, w_, h_ = boxes[0]
    blob(d, cx, cy + 60, w_ * 0.40, h_ * 0.26, pal, seed=31, n=15)
    bn = asset("dinonames", 12)
    bw, bh = place(img, bn, cx + 95, cy - 120, w=fit(bn, 230, 155))   # 从石头顶上露出来
    hm = asset("dinonames", 11)
    hw, hh = place(img, hm, cx - 130, cy - 280, w=fit(hm, 180, 200))  # 左上角那把锤子
    cx, cy, w_, h_ = boxes[1]
    base = cy + 120
    aw, ah = place(img, asset("dinonames", 2), cx, base, w=380, anchor="bottom")
    for sx in (-70, 70):
        d.line([cx + sx, base, cx + sx, base + 90], fill=pal["ink"], width=7)
    d.rounded_rectangle([cx - 150, base + 90, cx + 150, base + 210], radius=18,
                        fill=pal["paper"], outline=pal["ink"], width=9)
    return (f"两格等大：左格 1 块石头里露出 1 根化石腿骨（素材12，{bw}×{bh}px）+ "
            f"左上角 1 把地质锤（素材11，{hw}×{hh}px）/ "
            f"右格 1 只挖出来的恐龙（宽 {aw}px）+ 下面用 2 根吊线挂着 1 块空名牌（不写字）")


# ---------------------------------------------------------------- cloud（云是怎么来的）
# 素材：1 积云 / 2 水珠 / 3 灰尘 / 4 太阳

@page("cloud", 2)
def _(d, pal, img):
    """天上那团白既不是棉花也不是烟，是水变出来的 —— 三样里划掉两样。"""
    el = asset("cloud", 1)
    cw, ch = place(img, el, S / 2, 250, w=fit(el, 560, 400))
    xs, slot = lay(3)
    cy = 760
    ct = asset("cloud", 5)
    tw, th = place(img, ct, xs[0], cy, w=fit(ct, 250, 290))           # 棉花
    cross(d, xs[0], cy, max(tw, th) / 2 + 20, pal)
    sm = asset("cloud", 6)
    mw, mh = place(img, sm, xs[1], cy, w=fit(sm, 230, 300))           # 烟
    cross(d, xs[1], cy, max(mw, mh) / 2 + 20, pal)
    dr = asset("cloud", 2)
    drw = fit(dr, 250, 270)
    dw, dh = place(img, dr, xs[2], cy, w=drw)
    halo(img, dr, xs[2], cy, w=drw, color=rgb(pal["accent"]), grow=20, width=12)
    return (f"上面 1 朵云（素材1，{cw}×{ch}px）+ 下面 3 样等宽并排（间距 {slot:.0f}px）："
            f"1 团棉花（素材5，{tw}×{th}px，1 个大叉划掉）/ 1 缕烟（素材6，{mw}×{mh}px，"
            f"1 个大叉划掉）/ 1 颗水珠（素材2，{dw}×{dh}px，沿它自己的轮廓描 1 圈强调线）")


@page("cloud", 4)
def _(d, pal, img):
    """变成气的水我们看不见 —— 一样多的水，右边只剩淡淡的轮廓。"""
    n_gas = 24
    boxes = panel2(d, pal)
    cx, cy, w_, h_ = boxes[0]
    dw, dh = place(img, asset("cloud", 2), cx, cy, h=320)
    cx, cy, w_, h_ = boxes[1]
    rnd = random.Random(41)
    for _k in range(n_gas):
        gx = cx + rnd.uniform(-w_ * 0.40, w_ * 0.40)
        gy = cy + rnd.uniform(-h_ * 0.36, h_ * 0.36)
        d.ellipse([gx - 22, gy - 22, gx + 22, gy + 22], outline=pal["line"], width=6)
    return (f"两格等大：左格 1 颗看得见的水珠（素材2，{dw}×{dh}px，实心带描边）/ "
            f"右格同样的水变成了气 —— {n_gas} 个只有淡色轮廓的小圈，一个实心的都没有")


@page("cloud", 6)
def _(d, pal, img):
    """水珠得先找个芯：一粒灰尘就够一颗水珠抱住。"""
    du = asset("cloud", 3)
    dx, dy = 250, S / 2
    aw, ah = place(img, du, dx, dy, w=fit(du, 280, 300))
    dr = asset("cloud", 7)
    bx = 740
    bw, bh = place(img, dr, bx, dy, w=fit(dr, 420, 440))
    arrow(d, dx + aw / 2 + 30, dy, bx - bw / 2 - 30, dy, pal, w=12, head=32)
    rc = min(bw, bh) * 0.15                       # 圈出正中心那一点，芯在哪儿由程序指
    d.ellipse([bx - rc, dy - rc, bx + rc, dy + rc], outline=pal["accent"], width=9)
    return (f"左边 1 粒灰尘（素材3，{aw}×{ah}px）→ 1 支向右的箭头 → "
            f"右边 1 颗中心含着一粒灰尘的水珠（素材7，{bw}×{bh}px）；"
            f"水珠的正中心另有 1 个半径 {rc:.0f}px 的小圈，指的就是那个芯")


@page("cloud", 7)
def _(d, pal):
    """一颗水珠有多小：几百颗排起来才有一根头发那么宽。

    两百颗画在一根头发里，每颗只有 4px，看上去就是一条虚线 —— 数不清也比不出来。
    所以分两级：上面是整根头发，圈出它宽度的二十分之一；下面把那一小段放大，
    里面正好十颗。二十段 × 十颗 = 两百颗，比例还是由参数算出来的。
    """
    per_seg, segs = 10, 20
    bw = 500
    x0 = (S - bw) / 2
    y0, y1 = 120, 520
    d.rectangle([x0, y0, x0 + bw, y1], fill=pal["paper"])
    for x in (x0, x0 + bw):
        d.line([x, y0, x, y1], fill=pal["ink"], width=9)
    seg_w = bw / segs
    sx = x0 + seg_w * 9
    d.rectangle([sx, y0, sx + seg_w, y1], fill=pal["soft"])
    for x in (sx, sx + seg_w):
        d.line([x, y0, x, y1], fill=pal["accent"], width=5)
    ccx, ccy, cr = sx + seg_w / 2, 320, 78
    d.ellipse([ccx - cr, ccy - cr, ccx + cr, ccy + cr], outline=pal["accent"], width=12)
    bx0, bx1, by0, by1 = 112, 912, 640, 880
    d.line([ccx - cr * 0.7, ccy + cr * 0.7, bx0, by0], fill=pal["line"], width=6)
    d.line([ccx + cr * 0.7, ccy + cr * 0.7, bx1, by0], fill=pal["line"], width=6)
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=20, fill=pal["paper"],
                        outline=pal["ink"], width=9)
    dia = (bx1 - bx0) / per_seg
    for i in range(per_seg):
        cxx = bx0 + dia * (i + 0.5)
        disc(d, cxx, (by0 + by1) / 2, dia / 2 - 4,
             pal["accent"] if i % 2 else pal["soft"], pal, w=5)
    return (f"上面 1 根放大的头发，宽 {bw}px（两条边线）；中间涂色并圈出它宽度的 1/{segs}"
            f"（{seg_w:.0f}px 宽的一小段）；2 条引线接到下面的框，框里把那一小段再放大"
            f"{(bx1 - bx0) / seg_w:.0f} 倍：{per_seg} 颗水珠首尾相接，每颗 {dia:.0f}px，"
            f"合计正好 {dia * per_seg:.0f}px 填满整框 —— 整根头发就是 {segs}×{per_seg} = "
            f"{segs * per_seg} 颗那么宽")


@page("cloud", 8)
def _(d, pal):
    """一颗看不见，十颗也看不见，几千亿颗挤在一块儿就看见白了。

    三组的位置是手排的不是 lay()：三组的宽度差着几十倍，均分成三个等宽的槽，
    最后那片准会顶出右边距，前两组又缩在槽中间够不着箭头。
    """
    cy = S / 2
    g1x, g2x, g3x = 150, 400, 790
    r = 16
    disc(d, g1x, cy, r, pal["soft"], pal, w=5)
    n2 = 0
    for r_ in range(2):
        for c_ in range(5):
            disc(d, g2x - 92 + c_ * 46, cy - 23 + r_ * 46, r, pal["soft"], pal, w=5)
            n2 += 1
    cols, rows_, step = 40, 30, 8
    n3 = 0
    for r_ in range(rows_):
        for c_ in range(cols):
            px = g3x - (cols - 1) * step / 2 + c_ * step
            py = cy - (rows_ - 1) * step / 2 + r_ * step
            d.ellipse([px - 3.5, py - 3.5, px + 3.5, py + 3.5], fill=pal["soft"])
            n3 += 1
    arrow(d, g1x + r + 24, cy, g2x - 92 - r - 24, cy, pal, w=10, head=26)
    arrow(d, g2x + 92 + r + 24, cy, g3x - (cols - 1) * step / 2 - 24, cy, pal, w=10, head=26)
    return (f"3 组水珠横着排开：1 颗（半径 {r}px）/ {n2} 颗（2 行 ×5，间距 46px，还数得清）/ "
            f"{n3} 颗（{rows_} 行 ×{cols}，间距 {step}px，挤成一片才看得见白）；中间 2 支箭头")


@page("cloud", 11)
def _(d, pal, img):
    """水珠碰上水珠越碰越大，大到托不住就往下掉 —— 那就是雨。

    以前四档都是纯色的圆，最大的也才半径 74px。改成真水珠素材，三档水珠一档比一档大，
    最后掉下来的那一颗换成「正在下落的雨滴」素材。位置不走 lay()：四档的宽度差着两三倍，
    均分成四个等宽的槽，小的缩在槽中间够不着箭头，大的又顶出去；这里按各自的实际宽度
    一档一档往右排，两档之间永远留 70px 的箭头位。
    """
    dr = asset("cloud", 2)
    rn = asset("cloud", 8)
    ytop, gap = 290, 95
    w1 = fit(dr, 120, 200)                         # 小：两颗碰在一起
    w2 = fit(dr, 210, 260)                         # 中
    w3 = fit(dr, 250, 320)                         # 大
    w4 = fit(rn, 250, 320)                         # 大到托不住，掉下来
    x_left = MARGIN + 10
    p1 = x_left + w1 + 4                           # 两颗小水珠贴在一起，合起来的中心
    a1 = place(img, dr, p1 - w1 / 2 - 4, ytop, w=w1)
    place(img, dr, p1 + w1 / 2 + 4, ytop, w=w1)
    p2 = x_left + 2 * w1 + 8 + gap + w2 / 2
    a2 = place(img, dr, p2, ytop, w=w2)
    p3 = p2 + w2 / 2 + gap + w3 / 2
    a3 = place(img, dr, p3, ytop, w=w3)
    arrow(d, x_left + 2 * w1 + 8 + 16, ytop, p2 - w2 / 2 - 16, ytop, pal, w=11, head=30)
    arrow(d, p2 + w2 / 2 + 16, ytop, p3 - w3 / 2 - 16, ytop, pal, w=11, head=30)
    cy4, base = 730, S - MARGIN - 20
    a4 = place(img, rn, p3, cy4, w=w4)
    arrow(d, p3, ytop + a3[1] / 2 + 24, p3, cy4 - a4[1] / 2 - 24, pal, w=12, head=34)
    arrow(d, p3, cy4 + a4[1] / 2 + 20, p3, base - 24, pal, w=12, head=34)
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    return (f"4 档水珠，一档比一档大：2 颗小的贴在一起（素材2，各 {a1[0]}×{a1[1]}px）→ "
            f"1 颗中的（素材2，{a2[0]}×{a2[1]}px）→ 1 颗大的（素材2，{a3[0]}×{a3[1]}px）→ "
            f"1 颗正在下落的雨滴（素材8，{a4[0]}×{a4[1]}px）；前三档横着排、中间 2 支横向箭头，"
            f"第 3 档到第 4 档 1 支向下的箭头，雨滴再 1 支向下的箭头落到地线上")


# ---------------------------------------------------------------- fog（雾就是落在地上的云）
# 素材：1 光秃的树 / 2 水珠 / 3 长着松树的小山 / 4 太阳

@page("fog", 2)
def _(d, pal, img):
    """雾其实就是云，只不过这一朵没飘在天上，是贴着地面 —— 两朵云一模一样，只差高度。"""
    cl = asset("fog", 5)
    cw = fit(cl, 400, 280)                # 两格用同一个宽度，两朵云必定一模一样
    ch = scaled_h(cl, cw)
    ups = []
    aw = ah = 0
    for (cx, cy, w_, h_), high in zip(panel2(d, pal), (True, False)):
        base = cy + h_ / 2 - 60
        d.line([cx - w_ / 2 + 20, base, cx + w_ / 2 - 20, base], fill=pal["ink"], width=9)
        ccy = (cy - 180) if high else (base - ch / 2 + 6)   # 贴地那朵，云底正好压在地线上
        aw, ah = place(img, cl, cx, ccy, w=cw)
        ups.append(base - ccy)
    return (f"两格等大，两朵云是同一个素材缩到同一个尺寸（素材5，各 {aw}×{ah}px），形状完全一样："
            f"左格云心离地线 {ups[0]:.0f}px（飘在天上）/ 右格只离 {ups[1]:.0f}px，"
            f"云底正压在地线上（贴着地面）")


@page("fog", 4)
def _(d, pal, img):
    """空气一冷，水汽待不住，变成小水珠悬在半空 —— 前后一样多，只是变了样。"""
    n, cols, step = 9, 3, 135
    cy = S / 2
    lx, rx = 235, 785                  # 不走 lay(2)：两边的阵列大了，中间得空出箭头的位置
    r_gas = 46
    dr = asset("fog", 2)
    dw = fit(dr, 120, 140)             # 原来每颗才 64px 高，一颗一颗看不出是水珠
    aw = ah = 0
    for k in range(n):
        gx = lx - (cols - 1) * step / 2 + (k % cols) * step
        gy = cy - (cols - 1) * step / 2 + (k // cols) * step
        d.ellipse([gx - r_gas, gy - r_gas, gx + r_gas, gy + r_gas], outline=pal["line"], width=7)
    for k in range(n):
        dx = rx - (cols - 1) * step / 2 + (k % cols) * step
        dy = cy - (cols - 1) * step / 2 + (k // cols) * step
        aw, ah = place(img, dr, dx, dy, w=dw)
    arrow(d, 455, cy, 565, cy, pal, w=12, head=32)
    for k in range(3):                              # 变冷：三支短的向下箭头
        arrow(d, 470 + k * 50, cy - 230, 470 + k * 50, cy - 130, pal, w=9, head=24)
    return (f"左边 {n} 个只有淡轮廓的小圈（看不见的水汽，半径 {r_gas}px，{cols} 行 ×{cols}、"
            f"间距 {step}px）→ 1 支向右的箭头 → 右边 {n} 颗实心水珠（素材2，各 {aw}×{ah}px，"
            f"同样 {cols} 行 ×{cols}、同样间距）—— 前后正好一样多；"
            f"箭头上方 3 支向下的短箭头表示空气变冷")


@page("fog", 6)
def _(d, pal, img):
    """袖子上头发上全挂着细细的水珠，一颗一颗。"""
    n = 8                              # 原来 14 颗，每颗只有 76px；旁白没点名数目，减到 8 颗放大
    pts = [(x, S / 2 + 60 * math.sin(x / 180.0)) for x in range(MARGIN, S - MARGIN + 1, 6)]
    d.line(pts, fill=pal["bark"], width=26, joint="curve")
    dr = asset("fog", 2)
    xs, slot = lay(n)
    dw = fit(dr, slot * 0.86, 165)
    dh = scaled_h(dr, dw)
    aw = ah = 0
    for x in xs:
        y = S / 2 + 60 * math.sin(x / 180.0)
        # 珠顶咬住绒线，是挂在上面不是浮着
        aw, ah = place(img, dr, x, y + 13 + dh / 2 - 10, w=dw)
    return (f"1 根放大的绒线横贯整幅（粗 26px）+ 挂在上面的 {n} 颗水珠"
            f"（素材2，各 {aw}×{ah}px、间距 {slot:.0f}px），每颗的顶都咬在绒线上")


@page("fog", 8)
def _(d, pal, img):
    """雾天看得见的距离短得多，所以走路要慢、手要牵好。"""
    rows = [(1.00, "accent", "晴天能看多远"), (0.12, "soft", "雾天能看多远")]
    note = bars(d, pal, rows, h=96, gap=300)
    x0, full = MARGIN + 50, S - 2 * MARGIN - 100
    cy0 = S / 2 - 300 * (len(rows) - 1) / 2
    tr = asset("fog", 1)
    tw = fit(tr, 210, 265)             # 原来 170px 高，两头都卡住才不会顶穿右边距
    aw = ah = 0
    for i, (frac, _k, _t) in enumerate(rows):
        tx = min(x0 + full * frac - 52, S - MARGIN - 10 - tw / 2)
        aw, ah = place(img, tr, tx, cy0 + i * 300 - 48, w=tw, anchor="bottom")
    return note + (f"；两条的右端各站 1 棵树（素材1，各 {aw}×{ah}px，能看到的最远处），"
                   f"树脚就踩在各自那条的上边")


@page("fog", 10)
def _(d, pal, img):
    """太阳一出来，小水珠一颗一颗又变回看不见的气，雾就散了。"""
    n = 6
    base = 880
    r_gas = 34
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    sun = asset("fog", 4)
    sw, sh = place(img, sun, S - MARGIN - 200, 200, w=fit(sun, 250, 280))
    dr = asset("fog", 2)
    xs, slot = lay(n)
    dw = fit(dr, slot * 0.80, 185)     # 原来每颗 70px 高，地上那一排看着像一串小点
    aw = ah = 0
    for x in xs:
        aw, ah = place(img, dr, x, base, w=dw, anchor="bottom")
        arrow(d, x, base - ah - 20, x, 448, pal, w=10, head=26)     # 起点在水珠上方，终点在淡圈下方
        d.ellipse([x - r_gas, 400 - r_gas, x + r_gas, 400 + r_gas], outline=pal["line"], width=6)
    return (f"1 个太阳（素材4，{sw}×{sh}px）+ 1 条地线 + 地上 {n} 颗水珠"
            f"（素材2，各 {aw}×{ah}px、间距 {slot:.0f}px）；每颗头上 1 支向上的箭头，"
            f"起点在水珠上方 y={base - ah - 20:.0f}、终点在 y=448，箭头尖上方各 1 个半径 "
            f"{r_gas}px 的淡色空圈（变回看不见的气）—— {n} 条气流全是一头一尾的直线，没有闭合的圈")


# ---------------------------------------------------------------- hail（冰雹是怎么长大的）
# 素材：1 冰雹 / 2 剖开的冰雹 / 3 积雨云 / 4 切开的洋葱

@page("hail", 2)
def _(d, pal, img):
    """冰雹长在又高又厚的积雨云里，云顶比飞机还高。"""
    base = S - MARGIN - 60
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    ccx = S / 2 + 110
    cl = asset("hail", 3)
    aw, ah = place(img, cl, ccx, base, w=fit(cl, 560, 780), anchor="bottom")
    top = base - ah
    py = top + 150
    pl = asset("hail", 5)
    pw = fit(pl, 215, 150)
    px = max(MARGIN + pw / 2 + 10, ccx - aw / 2 - pw / 2 - 60)
    plw, plh = place(img, pl, px, py, w=pw)
    # 飞机的高度线，虚的，一直画到云身上。段数定死 5 段、间距按剩下的空当现算 ——
    # 写死 34px 的间距，云一宽空当就只剩一段，那条线读不出「一直连到云上」。
    n_seg = 5
    x_s, x_e = px + plw / 2 + 20, ccx - aw / 2 + 60
    pitch = (x_e - x_s) / n_seg
    for seg in range(n_seg):
        sx = x_s + seg * pitch
        d.line([sx, py, sx + pitch * 0.55, py], fill=pal["line"], width=6)
    d.line([MARGIN, top, S - MARGIN, top], fill=pal["line"], width=5)
    return (f"1 朵积雨云（素材3，{aw}×{ah}px，脚踩地线，云顶在 y={top}）+ "
            f"左边 1 架客机（素材5，{plw}×{plh}px）；飞机的高度虚线在 y={py}（{n_seg} 段短虚线"
            f"一直接到云身上，间距 {pitch:.0f}px），比云顶低 {py - top}px")


@page("hail", 4)
def _(d, pal):
    """云里的风不只往上：中间往上冲，两边往下沉，上上下下转个不停。

    气流页的硬规矩：每一段都有起点和箭头尖，段与段之间留缺口 ——
    首尾接死的曲线会被读成一个圈，读不出「从哪儿来、往哪儿去」。
    """
    d.ellipse([MARGIN + 20, 140, S - MARGIN - 20, 910], fill=pal["soft"],
              outline=pal["ink"], width=10)
    up_x = (452, 512, 572)
    dn_x = (250, 774)
    for x in up_x:
        arrow(d, x, 790, x, 250, pal, w=12, head=32)
    for x in dn_x:
        arrow(d, x, 380, x, 700, pal, w=12, head=32)
    # 弧段的起点／终点都离直箭头的头尾留出 30px 以上的缺口：
    # 接得太近会连成一条闭合的圈，那就读不出「从哪儿来、往哪儿去」了
    arcs = ((350, 350, -60, -180), (674, 350, -120, 0),
            (350, 760, 180, 60), (674, 760, 0, 120))
    for acx, acy, a0, a1 in arcs:
        arc_arrow(d, pal, acx, acy, 110, 80, a0, a1, w=10, head=26)
    return (f"1 朵积雨云的剖面：中间 {len(up_x)} 支向上的箭头（从 y=790 升到 y=250）+ "
            f"两侧 {len(dn_x)} 支向下的箭头（从 y=380 沉到 y=700）+ "
            f"{len(arcs)} 段开口的弧线箭头把上下接起来，每段起点 1 个圆点、终点 1 个箭头尖，"
            f"段与段之间留着缺口，画面里没有一条首尾相接的闭环")


@page("hail", 5)
def _(d, pal, img):
    """越往上越冷，升过某一条线水就冻住 —— 水珠一过那儿立刻裹上一层冰。

    上下两颗是同一个水珠素材、同一个尺寸，差别只有一样：线上那颗外面裹了一层冰。
    那层冰不画成一个同心圆（水珠不是正圆，套个圆就是两个东西摞着），而是拿 halo()
    沿水珠自己的轮廓膨胀出来的一圈 —— 结冰是贴着水珠的形状结的。
    """
    note = bands(d, pal, 2, mark=0)
    top = MARGIN + 40
    h = (S - 2 * MARGIN - 80) / 2
    line_y = top + h
    d.line([MARGIN, line_y, S - MARGIN, line_y], fill=pal["ink"], width=16)
    dr = asset("hail", 6)
    dw = fit(dr, 210, 210)
    dh = scaled_h(dr, dw)
    ice, grow = 30, 8
    aw, ah = place(img, dr, S / 2, line_y + 250, w=dw)
    halo(img, dr, S / 2, line_y - 250, w=dw, color=rgb(pal["accent"]), grow=grow, width=ice)
    place(img, dr, S / 2, line_y - 250, w=dw)
    y_from = line_y + 250 - ah / 2 - 24
    y_to = line_y - 250 + ah / 2 + grow + ice + 24
    arrow(d, S / 2, y_from, S / 2, y_to, pal, w=12, head=34)
    return (note + f"；分界线在 y={line_y:.0f}（加粗到 16px）；线下 1 颗光水珠（素材6，{aw}×{ah}px）+ "
            f"1 支穿过分界线的向上箭头（起点 y={y_from:.0f}、终点 y={y_to:.0f}）+ "
            f"线上同一个素材、同样 {aw}×{ah}px 的水珠，外面沿它自己的轮廓多裹了 {ice}px 厚的一层冰")


@page("hail", 7)
def _(d, pal):
    """上去结一层，掉下来化一点，再上去又结一层 —— 来回好多趟，一趟一圈。"""
    # 边距留宽一点：最大那颗半径 84px，用默认边距排到最右会顶出画面
    xs, slot = lay(6, margin=MARGIN + 60)
    ys = (760, 300, 760, 300, 760, 300)
    rs = (24, 36, 48, 60, 72, 84)
    ups = sum(1 for i in range(5) if ys[i + 1] < ys[i])
    downs = 5 - ups
    for i, (x, y, r) in enumerate(zip(xs, ys, rs)):
        rings(d, x, y, r, i + 1, pal, w=5)
    for i in range(5):
        gap_arrow(d, pal, xs[i], ys[i], xs[i + 1], ys[i + 1], rs[i] + 18, rs[i + 1] + 26)
    return (f"{len(rs)} 颗越来越大的冰雹（半径 {'/'.join(str(r) for r in rs)}px），"
            f"第 k 颗身上正好 k 圈（1/2/3/4/5/6 圈）；中间 {5} 支箭头，"
            f"{ups} 支向上、{downs} 支向下，每支都有明确的起点和箭头尖，不是一条闭合的圈")


@page("hail", 9)
def _(d, pal, img):
    """把一颗冰雹切开，里面一圈套一圈，像切开的洋葱。"""
    n = 7
    boxes = panel2(d, pal)
    cx, cy, w_, h_ = boxes[0]
    rings(d, cx, cy, 190, n, pal, w=7)
    disc(d, cx, cy, 16, pal["accent"], pal, w=0)
    cx, cy, w_, h_ = boxes[1]
    aw, ah = place(img, asset("hail", 4), cx, cy, w=w_ * 0.86)
    return (f"两格等大：左格 1 颗剖开的冰雹 —— {n} 圈同心圆（最外半径 190px，两色交替）+ "
            f"正中 1 个小核 / 右格 1 个切开的洋葱（素材4，宽 {aw}px）")


@page("hail", 11)
def _(d, pal, img):
    """洛杉矶的云不够高也不够冷，几乎不下冰雹；别的地方年年都有。"""
    n_hail = 4
    hs = (230, 430)                    # 原来 180/360，两朵都往上抬，小的那朵也看得出是云
    cloud_base = 600
    cl = asset("hail", 3)
    hl = asset("hail", 1)
    sizes = []
    hw_ = hh_ = 0
    for (cx, cy, w_, h_), ch, many in zip(panel2(d, pal), hs, (False, True)):
        base = cy + h_ / 2 - 50
        d.line([cx - w_ / 2 + 20, base, cx + w_ / 2 - 20, base], fill=pal["ink"], width=9)
        sizes.append(place(img, cl, cx, cloud_base, w=fit(cl, w_ * 0.92, ch), anchor="bottom"))
        if many:
            hxs, hslot = lay(n_hail, width=w_ * 0.94, margin=0)
            hw = fit(hl, hslot * 0.86, 115)
            for hx in hxs:
                x = cx - w_ * 0.47 + hx
                arrow(d, x, cloud_base + 40, x, cloud_base + 175, pal, w=9, head=24)
                hw_, hh_ = place(img, hl, x, cloud_base + 265, w=hw)
        else:
            cross(d, cx, cloud_base + 180, 100, pal)
    return (f"两格等大，两朵云是同一个素材（素材3）、脚都落在 y={cloud_base}："
            f"左格云 {sizes[0][0]}×{sizes[0][1]}px（洛杉矶，不够高），云下 1 个大叉（不下冰雹）/ "
            f"右格云 {sizes[1][0]}×{sizes[1][1]}px，云下 {n_hail} 支向下的箭头 + "
            f"{n_hail} 颗落下来的冰雹（素材1，各 {hw_}×{hh_}px）")


# ---------------------------------------------------------------- tornado（龙卷风）
# 素材：1 龙卷风 / 2 雷云 / 3 谷仓 / 4 陀螺

@page("tornado", 2)
def _(d, pal, img):
    """先得有一朵大雷云，云底下的空气开始慢慢打转。"""
    aw, ah = place(img, asset("tornado", 2), S / 2, 460, h=380, anchor="bottom")
    segs = ((0, 100), (120, 220), (240, 340))
    for a0, a1 in segs:
        arc_arrow(d, pal, S / 2, 660, 300, 92, a0, a1, w=11, head=28)
    return (f"1 朵大雷云（素材2，高 {ah}px）+ 云底下 {len(segs)} 段开口的弧线箭头，"
            f"都沿同一个椭圆（300×92px）、都朝同一个方向，各转 100°、段间留 20° 的缺口；"
            f"每段起点 1 个圆点、终点 1 个箭头尖 —— 读出来是「在打转」，不是一个画死的圈")


@page("tornado", 4)
def _(d, pal):
    """空气一边转一边往中间挤，圈子越挤越小，转得就越来越快。"""
    cx, cy = S / 2, S / 2
    specs = ((330, 250, 9), (220, 165, 12), (120, 90, 16))
    for k, (rx, ry, w) in enumerate(specs):
        a0 = -160 + k * 34
        arc_arrow(d, pal, cx, cy, rx, ry, a0, a0 + 250, w=w, head=24 + k * 4)
    corners = ((-1, -1), (1, -1), (-1, 1), (1, 1))
    for sx, sy in corners:
        arrow(d, cx + sx * 430, cy + sy * 330, cx + sx * 250, cy + sy * 192, pal, w=11, head=28)
    return (f"{len(specs)} 段开口的弧线箭头，一段比一段小（椭圆半径 330×250 / 220×165 / 120×90px），"
            f"三段同一个转向，越往里线越粗（9/12/16px，表示越转越快）；"
            f"外面 {len(corners)} 支斜着往中心挤的直箭头。每段弧都有起点圆点和箭头尖，一条闭环也没有")


@page("tornado", 6)
def _(d, pal, img):
    """尖碰到地面那一下才算龙卷风，没碰到地的只能叫漏斗云。"""
    gap = 170
    tw = 300
    for (cx, cy, w_, h_), touch in zip(panel2(d, pal), (False, True)):
        base = cy + h_ / 2 - 70
        d.line([cx - w_ / 2 + 20, base, cx + w_ / 2 - 20, base], fill=pal["ink"], width=9)
        tip = base if touch else base - gap
        place(img, asset("tornado", 1), cx, tip, w=tw, anchor="bottom")
        if not touch:
            dashed_v(d, cx, tip + 10, base - 6, pal, seg=16, w=6)
    return (f"两格等大，同一个龙卷风素材（宽各 {tw}px）：左格它的尖停在离地线 {gap}px 的地方"
            f"（漏斗云，中间 1 条虚线量出这段空当）/ 右格它的尖正好落在地线上（这才算龙卷风）")


@page("tornado", 8)
def _(d, pal, img):
    """柱子越细转得越凶，最凶的比高速路上的车还要快上一倍。

    两根柱子本来是两个梯形，现在换成两个真素材：粗的用素材1，又细又绳状的用素材5。
    素材换了，绕着柱子的旋转弧就不能再按梯形公式算半宽了 —— 改成 half_at() 从素材
    自己的 alpha 上量那一层有多宽，弧线永远贴着柱子当前的粗细走。
    """
    n_slow, n_fast = 2, 5
    ybot, hh = 530, 380
    foot = 0.86                        # 量柱子粗细一律取这个高度：离地 14% 的那一层
    info = []
    for cx, a_n, n_spin in ((S / 2 - 250, 1, n_slow), (S / 2 + 250, 5, n_fast)):
        a = asset("tornado", a_n)
        aw, ah = place(img, a, cx, ybot, h=hh, anchor="bottom")   # 两根按高度缩，必定一样高
        info.append((aw, ah, half_at(a, foot)[0] * aw * 2, n_spin))
        for k in range(n_spin):
            frac = 0.30 + 0.56 * k / (n_spin - 1) if n_spin > 1 else 0.5
            hr, cr = half_at(a, frac)
            yy = ybot - ah + ah * frac
            acx = cx - aw / 2 + cr * aw
            rx = max(24, hr * aw) + 26
            arc_arrow(d, pal, acx, yy, rx, 22, 200, 380, w=8, head=20, dot=False)
            disc(d, acx - rx, yy, 9, pal["accent"], pal, w=0)
    x0 = MARGIN + 60
    full = S - 2 * MARGIN - 120
    hbar(d, x0, 720, full * 0.50, 80, pal, pal["soft"])
    hbar(d, x0, 870, full * 1.00, 80, pal, pal["accent"])
    d.line([x0, 660, x0, 930], fill=pal["ink"], width=8)
    return (f"上面 2 根柱子一样高（各 {info[0][1]}px，脚都落在 y={ybot}）："
            f"粗的（素材1，外框 {info[0][0]}×{info[0][1]}px，离地 14% 处柱身宽 {info[0][2]:.0f}px）"
            f"绕着 {n_slow} 段弧线箭头 / 又细又绳状的（素材5，外框 {info[1][0]}×{info[1][1]}px，"
            f"同一高度柱身只有 {info[1][2]:.0f}px）绕着 {n_fast} 段；每段弧的半径都是从素材那一层的"
            f"实际宽度量出来的，起点 1 个圆点、终点 1 个箭头尖，不闭合。"
            f"下面 2 条左端对齐的横条：上条 50%（高速路上的车）/ 下条 100%（最凶的龙卷风），正好一倍")


@page("tornado", 10)
def _(d, pal, img):
    """中部平原年年都有，那儿暖空气和冷空气老撞在一起；加州几乎没有。"""
    n_side = 3
    t = asset("tornado", 1)
    tw = fit(t, 250, 700)              # 原来定死 190px，太小；两头都卡住再放大
    aw = ah = 0
    for (cx, cy, w_, h_), plains in zip(panel2(d, pal), (True, False)):
        base = cy + h_ / 2 - 50
        d.line([cx - w_ / 2 + 20, base, cx + w_ / 2 - 20, base], fill=pal["ink"], width=9)
        aw, ah = place(img, t, cx, base, w=tw, anchor="bottom")
        if plains:
            step = max(60, min(100, ah * 0.18))
            for k in range(n_side):
                yy = base - ah * 0.30 - k * step          # 箭头贴着柱子自己的高度排
                arrow(d, cx - 215, yy, cx - aw / 2 - 16, yy, pal, w=10, head=26)  # 暖空气，往右
                arrow(d, cx + 215, yy, cx + aw / 2 + 16, yy, pal, w=10, head=26)  # 冷空气，往左
        else:
            cross(d, cx, base - ah / 2, 150, pal)
    return (f"两格等大，每格 1 个龙卷风站在地线上（素材1，各 {aw}×{ah}px）："
            f"左格左边 {n_side} 支向右的箭头（暖空气）+ 右边 {n_side} 支向左的箭头（冷空气），"
            f"两边对着撞在中间那根柱子上，箭头尖都停在柱子外缘往外 16px，每支都有起点和箭头尖 / "
            f"右格同样 1 个龙卷风被 1 个大叉划掉（加州几乎没有）")
