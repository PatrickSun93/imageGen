# -*- coding: utf-8 -*-
"""第七批示意图页（3/5）：那时候的地球、加州、第一个发现、名字、云、雾、冰雹、龙卷风。"""
from draw_diagrams import (S, MARGIN, page, asset, place, lie_flat, poly, disc, arrow, cross,
                           lay, panel2, hbar, footprint, bands, flow_arrows, cmp_len,
                           cmp_height, cmp_count, bars, timeline, steps, magnify)
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


def cloudlet(d, cx, cy, w, pal, fill=None, edge=8):
    """一朵云：先画一圈放大的墨色圆，再压一圈正常大的填色圆 —— 只剩外轮廓，里面没有多余的线。

    形状完全由 w 决定，所以对比两格里的两朵云必定一模一样，差别只能来自位置。
    """
    f = fill if fill is not None else pal["paper"]
    u = w / 3.4
    specs = [(-1.25, 0.20, 0.62), (-0.62, -0.20, 0.88), (0.10, -0.34, 1.00),
             (0.80, -0.12, 0.80), (1.28, 0.20, 0.60),
             (-0.70, 0.38, 0.62), (0.10, 0.40, 0.66), (0.80, 0.38, 0.60)]
    for dx, dy, r in specs:
        disc(d, cx + dx * u, cy + dy * u, r * u + edge, pal["ink"], pal, w=0)
    for dx, dy, r in specs:
        disc(d, cx + dx * u, cy + dy * u, r * u, f, pal, w=0)
    return w, u * 2.1


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


def bone(d, cx, cy, L, pal, fill=None, w=5):
    """一根骨头：中间一条圆角杆，两头各两个圆。"""
    f = fill if fill is not None else pal["paper"]
    r = L * 0.20
    d.rounded_rectangle([cx - L / 2 + r * 0.6, cy - r * 0.5, cx + L / 2 - r * 0.6, cy + r * 0.5],
                        radius=r * 0.5, fill=f, outline=pal["ink"], width=w)
    for sx in (-1, 1):
        for sy in (-1, 1):
            disc(d, cx + sx * (L / 2 - r * 0.55), cy + sy * r * 0.45, r * 0.55, f, pal, w=w)


def lizard(d, cx, cy, L, pal, fill=None):
    """一只小蜥蜴的侧影：躯干、头、尾、四条腿。「龙」原本就是这个意思。"""
    f = fill if fill is not None else pal["soft"]
    lw = max(4, int(L * 0.05))
    d.line([(cx - L * 0.30, cy), (cx - L * 0.44, cy - L * 0.08), (cx - L * 0.52, cy - L * 0.22)],
           fill=pal["ink"], width=lw, joint="curve")
    for sx in (-0.20, 0.08):
        for dxx in (0.0, 0.10):
            d.line([cx + L * (sx + dxx), cy + L * 0.06,
                    cx + L * (sx + dxx - 0.05 + dxx), cy + L * 0.25],
                   fill=pal["ink"], width=lw)
    d.ellipse([cx - L * 0.32, cy - L * 0.12, cx + L * 0.20, cy + L * 0.12],
              fill=f, outline=pal["ink"], width=7)
    disc(d, cx + L * 0.27, cy - L * 0.03, L * 0.11, f, pal, w=7)
    disc(d, cx + L * 0.31, cy - L * 0.06, max(3, L * 0.018), pal["ink"], pal, w=0)


def crown(d, cx, cy, w_, pal, fill=None):
    """一顶王冠。"""
    h = w_ * 0.70
    poly(d, [(cx - w_ / 2, cy + h / 2), (cx - w_ / 2, cy - h / 2), (cx - w_ / 6, cy + h * 0.06),
             (cx, cy - h / 2 - h * 0.14), (cx + w_ / 6, cy + h * 0.06),
             (cx + w_ / 2, cy - h / 2), (cx + w_ / 2, cy + h / 2)],
         pal, fill if fill is not None else pal["accent"], 7)


def funnel(d, cx, ytop, ybot, wtop, wbot, pal, fill=None, w=8):
    """一根上粗下细的柱子。"""
    poly(d, [(cx - wtop / 2, ytop), (cx + wtop / 2, ytop),
             (cx + wbot / 2, ybot), (cx - wbot / 2, ybot)],
         pal, fill if fill is not None else pal["soft"], w)


def plane(d, cx, cy, s, pal, fill=None):
    """一架小飞机的俯视剪影。"""
    f = fill if fill is not None else pal["paper"]
    poly(d, [(cx - s, cy - s * 0.15), (cx + s * 0.72, cy - s * 0.20), (cx + s, cy),
             (cx + s * 0.72, cy + s * 0.20), (cx - s, cy + s * 0.15)], pal, f, 6)
    for sy in (-1, 1):
        poly(d, [(cx - s * 0.08, cy + sy * s * 0.08), (cx + s * 0.30, cy + sy * s * 0.08),
                 (cx - s * 0.16, cy + sy * s * 0.72), (cx - s * 0.42, cy + sy * s * 0.68)],
             pal, f, 6)
    poly(d, [(cx - s, cy), (cx - s * 0.80, cy - s * 0.50),
             (cx - s * 0.60, cy - s * 0.46), (cx - s * 0.72, cy)], pal, f, 5)


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
    n_grass = 20
    for (cx, cy, w_, h_), dino in zip(panel2(d, pal), (True, False)):
        base = cy + h_ / 2 - 60
        d.line([cx - w_ / 2 + 20, base, cx + w_ / 2 - 20, base], fill=pal["ink"], width=9)
        if dino:
            place(img, asset("oldworld", 3), cx, base, h=300, anchor="bottom")
        else:
            step = (w_ - 60) / n_grass
            for i in range(n_grass):
                gx = cx - w_ / 2 + 30 + step * (i + 0.5)
                d.line([gx, base, gx - 11, base - 72], fill=pal["soft"], width=8)
                d.line([gx, base, gx + 13, base - 58], fill=pal["soft"], width=8)
    return (f"两格等大：左格 1 只长脖子恐龙站在光地上（高 300px，0 丛草）/ "
            f"右格 {n_grass} 丛草铺满同一条地线（0 只恐龙）")


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
def _(d, pal):
    """那时候地球转得快，一天比现在短一点。"""
    spins = (3, 1)
    fracs = (0.86, 1.00)
    for (cx, cy, w_, h_), n_spin, frac in zip(panel2(d, pal), spins, fracs):
        ey = cy - 150
        disc(d, cx, ey, 130, pal["soft"], pal, w=9)
        for k in range(n_spin):
            a0 = -90 + 360 * k / n_spin + 10
            arc_arrow(d, pal, cx, ey, 182, 182, a0, a0 + 360 / n_spin - 34, w=9, head=24)
        x0 = cx - w_ / 2 + 34
        full = w_ - 68
        hbar(d, x0, cy + 250, full * frac, 76, pal, pal["accent"] if frac < 1 else pal["soft"])
        d.line([x0, cy + 180, x0, cy + 320], fill=pal["ink"], width=8)
    return (f"两格等大：左格（那时候）地球外面 {spins[0]} 段旋转弧箭头、一天的横条占格宽 {fracs[0] * 100:.0f}% / "
            f"右格（现在）{spins[1]} 段、横条占 {fracs[1] * 100:.0f}%；两条横条都从各自格子的左端起算")


# ---------------------------------------------------------------- california（加州有没有恐龙）
# 素材：1 菊石 / 2 海生爬行动物 / 3 鸭嘴龙 / 4 剑齿虎

@page("california", 2)
def _(d, pal):
    """别处的恐龙骨头一堆一堆，加州的一只手都数得过来。"""
    many, few = 24, 4
    for (cx, cy, w_, h_), lots in zip(panel2(d, pal), (True, False)):
        if lots:
            cols, rows_ = 4, 6
            sx, sy = (w_ - 90) / cols, (h_ - 260) / rows_
            for r_ in range(rows_):
                for c_ in range(cols):
                    bone(d, cx - (cols - 1) * sx / 2 + c_ * sx,
                         cy - (rows_ - 1) * sy / 2 + r_ * sy, sx * 0.80, pal)
        else:
            sy = 150
            for k in range(few):
                bone(d, cx, cy - (few - 1) * sy / 2 + k * sy, w_ * 0.42, pal)
    return f"两格等大：左格 {many} 根骨头（6 行 ×4）/ 右格 {few} 根（1 列），一根一根数得清"


@page("california", 5)
def _(d, pal, img):
    """菊石小的像纽扣，大的比盘子还宽 —— 同一个素材缩成两种大小。"""
    small, big = 70, 430
    note = cmp_height(img, d, pal, "california",
                      [(1, small, S / 2 - 300), (1, big, S / 2 + 150)])
    return note + f"；同一个菊石素材缩成两种大小，大的是小的 {big / small:.1f} 倍"


@page("california", 7)
def _(d, pal, img):
    """沧龙、鱼龙、菊石都住在水里，恐龙住在陆地上 —— 三样在水里，一样在陆上。"""
    n_water = 3
    for (cx, cy, w_, h_), water in zip(panel2(d, pal), (True, False)):
        if water:
            top = cy - h_ / 2 + 170
            d.rectangle([cx - w_ / 2 + 8, top, cx + w_ / 2 - 8, cy + h_ / 2 - 8], fill=pal["soft"])
            for i in range(9):                                  # 水面的波纹
                wx = cx - w_ / 2 + 10 + i * (w_ - 20) / 9
                d.arc([wx, top - 22, wx + (w_ - 20) / 9, top + 22], 180, 360,
                      fill=pal["ink"], width=7)
            slot = (cy + h_ / 2 - 20 - top) / 3
            place(img, asset("california", 2), cx, top + slot * 0.5, w=380)
            place(img, asset("california", 2), cx, top + slot * 1.5, w=250)
            place(img, asset("california", 1), cx, top + slot * 2.5, w=150)
        else:
            base = cy + h_ / 2 - 70
            d.line([cx - w_ / 2 + 20, base, cx + w_ / 2 - 20, base], fill=pal["ink"], width=9)
            place(img, asset("california", 3), cx, base, w=400, anchor="bottom")
    return (f"两格等大：左格水面以下 {n_water} 样（2 只海生爬行动物 + 1 个菊石，上下分三层不叠）/ "
            f"右格陆地上 1 只恐龙站在地线上")


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
    """那一颗牙是鬣蜥牙的二十倍 —— 下面正好二十颗小牙首尾相接，和上面一样长。"""
    return cmp_len(img, d, pal, "firstfind", 1, 1, n_b=20, span=780)


@page("firstfind", 9)
def _(d, pal, img):
    """那根尖骨头，他不知道该搁哪儿，就插在了鼻子上。"""
    base = S - MARGIN - 110
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    aw, ah = place(img, asset("firstfind", 3), S / 2, base, h=560, anchor="bottom")
    nx = S / 2 - aw / 2 + aw * 0.06
    ny = base - ah + ah * 0.30
    poly(d, [(nx - 28, ny + 30), (nx + 28, ny + 30), (nx, ny - 96)], pal, pal["accent"], 7)
    d.ellipse([nx - 92, ny - 128, nx + 92, ny + 72], outline=pal["accent"], width=12)
    return f"1 只禽龙站在地线上（高 {ah}px）+ 鼻子上 1 根尖骨头 + 1 个圈住它的圈"


@page("firstfind", 10)
def _(d, pal, img):
    """那根尖骨头不长在鼻子上，长在大拇指上。"""
    spots = ((0.06, 0.30), (0.30, 0.64))
    widths = []
    for (cx, cy, w_, h_), spot, nose in zip(panel2(d, pal), spots, (True, False)):
        base = cy + h_ / 2 - 70
        d.line([cx - w_ / 2 + 20, base, cx + w_ / 2 - 20, base], fill=pal["ink"], width=9)
        aw, ah = place(img, asset("firstfind", 3), cx, base, w=w_ * 0.92, anchor="bottom")
        widths.append(aw)
        sx = cx - aw / 2 + aw * spot[0]
        sy = base - ah + ah * spot[1]
        poly(d, [(sx - 20, sy + 24), (sx + 20, sy + 24), (sx, sy - 74)], pal, pal["accent"], 6)
        if nose:
            cross(d, sx, sy - 16, 96, pal)
        else:
            d.ellipse([sx - 84, sy - 106, sx + 84, sy + 62], outline=pal["accent"], width=12)
    return (f"两格等大，同一只禽龙（宽各 {widths[0]}px）站在各自的地线上："
            "左格尖骨头插在鼻子上、被 1 个大叉划掉 / 右格尖骨头长在大拇指上、被 1 个圈圈出来")


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
    """把一个名字拆成几块，横排。glyphs 是 [画法函数, ...]，块数就是名字的段数。"""
    xs, slot = lay(len(glyphs))
    for gx, g in zip(xs, glyphs):
        wordblock(d, gx, top + h / 2, slot * 0.80, h, pal)
        g(gx, top + h / 2, slot * 0.80, h)
    arrow(d, S / 2, top + h + 20, S / 2, top + h + 130, pal, w=12, head=32)
    return len(glyphs), top + h + 150


@page("dinonames", 2)
def _(d, pal, img):
    """名字是拼出来的：前一半说它的样子，后面那个「龙」原本是蜥蜴。"""
    y0, y1 = 250, 560
    d.rounded_rectangle([MARGIN + 50, y0, S - MARGIN - 50, y1], radius=28,
                        fill=pal["paper"], outline=pal["ink"], width=10)
    d.line([S / 2, y0, S / 2, y1], fill=pal["ink"], width=10)
    aw, ah = place(img, asset("dinonames", 1), (MARGIN + 50 + S / 2) / 2, (y0 + y1) / 2, w=330)
    lizard(d, (S - MARGIN - 50 + S / 2) / 2, (y0 + y1) / 2, 300, pal)
    return (f"1 个名字拆成左右两半（1 个大框 + 中间 1 条竖线）："
            f"左半 1 只恐龙的样子（素材1，宽 {aw}px）/ 右半 1 只蜥蜴（体长 300px）")


@page("dinonames", 4)
def _(d, pal, img):
    """三、角、脸 —— 拆成三块，合起来就是「长着三只角的脸」。"""
    def g_three(gx, gy, gw, gh):
        for k in range(3):
            disc(d, gx - 74 + k * 74, gy, 26, pal["accent"], pal, w=6)

    def g_horn(gx, gy, gw, gh):
        poly(d, [(gx - 34, gy + 70), (gx + 34, gy + 70), (gx, gy - 76)], pal, pal["soft"], 7)

    def g_face(gx, gy, gw, gh):
        disc(d, gx, gy, 78, pal["soft"], pal, w=7)
        disc(d, gx - 28, gy - 18, 12, pal["ink"], pal, w=0)

    n, ytop = _name_blocks(d, pal, [g_three, g_horn, g_face])
    base = S - MARGIN - 40
    aw, ah = place(img, asset("dinonames", 1), S / 2, base, w=640, anchor="bottom")
    hx = S / 2 - aw / 2 + aw * 0.16
    hy = base - ah + ah * 0.32
    d.ellipse([hx - aw * 0.15, hy - ah * 0.22, hx + aw * 0.15, hy + ah * 0.22],
              outline=pal["accent"], width=12)
    return (f"{n} 个词块（3 个点 / 1 只角 / 1 张脸）+ 1 支向下的箭头 + "
            f"1 只三角龙（宽 {aw}px）+ 1 个圈住它脸上那几只角的圈")


@page("dinonames", 6)
def _(d, pal, img):
    """暴君、蜥蜴、王 —— 三块，合起来是「暴君蜥蜴之王」。"""
    n_teeth = 7

    def g_tyrant(gx, gy, gw, gh):
        x0 = gx - gw * 0.34
        step = gw * 0.68 / n_teeth
        d.line([x0, gy - 60, x0 + step * n_teeth, gy - 60], fill=pal["ink"], width=8)
        for k in range(n_teeth):
            poly(d, [(x0 + step * k, gy - 60), (x0 + step * (k + 0.5), gy + 40),
                     (x0 + step * (k + 1), gy - 60)], pal, pal["paper"], 5)

    def g_lizard(gx, gy, gw, gh):
        lizard(d, gx, gy, gw * 0.80, pal)

    def g_king(gx, gy, gw, gh):
        crown(d, gx, gy, gw * 0.58, pal)

    n, ytop = _name_blocks(d, pal, [g_tyrant, g_lizard, g_king])
    base = S - MARGIN - 40
    aw, ah = place(img, asset("dinonames", 2), S / 2, base, w=560, anchor="bottom")
    return f"{n} 个词块（{n_teeth} 颗尖牙 / 1 只蜥蜴 / 1 顶王冠）+ 1 支向下的箭头 + 1 只霸王龙（宽 {aw}px）"


@page("dinonames", 8)
def _(d, pal, img):
    """快 + 贼 —— 两块，合起来是「跑得快的贼」。"""
    def g_fast(gx, gy, gw, gh):
        for k in range(3):
            yy = gy - 56 + k * 56
            arrow(d, gx - gw * 0.30, yy, gx + gw * 0.30, yy, pal, w=10, head=26)

    def g_thief(gx, gy, gw, gh):
        d.ellipse([gx - 52, gy - 6, gx + 52, gy + 76], fill=pal["paper"],
                  outline=pal["ink"], width=7)
        arrow(d, gx + 20, gy + 20, gx + gw * 0.34, gy - 62, pal, w=10, head=26)

    n, ytop = _name_blocks(d, pal, [g_fast, g_thief])
    base = S - MARGIN - 40
    aw, ah = place(img, asset("dinonames", 3), S / 2, base, w=560, anchor="bottom")
    return (f"{n} 个词块（3 支向右的箭头＝快 / 1 枚蛋被 1 支箭头拽走＝贼）+ "
            f"1 支向下的箭头 + 1 只迅猛龙（宽 {aw}px）")


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
    bone(d, cx + 40, cy - 140, 230, pal)
    d.rectangle([cx - 150, cy - 300, cx - 116, cy - 110], fill=pal["bark"],
                outline=pal["ink"], width=7)                            # 锤柄
    d.rounded_rectangle([cx - 214, cy - 344, cx - 52, cy - 292], radius=12,
                        fill=pal["soft"], outline=pal["ink"], width=7)  # 锤头
    cx, cy, w_, h_ = boxes[1]
    base = cy + 120
    aw, ah = place(img, asset("dinonames", 2), cx, base, w=380, anchor="bottom")
    for sx in (-70, 70):
        d.line([cx + sx, base, cx + sx, base + 90], fill=pal["ink"], width=7)
    d.rounded_rectangle([cx - 150, base + 90, cx + 150, base + 210], radius=18,
                        fill=pal["paper"], outline=pal["ink"], width=9)
    return ("两格等大：左格 1 块石头里露出 1 根骨头 + 1 把锤子（有人把它挖出来）/ "
            f"右格 1 只挖出来的恐龙（宽 {aw}px）+ 下面用 2 根吊线挂着 1 块空名牌（不写字）")


# ---------------------------------------------------------------- cloud（云是怎么来的）
# 素材：1 积云 / 2 水珠 / 3 灰尘 / 4 太阳

@page("cloud", 2)
def _(d, pal, img):
    """天上那团白既不是棉花也不是烟，是水变出来的 —— 三样里划掉两样。"""
    place(img, asset("cloud", 1), S / 2, 250, w=560)
    xs, slot = lay(3)
    cy = 760
    for dx, dy, r in ((-0.55, 0.20, 0.42), (-0.12, -0.20, 0.52), (0.36, 0.06, 0.46),
                      (-0.12, 0.34, 0.40), (0.42, 0.42, 0.34)):       # 棉花：五个团
        disc(d, xs[0] + dx * 190, cy + dy * 190, r * 110, pal["paper"], pal, w=7)
    cross(d, xs[0], cy, 130, pal)
    for k in range(3):                                               # 烟：三缕往上飘
        sx = xs[1] - 70 + k * 70
        pts = [(sx + 34 * math.sin(t / 42.0), cy + 120 - t) for t in range(0, 250, 10)]
        d.line(pts, fill=pal["soft"], width=12, joint="curve")
    cross(d, xs[1], cy, 130, pal)
    dw, dh = place(img, asset("cloud", 2), xs[2], cy, h=190)
    d.ellipse([xs[2] - 130, cy - 130, xs[2] + 130, cy + 130], outline=pal["accent"], width=12)
    return ("上面 1 朵云（素材1，宽 560px）+ 下面 3 样并排：棉花（5 个团，1 个大叉划掉）/ "
            f"烟（3 缕，1 个大叉划掉）/ 1 颗水珠（素材2，高 {dh}px，1 个圈圈出来）")


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
    dx, dy = 280, S / 2
    aw, ah = place(img, asset("cloud", 3), dx, dy, w=130)
    arrow(d, dx + 110, dy, 560, dy, pal, w=12, head=32)
    R = 190
    disc(d, 780, dy, R, pal["soft"], pal, w=10)
    iw, ih = place(img, asset("cloud", 3), 780, dy, w=80)
    return (f"左边 1 粒灰尘（素材3，宽 {aw}px）→ 1 支向右的箭头 → "
            f"右边 1 颗水珠（半径 {R}px），正中心裹着同一粒灰尘（缩到宽 {iw}px）")


@page("cloud", 7)
def _(d, pal):
    """一颗水珠有多小：几百颗排起来才有一根头发那么宽。"""
    n = 200
    band = 800
    x0 = (S - band) / 2
    y0, y1 = 140, 884
    d.rectangle([x0, y0, x0 + band, y1], fill=pal["paper"])
    for x in (x0, x0 + band):
        d.line([x, y0, x, y1], fill=pal["ink"], width=9)
    dia = band / n
    cy = (y0 + y1) / 2
    for i in range(n):                       # 两色交替，看得出是一颗一颗，不是一条线
        cxx = x0 + dia * (i + 0.5)
        d.ellipse([cxx - dia / 2, cy - dia / 2, cxx + dia / 2, cy + dia / 2],
                  fill=pal["accent"] if i % 2 else pal["soft"])
    for x in (x0, x0 + band):                # 两端的对齐刻度
        for seg in range(5):
            yy = cy + 60 + seg * 26
            d.line([x, yy, x, yy + 13], fill=pal["line"], width=5)
    return (f"1 根放大的头发，宽 {band}px（上下贯穿画面，两条边线）；"
            f"里面 {n} 颗水珠首尾相接，每颗 {dia:.0f}px，合计正好 {dia * n:.0f}px = 头发的宽度")


@page("cloud", 8)
def _(d, pal):
    """一颗看不见，十颗也看不见，几千亿颗挤在一块儿就看见白了。"""
    xs, slot = lay(3)
    cy = S / 2
    counts = []
    disc(d, xs[0], cy, 6, pal["line"], pal, w=0)
    counts.append(1)
    n2 = 0
    for r_ in range(2):
        for c_ in range(5):
            disc(d, xs[1] - 36 + c_ * 18, cy - 9 + r_ * 18, 6, pal["line"], pal, w=0)
            n2 += 1
    counts.append(n2)
    cols, rows_ = 40, 30
    n3 = 0
    for r_ in range(rows_):
        for c_ in range(cols):
            px = xs[2] - (cols - 1) * 8 / 2 + c_ * 8
            py = cy - (rows_ - 1) * 8 / 2 + r_ * 8
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=pal["soft"])
            n3 += 1
    counts.append(n3)
    arrow(d, xs[0] + 40, cy, xs[1] - 70, cy, pal, w=10, head=26)
    arrow(d, xs[1] + 70, cy, xs[2] - 180, cy, pal, w=10, head=26)
    return (f"3 组水珠横着排开：{counts[0]} 颗 / {counts[1]} 颗（2 行 ×5）/ "
            f"{counts[2]} 颗（{rows_} 行 ×{cols}，挤成一片才看得见白），中间 2 支箭头")


@page("cloud", 11)
def _(d, pal):
    """水珠碰上水珠越碰越大，大到托不住就往下掉 —— 那就是雨。"""
    xs, slot = lay(4)
    cy = 440
    rs = (34, 52, 74, 74)
    disc(d, xs[0] - 40, cy, rs[0], pal["soft"], pal, w=8)
    disc(d, xs[0] + 40, cy, rs[0], pal["soft"], pal, w=8)
    disc(d, xs[1], cy, rs[1], pal["soft"], pal, w=8)
    disc(d, xs[2], cy, rs[2], pal["soft"], pal, w=8)
    disc(d, xs[3], cy - 40, rs[3], pal["accent"], pal, w=8)
    gap_arrow(d, pal, xs[0] + 40, cy, xs[1], cy, rs[0] + 16, rs[1] + 20)
    gap_arrow(d, pal, xs[1], cy, xs[2], cy, rs[1] + 16, rs[2] + 20)
    gap_arrow(d, pal, xs[2], cy, xs[3], cy - 40, rs[2] + 16, rs[3] + 20)
    base = S - MARGIN - 60
    arrow(d, xs[3], cy - 40 + rs[3] + 24, xs[3], base - 24, pal, w=12, head=34)
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    return (f"4 步横着排开：2 颗小水珠（半径 {rs[0]}px）→ 1 颗 {rs[1]}px → 1 颗 {rs[2]}px → "
            f"同样大的 1 颗往下掉；中间 3 支横向箭头 + 最后 1 支到地线的向下箭头")


# ---------------------------------------------------------------- fog（雾就是落在地上的云）
# 素材：1 光秃的树 / 2 水珠 / 3 长着松树的小山 / 4 太阳

@page("fog", 2)
def _(d, pal):
    """雾其实就是云，只不过这一朵没飘在天上，是贴着地面 —— 两朵云一模一样，只差高度。"""
    cw = 340
    ups = []
    for (cx, cy, w_, h_), high in zip(panel2(d, pal), (True, False)):
        base = cy + h_ / 2 - 60
        d.line([cx - w_ / 2 + 20, base, cx + w_ / 2 - 20, base], fill=pal["ink"], width=9)
        ccy = (cy - 180) if high else (base - 95)
        cloudlet(d, cx, ccy, cw, pal, fill=pal["soft"])   # 框底是 paper，云得换个色才看得出来
        ups.append(base - ccy)
    return (f"两格等大，两朵云由同一个 w={cw}px 画出来、形状完全一样："
            f"左格云心离地线 {ups[0]:.0f}px（飘在天上）/ 右格只离 {ups[1]:.0f}px（贴着地面）")


@page("fog", 4)
def _(d, pal, img):
    """空气一冷，水汽待不住，变成小水珠悬在半空 —— 前后一样多，只是变了样。"""
    n = 14
    xs, slot = lay(2)
    cy = S / 2
    step = 78
    cols = 4
    for k in range(n):
        gx = xs[0] - (cols - 1) * step / 2 + (k % cols) * step
        gy = cy - 1.5 * step + (k // cols) * step
        d.ellipse([gx - 24, gy - 24, gx + 24, gy + 24], outline=pal["line"], width=6)
    for k in range(n):
        dx = xs[1] - (cols - 1) * step / 2 + (k % cols) * step
        dy = cy - 1.5 * step + (k // cols) * step
        place(img, asset("fog", 2), dx, dy, h=64)
    arrow(d, 400, cy, 620, cy, pal, w=12, head=32)
    for k in range(3):                              # 变冷：三支短的向下箭头
        arrow(d, 430 + k * 80, cy - 210, 430 + k * 80, cy - 110, pal, w=9, head=24)
    return (f"左边 {n} 个只有淡轮廓的小圈（看不见的水汽，4 列 78px 间距）→ 1 支向右的箭头 → "
            f"右边 {n} 颗实心水珠（素材2，同样 4 列同样间距）；箭头上方 3 支向下的短箭头表示空气变冷")


@page("fog", 6)
def _(d, pal, img):
    """袖子上头发上全挂着细细的水珠，一颗一颗。"""
    n = 14
    pts = [(x, S / 2 + 60 * math.sin(x / 180.0)) for x in range(MARGIN, S - MARGIN + 1, 6)]
    d.line(pts, fill=pal["bark"], width=26, joint="curve")
    xs, slot = lay(n)
    for x in xs:
        y = S / 2 + 60 * math.sin(x / 180.0)
        place(img, asset("fog", 2), x, y + 46, h=76)
    return f"1 根放大的绒线横贯整幅（粗 26px）+ 挂在上面的 {n} 颗水珠（素材2，高 76px、间距 {slot:.0f}px）"


@page("fog", 8)
def _(d, pal, img):
    """雾天看得见的距离短得多，所以走路要慢、手要牵好。"""
    rows = [(1.00, "accent", "晴天能看多远"), (0.12, "soft", "雾天能看多远")]
    note = bars(d, pal, rows, h=96, gap=300)
    x0, full = MARGIN + 50, S - 2 * MARGIN - 100
    cy0 = S / 2 - 300 * (len(rows) - 1) / 2
    for i, (frac, _k, _t) in enumerate(rows):
        place(img, asset("fog", 1), x0 + full * frac - 52, cy0 + i * 300 - 48,
              h=170, anchor="bottom")
    return note + "；两条的右端各站 1 棵树（能看到的最远处），树脚就踩在各自那条的上边"


@page("fog", 10)
def _(d, pal, img):
    """太阳一出来，小水珠一颗一颗又变回看不见的气，雾就散了。"""
    n = 6
    base = 880
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    place(img, asset("fog", 4), S - MARGIN - 200, 210, w=250)
    xs, slot = lay(n)
    for x in xs:
        place(img, asset("fog", 2), x, base, h=70, anchor="bottom")
        arrow(d, x, base - 84, x, 448, pal, w=10, head=26)          # 起点在水珠上方，终点在淡圈下方
        d.ellipse([x - 26, 400 - 26, x + 26, 400 + 26], outline=pal["line"], width=6)
    return (f"1 个太阳（素材4）+ 1 条地线 + 地上 {n} 颗水珠（素材2，高 70px）；"
            f"每颗头上 1 支向上的箭头，起点在水珠上方 y=796、终点在 y=448，"
            f"箭头尖上方各 1 个淡色空圈（变回看不见的气）—— {n} 条气流全是一头一尾的直线，没有闭合的圈")


# ---------------------------------------------------------------- hail（冰雹是怎么长大的）
# 素材：1 冰雹 / 2 剖开的冰雹 / 3 积雨云 / 4 切开的洋葱

@page("hail", 2)
def _(d, pal, img):
    """冰雹长在又高又厚的积雨云里，云顶比飞机还高。"""
    ch = 760
    base = S - MARGIN - 60
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    ccx = S / 2 + 60
    aw, ah = place(img, asset("hail", 3), ccx, base, h=ch, anchor="bottom")
    top = base - ah
    py = top + 150
    px = max(MARGIN + 110, ccx - aw / 2 - 110)
    plane(d, px, py, 82, pal)
    for seg in range(9):                      # 飞机的高度线，虚的，一直画到云身上
        sx = px + 96 + seg * 34
        d.line([sx, py, sx + 18, py], fill=pal["line"], width=6)
    d.line([MARGIN, top, S - MARGIN, top], fill=pal["line"], width=5)
    return (f"1 朵积雨云（素材3，高 {ah}px，脚踩地线，云顶在 y={top}）+ 左边 1 架飞机；"
            f"飞机的高度虚线在 y={py}，比云顶低 {py - top}px")


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
def _(d, pal):
    """越往上越冷，升过某一条线水就冻住 —— 水珠一过那儿立刻裹上一层冰。"""
    note = bands(d, pal, 2, mark=0)
    top = MARGIN + 40
    h = (S - 2 * MARGIN - 80) / 2
    line_y = top + h
    d.line([MARGIN, line_y, S - MARGIN, line_y], fill=pal["ink"], width=16)
    r = 54
    disc(d, S / 2, line_y + 250, r, pal["paper"], pal, w=9)
    arrow(d, S / 2, line_y + 250 - r - 24, S / 2, line_y - 250 + r + 24, pal, w=12, head=34)
    disc(d, S / 2, line_y - 250, r + 26, pal["accent"], pal, w=9)
    disc(d, S / 2, line_y - 250, r, pal["paper"], pal, w=9)
    return (note + f"；分界线在 y={line_y:.0f}（加粗到 16px）；线下 1 颗光水珠（半径 {r}px）+ "
            f"1 支穿过分界线的向上箭头（起点 y={line_y + 250 - r - 24:.0f}、终点 y={line_y - 250 + r + 24:.0f}）+ "
            f"线上同一颗水珠外面多了 1 圈冰（外半径 {r + 26}px）")


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
    hs = (180, 360)
    cloud_base = 560
    for (cx, cy, w_, h_), ch, many in zip(panel2(d, pal), hs, (False, True)):
        base = cy + h_ / 2 - 50
        d.line([cx - w_ / 2 + 20, base, cx + w_ / 2 - 20, base], fill=pal["ink"], width=9)
        place(img, asset("hail", 3), cx, cloud_base, h=ch, anchor="bottom")
        if many:
            hxs, hslot = lay(n_hail, width=w_ * 0.86, margin=0)
            for hx in hxs:
                x = cx - w_ * 0.43 + hx
                arrow(d, x, cloud_base + 40, x, cloud_base + 170, pal, w=9, head=24)
                place(img, asset("hail", 1), x, cloud_base + 260, h=64)
        else:
            cross(d, cx, cloud_base + 170, 92, pal)
    return (f"两格等大，两朵云的脚都落在 y={cloud_base}：左格云高 {hs[0]}px（洛杉矶），云下 1 个大叉（不下冰雹）/ "
            f"右格云高 {hs[1]}px，云下 {n_hail} 支向下的箭头 + {n_hail} 颗落下来的冰雹")


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
def _(d, pal):
    """柱子越细转得越凶，最凶的比高速路上的车还要快上一倍。"""
    n_slow, n_fast = 2, 5
    for cx, wbot, n_spin in ((S / 2 - 250, 150, n_slow), (S / 2 + 250, 60, n_fast)):
        funnel(d, cx, 150, 520, 220, wbot, pal)
        for k in range(n_spin):
            yy = 200 + k * (280 / max(1, n_spin - 1)) if n_spin > 1 else 340
            half = (220 + (wbot - 220) * (yy - 150) / 370) / 2
            arc_arrow(d, pal, cx, yy, half + 30, 24, 200, 380, w=8, head=20, dot=False)
            disc(d, cx - half - 30, yy, 9, pal["accent"], pal, w=0)
    x0 = MARGIN + 60
    full = S - 2 * MARGIN - 120
    hbar(d, x0, 720, full * 0.50, 80, pal, pal["soft"])
    hbar(d, x0, 870, full * 1.00, 80, pal, pal["accent"])
    d.line([x0, 660, x0, 930], fill=pal["ink"], width=8)
    return (f"上面 2 根柱子一样高（350px）：粗的底宽 150px、绕着 {n_slow} 段弧线箭头 / "
            f"细的底宽 60px、绕着 {n_fast} 段；每段弧都有起点圆点和箭头尖，不闭合。"
            f"下面 2 条左端对齐的横条：上条 50%（高速路上的车）/ 下条 100%（最凶的龙卷风），正好一倍")


@page("tornado", 10)
def _(d, pal, img):
    """中部平原年年都有，那儿暖空气和冷空气老撞在一起；加州几乎没有。"""
    n_side = 3
    tw = 190
    for (cx, cy, w_, h_), plains in zip(panel2(d, pal), (True, False)):
        base = cy + h_ / 2 - 50
        d.line([cx - w_ / 2 + 20, base, cx + w_ / 2 - 20, base], fill=pal["ink"], width=9)
        aw, ah = place(img, asset("tornado", 1), cx, base, w=tw, anchor="bottom")
        if plains:
            for k in range(n_side):
                yy = 620 + k * 100
                arrow(d, cx - 205, yy, cx - 118, yy, pal, w=10, head=26)    # 暖空气，往右
                arrow(d, cx + 205, yy, cx + 118, yy, pal, w=10, head=26)    # 冷空气，往左
        else:
            cross(d, cx, base - ah / 2, 150, pal)
    return (f"两格等大，每格 1 个龙卷风站在地线上（宽 {tw}px）："
            f"左格左边 {n_side} 支向右的箭头（暖空气）+ 右边 {n_side} 支向左的箭头（冷空气），"
            f"两边对着撞在中间那根柱子上，每支都有起点和箭头尖 / "
            f"右格同样 1 个龙卷风被 1 个大叉划掉（加州几乎没有）")
