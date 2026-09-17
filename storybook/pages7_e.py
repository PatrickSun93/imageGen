# -*- coding: utf-8 -*-
"""第七批示意图页（4/5）：天气预报、露水、猫胡须、狗鼻子、松鼠、蝙蝠、章鱼、企鹅。"""
from draw_diagrams import (S, MARGIN, page, asset, place, lie_flat, poly, disc, arrow, cross,
                           lay, panel2, hbar, footprint, bands, wave, cmp_len, cmp_height,
                           cmp_count, bars, timeline, steps, magnify)
import math, random


def _drop(d, cx, cy, r, pal, fill=None, w=6):
    """一颗水滴：下面一个圆，上面收成尖。整颗是一条闭合轮廓，没有两条线交叉。"""
    pts = [(cx, cy - r * 2.0)]
    for i in range(17):
        a = math.radians(-40 + i * 260 / 16)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    poly(d, pts, pal, fill if fill is not None else pal["soft"], w)


def _cat_side(d, pal, cx, cy, half, reach, n=3, r=60, lim=None):
    """侧看的猫脸：一个圆 + 每边 n 根胡须，最外一根的尖正好落在 cy±half，总张开 2*half。

    lim=(上界, 下界) 时胡须画到边就停（不许穿进墙里），返回每根停住的位置 —— 那就是接触点。
    """
    disc(d, cx, cy, r, pal["paper"], pal, w=8)
    hits = []
    for s in (-1, 1):
        for i in range(n):
            ty = cy + s * half * (1 - i * 0.34)
            pts, hit = [], None
            for k in range(25):
                t = k / 24
                px = cx + r * 0.6 + (reach - r * 0.6) * t
                py = cy + (ty - cy) * t - s * 26 * math.sin(math.pi * t)
                if lim and not (lim[0] <= py <= lim[1]):
                    hit = pts[-1] if pts else (px, py)
                    break
                pts.append((px, py))
            if len(pts) > 1:
                d.line(pts, fill=pal["ink"], width=8, joint="curve")
            if hit:
                hits.append(hit)
    return hits


# ---------------------------------------------------------------- forecast（明天会下雨吗）

@page("forecast", 2)
def _(d, pal, img):
    """要算明天先得量今天：温度、气压、风向、湿度 —— 正好四样。"""
    place(img, asset("forecast", 1), S / 2, MARGIN + 330, h=290, anchor="bottom")
    xs, slot = lay(4)
    cy = 720
    # 1 温度计
    x = xs[0]
    d.rounded_rectangle([x - 28, cy - 160, x + 28, cy + 80], radius=28,
                        fill=pal["paper"], outline=pal["ink"], width=7)
    d.rectangle([x - 14, cy - 60, x + 14, cy + 70], fill=pal["accent"])
    disc(d, x, cy + 108, 48, pal["accent"], pal, w=7)
    # 2 气压表
    x = xs[1]
    disc(d, x, cy - 10, 104, pal["paper"], pal, w=8)
    for i in range(8):
        a = math.pi * 2 * i / 8
        d.line([x + 80 * math.cos(a), cy - 10 + 80 * math.sin(a),
                x + 98 * math.cos(a), cy - 10 + 98 * math.sin(a)], fill=pal["ink"], width=6)
    arrow(d, x, cy - 10, x + 72 * math.cos(-1.1), cy - 10 + 72 * math.sin(-1.1), pal, w=8, head=18)
    # 3 风向标
    x = xs[2]
    d.line([x, cy + 150, x, cy - 100], fill=pal["ink"], width=11)
    arrow(d, x - 96, cy - 100, x + 96, cy - 100, pal, w=9, head=26)
    # 4 湿度（一颗水滴）
    _drop(d, xs[3], cy + 30, 86, pal, pal["soft"], 8)
    return "1 个百叶箱（素材1）+ 下面 4 样量具：温度计 / 气压表 / 风向标 / 水滴（潮不潮），正好 4 样"


@page("forecast", 5)
def _(d, pal, img):
    """气球一路往上，越高越冷 —— 越上面那根温度条越短。"""
    n = 4
    top, h = MARGIN + 40, (S - 2 * MARGIN - 80) / n
    note = bands(d, pal, n, mark=0, top=top, h=h)
    bx = 300
    place(img, asset("forecast", 2), bx, top + h * 0.5, h=h * 0.68)
    arrow(d, bx, S - MARGIN - 70, bx, top + h * 0.95, pal, w=12, head=32)
    lens = [120, 220, 320, 420]          # 顶层最短 = 最冷
    for i in range(n):
        hbar(d, 560, top + h * (i + 0.5), lens[i], 76, pal, pal["paper"])
    return (note + f"；1 支从最下面直通最上层的箭头带着气球往上，"
                   f"右边 4 根左端对齐的温度条 {lens[0]}/{lens[1]}/{lens[2]}/{lens[3]}px，越往上越短")


@page("forecast", 7)
def _(d, pal, img):
    """雷达往外发一下，碰到雨点弹回来 —— 去和回是两道，各有各的箭头。"""
    place(img, asset("forecast", 3), 165, 820, h=430, anchor="bottom")
    n = 12
    for i in range(n):
        _drop(d, 860 + (i % 4 - 1.5) * 90, 490 + (i // 4 - 1) * 120, 30, pal, pal["soft"])
    x0, x1 = 330, 700
    wave(d, x0, x1, 270, pal, cycles=4, amp=54, w=10)
    arrow(d, x0, 175, x1, 175, pal, w=11, head=30)
    wave(d, x0, x1, 620, pal, cycles=4, amp=54, w=10)
    arrow(d, x1, 730, x0, 730, pal, w=11, head=30)
    return (f"1 座雷达（素材3）+ 右边 {n} 颗雨点：上面 1 道声波 + 1 支向右的箭头（发出去），"
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
def _(d, pal):
    """晴的夜热全跑光，草叶上结露；有云的夜挡回来一半，草叶是干的。"""
    up, drops = 4, 0
    out = []
    for (cx, cy, w_, h_), cloudy in zip(panel2(d, pal), (False, True)):
        base = cy + h_ * 0.34
        ctop = cy - h_ * 0.34
        d.line([cx - w_ * 0.44, base, cx + w_ * 0.44, base], fill=pal["ink"], width=9)
        for i in range(3):
            gx = cx - 110 + i * 110
            lean = -1 if i == 1 else 1
            pts = [(gx, base)]
            for k in range(1, 9):
                t = k / 8
                pts.append((gx + (16 + 34 * t) * lean * t, base - 190 * t))
            d.line(pts, fill=pal["soft"], width=13, joint="curve")
            if not cloudy:
                for j in range(2):
                    px, py = pts[3 + j * 3]
                    _drop(d, px, py, 15, pal, pal["paper"], 5)
                    drops += 1
        if cloudy:
            seg, gap_ = 100, 34
            for i in (-1, 0, 1):
                sx = cx + i * (seg + gap_)
                d.rounded_rectangle([sx - seg / 2, ctop, sx + seg / 2, ctop + 96], radius=44,
                                    fill=pal["soft"], outline=pal["ink"], width=8)
            for s in (-1, 1):
                arrow(d, cx + s * 67, base - 260, cx + s * 67, ctop - 80, pal, w=9, head=24)
                arrow(d, cx + s * 150, ctop + 120, cx + s * 150, base - 260, pal, w=9, head=24)
            out.append("右格 1 排云（3 段 + 2 条缝）：2 支穿过缝跑掉 + 2 支被云挡回来")
        else:
            for i in range(up):
                arrow(d, cx - 150 + i * 100, base - 260, cx - 150 + i * 100,
                      cy - h_ * 0.44, pal, w=9, head=24)
            out.append(f"左格 没有云：{up} 支热箭头全部向上跑掉")
    return " / ".join(out) + f"；左格 3 根草上共 {drops} 颗露珠，右格 3 根草是干的"


@page("dew", 8)
def _(d, pal, img):
    """不是天上掉的（划掉），不是草根冒的（划掉），是叶子旁边的空气里现出来的。"""
    xs, slot = lay(3)
    base, hh = S - MARGIN - 200, 380
    d.rectangle([MARGIN, base, S - MARGIN, S - MARGIN], fill=pal["bark"], outline=pal["ink"], width=8)
    a = asset("dew", 1)
    for x in xs:
        place(img, a, x, base, h=hh, anchor="bottom")
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
    return (f"3 格并排、3 片草叶都高 {hh}px 站同一条地线：左格 从天上掉（1 支向下的箭头，划掉）/ "
            f"中格 从草根冒（1 支向上的箭头，划掉）/ 右格 从旁边的空气里来（2 支指向叶子的箭头，没划）")


@page("dew", 10)
def _(d, pal, img):
    """霜不是冻住的露，是水汽一步跨过去直接长成的冰。"""
    frost = asset("dew", 3)
    y1, y2 = 300, 730
    for y in (y1, y2):
        for k in range(9):
            disc(d, 90 + (k % 3) * 42, y - 42 + (k // 3) * 42, 9, pal["soft"], pal, w=0)
        place(img, frost, 850, y, h=250)
    arrow(d, 250, y1, 380, y1, pal, w=9, head=24)
    _drop(d, 470, y1 + 14, 50, pal, pal["soft"])
    arrow(d, 570, y1, 700, y1, pal, w=9, head=24)
    cross(d, 512, y1, 150, pal, w=16)
    arrow(d, 250, y2, 700, y2, pal, w=12, head=30)
    return ("上排 2 步（水汽 → 水珠 → 霜，2 支短箭头合计 260px）整排被 1 个大叉划掉；"
            "下排 1 步（水汽 → 霜，1 支长箭头 450px），两排的霜一样大（高 250px）")


# ---------------------------------------------------------------- whisker（猫的胡须有什么用）

@page("whisker", 2)
def _(d, pal, img):
    """胡须不只长在嘴边：嘴边、眼睛上面、下巴、前腿后面，一共 4 处。"""
    cx, cy = S / 2, S / 2 + 20
    w_, h_ = place(img, asset("whisker", 1), cx, cy, h=S - 2 * MARGIN - 120)
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
def _(d, pal):
    """胡须向左右张开的宽度，正好等于身上最宽的那一处 —— 两个宽度是同一个数。"""
    span = 620
    cx = S / 2
    head_y, body_y = 340, 700
    d.ellipse([cx - span / 2, body_y - 230, cx + span / 2, body_y + 230],
              fill=pal["soft"], outline=pal["ink"], width=9)
    d.line([cx, body_y + 200, cx, 985], fill=pal["ink"], width=16)
    disc(d, cx, head_y, 125, pal["paper"], pal, w=9)
    n = 4
    for s in (-1, 1):
        poly(d, [(cx + s * 44, head_y - 104), (cx + s * 126, head_y - 175),
                 (cx + s * 122, head_y - 68)], pal, pal["paper"], 8)
        for i in range(n):
            rx, ry = cx + s * 95, head_y - 40 + i * 28
            tx, ty = cx + s * span / 2, head_y - 160 + i * 105
            pts = []
            for k in range(9):
                t = k / 8
                pts.append((rx + (tx - rx) * t, ry + (ty - ry) * t - 46 * math.sin(math.pi * t)))
            d.line(pts, fill=pal["ink"], width=9, joint="curve")
    for s in (-1, 1):
        x = cx + s * span / 2
        for seg in range(8):
            y = head_y - 120 + seg * 60
            d.line([x, y, x, y + 30], fill=pal["line"], width=6)
    return (f"俯视：身体最宽处 {span}px，每边 {n} 根胡须、尖到尖也正好 {span}px，"
            f"两个宽度用的是同一个数；两端各 1 条竖虚线把这两个宽度对齐")


@page("whisker", 6)
def _(d, pal):
    """胡须碰不到边，身子就过得去；碰到了，就退回来。"""
    half, reach, cx = 120, 260, 260
    wide, narrow = 300, 180
    out = []
    for (rt, rb, hole, fwd) in ((40, 490, wide, True), (534, 984, narrow, False)):
        mid = (rt + rb) / 2
        d.rectangle([MARGIN, rt, S - MARGIN, mid - hole / 2], fill=pal["bark"],
                    outline=pal["ink"], width=8)
        d.rectangle([MARGIN, mid + hole / 2, S - MARGIN, rb], fill=pal["bark"],
                    outline=pal["ink"], width=8)
        hits = _cat_side(d, pal, cx, mid, half, reach, lim=(mid - hole / 2, mid + hole / 2))
        for hx, hy in hits:
            disc(d, hx, hy, 18, pal["accent"], pal, w=6)
        if fwd:
            arrow(d, 620, mid, 900, mid, pal, w=12, head=32)
        else:
            arrow(d, 900, mid, 620, mid, pal, w=12, head=32)
        out.append(f"洞口 {hole}px，碰到 {len(hits)} 处，1 支{'往里走' if fwd else '往回退'}的箭头")
    return f"两排同一只猫、胡须上下张开都是 {2 * half}px：上排 " + out[0] + "；下排 " + out[1]


@page("whisker", 9)
def _(d, pal):
    """剪短一截就量不准了：胡须进得去，身子还是过不去。"""
    hole, full, cut = 300, 380, 200
    cx = S / 2
    d.rectangle([MARGIN, 120, cx - hole / 2, 940], fill=pal["bark"], outline=pal["ink"], width=8)
    d.rectangle([cx + hole / 2, 120, S - MARGIN, 940], fill=pal["bark"], outline=pal["ink"], width=8)
    rows = ((300, full, "hit"), (560, cut, "ok"), (800, full, "cross"))
    for y, val, kind in rows:
        half = val / 2
        keep = min(half, hole / 2)
        if kind == "cross":
            d.rounded_rectangle([cx - keep, y - 55, cx + keep, y + 55], radius=40,
                                fill=pal["soft"], outline=pal["ink"], width=8)
        else:
            disc(d, cx, y, 54, pal["paper"], pal, w=8)
            for k in (-40, 0, 40):
                for s in (-1, 1):
                    d.line([cx + s * 40, y + k * 0.5, cx + s * keep, y + k],
                           fill=pal["ink"], width=8)
        for s in (-1, 1):
            if half > hole / 2:
                for seg in range(2):
                    x = cx + s * (hole / 2 + seg * 22)
                    d.line([x, y - 26, x + s * 14, y - 26], fill=pal["line"], width=6)
                    d.line([x, y + 26, x + s * 14, y + 26], fill=pal["line"], width=6)
                if kind == "cross":
                    cross(d, cx + s * hole / 2, y, 40, pal, w=12)
                else:
                    disc(d, cx + s * hole / 2, y, 20, pal["accent"], pal, w=6)
    return (f"洞口 {hole}px 不变，三行左右居中：完整胡须 {full}px（比洞口宽 {full - hole}px，"
            f"两边各 1 个接触点）/ 剪短后 {cut}px（进得去，两边各空 {(hole - cut) // 2}px）/ "
            f"身体 {full}px（和完整胡须一样宽，两边各 1 个叉：撞上了）")


@page("whisker", 11)
def _(d, pal, img):
    """掉下一根，过些天又长出来，长到该有的长短就停住 —— 第 4 行和第 1 行一样长。"""
    a = lie_flat(asset("whisker", 2))
    full, short = 620, 250
    x0 = MARGIN + 90
    ys = (180, 420, 660, 900)
    lens = (full, 0, short, full)
    for y, L in zip(ys, lens):
        disc(d, x0, y, 20, pal["accent"], pal, w=6)
        if L:
            place(img, a, x0 + 30 + L / 2, y, w=L)
    for i in range(3):
        arrow(d, x0 - 46, ys[i] + 46, x0 - 46, ys[i + 1] - 46, pal, w=8, head=20)
    return (f"4 行左端对齐、行间 3 支箭头：第 1 行整根 {full}px / 第 2 行空的（掉了）/ "
            f"第 3 行新长出来 {short}px / 第 4 行 {full}px，和第 1 行完全相同（长到该有的长短就停）")


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
    pw, ph = place(img, asset("dognose", 3), 230, S - MARGIN - 40, h=820, anchor="bottom")
    n = 6
    for i in range(n):
        x = 520 + (i % 2) * 40
        y = 180 + i * 118
        d.rectangle([x, y, x + 380, y + 150], fill=pal["paper"] if i % 2 else pal["soft"],
                    outline=pal["ink"], width=7)
    return f"1 根电线杆（素材3，{pw}×{ph}px）+ 右边 {n} 张一张压着一张的纸条（每张错开 40px，后贴的压住先贴的）"


@page("dognose", 10)
def _(d, pal):
    """昨天有只猫从这儿走过去：味道一路变新，所以还知道是往哪边走的。"""
    n = 7
    base = S - MARGIN - 180
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=9)
    xs, slot = lay(n)
    r0, dr = 18, 7
    for i, x in enumerate(xs):
        footprint(d, x, base - 40 + (0 if i % 2 else 50), 74, pal, pal["bark"])
        r = r0 + i * dr
        d.ellipse([x - r, 420 - r, x + r, 420 + r], outline=pal["accent"], width=7)
    arrow(d, xs[0], 200, xs[-1], 200, pal, w=12, head=32)
    return (f"1 条地线上 {n} 个左右交错的脚印，每个上面 1 个味道圈：半径从 {r0}px 一路涨到 "
            f"{r0 + (n - 1) * dr}px（越往前越新），上面 1 支指着走向的箭头")


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
    n = 6
    base = S - MARGIN - 90
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    xs, slot = lay(n)
    tree = asset("squirrel", 3)
    tw = slot * 0.78
    for x in xs:
        place(img, tree, x, base, w=tw, anchor="bottom")
    nut = asset("squirrel", 2)
    for i in (1, 4):
        place(img, nut, xs[i] - 45, base, h=90, anchor="bottom")
        d.ellipse([xs[i] - 125, base - 125, xs[i] + 35, base + 35], outline=pal["accent"], width=10)
    return (f"同一条地线上 {n} 棵小树，各宽 {tw:.0f}px、槽宽 {slot:.0f}px（互不挨着）；"
            f"其中 2 棵根边各 1 个果子、各 1 个圈（正好是前面忘掉的那 2 个）")


# ---------------------------------------------------------------- bat（蝙蝠在黑里怎么飞）

@page("bat", 2)
def _(d, pal, img):
    """那对翅膀是手指撑开的一层皮 —— 圈出翅膀上那几根指骨。"""
    return magnify(img, d, pal, "bat", 1, (0.22, 0.46), w=S - 2 * MARGIN - 80, r=0.13)


@page("bat", 4)
def _(d, pal):
    """我们的叫声稀，蝙蝠的叫声密 —— 密到我们的耳朵听不见。"""
    slow, fast = 3, 15
    x0, x1 = MARGIN + 60, S - MARGIN - 260
    wave(d, x0, x1, 330, pal, cycles=slow, amp=110, w=12)
    wave(d, x0, x1, 730, pal, cycles=fast, amp=52, w=8)
    for cy, deaf in ((330, False), (730, True)):
        ex = S - MARGIN - 130
        d.arc([ex - 90, cy - 120, ex + 90, cy + 120], 270, 90, fill=pal["ink"], width=12)
        d.arc([ex - 40, cy - 60, ex + 40, cy + 60], 270, 90, fill=pal["ink"], width=10)
        if deaf:
            cross(d, ex, cy, 96, pal, w=14)
    return (f"上排 {slow} 个波（听得见的，一个波 {(x1 - x0) / slow:.0f}px）/ "
            f"下排 {fast} 个波（蝙蝠的，一个波 {(x1 - x0) / fast:.0f}px，密 {fast // slow} 倍）；"
            f"两排各 1 只耳朵，下排那只打了 1 个叉")


@page("bat", 5)
def _(d, pal, img):
    """声音喊出去一直往前跑，撞到东西弹回来 —— 去一道、回一道，方向分得清。"""
    place(img, asset("bat", 1), MARGIN + 180, 512, w=300)
    dw, dh = place(img, asset("bat", 2), S - MARGIN - 170, 512, h=560)
    x0, x1 = 400, 634
    wave(d, x0, x1, 300, pal, cycles=4, amp=56, w=10)
    arrow(d, x0, 180, x1, 180, pal, w=11, head=30)
    wave(d, x0, x1, 720, pal, cycles=4, amp=56, w=10)
    arrow(d, x1, 840, x0, 840, pal, w=11, head=30)
    return ("1 只蝙蝠 + 1 扇门（都是素材）：上面 1 道声波 + 1 支向右的箭头（喊出去），"
            "下面 1 道声波 + 1 支向左的箭头（弹回来），两道分开画")


@page("bat", 6)
def _(d, pal, img):
    """弹回来得快，东西就在近处；弹回来得慢，东西就还远着。"""
    bat, door = asset("bat", 1), asset("bat", 2)
    trips = []
    for cy, dxx in ((300, 520), (740, 900)):
        place(img, bat, MARGIN + 130, cy, w=220)
        place(img, door, dxx, cy, h=280)
        x0, x1 = MARGIN + 260, dxx - 95
        arrow(d, x0, cy - 130, x1, cy - 130, pal, w=10, head=26)
        arrow(d, x1, cy + 130, x0, cy + 130, pal, w=10, head=26)
        trips.append(x1 - x0)
    return (f"两排同一只蝙蝠、同一扇门：上排来回的路 {trips[0]:.0f}px（近），"
            f"下排 {trips[1]:.0f}px（远，{trips[1] / trips[0]:.1f} 倍）；"
            f"每排都有 1 支向右的箭头（喊出去）和 1 支向左的箭头（弹回来）")


@page("bat", 8)
def _(d, pal, img):
    """远的时候慢慢叫，快抓住了就叫成一串。"""
    place(img, asset("bat", 1), MARGIN + 150, 512, w=260)
    place(img, asset("bat", 3), S - MARGIN - 140, 512, h=200)
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
    return (f"1 只蝙蝠 → 1 只小虫，中间 {n} 下叫声：第 1 个间隔 {pxs[1] - pxs[0]:.0f}px，"
            f"最后 1 个 {pxs[-1] - pxs[-2]:.0f}px（越靠近虫子越密），上面 1 支指向虫子的箭头")


@page("bat", 11)
def _(d, pal, img):
    """这个本事叫回声定位；海里的船也这么干，往水底喊一声，听回声有多深。"""
    for (cx, cy, w_, h_), boat in zip(panel2(d, pal), (False, True)):
        top = cy - h_ * 0.40
        if boat:
            d.line([cx - w_ * 0.46, top + 90, cx + w_ * 0.46, top + 90], fill=pal["ink"], width=8)
            d.rectangle([cx - 40, top - 80, cx + 40, top], fill=pal["soft"],
                        outline=pal["ink"], width=8)
            poly(d, [(cx - 150, top), (cx + 150, top), (cx + 105, top + 90), (cx - 105, top + 90)],
                 pal, pal["paper"], 8)
        else:
            place(img, asset("bat", 1), cx, top + 40, w=w_ * 0.62)
        floor_y = cy + h_ * 0.30
        d.rectangle([cx - w_ * 0.46, floor_y, cx + w_ * 0.46, floor_y + 120],
                    fill=pal["bark"], outline=pal["ink"], width=8)
        arrow(d, cx - 90, top + 190, cx - 90, floor_y - 40, pal, w=10, head=26)
        arrow(d, cx + 90, floor_y - 40, cx + 90, top + 190, pal, w=10, head=26)
    return ("左格 1 只蝙蝠 + 下面 1 片墙 / 右格 1 条船 + 下面 1 片海底："
            "两格各 1 支向下的箭头（喊出去）和 1 支向上的箭头（回声弹回来），两支分开左右画")


# ---------------------------------------------------------------- octopus（章鱼有三个心脏）

@page("octopus", 2)
def _(d, pal, img):
    """两个小心脏挨着鳃，把血压进鳃里；中间那个大的，再把血送到全身。"""
    xs, slot = lay(3)
    heart, gill = asset("octopus", 2), asset("octopus", 3)
    small, big, cy = 180, 300, 620
    for i, x in enumerate(xs):
        place(img, heart, x, cy, h=big if i == 1 else small)
    for i in (0, 2):
        place(img, gill, xs[i], 250, h=180)
        arrow(d, xs[i], cy - small / 2 - 10, xs[i], 360, pal, w=10, head=26)
    for s in (-1, 1):
        arrow(d, xs[1] + s * 60, cy + 170, xs[1] + s * 250, cy + 330, pal, w=10, head=26)
    return (f"3 个心脏排成一排：两边 2 个小的（各高 {small}px）+ 中间 1 个大的（高 {big}px，"
            f"是小的 {big / small:.1f} 倍）；2 个小的各 1 支向上的箭头指向它头上的鳃，"
            f"大的 2 支向下的箭头指向全身")


@page("octopus", 4)
def _(d, pal, img):
    """游起来的时候，中间那个大心脏会停下来不跳；爬的时候才跳。"""
    oct_, heart = asset("octopus", 1), asset("octopus", 2)
    for (cx, cy, w_, h_), swim in zip(panel2(d, pal), (True, False)):
        place(img, oct_, cx, cy - h_ * 0.22, w=w_ * 0.86)
        hy = cy + h_ * 0.25
        place(img, heart, cx, hy, h=190)
        if swim:
            cross(d, cx, hy, 120, pal, w=16)
        else:
            for i in range(3):
                r = 120 + i * 34
                d.ellipse([cx - r, hy - r, cx + r, hy + r], outline=pal["accent"], width=8)
    return ("两格的章鱼和心脏一样大：左格 游（大心脏上 1 个叉 = 停住不跳）/ "
            "右格 爬（大心脏外面 3 圈跳动的圈）")


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
    place(img, asset("octopus", 1), 250, 320, w=380)
    base = S - MARGIN - 60
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    poly(d, [(620, base), (660, base - 210), (790, base - 260), (910, base - 190), (950, base)],
         pal, pal["bark"], 9)
    d.ellipse([700, base - 150, 900, base], fill=pal["ground"], outline=pal["ink"], width=7)
    cw, ch = place(img, asset("octopus", 4), 800, base - 14, h=110, anchor="bottom")
    pts = []
    for k in range(25):
        t = k / 24
        pts.append((330 + 360 * t, 430 + (base - 250 - 430) * t + 120 * math.sin(math.pi * t)))
    d.line(pts, fill=pal["soft"], width=26, joint="curve")
    n_suck = 7
    for i in range(n_suck):
        px, py = pts[3 + i * 3]
        disc(d, px, py, 13, pal["paper"], pal, w=5)
    arrow(d, 650, 620, 450, 450, pal, w=9, head=24)
    return (f"1 只章鱼 + 1 条搭到石头上的胳膊（{n_suck} 个吸盘）+ 石头底下 1 个洞、洞里 1 只螃蟹"
            f"（高 {ch}px，被石头挡住一半）；1 支从接触的那头指回脑袋的箭头")


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
    fw, fh = place(img, asset("penguin", 2), xs[0], cy, h=560)
    bw, bh = place(img, asset("penguin", 3), xs[1], cy, w=slot * 0.74)
    n = 10
    for i in range(n):
        s = -1 if i < 5 else 1
        disc(d, xs[0] + s * (130 + (i % 2) * 40), cy + 120 + (i % 5) * 56,
             15, pal["paper"], pal, w=5)
    arrow(d, xs[0] + slot * 0.40, cy, xs[1] - slot * 0.40, cy, pal, w=11, head=28)
    return (f"2 格 + 中间 1 支箭头：1 根带绒的羽毛（高 {fh}px，绒的两边共兜着 {n} 个空气小点）"
            f"→ 1 条被子（宽 {bw}px）")


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
def _(d, pal):
    """天最冷的时候挤成一团：外面的顶着风，里面的暖烘烘。"""
    rings, step, rr = 4, 88, 40
    cx, cy = 560, S / 2
    total, warm = 0, 0
    for k in range(rings + 1):
        m = 1 if k == 0 else 6 * k
        for i in range(m):
            a = 2 * math.pi * i / m + (0.5 if k % 2 else 0.0)
            inner = k <= 2
            disc(d, cx + k * step * math.cos(a), cy + k * step * math.sin(a), rr,
                 pal["accent"] if inner else pal["paper"], pal, w=7)
            total += 1
            warm += 1 if inner else 0
    winds = 3
    for i in range(winds):
        arrow(d, MARGIN + 20, 300 + i * 212, cx - rings * step - rr - 20, 300 + i * 212,
              pal, w=11, head=28)
    return (f"1 团 {total} 只（中心 1 + 4 圈 6/12/18/24，圈距 {step}px、每只半径 {rr}px，挨着但不压着）："
            f"里面 {warm} 只填暖色、外面 {total - warm} 只；左边 {winds} 支吹到团外沿的风箭头")


@page("penguin", 10)
def _(d, pal):
    """团里比团外暖得多，中间那只有时候还嫌热，自己挪到边上去。"""
    cx, cy, R, rr = 440, 540, 280, 46
    n, gap_i = 14, 12
    disc(d, cx, cy, R, pal["accent"], pal, w=10)
    on = 0
    for i in range(n):
        if i == gap_i:
            continue
        a = 2 * math.pi * i / n - math.pi / 2
        disc(d, cx + R * math.cos(a), cy + R * math.sin(a), rr, pal["paper"], pal, w=7)
        on += 1
    ga = 2 * math.pi * gap_i / n - math.pi / 2
    disc(d, cx, cy, rr, pal["soft"], pal, w=7)
    gx, gy = cx + (R + 130) * math.cos(ga), cy + (R + 130) * math.sin(ga)
    disc(d, gx, gy, rr, pal["soft"], pal, w=7)
    arrow(d, cx + 62 * math.cos(ga), cy + 62 * math.sin(ga),
          gx - 70 * math.cos(ga), gy - 70 * math.sin(ga), pal, w=10, head=26)
    inside, outside = 420, 120
    for x, v, key in ((850, inside, "accent"), (950, outside, "soft")):
        d.rounded_rectangle([x - 40, 900 - v, x + 40, 900], radius=20,
                            fill=pal[key], outline=pal["ink"], width=8)
    return (f"1 个填了暖色的圆（团里）+ 圆周上 {on} 只 + 1 处空出来的缺口；"
            f"中间那只（圆心 1 只）顺着 1 支箭头穿过缺口挪到圆外（圆外那只是同 1 只，挪之后）；"
            f"右边 2 根温度条：团里 {inside}px、团外 {outside}px（{inside / outside:.1f} 倍）")
