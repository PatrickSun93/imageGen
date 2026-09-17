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
