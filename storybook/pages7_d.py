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
