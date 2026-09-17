# -*- coding: utf-8 -*-
"""第七批示意图页（4/5）：天气预报、露水、猫胡须、狗鼻子、松鼠、蝙蝠、章鱼、企鹅。"""
from draw_diagrams import (S, MARGIN, page, asset, place, lie_flat, poly, disc, arrow, cross,
                           lay, panel2, hbar, footprint, bands, wave, cmp_len, cmp_height,
                           cmp_count, bars, timeline, steps, magnify, halo, silhouette)
from PIL import ImageColor
import math, random


def rgb(c):
    """调色板里存的是 "#c17a45" 这样的字符串，halo() 要的是 (r, g, b)。"""
    return ImageColor.getrgb(c)


def _box(a, box_w, box_h):
    """素材等比缩进这个盒子以后的实际 (宽, 高) —— 先算出来，再决定怎么摆。

    只按 h= 缩放会坑胖素材（一张 1.6:1 的图定高 300 就撑到 480 宽，压到邻居身上），
    只按 w= 缩放会坑瘦素材（定宽 380 能把高撑到八百多，直接冲出画面）。素材长什么样
    是模型说了算，页面代码不该替它猜 —— 两个方向都量一次，不出界由构造保证。
    """
    s = min(box_w / a.width, box_h / a.height)
    return max(1, round(a.width * s)), max(1, round(a.height * s))


def _fit(img, a, cx, cy, box_w, box_h, anchor="center"):
    """按 _box 算出的尺寸摆上去，返回实际占位 (宽, 高) —— 构造清单里直接打这个数。"""
    w_, _h = _box(a, box_w, box_h)
    return place(img, a, cx, cy, w=w_, anchor=anchor)


def _cap(a, h, max_w):
    """想要这么高，但宽不许超过 max_w —— 超了就按宽度反推一个矮一点的高度。

    同一张素材要摆出固定倍数的两个尺寸时用它：大的那个先 cap，小的按倍数算，
    倍数就还是准的（_fit 两个方向各挑各的，倍数会被挑没）。
    """
    return min(h, max_w * a.height / a.width)


def _dash(d, pal, x0, y0, x1, y1, seg=30, gap=30, w=6):
    """一条虚线（横或竖都行），返回画了几段。"""
    n = 0
    total = math.hypot(x1 - x0, y1 - y0)
    if total <= 0:
        return 0
    ux, uy = (x1 - x0) / total, (y1 - y0) / total
    t = 0.0
    while t < total:
        e = min(t + seg, total)
        d.line([x0 + ux * t, y0 + uy * t, x0 + ux * e, y0 + uy * e], fill=pal["line"], width=w)
        t += seg + gap
        n += 1
    return n


def _ruler(d, pal, x0, y, length, w=8, tick=26):
    """一根量尺：两端各 1 根短竖线 + 中间一条双箭头的横线。长度由调用方给死。"""
    for x in (x0, x0 + length):
        d.line([x, y - tick, x, y + tick], fill=pal["ink"], width=w)
    arrow(d, x0 + length / 2, y, x0 + 6, y, pal, w=w, head=22)
    arrow(d, x0 + length / 2, y, x0 + length - 6, y, pal, w=w, head=22)


def _drop(d, cx, cy, r, pal, fill=None, w=6):
    """一颗水滴：下面一个圆，上面收成尖。整颗是一条闭合轮廓，没有两条线交叉。"""
    pts = [(cx, cy - r * 2.0)]
    for i in range(17):
        a = math.radians(-40 + i * 260 / 16)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    poly(d, pts, pal, fill if fill is not None else pal["soft"], w)


# 侧看的猫脸以前是「一个圆 + 六根手画的线」，现在整张脸是素材5，胡须的张开由素材
# 自己的外框量出来 —— 程序不再替模型画脸。


# ---------------------------------------------------------------- forecast（明天会下雨吗）

@page("forecast", 2)
def _(d, pal, img):
    """要算明天先得量今天：温度、气压、风向、湿度 —— 正好四样。"""
    bw, bh = _fit(img, asset("forecast", 1), S / 2, MARGIN + 390, 560, 360, anchor="bottom")
    xs, slot = lay(4)
    cy = 720
    box = (slot * 0.88, 450)
    tw, th = _fit(img, asset("forecast", 5), xs[0], cy, *box)      # 1 温度计
    gw, gh = _fit(img, asset("forecast", 6), xs[1], cy, *box)      # 2 气压表
    x = xs[2]                                                     # 3 风向标
    d.line([x, cy + 160, x, cy - 110], fill=pal["ink"], width=11)
    arrow(d, x - 96, cy - 110, x + 96, cy - 110, pal, w=9, head=26)
    _drop(d, xs[3], cy + 40, 88, pal, pal["soft"], 8)             # 4 湿度
    return (f"1 个百叶箱（素材1，{bw}×{bh}px）+ 下面 4 样量具：温度计（素材5，{tw}×{th}px）/ "
            f"气压表（素材6，{gw}×{gh}px）/ 风向标（1 根杆 + 1 支横箭头）/ "
            f"1 颗水滴（潮不潮），正好 4 样")


@page("forecast", 5)
def _(d, pal, img):
    """气球一路往上，越高越冷 —— 越上面那根温度条越短。"""
    # 层数从 4 减到 3：气球是这页的主角，挤在 1/4 页高的一层里只剩 150px，看不清。
    n = 3
    top, h = MARGIN, (S - 2 * MARGIN) / n
    note = bands(d, pal, n, mark=0, top=top, h=h)
    bx = 290
    bw, bh = _fit(img, asset("forecast", 2), bx, top + h * 0.5, 380, h * 0.92)
    arrow(d, bx, S - MARGIN - 60, bx, top + h * 0.96, pal, w=12, head=32)
    lens = [140, 290, 440]               # 顶层最短 = 最冷
    x0 = 520
    for i in range(n):
        hbar(d, x0, top + h * (i + 0.5), lens[i], 86, pal, pal["paper"])
    return (note + f"；最上面那层里 1 只气球（素材2，{bw}×{bh}px）+ "
                   f"1 支从最下面直通最上层的箭头带着它往上；"
                   f"右边 {n} 根左端对齐的温度条 {lens[0]}/{lens[1]}/{lens[2]}px，越往上越短")


@page("forecast", 7)
def _(d, pal, img):
    """雷达往外发一下，碰到雨点弹回来 —— 去和回是两道，各有各的箭头。"""
    rw, rh = _fit(img, asset("forecast", 3), 175, 820, 290, 430, anchor="bottom")
    n, r = 12, 30
    # 最右那一列以前圆心落在 x=995、半径 30，画到 1025 —— 越过右边 30px 留白。
    # 整块雨点往左挪 35px：最右边缘 960+30=990，最左 690-30=660，都在留白里。
    for i in range(n):
        _drop(d, 825 + (i % 4 - 1.5) * 90, 490 + (i // 4 - 1) * 120, r, pal, pal["soft"])
    x0, x1 = 340, 690
    wave(d, x0, x1, 270, pal, cycles=4, amp=54, w=10)
    arrow(d, x0, 175, x1, 175, pal, w=11, head=30)
    wave(d, x0, x1, 620, pal, cycles=4, amp=54, w=10)
    arrow(d, x1, 730, x0, 730, pal, w=11, head=30)
    return (f"1 座雷达（素材3，{rw}×{rh}px）+ 右边 {n} 颗雨点（4 列 ×3 行，各半径 {r}px，"
            f"最右一颗的右边缘在 x=990，没越过留白）：上面 1 道声波 + 1 支向右的箭头（发出去），"
            f"下面 1 道声波 + 1 支向左的箭头（弹回来），两道分开画，方向不会看反")


@page("forecast", 9)
def _(d, pal):
    """把空气切成一个一个小方块，每块都有自己的数。"""
    cols = rows = 6
    side = S - 2 * MARGIN - 80
    x0 = y0 = (S - side) / 2
    cw = side / cols
    n = 0
    for r_ in range(rows):
        for c_ in range(cols):
            cx, cy = x0 + cw * (c_ + .5), y0 + cw * (r_ + .5)
            d.rectangle([cx - cw / 2, cy - cw / 2, cx + cw / 2, cy + cw / 2],
                        fill=pal["paper"] if (r_ + c_) % 2 else pal["soft"],
                        outline=pal["ink"], width=5)
            disc(d, cx, cy, 16, pal["accent"], pal, w=0)
            n += 1
    return f"1 张切成 {rows}×{cols} = {n} 个小方块的格子，每块正中 1 个点（那一块自己的数）"


@page("forecast", 10)
def _(d, pal):
    """一步一步往前推：每推一步，那块空气就往前挪一格。"""
    k, side = 4, 150
    xs, slot = lay(k)
    cy = S / 2
    cw = side / 4
    for s_ in range(k):
        x0, y0 = xs[s_] - side / 2, cy - side / 2
        for r_ in range(4):
            for c_ in range(4):
                on = (r_ == 3 - s_ and c_ == s_)
                d.rectangle([x0 + c_ * cw, y0 + r_ * cw, x0 + (c_ + 1) * cw, y0 + (r_ + 1) * cw],
                            fill=pal["accent"] if on else pal["paper"], outline=pal["ink"], width=4)
    for i in range(k - 1):
        arrow(d, xs[i] + side / 2 + 14, cy, xs[i + 1] - side / 2 - 14, cy, pal, w=8, head=18)
    return (f"{k} 步横着排开，每步 1 张 4×4 的格子，中间 {k - 1} 支箭头；"
            f"着色的那一块每步往前挪 1 格，{k} 步正好从左下角走到右上角")


@page("forecast", 11)
def _(d, pal):
    """算明天很准，算下个星期就跑偏了 —— 五条路一开始挨在一起，越往后越散。"""
    x0, x1 = MARGIN + 80, S - MARGIN - 90
    cy, n = S / 2, 5
    near, far = 26, 620
    for i in range(n):
        t = i / (n - 1) - .5
        pts = []
        for k in range(21):
            u = k / 20
            spread = near + (far - near) * u ** 2
            pts.append((x0 + (x1 - x0) * u, cy + t * spread + math.sin(u * 9 + i) * 12 * u))
        d.line(pts, fill=pal["soft"] if i % 2 else pal["accent"], width=9, joint="curve")
        arrow(d, pts[-2][0], pts[-2][1], pts[-1][0], pts[-1][1], pal, w=9, head=22)
    mx = x0 + (x1 - x0) * 0.28
    for seg in range(12):
        y = MARGIN + 40 + seg * 78
        d.line([mx, y, mx, y + 38], fill=pal["line"], width=6)
    return (f"1 个起点分出 {n} 条路，每条末端 1 支箭头：起点处总散开 {near}px、终点处 {far}px"
            f"（{far // near} 倍）；28% 处 1 条竖虚线（算到明天，{n} 条还挨在一起）")


# ---------------------------------------------------------------- dew（早上草叶上的水珠）

@page("dew", 2)
def _(d, pal):
    """空气里一直有水，散成极小的粒 —— 放大了才看得见。"""
    x0, y0, w_, h_ = MARGIN + 30, MARGIN + 60, 470, 470
    d.rectangle([x0, y0, x0 + w_, y0 + h_], fill=pal["paper"], outline=pal["ink"], width=8)
    rnd = random.Random(11)
    spots, cells, n = {}, 8, 0
    for r_ in range(cells):
        for c_ in range(cells):
            jx, jy = rnd.randint(-10, 10), rnd.randint(-10, 10)
            spots[(r_, c_)] = (jx, jy)
            disc(d, x0 + w_ * (c_ + .5) / cells + jx, y0 + h_ * (r_ + .5) / cells + jy,
                 5, pal["soft"], pal, w=0)
            n += 1
    sx, sy = x0 + w_ * 1.5 / cells, y0 + h_ * 1.5 / cells
    sr = w_ * 1.6 / cells
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], outline=pal["accent"], width=9)
    bx, by, br = S - MARGIN - 240, S - MARGIN - 240, 230
    disc(d, bx, by, br, pal["paper"], pal, w=9)
    d.ellipse([bx - br, by - br, bx + br, by + br], outline=pal["accent"], width=9)
    k = 0
    for r_ in range(3):
        for c_ in range(3):
            jx, jy = spots[(r_, c_)]
            disc(d, bx + (c_ - 1) * 120 + jx * 2, by + (r_ - 1) * 120 + jy * 2,
                 26, pal["soft"], pal, w=5)
            k += 1
    return (f"1 格空气里 {n} 个小得看不出来的水粒（{cells}×{cells}，每个半径 5px），"
            f"左上角圈出的 {k} 个（3×3）放大到右下角的大圆里，半径 26px（放大 {26 // 5} 倍）")


@page("dew", 4)
def _(d, pal):
    """热的时候口袋大，凉下来口袋小，装不下的只好出来。"""
    warm, cool = 12, 5
    out = warm - cool
    for (cx, cy, w_, h_), hot in zip(panel2(d, pal), (True, False)):
        bw, bh = w_ * (0.80 if hot else 0.52), h_ * (0.52 if hot else 0.34)
        by = cy - h_ * 0.12
        d.rounded_rectangle([cx - bw / 2, by - bh / 2, cx + bw / 2, by + bh / 2], radius=40,
                            fill=pal["paper"], outline=pal["ink"], width=9)
        k, cols = (warm, 4) if hot else (cool, 3)
        rows = math.ceil(k / cols)
        for i in range(k):
            px = cx - bw * 0.34 + (i % cols) * (bw * 0.68 / (cols - 1))
            py = by - bh * 0.26 + (i // cols) * (bh * 0.52 / max(1, rows - 1))
            disc(d, px, py, 18, pal["soft"], pal, w=5)
        if not hot:
            for i in range(out):
                _drop(d, cx - w_ * 0.38 + i * (w_ * 0.76 / (out - 1)), cy + h_ * 0.30,
                      24, pal, pal["soft"])
    return (f"左格 热（大口袋 368×439px，装 {warm} 粒）/ 右格 凉（小口袋 239×287px，只装 {cool} 粒），"
            f"装不下的 {out} 粒落到下面变成 {out} 颗水珠：{warm} = {cool} + {out}")


@page("dew", 6)
def _(d, pal, img):
    """晴的夜热全跑光，草叶上结露；有云的夜挡回来一半，草叶是干的。"""
    up, n_grass = 4, 3
    wet, dry = asset("dew", 1), asset("dew", 5)
    out, sizes = [], []
    for (cx, cy, w_, h_), cloudy in zip(panel2(d, pal), (False, True)):
        base = cy + h_ * 0.34
        ctop = cy - h_ * 0.34
        d.line([cx - w_ * 0.44, base, cx + w_ * 0.44, base], fill=pal["ink"], width=9)
        gw, gh = 0, 0
        for i in range(n_grass):
            gw, gh = _fit(img, dry if cloudy else wet, cx + (i - 1) * 118, base,
                          108, 220, anchor="bottom")
        sizes.append((gw, gh))
        if cloudy:
            cw, ch = _fit(img, asset("dew", 4), cx, ctop + 70, 300, 170)
            for s in (-1, 1):
                # 云两边的空处：跑得掉
                arrow(d, cx + s * 190, base - 240, cx + s * 190, ctop - 40, pal, w=9, head=24)
                # 正撞上云：被挡回来
                arrow(d, cx + s * 62, ctop + 70 + ch / 2 + 20, cx + s * 62, base - 240,
                      pal, w=9, head=24)
            out.append(f"右格 天上 1 朵云（素材4，{cw}×{ch}px）：{up // 2} 支从云两边的空处跑掉 + "
                       f"{up // 2} 支撞上云被挡回来（正好一半）")
        else:
            for i in range(up):
                arrow(d, cx - 150 + i * 100, base - 240, cx - 150 + i * 100,
                      cy - h_ * 0.44, pal, w=9, head=24)
            out.append(f"左格 天上没有云：{up} 支热箭头全部向上跑掉")
    return (" / ".join(out) + f"；两格各 {n_grass} 片草叶、站同一条地线、按同一个盒子等比缩放："
            f"左格是带露珠的（素材1，各 {sizes[0][0]}×{sizes[0][1]}px）/ "
            f"右格是干的（素材5，各 {sizes[1][0]}×{sizes[1][1]}px）")


@page("dew", 8)
def _(d, pal, img):
    """不是天上掉的（划掉），不是草根冒的（划掉），是叶子旁边的空气里现出来的。"""
    xs, slot = lay(3)
    base = S - MARGIN - 200
    d.rectangle([MARGIN, base, S - MARGIN, S - MARGIN], fill=pal["bark"], outline=pal["ink"], width=8)
    a = asset("dew", 1)
    ww = hh = 0
    for x in xs:
        ww, hh = _fit(img, a, x, base, slot * 0.86, 380, anchor="bottom")
    # 1 从天上掉下来 —— 划掉
    for k in range(3):
        _drop(d, xs[0] - 70 + k * 70, MARGIN + 100, 20, pal, pal["soft"], 5)
    arrow(d, xs[0], MARGIN + 170, xs[0], base - hh - 30, pal, w=9, head=24)
    cross(d, xs[0], MARGIN + 260, 62, pal, w=14)
    # 2 从草根冒上来 —— 划掉
    arrow(d, xs[1], S - MARGIN - 40, xs[1], base - 120, pal, w=9, head=24)
    cross(d, xs[1], base + 100, 62, pal, w=14)
    # 3 旁边的空气里来的 —— 不划
    for k in range(6):
        disc(d, xs[2] - 180 - (k % 3) * 34, 480 + (k // 3) * 42, 8, pal["soft"], pal, w=0)
    arrow(d, xs[2] - 160, 520, xs[2] - 60, 520, pal, w=9, head=24)
    arrow(d, xs[2] + 160, 610, xs[2] + 60, 610, pal, w=9, head=24)
    return (f"3 格并排、3 片草叶都是 {ww}×{hh}px（同 1 张素材1、同一个盒子）、站同一条地线："
            f"左格 从天上掉（1 支向下的箭头，划掉）/ "
            f"中格 从草根冒（1 支向上的箭头，划掉）/ 右格 从旁边的空气里来（2 支指向叶子的箭头，没划）")


@page("dew", 10)
def _(d, pal, img):
    """霜不是冻住的露，是水汽一步跨过去直接长成的冰。"""
    frost = asset("dew", 3)
    y1, y2 = 300, 730
    fw = fh = 0
    for y in (y1, y2):
        for k in range(9):
            disc(d, 90 + (k % 3) * 42, y - 42 + (k // 3) * 42, 9, pal["soft"], pal, w=0)
        fw, fh = _fit(img, frost, 850, y, 280, 250)
    dw, dh = _fit(img, asset("dew", 6), 500, y1, 200, 200)
    arrow(d, 250, y1, 370, y1, pal, w=9, head=24)
    arrow(d, 630, y1, 750, y1, pal, w=9, head=24)
    cross(d, 500, y1, 165, pal, w=16)
    arrow(d, 250, y2, 750, y2, pal, w=12, head=30)
    return (f"上排 2 步（水汽 → 1 颗水珠（素材6，{dw}×{dh}px）→ 霜，2 支短箭头合计 240px）"
            f"整排被 1 个大叉划掉；下排 1 步（水汽 → 霜，1 支长箭头 500px）；"
            f"两排的霜一样大（同 1 张素材3，各 {fw}×{fh}px）")


# ---------------------------------------------------------------- whisker（猫的胡须有什么用）

@page("whisker", 2)
def _(d, pal, img):
    """胡须不只长在嘴边：嘴边、眼睛上面、下巴、前腿后面，一共 4 处。"""
    cx, cy = S / 2, S / 2 + 20
    w_, h_ = _fit(img, asset("whisker", 1), cx, cy, S - 2 * MARGIN - 40, S - 2 * MARGIN - 120)
    spots = [(0.18, 0.44), (0.30, 0.26), (0.21, 0.60), (0.48, 0.78)]
    for sx, sy in spots:
        hx, hy = cx - w_ / 2 + w_ * sx, cy - h_ / 2 + h_ * sy
        d.ellipse([hx - 62, hy - 48, hx + 62, hy + 48], outline=pal["accent"], width=10)
    return f"1 只猫（素材1，{w_}×{h_}px）+ {len(spots)} 个圈：嘴边 / 眼睛上面 / 下巴 / 前腿后面"


@page("whisker", 3)
def _(d, pal):
    """别的毛只是浅浅地插在皮上，胡须扎得很深，根上还连着神经。"""
    shallow, deep = 40, 160
    for (cx, cy, w_, h_), whisk in zip(panel2(d, pal), (False, True)):
        skin = cy - 40
        d.rectangle([cx - w_ * 0.46, skin, cx + w_ * 0.46, skin + 300],
                    fill=pal["bark"], outline=pal["ink"], width=8)
        if whisk:
            d.line([cx, skin + deep, cx, skin - 300], fill=pal["ink"], width=20)
            for i in range(3):
                a = math.radians(35 + i * 55)
                d.line([cx, skin + deep, cx + 120 * math.cos(a), skin + deep + 120 * math.sin(a)],
                       fill=pal["accent"], width=8)
            disc(d, cx, skin + deep, 34, pal["accent"], pal, w=7)
        else:
            for i in (-1, 0, 1):
                d.line([cx + i * 130, skin + shallow, cx + i * 130, skin - 170],
                       fill=pal["ink"], width=11)
    return (f"左格 3 根普通的毛，根只扎进皮 {shallow}px / 右格 1 根胡须，根扎进 {deep}px"
            f"（{deep // shallow} 倍），根上还连着 3 条神经")


@page("whisker", 5)
def _(d, pal, img):
    """胡须向左右张开的宽度，正好等于身上最宽的那一处 —— 两个宽度是同一个数。

    整只猫改成素材4（俯视）。胡须张开多宽是模型画的，程序量不出来，所以「相等」这句话
    不能再靠 span=620 这个共享变量了 —— 改成靠标注保证：两条竖虚线落在素材外框的左右
    两边（这是程序真量得出来的数），上下各 1 根一样长的量尺，一根量胡须、一根量身子，
    两根长度是同一个变量。相等由这两根尺子说了算，不由模型说了算。
    """
    cx, cy = S / 2, S / 2 + 10
    span, tall = _fit(img, asset("whisker", 4), cx, cy, 640, 690)
    top_y, bot_y = cy - tall / 2 - 75, cy + tall / 2 + 75
    segs = 0
    for s in (-1, 1):
        segs += _dash(d, pal, cx + s * span / 2, top_y - 45, cx + s * span / 2, bot_y + 45)
    _ruler(d, pal, cx - span / 2, top_y, span)
    _ruler(d, pal, cx - span / 2, bot_y, span)
    return (f"俯视的猫 1 只（素材4，{span}×{tall}px）：两条竖虚线（共 {segs} 段）正落在素材"
            f"外框的左右两边；上面 1 根量尺量胡须张开、下面 1 根量尺量身子最宽处，"
            f"两根都是 {span}px —— 同一个变量画出来的，不多也不少")


@page("whisker", 6)
def _(d, pal, img):
    """胡须碰不到边，身子就过得去；碰到了，就退回来。

    洞口以前是两块手画的 rectangle，现在是素材3（侧面带方洞的纸箱）。洞口本身多宽是
    模型画的，所以两排不比绝对值，比倍数：同一张箱子素材，下排整个缩到 0.6 倍，
    洞口跟着缩到 0.6 倍 —— 这个倍数是程序给的。猫脸两排一样大。
    """
    head, box = asset("whisker", 5), asset("whisker", 3)
    k = 0.6
    hx, bx = 220, 780
    hw, hh = _box(head, 340, 330)
    bw, bh = _box(box, 400, 430)
    out = []
    for cy, f, fwd in ((262, 1.0, True), (762, k, False)):
        place(img, head, hx, cy, w=hw)
        w2, h2 = place(img, box, bx, cy, w=round(bw * f))
        left = bx - w2 / 2
        for s in (-1, 1):          # 胡须上下张开那两条线 = 素材自己的外框上下边
            y = cy + s * hh / 2
            _dash(d, pal, hx + hw / 2 + 10, y, left - 16, y)
            if not fwd:
                disc(d, left - 16, y, 18, pal["accent"], pal, w=6)
        x1, x2 = hx + hw / 2 + 40, left - 40
        arrow(d, *((x1, cy, x2, cy) if fwd else (x2, cy, x1, cy)), pal=pal, w=12, head=32)
        out.append(f"{'上' if fwd else '下'}排 箱子 {w2}×{h2}px，"
                   f"1 支{'往里走' if fwd else '往回退'}的箭头"
                   + ("" if fwd else "，两条胡须线顶在箱面上，各 1 个接触点（共 2 个）"))
    return (f"两排同一只猫脸（素材5，都是 {hw}×{hh}px，两条横虚线正落在它外框的上下边，"
            f"胡须上下张开都是 {hh}px）：" + out[0] + "；" + out[1] +
            f"（下排的箱子是上排的 {k} 倍，洞口也就是 {k} 倍）")


@page("whisker", 9)
def _(d, pal, img):
    """剪短一截就量不准了：胡须进得去，身子还是过不去。

    「完整 / 剪短」用的是同一张胡须素材（素材2）的两个长度，剪短那根就是短的那个数；
    「身子」那行是整只猫（素材4）的实际占宽，第 1 行的胡须就照这个数来 —— 两行是同
    一个变量，第 5 页那句「一样宽」在这里还站得住。三行右边是同一个箱子。
    """
    cat, whi, box = asset("whisker", 4), lie_flat(asset("whisker", 2)), asset("whisker", 3)
    bw, bh = _box(box, 300, 230)
    bx, x0 = 810, MARGIN + 60
    full, cat_h = _box(cat, 430, 355)      # 身子能放多大放多大，它的实际占宽就是那个数
    cut = round(full * 0.53)
    rows = ((185, full, whi, 300, "cross", "完整的胡须（素材2）"),
            (445, cut, whi, 560, "in", "剪短以后（同 1 张素材2）"),
            (760, full, cat, 962, "cross", "猫的身子（素材4）"))
    for cy, L, a, my, kind, _t in rows:
        place(img, box, bx, cy, w=bw)
        place(img, a, x0 + L / 2, cy, w=L)
        _ruler(d, pal, x0, my, L)
        if kind == "in":
            arrow(d, x0 + L + 40, cy, bx - bw / 2 - 30, cy, pal, w=11, head=28)
        else:
            cross(d, bx, cy, min(bw, bh) * 0.42, pal, w=14)
    return (f"三行左端都从 {x0}px 起算、各 1 根量尺，右边三次是同一个箱子（素材3，"
            f"各 {bw}×{bh}px）：第 1 行 完整的胡须 {full}px → 箱子上 1 个叉（过不去）/ "
            f"第 2 行 剪短后 {cut}px（只有完整的 53%）→ 1 支进箱子的箭头（进得去）/ "
            f"第 3 行 身子 {full}px，和第 1 行一模一样（用的是同一个数）→ 1 个叉："
            f"胡须骗了它，身子还是过不去")


@page("whisker", 11)
def _(d, pal, img):
    """掉下一根，过些天又长出来，长到该有的长短就停住 —— 第 4 行和第 1 行一样长。"""
    a = lie_flat(asset("whisker", 2))
    # 整根的长度不再写死 620：先让素材在「宽 620 × 高 190（行距 240 减去缝）」里缩一次，
    # 拿它实际占的宽当「整根」，短的按 0.4 倍算。素材再胖也撑不破行距，而「第 4 行和
    # 第 1 行一样长」用的还是同一个变量。
    full, fh = _box(a, 620, 190)
    short = round(full * 0.4)
    x0 = MARGIN + 90
    ys = (180, 420, 660, 900)
    lens = (full, 0, short, full)
    for y, L in zip(ys, lens):
        disc(d, x0, y, 20, pal["accent"], pal, w=6)
        if L:
            place(img, a, x0 + 30 + L / 2, y, w=L)
    for i in range(3):
        arrow(d, x0 - 46, ys[i] + 46, x0 - 46, ys[i + 1] - 46, pal, w=8, head=20)
    return (f"4 行左端对齐、行间 3 支箭头，行距 {ys[1] - ys[0]}px：第 1 行整根 {full}px"
            f"（高 {fh}px）/ 第 2 行空的（掉了）/ 第 3 行新长出来 {short}px（整根的 40%）/ "
            f"第 4 行 {full}px，和第 1 行完全相同（长到该有的长短就停）")


# ---------------------------------------------------------------- dognose（狗为什么一路闻过去）

@page("dognose", 2)
def _(d, pal):
    """人 1 份，狗 40 份 —— 一个点一份，数得清。"""
    one, many, cols = 1, 40, 8
    rows = math.ceil(many / cols)
    for (cx, cy, w_, h_), dog in zip(panel2(d, pal), (False, True)):
        if dog:
            for i in range(many):
                disc(d, cx - w_ * 0.36 + (i % cols) * (w_ * 0.72 / (cols - 1)),
                     cy - h_ * 0.30 + (i // cols) * (h_ * 0.60 / (rows - 1)),
                     18, pal["accent"], pal, w=5)
        else:
            disc(d, cx, cy, 18, pal["soft"], pal, w=5)
    return f"左格 {one} 个点（人）/ 右格 {many} 个点（狗，{rows} 行 ×{cols}），正好 {many // one} 倍"


@page("dognose", 4)
def _(d, pal, img):
    """左边鼻孔和右边鼻孔分开来闻，两边闻到的不一样多。"""
    hw, hh = place(img, asset("dognose", 2), S / 2, 275, h=430)
    for seg in range(8):
        y = 500 + seg * 62
        d.line([S / 2, y, S / 2, y + 30], fill=pal["line"], width=6)
    left_v, right_v = 170, 340
    for s, v, key in ((-1, left_v, "soft"), (1, right_v, "accent")):
        x = S / 2 + s * 240
        d.rounded_rectangle([x - 70, 600, x + 70, 600 + v], radius=24,
                            fill=pal[key], outline=pal["ink"], width=8)
        arrow(d, x, 570, S / 2 + s * 70, 470, pal, w=9, head=24)
    return (f"1 个狗鼻子（素材2，高 {hh}px）+ 中间 1 条竖虚线把左右分开；"
            f"左边 1 根 {left_v}px 的条、右边 1 根 {right_v}px 的条（右边是左边的 {right_v / left_v:.0f} 倍），"
            f"各 1 支指向那一侧鼻孔的箭头")


@page("dognose", 6)
def _(d, pal, img):
    """吸气从鼻孔前面进，呼气从两边的缝里出 —— 出去的风绕开了前面的味。"""
    cy = 330
    hw, hh = place(img, asset("dognose", 2), S / 2, cy, h=430)
    nose = cy + hh * 0.22
    n = 14
    for i in range(n):
        disc(d, S / 2 - 150 + (i % 7) * 50, 760 + (i // 7) * 60, 13, pal["soft"], pal, w=0)
    arrow(d, S / 2, 720, S / 2, nose + 30, pal, w=12, head=30)
    for s in (-1, 1):
        arrow(d, S / 2 + s * 60, nose + 20, S / 2 + s * 330, nose + 250, pal, w=10, head=26)
    return (f"1 个狗鼻子：1 支从前面那团味道指向鼻孔的箭头（吸进去，向上）+ "
            f"2 支从鼻子两侧斜着往后下方的箭头（呼出去，绕开前面）；前方 {n} 个味道小点没被吹散")


@page("dognose", 8)
def _(d, pal, img):
    """一根电线杆上留着好几只狗写下的消息，一张压着一张。"""
    pw, ph = _fit(img, asset("dognose", 3), 230, S - MARGIN - 40, 400, 820, anchor="bottom")
    n = 6
    for i in range(n):
        x = 520 + (i % 2) * 40
        y = 180 + i * 118
        d.rectangle([x, y, x + 380, y + 150], fill=pal["paper"] if i % 2 else pal["soft"],
                    outline=pal["ink"], width=7)
    return f"1 根电线杆（素材3，{pw}×{ph}px）+ 右边 {n} 张一张压着一张的纸条（每张错开 40px，后贴的压住先贴的）"


@page("dognose", 10)
def _(d, pal, img):
    """昨天有只猫从这儿走过去：味道一路变新，所以还知道是往哪边走的。

    以前这页用 footprint() 画脚印 —— 那是个三趾恐龙脚印，可这页讲的是猫。换成素材4
    （俯视的猫脚印），画的东西和旁白说的才是一回事。
    """
    n = 6
    base = S - MARGIN - 190
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=9)
    xs, slot = lay(n)
    paw = asset("dognose", 4)
    pw, ph = _box(paw, slot * 0.94, 190)
    r0, dr = 20, 9
    for i, x in enumerate(xs):
        place(img, paw, x, base - 30 + (0 if i % 2 else 70), w=pw)
        r = r0 + i * dr
        d.ellipse([x - r, 400 - r, x + r, 400 + r], outline=pal["accent"], width=7)
    arrow(d, xs[0], 190, xs[-1], 190, pal, w=12, head=32)
    return (f"1 条地线上 {n} 个左右交错的猫脚印（素材4，同 1 张、各 {pw}×{ph}px），"
            f"每个上面 1 个味道圈：半径从 {r0}px 一路涨到 {r0 + (n - 1) * dr}px"
            f"（越往前越新），上面 1 支指着走向的箭头")


# ---------------------------------------------------------------- squirrel（松鼠记得埋在哪儿吗）

@page("squirrel", 2)
def _(d, pal):
    """不是几十个，是好几千个 —— 左格 30 个，右格 3000 个。"""
    few, cols_f = 30, 6
    many, cols_m = 3000, 40
    rows_f, rows_m = few // cols_f, many // cols_m
    for (cx, cy, w_, h_), lots in zip(panel2(d, pal), (False, True)):
        k, cols, rows = (many, cols_m, rows_m) if lots else (few, cols_f, rows_f)
        for i in range(k):
            px = cx - w_ * 0.42 + (i % cols) * (w_ * 0.84 / (cols - 1))
            py = cy - h_ * 0.42 + (i // cols) * (h_ * 0.84 / (rows - 1))
            if lots:
                disc(d, px, py, 3.5, pal["bark"], pal, w=0)
            else:
                disc(d, px, py, 26, pal["accent"], pal, w=5)
    return (f"左格 {few} 个（{rows_f} 行 ×{cols_f}，各半径 26px）/ "
            f"右格 {many} 个（{rows_m} 行 ×{cols_m}，各半径 3.5px），正好 {many // few} 倍")


@page("squirrel", 4)
def _(d, pal, img):
    """埋下去以前，先把果子在自己脸上蹭一蹭，蹭上一点味道。"""
    sw, sh = place(img, asset("squirrel", 1), S / 2, 280, h=380)
    cy = 760
    x1, x2 = S / 2 - 210, S / 2 + 210
    nut = asset("squirrel", 2)
    aw, ah = place(img, nut, x1, cy, h=210)
    place(img, nut, x2, cy, h=210)
    arrow(d, x1 + 120, cy, x2 - 120, cy, pal, w=11, head=28)
    for i in range(3):
        r = 96 + i * 34
        d.arc([x2 - r, cy - r, x2 + r, cy + r], -60, 60, fill=pal["accent"], width=8)
    return (f"1 只松鼠（素材1，高 {sh}px）+ 下面 2 个一样大的果子（蹭之前 / 蹭之后，都高 {ah}px）"
            f"+ 中间 1 支箭头；蹭过的那个右边 3 道味道弧线")


@page("squirrel", 6)
def _(d, pal):
    """埋下十个，大概能挖回七八个，剩下的忘了。"""
    buried, found = 10, 8
    note = bars(d, pal, [(1.0, "soft", f"埋下 {buried} 个"),
                         (found / buried, "accent", f"挖回 {found} 个")])
    x0, full = MARGIN + 50, S - 2 * MARGIN - 100
    cell, cy0 = full / buried, S / 2 - 95
    for i, k in enumerate((buried, found)):
        cy = cy0 + i * 190
        for j in range(1, k):
            d.line([x0 + cell * j, cy - 40, x0 + cell * j, cy + 40], fill=pal["ink"], width=5)
    for j in range(found, buried):
        cross(d, x0 + cell * (j + 0.5), cy0 + 190, 34, pal, w=10)
    return (note + f"；上条切成 {buried} 格、下条切成 {found} 格（每格 {cell:.0f}px），"
                   f"缺的 {buried - found} 格各 1 个叉：{buried} = {found} + {buried - found}")


@page("squirrel", 9)
def _(d, pal, img):
    """忘掉的那两个就一直留在土里：外面下着雪，里面一动不动。"""
    n = 3
    top, h = MARGIN + 40, (S - 2 * MARGIN - 80) / n
    note = bands(d, pal, n, top=top, h=h)
    snow = 12
    for i in range(snow):
        disc(d, MARGIN + 70 + i * 74, top + h * (0.30 + 0.40 * (i % 2)), 12, pal["paper"], pal, w=0)
    nut = asset("squirrel", 2)
    aw, ah = 0, 0
    for s in (-1, 1):
        aw, ah = place(img, nut, S / 2 + s * 200, top + h * 1.5, h=210)
    return note + f"；第 1 层（雪）里 {snow} 片雪点，第 2 层（土）里埋着 2 个果子，各高 {ah}px"


@page("squirrel", 11)
def _(d, pal, img):
    """一片林子里，总有好些棵树是松鼠当初忘掉的那几个果子长成的。"""
    # 6 棵树挤在一行，每棵才 125px 宽，树看着像草。减到 4 棵，树和果子都大起来。
    n = 4
    base = S - MARGIN - 80
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    xs, slot = lay(n)
    tree, nut = asset("squirrel", 3), asset("squirrel", 2)
    tw, th = _box(tree, slot * 0.86, 720)
    for x in xs:
        place(img, tree, x, base, w=tw, anchor="bottom")
    nw, nh = _box(nut, 175, 215)
    for i in (1, 3):
        place(img, nut, xs[i] - tw * 0.38, base, w=nw, anchor="bottom")
        halo(img, nut, xs[i] - tw * 0.38, base, w=nw, color=rgb(pal["accent"]),
             grow=14, width=10, anchor="bottom")
    return (f"同一条地线上 {n} 棵小树（素材3，各 {tw}×{th}px、槽宽 {slot:.0f}px，互不挨着）；"
            f"其中 2 棵根边各 1 个果子（素材2，各 {nw}×{nh}px），果子外面各 1 圈沿它自己"
            f"轮廓画的强调线（正好是前面忘掉的那 2 个）")


# ---------------------------------------------------------------- bat（蝙蝠在黑里怎么飞）

@page("bat", 2)
def _(d, pal, img):
    """那对翅膀是手指撑开的一层皮 —— 圈出翅膀上那几根指骨。"""
    return magnify(img, d, pal, "bat", 1, (0.22, 0.46), w=S - 2 * MARGIN - 80, r=0.13)


@page("bat", 4)
def _(d, pal, img):
    """我们的叫声稀，蝙蝠的叫声密 —— 密到我们的耳朵听不见。"""
    slow, fast = 3, 15
    x0, x1 = MARGIN + 50, S - MARGIN - 330
    wave(d, x0, x1, 330, pal, cycles=slow, amp=110, w=12)
    wave(d, x0, x1, 730, pal, cycles=fast, amp=52, w=8)
    ear = asset("bat", 5)                      # 耳朵以前是两条嵌套的 arc
    ew, eh = _box(ear, 270, 300)
    for cy, deaf in ((330, False), (730, True)):
        ex = S - MARGIN - 160
        place(img, ear, ex, cy, w=ew)
        if deaf:
            cross(d, ex, cy, min(ew, eh) * 0.55, pal, w=14)
    return (f"上排 {slow} 个波（听得见的，一个波 {(x1 - x0) / slow:.0f}px）/ "
            f"下排 {fast} 个波（蝙蝠的，一个波 {(x1 - x0) / fast:.0f}px，密 {fast // slow} 倍）；"
            f"两排各 1 只耳朵（素材5，同 1 张、各 {ew}×{eh}px），下排那只打了 1 个叉")


@page("bat", 5)
def _(d, pal, img):
    """声音喊出去一直往前跑，撞到东西弹回来 —— 去一道、回一道，方向分得清。"""
    bw, bh = _fit(img, asset("bat", 1), MARGIN + 170, 512, 300, 320)
    dw, dh = _fit(img, asset("bat", 2), S - MARGIN - 170, 512, 300, 560)
    # 旁白里那个比方：「像皮球扔到墙上，又弹回自己手里」—— 皮球本来就有素材，摆上
    ballw, ballh = _fit(img, asset("bat", 4), 540, 512, 210, 210)
    x0, x1 = 390, 640
    wave(d, x0, x1, 290, pal, cycles=4, amp=56, w=10)
    arrow(d, x0, 170, x1, 170, pal, w=11, head=30)
    wave(d, x0, x1, 730, pal, cycles=4, amp=56, w=10)
    arrow(d, x1, 850, x0, 850, pal, w=11, head=30)
    return (f"1 只蝙蝠（素材1，{bw}×{bh}px）+ 1 扇门（素材2，{dw}×{dh}px）+ 中间 1 个皮球"
            f"（素材4，{ballw}×{ballh}px，旁白里那个比方）：上面 1 道声波 + 1 支向右的箭头"
            f"（喊出去），下面 1 道声波 + 1 支向左的箭头（弹回来），两道分开画")


@page("bat", 6)
def _(d, pal, img):
    """弹回来得快，东西就在近处；弹回来得慢，东西就还远着。"""
    bat, door = asset("bat", 1), asset("bat", 2)
    bw, bh = _box(bat, 220, 360)
    dw, dh = _box(door, 170, 300)
    trips = []
    for cy, dxx in ((300, 520), (740, 900)):
        place(img, bat, MARGIN + 130, cy, w=bw)
        place(img, door, dxx, cy, w=dw)
        # 箭头那一头以前写死在门左边 95px 处 —— 门实际多宽得问素材，别替它猜
        x0, x1 = MARGIN + 130 + bw / 2 + 30, dxx - dw / 2 - 25
        arrow(d, x0, cy - 130, x1, cy - 130, pal, w=10, head=26)
        arrow(d, x1, cy + 130, x0, cy + 130, pal, w=10, head=26)
        trips.append(x1 - x0)
    return (f"两排同一只蝙蝠（各 {bw}×{bh}px）、同一扇门（各 {dw}×{dh}px）："
            f"上排来回的路 {trips[0]:.0f}px（近），"
            f"下排 {trips[1]:.0f}px（远，{trips[1] / trips[0]:.1f} 倍）；"
            f"每排都有 1 支向右的箭头（喊出去）和 1 支向左的箭头（弹回来）")


@page("bat", 8)
def _(d, pal, img):
    """远的时候慢慢叫，快抓住了就叫成一串。"""
    bw, bh = _fit(img, asset("bat", 1), MARGIN + 150, 512, 260, 360)
    mw, mh = _fit(img, asset("bat", 3), S - MARGIN - 140, 512, 200, 230)
    x0, x1 = MARGIN + 300, S - MARGIN - 260
    d.line([x0, 512, x1, 512], fill=pal["ink"], width=8)
    n, r = 12, 0.87
    wts = [r ** i for i in range(n - 1)]
    tot = sum(wts)
    pxs = [x0]
    for k in wts:
        pxs.append(pxs[-1] + (x1 - x0) * k / tot)
    for px in pxs:
        d.line([px, 512 - 70, px, 512 + 70], fill=pal["accent"], width=7)
    arrow(d, x0, 512 - 200, x1, 512 - 200, pal, w=11, head=30)
    return (f"1 只蝙蝠（{bw}×{bh}px）→ 1 只小虫（{mw}×{mh}px），"
            f"中间 {n} 下叫声：第 1 个间隔 {pxs[1] - pxs[0]:.0f}px，"
            f"最后 1 个 {pxs[-1] - pxs[-2]:.0f}px（越靠近虫子越密），上面 1 支指向虫子的箭头")


@page("bat", 11)
def _(d, pal, img):
    """这个本事叫回声定位；海里的船也这么干，往水底喊一声，听回声有多深。"""
    sizes = []
    for (cx, cy, w_, h_), boat in zip(panel2(d, pal), (False, True)):
        top = cy - h_ * 0.40
        if boat:
            d.line([cx - w_ * 0.46, top + 96, cx + w_ * 0.46, top + 96], fill=pal["ink"], width=8)
            # 船以前是「多边形船身 + 矩形烟囱」，左格却是模型画的蝙蝠，两边不是一种画法
            sizes.append(_fit(img, asset("bat", 6), cx, top + 106, w_ * 0.70, 190,
                              anchor="bottom"))
        else:
            sizes.append(_fit(img, asset("bat", 1), cx, top + 110, w_ * 0.70, 260))
        floor_y = cy + h_ * 0.30
        d.rectangle([cx - w_ * 0.46, floor_y, cx + w_ * 0.46, floor_y + 120],
                    fill=pal["bark"], outline=pal["ink"], width=8)
        arrow(d, cx - 90, top + 270, cx - 90, floor_y - 40, pal, w=10, head=26)
        arrow(d, cx + 90, floor_y - 40, cx + 90, top + 270, pal, w=10, head=26)
    return (f"左格 1 只蝙蝠（素材1，{sizes[0][0]}×{sizes[0][1]}px）+ 下面 1 片墙 / "
            f"右格 1 条船（素材6，{sizes[1][0]}×{sizes[1][1]}px，坐在 1 条水面线上）+ "
            f"下面 1 片海底：两格各 1 支向下的箭头（喊出去）和 1 支向上的箭头（回声弹回来），"
            f"两支分开左右画")


# ---------------------------------------------------------------- octopus（章鱼有三个心脏）

@page("octopus", 2)
def _(d, pal, img):
    """两个小心脏挨着鳃，把血压进鳃里；中间那个大的，再把血送到全身。"""
    xs, slot = lay(3)
    heart, gill = asset("octopus", 2), asset("octopus", 3)
    # 心脏 180px、鳃 180px 都太小（鳃那一把羽状细丝这个尺寸必糊）。放大，但倍数要准：
    # 大的先按槽宽 cap 一次，小的照 2/3 算 —— 两个都只按高度缩放，1.5 倍就是 1.5 倍。
    big = _cap(heart, 330, slot * 0.92)
    small = big * 2 / 3
    cy, gy = 650, 250
    hw = hh = sw = sh = 0
    for i, x in enumerate(xs):
        if i == 1:
            hw, hh = place(img, heart, x, cy, h=big)
        else:
            sw, sh = place(img, heart, x, cy, h=small)
    gw, gh = 0, 0
    for i in (0, 2):
        gw, gh = _fit(img, gill, xs[i], gy, slot * 0.92, 260)
        arrow(d, xs[i], cy - small / 2 - 15, xs[i], gy + gh / 2 + 20, pal, w=10, head=26)
    for s in (-1, 1):
        arrow(d, xs[1] + s * 60, cy + big / 2 + 15, xs[1] + s * 250, cy + big / 2 + 150,
              pal, w=10, head=26)
    return (f"3 个心脏排成一排（都是素材2）：两边 2 个小的（各 {sw}×{sh}px）+ 中间 1 个大的"
            f"（{hw}×{hh}px，正好是小的 {big / small:.1f} 倍，两个都只按高度缩放）；"
            f"2 个小的头上各 1 片鳃（素材3，各 {gw}×{gh}px）、各 1 支向上的箭头指着它；"
            f"大的 2 支向下的箭头指向全身")


@page("octopus", 4)
def _(d, pal, img):
    """游起来的时候，中间那个大心脏会停下来不跳；爬的时候才跳。"""
    oct_, heart = asset("octopus", 1), asset("octopus", 2)
    ow = oh = sw = sh = 0
    for (cx, cy, w_, h_), swim in zip(panel2(d, pal), (True, False)):
        ow, oh = _fit(img, oct_, cx, cy - h_ * 0.24, w_ * 0.86, h_ * 0.40)
        hy = cy + h_ * 0.24
        sw, sh = _fit(img, heart, cx, hy, w_ * 0.56, 250)          # 心脏原来才 190px
        if swim:
            cross(d, cx, hy, min(sw, sh) * 0.62, pal, w=16)
        else:
            for i in range(3):
                r = min(sw, sh) * 0.62 + i * 32
                d.ellipse([cx - r, hy - r, cx + r, hy + r], outline=pal["accent"], width=8)
    return (f"两格的章鱼和心脏一样大（章鱼各 {ow}×{oh}px、心脏各 {sw}×{sh}px）："
            f"左格 游（大心脏上 1 个叉 = 停住不跳）/ 右格 爬（大心脏外面 3 圈跳动的圈）")


@page("octopus", 6)
def _(d, pal, img):
    """神经细胞一大半长在那八条胳膊上，脑袋里反而少。"""
    place(img, asset("octopus", 1), S / 2, MARGIN + 170, h=280)
    arms, head = 0.65, 0.35
    note = bars(d, pal, [(arms, "accent", "八条胳膊"), (head, "soft", "脑袋")])
    x0, full = MARGIN + 50, S - 2 * MARGIN - 100
    cy = S / 2 - 95
    for j in range(1, 8):
        x = x0 + full * arms * j / 8
        d.line([x, cy - 40, x, cy + 40], fill=pal["ink"], width=5)
    return (note + f"；上面那条切成 8 格（八条胳膊各 1 格，每格 {full * arms / 8:.0f}px），"
                   f"下面那条是脑袋，只有上面那条的 {head / arms * 100:.0f}%")


@page("octopus", 9)
def _(d, pal, img):
    """全身上下只有嘴是硬的：嘴那么大的洞，整只章鱼都挤得过去。"""
    beak = 96
    xs, slot = lay(3)
    cy = S / 2
    note = steps(img, d, pal, "octopus", [1, None, 1], cy=cy, arrows=False)
    d.ellipse([xs[0] + 40 - beak / 2, cy + 60 - beak / 2,
               xs[0] + 40 + beak / 2, cy + 60 + beak / 2], outline=pal["accent"], width=10)
    d.rectangle([xs[1] - 46, MARGIN + 110, xs[1] + 46, S - MARGIN - 110],
                fill=pal["bark"], outline=pal["ink"], width=8)
    disc(d, xs[1], cy, beak / 2, pal["ground"], pal, w=8)
    arrow(d, xs[0] + slot * 0.42, cy, xs[1] - 70, cy, pal, w=10, head=26)
    arrow(d, xs[1] + 70, cy, xs[2] - slot * 0.42, cy, pal, w=10, head=26)
    return (note + f"（中间那格是墙，不放素材）；墙上的洞直径 {beak}px，"
                   f"和左边圈出来的嘴一模一样大（{beak}px）；1 支箭头进洞、1 支箭头出洞")


@page("octopus", 11)
def _(d, pal, img):
    """胳膊一贴上石头，吸盘就尝出底下藏没藏着螃蟹。"""
    # 以前：一条粗线加 7 个 disc 当胳膊、5 点 poly 加一个椭圆当石头，旁边却是 380px 的
    # 模型章鱼。现在胳膊、石头、螃蟹全是素材，吸盘是模型画的，所以不再报吸盘数目
    # （旁白也没点名几个）。螃蟹改成整只露在外面，外面 1 圈沿轮廓的强调线。
    ow, oh = _fit(img, asset("octopus", 1), 250, 300, 420, 400)
    base = S - MARGIN - 40
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    rw, rh = _fit(img, asset("octopus", 6), 735, base, 480, 400, anchor="bottom")
    aw, ah = _fit(img, asset("octopus", 5), 470, 590, 390, 320)
    crab = asset("octopus", 4)
    cw, ch = _box(crab, 260, 220)
    place(img, crab, 735, base - 8, w=cw, anchor="bottom")
    halo(img, crab, 735, base - 8, w=cw, color=rgb(pal["accent"]), grow=14, width=10,
         anchor="bottom")
    arrow(d, 620, 630, 380, 455, pal, w=9, head=24)
    return (f"1 只章鱼（素材1，{ow}×{oh}px）+ 1 条搭到石头上的胳膊（素材5，{aw}×{ah}px，"
            f"吸盘是素材自己带的）+ 1 块底下有洞的石头（素材6，{rw}×{rh}px，站在地线上）"
            f"+ 洞里 1 只螃蟹（素材4，{cw}×{ch}px，整只都露在外面，外面 1 圈沿它自己轮廓"
            f"画的强调线）；1 支从胳膊贴着石头那一头指回脑袋的箭头")


# ---------------------------------------------------------------- penguin（企鹅站在冰上为什么不冷）

@page("penguin", 2)
def _(d, pal, img):
    """企鹅身上三层：外面羽毛，羽毛底下压着空气，皮底下还有厚厚的脂肪。"""
    pw, ph = place(img, asset("penguin", 1), S / 2, MARGIN + 270, h=250, anchor="bottom")
    n, top, h = 3, 330, 200
    note = bands(d, pal, n, mark=2, top=top, h=h)
    feathers, airs = 9, 12
    for i in range(feathers):
        x = MARGIN + 90 + i * 100
        d.line([x, top + 30, x + 40, top + h - 30], fill=pal["ink"], width=9)
    for i in range(airs):
        disc(d, MARGIN + 80 + i * 78, top + h + h * (0.35 if i % 2 else 0.65),
             15, pal["paper"], pal, w=5)
    return (note + f"；上面 1 只企鹅（高 {ph}px）；第 1 层 {feathers} 根羽毛 / "
                   f"第 2 层 {airs} 个空气小点 / 第 3 层（脂肪）填了强调色")


@page("penguin", 4)
def _(d, pal, img):
    """羽毛根上的绒把空气兜住了，空气不爱传热，就成了一层被子。"""
    xs, slot = lay(2)
    cy = S / 2
    fw, fh = _fit(img, asset("penguin", 2), xs[0], cy, slot * 0.72, 560)
    bw, bh = _fit(img, asset("penguin", 3), xs[1], cy, slot * 0.74, 420)
    n = 10
    for i in range(n):                       # 小点贴着羽毛的实际外框走，不写死 130px
        s = -1 if i < 5 else 1
        disc(d, xs[0] + s * (fw / 2 + 18 + (i % 2) * 40), cy + 120 + (i % 5) * 56,
             15, pal["paper"], pal, w=5)
    arrow(d, xs[0] + slot * 0.40, cy, xs[1] - slot * 0.40, cy, pal, w=11, head=28)
    return (f"2 格 + 中间 1 支箭头：1 根带绒的羽毛（素材2，{fw}×{fh}px，两边贴着它的外框"
            f"共兜着 {n} 个空气小点）→ 1 条被子（素材3，{bw}×{bh}px）")


@page("penguin", 6)
def _(d, pal):
    """往下的血管和往上的紧紧贴在一块儿：热还没到脚，就被带回去了。"""
    cx = S / 2
    top, foot_y = MARGIN + 60, S - MARGIN - 190
    poly(d, [(cx - 160, top), (cx + 160, top), (cx + 120, foot_y), (cx - 120, foot_y)],
         pal, pal["paper"], 10)
    poly(d, [(cx - 120, foot_y), (cx + 120, foot_y), (cx + 230, foot_y + 130),
             (cx - 230, foot_y + 130)], pal, pal["bark"], 10)
    down_x, up_x = cx - 70, cx + 70
    per = 3
    for x, dn in ((down_x, True), (up_x, False)):
        d.rounded_rectangle([x - 24, top + 40, x + 24, foot_y - 40], radius=24,
                            fill=pal["soft"] if dn else pal["paper"],
                            outline=pal["ink"], width=7)
        for k in range(per):
            ay = top + 140 + k * (foot_y - top - 320) / 2
            if dn:
                arrow(d, x, ay, x, ay + 110, pal, w=9, head=24)
            else:
                arrow(d, x, ay + 110, x, ay, pal, w=9, head=24)
    heat = 4
    for k in range(heat):
        hy = top + 180 + k * 150
        arrow(d, down_x + 30, hy, up_x - 30, hy, pal, w=8, head=20)
    return (f"1 条腿的剖面，里面 2 条并排、互不相接的血管（中心相距 {up_x - down_x}px）："
            f"左边那条往下（{per} 支向下的箭头）、右边那条往上（{per} 支向上的箭头）；"
            f"中间 {heat} 支从往下那条指向往上那条的热箭头，脚在最下面")


@page("penguin", 8)
def _(d, pal, img):
    """天最冷的时候挤成一团：外面的顶着风，里面的暖烘烘。

    以前是 61 个 disc —— 一个圆点顶一只企鹅。换成素材以后一只只剩 80px，糊成一片，
    那就从「太简笔」变成「太小」。旁白只说「几千只」，没点名具体数目，所以这里减到
    11 只、每只放到 200px 以上：看得清一只是一只，比数得出 61 个圆点要紧。
    """
    p = asset("penguin", 4)
    pw, ph = _box(p, 210, 210)
    cx, cy = 585, S / 2
    inner, outer, r_in, r_out = 3, 8, 115, 265
    disc(d, cx, cy, 250, pal["accent"], pal, w=8)          # 团里的热
    for k, (m, R, off) in enumerate(((inner, r_in, 0.0), (outer, r_out, 0.4))):
        for i in range(m):
            a = 2 * math.pi * i / m + off
            place(img, p, cx + R * math.cos(a), cy + R * math.sin(a), w=pw)
    winds = 3
    for i in range(winds):
        arrow(d, MARGIN + 15, 300 + i * 212, cx - r_out - pw / 2 - 25, 300 + i * 212,
              pal, w=11, head=28)
    return (f"1 团 {inner + outer} 只企鹅（都是素材4、同 1 张、各 {pw}×{ph}px）："
            f"里圈 {inner} 只（半径 {r_in}px）+ 外圈 {outer} 只（半径 {r_out}px，一只挨着一只）；"
            f"底下 1 个半径 250px 的暖色圆 = 团里的热（里圈那 {inner} 只整个坐在上面）；"
            f"左边 {winds} 支吹到团外沿的风箭头")


@page("penguin", 10)
def _(d, pal, img):
    """团里比团外暖得多，中间那只有时候还嫌热，自己挪到边上去。

    和第 8 页同一个道理：14 个 disc 换成素材以后一只只剩 92px，所以减到圈上 7 只，
    每只 200px 往上。缺口开在正上方，圆心那只顺着箭头从缺口里走出去 —— 挪出来那只
    和圆心那只是同 1 张素材、同样大，一眼看得出是从圈里出来的。
    """
    p = asset("penguin", 4)
    pw, ph = _box(p, 200, 200)
    cx, cy, R = 400, 620, 230
    n, gap_i = 8, 0                      # i=0 就是正上方那一格，空着当缺口
    disc(d, cx, cy, R, pal["accent"], pal, w=10)
    on = 0
    for i in range(n):
        if i == gap_i:
            continue
        a = 2 * math.pi * i / n - math.pi / 2
        place(img, p, cx + R * math.cos(a), cy + R * math.sin(a), w=pw)
        on += 1
    place(img, p, cx, cy, w=pw)                          # 圆心那只（挪之前）
    gy = cy - (R + 175)
    place(img, p, cx, gy, w=pw)                          # 同 1 只，挪之后
    arrow(d, cx, cy - ph / 2 - 20, cx, gy + ph / 2 + 25, pal, w=10, head=26)
    inside, outside = 420, 120
    for x, v, key in ((855, inside, "accent"), (950, outside, "soft")):
        d.rounded_rectangle([x - 40, 930 - v, x + 40, 930], radius=20,
                            fill=pal[key], outline=pal["ink"], width=8)
    return (f"1 个填了暖色的圆（团里，半径 {R}px）+ 圆周上 {on} 只企鹅（素材4，各 {pw}×{ph}px）"
            f"+ 正上方 1 处空出来的缺口；圆心 1 只顺着 1 支向上的箭头穿过缺口挪到圆外"
            f"（圆外那只和圆心那只是同 1 张素材、同样大，就是挪之后的它）；"
            f"右边 2 根温度条：团里 {inside}px、团外 {outside}px（{inside / outside:.1f} 倍）")
