# -*- coding: utf-8 -*-
"""第七批示意图页（5/5）：骆驼、蛇、蝌蚪、海龟、猫头鹰、鲸鱼、蜘蛛、长颈鹿。"""
from draw_diagrams import (S, MARGIN, page, asset, place, lie_flat, poly, disc, arrow, cross,
                           lay, panel2, hbar, footprint, bands, ngon, cmp_len, cmp_height,
                           cmp_count, bars, timeline, steps, magnify)
import math, random


# ---------------------------------------------------------------- 这一批自己要用的小图元

def _drop(d, pal, cx, cy, r):
    """一滴水：一个圆加一个尖，一笔多边形画完，不会留下互相穿过去的描边。"""
    pts = [(cx, cy - r * 2.2)]
    for k in range(1, 24):
        a = -math.pi / 2 + 2 * math.pi * k / 24
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    poly(d, pts, pal, pal["soft"], 6)


def _person(d, pal, cx, base, h):
    """一个小人：脚底落在 base，总高正好 h —— 比高矮的页要的就是这个 h。"""
    r = h * 0.10
    hy = base - h + r
    disc(d, cx, hy, r, pal["paper"], pal, w=7)
    hip = base - h * 0.45
    d.line([cx, hy + r, cx, hip], fill=pal["ink"], width=max(8, int(h * 0.035)))
    d.line([cx - h * 0.16, base - h * 0.62, cx + h * 0.16, base - h * 0.62],
           fill=pal["ink"], width=max(7, int(h * 0.030)))
    for s in (-1, 1):
        d.line([cx, hip, cx + s * h * 0.13, base], fill=pal["ink"], width=max(7, int(h * 0.030)))
    return h


def _tad(d, pal, cx, cy, L, bumps=0, legs=0):
    """一只蝌蚪的简图：圆身子（头朝左）+ 尾巴。bumps 是屁股后的小包数，legs 是后腿数。"""
    r = L * 0.26
    disc(d, cx - L * 0.22, cy, r, pal["soft"], pal, w=8)
    poly(d, [(cx - L * 0.04, cy - r * 0.58), (cx + L * 0.50, cy - r * 0.30),
             (cx + L * 0.50, cy + r * 0.30), (cx - L * 0.04, cy + r * 0.58)], pal, pal["soft"], 8)
    for i in range(bumps):
        disc(d, cx + L * 0.04, cy + (1 if i else -1) * r * 0.66, L * 0.075, pal["accent"], pal, w=7)
    for i in range(legs):
        s = 1 if i else -1
        pts = [(cx + L * 0.03, cy + s * r * 0.50), (cx + L * 0.17, cy + s * r * 1.20),
               (cx + L * 0.31, cy + s * r * 1.55)]
        d.line(pts, fill=pal["ink"], width=int(L * 0.05) + 7, joint="curve")
        d.line(pts, fill=pal["accent"], width=max(3, int(L * 0.05)), joint="curve")
    return r


def _tuft(d, pal, cx, cy, s, n=3, up=True):
    """一丛鳃：n 根从同一个点散开的细丝。根数由参数保证。"""
    for k in range(n):
        a = math.radians((-140 if up else 140) + (k - (n - 1) / 2) * (34 if up else -34))
        pts = [(cx, cy), (cx + s * 0.55 * math.cos(a), cy + s * 0.55 * math.sin(a)),
               (cx + s * math.cos(a), cy + s * math.sin(a))]
        d.line(pts, fill=pal["ink"], width=9, joint="curve")
        d.line(pts, fill=pal["accent"], width=4, joint="curve")
    return n


def _spokes(d, pal, cx, cy, n, r0, r1, color=None, w=6, rot=-math.pi / 2):
    """从中心均匀放射 n 根辐条：夹角一律 360/n，外端全落在同一个圆上。"""
    for i in range(n):
        a = rot + 2 * math.pi * i / n
        d.line([cx + r0 * math.cos(a), cy + r0 * math.sin(a),
                cx + r1 * math.cos(a), cy + r1 * math.sin(a)],
               fill=color or pal["ink"], width=w)
    return n


def _spoke_pt(cx, cy, n, i, r, rot=-math.pi / 2):
    a = rot + 2 * math.pi * i / n
    return cx + r * math.cos(a), cy + r * math.sin(a)


def _spiral_pts(cx, cy, turn_r, start=-math.pi / 2, per=96, turns=None):
    """极坐标算螺旋：turn_r 是一串半径控制点，均匀落在 0..turns 圈上。

    默认一个控制点管一圈（turn_r 的长度 = 圈数 + 1）；turns 给了就按它来，
    半圈、一圈半这种也画得准。圈数和圈距全写在参数里，不靠手画。
    """
    turns = (len(turn_r) - 1) if turns is None else turns
    n = max(2, int(round(turns * per)))
    seg = max(1, len(turn_r) - 1)
    pts = []
    for i in range(n + 1):
        t = turns * i / n                        # 已经走过的圈数
        u = seg * i / n                          # 在控制点列上的位置
        k = min(int(u), seg - 1)
        r = turn_r[k] + (turn_r[k + 1] - turn_r[k]) * (u - k)
        a = start + 2 * math.pi * t
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def _shrinking_radii(r_out, r_in, n, ratio=0.45):
    """从外往里 n 圈，圈距一圈比一圈窄（最里那圈的间距是最外那圈的 ratio 倍）。

    返回 (每圈半径, 每个圈距)，圈距直接打进构造清单 —— 「一圈比一圈密」是算出来的。
    """
    g = [1.0 - (1.0 - ratio) * i / max(1, n - 1) for i in range(n)]
    k = (r_out - r_in) / sum(g)
    rr, r = [r_out], r_out
    for gi in g:
        r -= gi * k
        rr.append(r)
    return rr, [gi * k for gi in g]


def _plen(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


# ================================================================ camel 驼峰里装的是什么

@page("camel", 2)
def _(d, pal, img):
    """驼峰里装的是脂肪，像一大块黄油 —— 两个包，就对两块黄油。"""
    cw, ch = place(img, asset("camel", 1), S / 2, 300, w=700)
    xs, slot = lay(2)
    butter = lie_flat(asset("camel", 3))
    bw = bh = 0
    for x in xs:
        bw, bh = place(img, butter, x, 820, w=slot * 0.60)
    for s, x in zip((-1, 1), xs):                 # 两个驼峰各一支箭头指到自己那块黄油
        arrow(d, S / 2 + s * 70, 580, x, 690, pal, w=10, head=26)
    return (f"1 峰骆驼（素材，宽 {cw}px）+ 下面 2 块黄油（各 {bw}×{bh}px），"
            f"背上 2 个包对 2 块，2 支箭头一一指过去")


@page("camel", 4)
def _(d, pal, img):
    """脂肪化开：一边出力气，一边还出一点水。"""
    bw, bh = place(img, lie_flat(asset("camel", 3)), MARGIN + 220, S / 2, w=380)
    x0 = MARGIN + 430
    arrow(d, x0, S / 2 - 90, S - MARGIN - 70, MARGIN + 210, pal, w=16, head=40)   # 力气：粗
    arrow(d, x0, S / 2 + 90, S - MARGIN - 330, S - MARGIN - 260, pal, w=6, head=18)  # 水：细
    n = 3
    for i in range(n):
        _drop(d, pal, S - MARGIN - 280 + i * 105, S - MARGIN - 150, 34)
    return (f"1 块脂肪（素材 {bw}×{bh}px）分出 2 路：上面 1 支粗箭头（线宽 16px，力气）/ "
            f"下面 1 支细箭头（线宽 6px）通到 {n} 滴水")


@page("camel", 6)
def _(d, pal, img):
    """一百升够装满十个水桶，我一天连一桶都不到 —— 桶必须一模一样大。"""
    b = asset("camel", 2)
    h = 165
    top = MARGIN + 215
    bw, bh = place(img, b, S / 2, top, h=h, anchor="bottom")
    d.line([MARGIN, top + 45, S - MARGIN, top + 45], fill=pal["line"], width=6)
    xs, slot = lay(5)
    n = 0
    for r_ in range(2):
        for x in xs:
            place(img, b, x, top + 300 + r_ * 300, h=h, anchor="bottom")
            n += 1
    return (f"上面 1 个水桶（我一天喝的）/ 下面 {n} 个水桶（骆驼一口气，2 行 ×5），"
            f"桶高一律 {bh}px、宽 {bw}px，间距 {slot:.0f}px，中间 1 条分隔线")


@page("camel", 8)
def _(d, pal):
    """白天让身子先变热，热得受不了才出汗 —— 出汗线越高，汗越少。"""
    out = []
    for (cx, cy, w_, h_), (thr, drops) in zip(panel2(d, pal), ((0.30, 6), (0.72, 2))):
        x0, x1 = cx - w_ * 0.36, cx + w_ * 0.36
        base, top = cy + h_ * 0.30, cy - h_ * 0.38
        ty = base - (base - top) * thr
        d.line([x0, ty, x1, ty], fill=pal["accent"], width=9)          # 出汗线
        pts = [(x0 + (x1 - x0) * t / 12, base - (base - ty) * min(1.0, t / 7.0))
               for t in range(13)]
        d.line(pts, fill=pal["ink"], width=11, joint="curve")          # 体温曲线，碰到出汗线就压平
        for i in range(drops):
            _drop(d, pal, x0 + (x1 - x0) * (i + 0.5) / drops, base + 96, 21)
        out.append(f"出汗线在框高 {thr * 100:.0f}% 处、下面 {drops} 滴汗")
    return "两格等大：左格（我们）" + out[0] + " / 右格（骆驼）" + out[1]


@page("camel", 10)
def _(d, pal):
    """它的红细胞是长长的椭圆，缺水的时候也挤得过去。"""
    n, tube = 6, 120
    out = []
    for (cx, cy, w_, h_), (rw, rh) in zip(panel2(d, pal), ((104, 104), (46, 104))):
        y0 = cy - h_ * 0.38
        d.rounded_rectangle([cx - tube / 2, y0, cx + tube / 2, y0 + 700],
                            radius=54, fill=pal["paper"], outline=pal["ink"], width=9)
        for i in range(n):
            yc = y0 + 700 * (i + 0.5) / n
            d.ellipse([cx - rw / 2, yc - rh / 2, cx + rw / 2, yc + rh / 2],
                      fill=pal["accent"], outline=pal["ink"], width=7)
        arrow(d, cx, y0 + 740, cx, y0 + 830, pal, w=9, head=24)
        out.append(f"{n} 个红细胞（{rw}×{rh}px），两边各余 {(tube - rw) / 2:.0f}px")
    return (f"两格的管子一样宽（{tube}px）：左格（我们）圆红细胞，" + out[0] +
            " / 右格（骆驼）长椭圆红细胞，" + out[1] + "，所以挤得过去")


# ================================================================ snake 蛇没有腿怎么走

@page("snake", 2)
def _(d, pal, img):
    """肚皮上有一排鳞，一片挨着一片，从脖子排到尾巴。"""
    sw, sh = place(img, asset("snake", 1), S / 2, 300, w=S - 2 * MARGIN - 60)
    n = 14
    span = S - 2 * MARGIN - 80
    unit = span / n
    sc = asset("snake", 2)
    for i in range(n):
        place(img, sc, MARGIN + 40 + unit * (i + 0.5), 800, w=unit)
    d.line([MARGIN + 40, 700, S - MARGIN - 40, 700], fill=pal["line"], width=5)
    return (f"上面 1 条蛇（素材，宽 {sw}px）/ 下面 {n} 片腹鳞首尾相接铺满 {unit * n:.0f}px，"
            f"每片宽 {unit:.0f}px，一片挨着一片没有缝")


@page("snake", 4)
def _(d, pal, img):
    """鳞勾着地面，身子被推着往前 —— 每片鳞一支往后的小箭头，合起来一支往前的大箭头。"""
    base = 760
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=11)
    n = 8
    xs, slot = lay(n)
    sc = asset("snake", 2)
    sw = 0
    for x in xs:
        sw, sh = place(img, sc, x, base, h=90, anchor="bottom")
        arrow(d, x, base + 40, x - 62, base + 96, pal, w=7, head=20)   # 往后勾一下
    arrow(d, MARGIN + 120, 240, S - MARGIN - 120, 240, pal, w=14, head=36)  # 身子往前走
    return (f"地线上 {n} 片腹鳞（素材，各 {sw}×90px、间距 {slot:.0f}px），"
            f"每片配 1 支往后勾的小箭头，上方 1 支往前的大箭头（长 {S - 2 * MARGIN - 240}px）")


@page("snake", 6)
def _(d, pal):
    """一个弯推一下，像浪一样从头传到尾巴尖。"""
    cy, cycles, amp = S / 2 + 50, 2, 150
    x0, x1 = MARGIN + 50, S - MARGIN - 50
    pts = [(x0 + (x1 - x0) * t / 240, cy + amp * math.sin(2 * math.pi * cycles * t / 240))
           for t in range(241)]
    d.line(pts, fill=pal["ink"], width=36, joint="curve")
    d.line(pts, fill=pal["soft"], width=22, joint="curve")
    bends = 2 * cycles
    for k in range(bends):
        frac = (0.25 + k * 0.5) / cycles
        s = 1 if k % 2 == 0 else -1
        x = x0 + (x1 - x0) * frac
        arrow(d, x, cy + s * amp, x, cy + s * (amp + 135), pal, w=10, head=26)
    arrow(d, MARGIN + 140, MARGIN + 90, S - MARGIN - 140, MARGIN + 90, pal, w=12, head=32)
    return (f"1 条正弦形的身子（{cycles} 个整波、波幅 {amp}px），{bends} 个弯各 1 支侧推箭头、"
            f"方向左右交替，上方 1 支往前的箭头")


@page("snake", 8)
def _(d, pal):
    """我们只有二十四根肋骨，它有好几百根。"""
    out = []
    for (cx, cy, w_, h_), (pairs, lw, dy) in zip(panel2(d, pal), ((12, 9, 30), (100, 3, 5))):
        top, bot = cy - h_ * 0.42, cy + h_ * 0.42
        for i in range(pairs):
            y = top + (bot - top) * (i + 0.5) / pairs
            for s in (-1, 1):
                d.line([cx, y, cx + s * w_ * 0.36, y + dy], fill=pal["bark"], width=lw)
        d.line([cx, top, cx, bot], fill=pal["ink"], width=18)          # 脊柱压在上面
        out.append(f"{pairs} 对共 {pairs * 2} 根肋骨（行距 {(bot - top) / pairs:.1f}px）")
    return "两格等大等高：左格（我们）" + out[0] + " / 右格（蛇）" + out[1]


@page("snake", 10)
def _(d, pal, img):
    """沙漠里的蛇斜着甩出去，沙上留下一排斜道。"""
    sw, sh = place(img, asset("snake", 1), S / 2, 260, w=S - 2 * MARGIN - 140)
    sand = 620
    d.line([MARGIN, sand, S - MARGIN, sand], fill=pal["line"], width=8)
    n, ang, ln, gap = 6, 35, 230, 140
    dx, dy = ln * math.cos(math.radians(ang)), ln * math.sin(math.radians(ang))
    for i in range(n):
        x = MARGIN + 80 + i * gap
        d.line([x, 900, x + dx, 900 - dy], fill=pal["ink"], width=30)
        d.line([x, 900, x + dx, 900 - dy], fill=pal["bark"], width=18)
    arrow(d, MARGIN + 150, sand + 60, S - MARGIN - 150, sand + 60, pal, w=11, head=28)
    return (f"上面 1 条蛇（素材，宽 {sw}px）；沙面下 {n} 道平行斜印，每道倾斜 {ang}°、"
            f"长 {ln}px、间距 {gap}px，另有 1 支前进箭头")


# ================================================================ tadpole 小蝌蚪怎么变成青蛙

@page("tadpole", 3)
def _(d, pal, img):
    """刚出来的蝌蚪没有腿，脖子两边长着一丛鳃。"""
    cx, cy = S / 2, S / 2 + 30
    w_, h_ = place(img, asset("tadpole", 1), cx, cy, w=S - 2 * MARGIN - 140)
    hx = cx - w_ * 0.26
    n = 3
    _tuft(d, pal, hx, cy - h_ * 0.20, 150, n, up=True)
    _tuft(d, pal, hx, cy + h_ * 0.20, 150, n, up=False)
    d.ellipse([hx - w_ * 0.20, cy - h_ * 0.58, hx + w_ * 0.20, cy + h_ * 0.58],
              outline=pal["accent"], width=12)
    return (f"1 只蝌蚪（素材 {w_}×{h_}px，身上 0 条腿），头两侧各 1 丛鳃、每丛 {n} 根"
            f"（共 {2 * n} 根），外面 1 个强调色的圈")


@page("tadpole", 4)
def _(d, pal):
    """屁股后面先鼓出两个小包，小包慢慢伸长，变成两条后腿。"""
    cy = S / 2
    xs, slot = lay(3)
    L = slot * 0.70
    stages = ((0, 0), (2, 0), (0, 2))
    for x, (bumps, legs) in zip(xs, stages):
        _tad(d, pal, x, cy, L, bumps=bumps, legs=legs)
    for i in range(2):
        arrow(d, xs[i] + slot * 0.40, cy, xs[i + 1] - slot * 0.40, cy, pal, w=10, head=26)
    return (f"3 格横排（体长都是 {L:.0f}px）：第 1 格光身子（0 个包 0 条腿）/ "
            f"第 2 格屁股后 2 个小包 / 第 3 格 2 条伸长的后腿，中间 2 支箭头")


@page("tadpole", 5)
def _(d, pal):
    """后腿长好了前腿才长：先藏在皮里，忽然从两边顶出来。"""
    out = []
    for (cx, cy, w_, h_), outside in zip(panel2(d, pal), (False, True)):
        L = w_ * 0.74
        r = _tad(d, pal, cx, cy, L, legs=2)
        for i in range(2):
            s = 1 if i else -1
            bx, by = cx - L * 0.20, cy + s * r * 0.44
            ex, ey = (bx - L * 0.30, by + s * r * 0.95) if outside else (bx + L * 0.03, by + s * r * 0.40)
            if outside:
                pts = [(bx, by), ((bx + ex) / 2, by + s * r * 0.75), (ex, ey)]
                d.line(pts, fill=pal["ink"], width=int(L * 0.05) + 7, joint="curve")
                d.line(pts, fill=pal["accent"], width=max(3, int(L * 0.05)), joint="curve")
            else:
                for k in range(5):                    # 藏在皮里：虚线，整条都在身子轮廓里面
                    t0, t1 = k / 5 + 0.03, (k + 1) / 5 - 0.03
                    d.line([bx + (ex - bx) * t0, by + (ey - by) * t0,
                            bx + (ex - bx) * t1, by + (ey - by) * t1],
                           fill=pal["ink"], width=7)
        out.append("2 条前腿" + ("伸到身子外面（实线）" if outside else "藏在身子里面（5 段虚线）"))
    return "两格等大，都是 2 条长好的后腿：左格 " + out[0] + " / 右格 " + out[1]


@page("tadpole", 7)
def _(d, pal):
    """鳃慢慢不见，身体里长出了肺，得浮到水面吸一口空气。"""
    out = []
    for (cx, cy, w_, h_), surfaced in zip(panel2(d, pal), (False, True)):
        wl = cy - h_ * 0.34
        d.line([cx - w_ * 0.46, wl, cx + w_ * 0.46, wl], fill=pal["line"], width=10)
        by = wl + (10 if surfaced else h_ * 0.30)
        L = w_ * 0.66
        r = _tad(d, pal, cx, by, L)
        if surfaced:
            for s in (-1, 1):                          # 身体里 2 个肺
                disc(d, cx - L * 0.22 + s * r * 0.42, by + r * 0.10, r * 0.34,
                     pal["accent"], pal, w=6)
            arrow(d, cx - L * 0.30, wl - 40, cx - L * 0.30, wl - 190, pal, w=11, head=28)
            out.append("身体里 2 个肺 + 1 支向上的吸气箭头，头顶到水面")
        else:
            n = _tuft(d, pal, cx - L * 0.24, by - r * 0.80, 110, 3, up=True)
            _tuft(d, pal, cx - L * 0.24, by + r * 0.80, 110, 3, up=False)
            out.append(f"水下 2 丛鳃、每丛 {n} 根（共 {2 * n} 根），0 个肺")
    return "两格等大、水面线一样高：左格（蝌蚪）" + out[0] + " / 右格（青蛙）" + out[1]


@page("tadpole", 8)
def _(d, pal):
    """蝌蚪吃水草，肠子又细又长；青蛙吃虫子，肠子变短变粗。"""
    out = []
    for (cx, cy, w_, h_), (turns, lw, r0, r1) in zip(panel2(d, pal),
                                                     ((5, 12, 22, 170), (1.5, 34, 46, 150))):
        pts = _spiral_pts(cx, cy, [r0, r1], turns=turns)
        d.line(pts, fill=pal["ink"], width=lw + 8, joint="curve")
        d.line(pts, fill=pal["soft"], width=lw, joint="curve")
        out.append(f"盘 {turns} 圈、线宽 {lw}px、拉直了长 {_plen(pts):.0f}px")
    return "两格等大：左格（蝌蚪，吃水草）" + out[0] + " / 右格（青蛙，吃虫子）" + out[1]


@page("tadpole", 11)
def _(d, pal, img):
    """卵、蝌蚪、长腿蝌蚪、青蛙 —— 四个模样是同一只。"""
    cy = S / 2
    note = steps(img, d, pal, "tadpole", [3, 1, 1, 2], cy=cy)
    xs, slot = lay(4)
    x3 = xs[2]
    for s in (-1, 1):                                  # 第 3 格另加 2 条后腿
        pts = [(x3 + slot * 0.10, cy + s * slot * 0.06),
               (x3 + slot * 0.21, cy + s * slot * 0.19),
               (x3 + slot * 0.31, cy + s * slot * 0.26)]
        d.line(pts, fill=pal["ink"], width=15, joint="curve")
        d.line(pts, fill=pal["accent"], width=7, joint="curve")
    return note + "：卵 / 蝌蚪 / 长腿蝌蚪（另加 2 条后腿）/ 青蛙，4 个模样是同一只"


# ================================================================ seaturtle 海龟怎么找回出生的那片海滩

@page("seaturtle", 3)
def _(d, pal, img):
    """用后脚挖坑，挖得比自己还深，再下一百多个蛋。"""
    sand = 340
    d.rectangle([MARGIN, sand, S - MARGIN, S - MARGIN], fill=pal["bark"],
                outline=pal["ink"], width=7)
    pit_w, depth = 520, 600
    px0 = S / 2 - pit_w / 2
    d.rounded_rectangle([px0, sand, px0 + pit_w, sand + depth], radius=70,
                        fill=pal["ground"], outline=pal["ink"], width=8)
    tw, th = place(img, asset("seaturtle", 1), S / 2, sand + 8, w=430, anchor="bottom")
    for seg in range(10):                              # 坑深的量线
        y = sand + 14 + seg * (depth - 20) / 10
        d.line([px0 - 46, y, px0 - 46, y + (depth - 20) / 20], fill=pal["line"], width=6)
    cols, rows_ = 12, 9
    pitch, r = 36, 15
    ex0 = S / 2 - pitch * (cols - 1) / 2
    ey0 = sand + depth - 60 - pitch * (rows_ - 1)
    n = 0
    for r_ in range(rows_):
        for c_ in range(cols):
            disc(d, ex0 + c_ * pitch, ey0 + r_ * pitch, r, pal["paper"], pal, w=5)
            n += 1
    return (f"沙面下 1 个坑，深 {depth}px，比上面那只龟的体长 {tw}px 还深；"
            f"坑里 {n} 个蛋（{rows_} 行 ×{cols}，间距 {pitch}px）")


@page("seaturtle", 4)
def _(d, pal, img):
    """沙子凉的时候孵出来多是男孩，热的时候多是女孩 —— 只有点的颜色数目不同。"""
    baby = asset("seaturtle", 2)
    out = []
    for (cx, cy, w_, h_), (sun, hot) in zip(panel2(d, pal), ((45, 1), (85, 5))):
        disc(d, cx, cy - h_ * 0.36, sun, pal["accent"] if sun > 60 else pal["paper"], pal, w=8)
        n = 6
        for i in range(n):
            r_, c_ = divmod(i, 3)
            bx = cx + (c_ - 1) * w_ * 0.28
            by = cy - h_ * 0.02 + r_ * h_ * 0.26
            place(img, baby, bx, by, w=w_ * 0.24)
            disc(d, bx, by + h_ * 0.11, 16, pal["accent"] if i < hot else pal["soft"], pal, w=5)
        out.append(f"太阳半径 {sun}px、{n} 只小龟、{hot} 个强调色点 + {n - hot} 个 soft 点")
    return "两格等大：左格（沙子凉）" + out[0] + " / 右格（沙子热）" + out[1]


@page("seaturtle", 7)
def _(d, pal, img):
    """爬这几分钟里，它们记下的是地下磁力的方向。"""
    sand = 520
    d.rectangle([MARGIN, sand, S - MARGIN, S - MARGIN], fill=pal["bark"],
                outline=pal["ink"], width=7)
    n = 3
    xs, slot = lay(n + 1)
    bw = 0
    for i in range(n):
        bw, bh = place(img, asset("seaturtle", 2), xs[i], sand - 30, w=200, anchor="bottom")
    arrow(d, MARGIN + 120, sand - 240, S - MARGIN - 120, sand - 240, pal, w=12, head=32)
    k, ang, alen = 5, 20, 140
    ax, ay = alen * math.cos(math.radians(ang)) / 2, alen * math.sin(math.radians(ang)) / 2
    for i in range(k):
        x = MARGIN + 130 + i * (S - 2 * MARGIN - 260) / (k - 1)
        y = sand + 200
        arrow(d, x - ax, y + ay, x + ax, y - ay, pal, w=10, head=26)
    return (f"沙滩上 {n} 只小龟（素材，各宽 {bw}px）朝同一个方向爬，上面 1 支路径箭头；"
            f"沙层下面 {k} 支磁力箭头，方向完全相同（都倾斜 {ang}°、都长 {alen}px）")


@page("seaturtle", 8)
def _(d, pal, img):
    """地球本身是块大磁铁，每一段海岸磁力的劲儿都不一样。"""
    cx, cy, R = S / 2, S / 2 + 20, 300
    disc(d, cx, cy, R, pal["soft"], pal, w=10)
    place(img, asset("seaturtle", 4).rotate(75, expand=True), cx, cy, h=R * 1.3)
    lens = [60, 95, 130, 165, 200]
    angs = [-108, -50, 10, 70, 150]
    for L_, a_ in zip(lens, angs):
        t = math.radians(a_)
        x0_, y0_ = cx + R * math.cos(t), cy + R * math.sin(t)
        arrow(d, x0_, y0_, x0_ + L_ * math.cos(t), y0_ + L_ * math.sin(t), pal, w=9, head=24)
    t = math.radians(angs[2])
    hx, hy = cx + R * math.cos(t), cy + R * math.sin(t)
    d.ellipse([hx - 52, hy - 52, hx + 52, hy + 52], outline=pal["accent"], width=12)
    return (f"1 个地球圆（半径 {R}px），中间 1 块斜着的磁铁（素材）；圆周上 {len(lens)} 个海岸点"
            f"各 1 支箭头，长度 {'/'.join(str(x) for x in lens)}px、方向各不相同，"
            f"其中 1 个被圈了起来（出生的那片海滩）")


@page("seaturtle", 10)
def _(d, pal):
    """游过的路加起来上万公里，比从我们家走到南极还远。"""
    note = bars(d, pal, [(1.00, "accent", "海龟一辈子游的路"), (0.69, "soft", "我们家到南极")])
    return note + "，海龟那条正好是另一条的 1.45 倍（所以「还要远」）"


# ================================================================ owl 猫头鹰的眼睛不会转

@page("owl", 3)
def _(d, pal):
    """它的眼睛不是球，是两根小管子，前面粗后面细。"""
    out = []
    for (cx, cy, w_, h_), tube in zip(panel2(d, pal), (False, True)):
        hr = w_ * 0.40
        disc(d, cx, cy, hr, pal["paper"], pal, w=9)                 # 从上往下看的一个头
        for s in (-1, 1):
            ex = cx + s * hr * 0.42
            if tube:
                poly(d, [(ex - 55, cy - hr * 0.66), (ex + 55, cy - hr * 0.66),
                         (ex + 24, cy + hr * 0.38), (ex - 24, cy + hr * 0.38)],
                     pal, pal["soft"], 8)
            else:
                disc(d, ex, cy - hr * 0.30, 55, pal["soft"], pal, w=8)
        out.append("2 个圆眼球（直径 110px）" if not tube else
                   "2 根管子眼（前端宽 110px、后端宽 48px，前是后的 2.3 倍）")
    return "两格等大，每格 1 个头：左格（我们）" + out[0] + " / 右格（猫头鹰）" + out[1]


@page("owl", 4)
def _(d, pal):
    """管子被骨头卡在眼窝里，一动也动不了。"""
    out = []
    for (cx, cy, w_, h_), free in zip(panel2(d, pal), (True, False)):
        base = cy + 90
        if free:
            disc(d, cx, base, 90, pal["soft"], pal, w=9)
            for a_ in (-40, 0, 40):
                t = math.radians(-90 + a_)
                arrow(d, cx, base, cx + 300 * math.cos(t), base + 300 * math.sin(t),
                      pal, w=10, head=28)
            out.append("1 个圆眼球 + 3 支不同方向的视线箭头（-40°/0°/+40°）")
        else:
            poly(d, [(cx - 60, base - 230), (cx + 60, base - 230),
                     (cx + 26, base + 40), (cx - 26, base + 40)], pal, pal["soft"], 9)
            for s in (-1, 1):                                    # 卡住它的 2 块骨头
                d.rounded_rectangle([cx + s * 76 - 26, base - 250, cx + s * 76 + 26, base + 60],
                                    radius=18, fill=pal["bark"], outline=pal["ink"], width=8)
            arrow(d, cx, base - 250, cx, base - 380, pal, w=10, head=28)
            for s in (-1, 1):
                cross(d, cx + s * 168, base - 330, 48, pal)
            out.append("1 根管子 + 2 块卡住它的骨头 + 1 支只能朝正前的箭头 + 2 个叉")
    return "两格等大：左格（我们）" + out[0] + " / 右格（猫头鹰）" + out[1]


@page("owl", 6)
def _(d, pal, img):
    """它的脖子里藏着十四节骨头，我们只有七节。"""
    bone = asset("owl", 4)
    total = 700
    out = []
    for (cx, cy, w_, h_), n in zip(panel2(d, pal), (7, 14)):
        each = total / n
        top = cy - total / 2
        bw = bh = 0
        for i in range(n):
            bw, bh = place(img, bone, cx, top + each * (i + 1), h=each * 0.94, anchor="bottom")
        out.append(f"{n} 节（每节 {bw}×{bh}px）")
    return (f"两格等大、两摞总高都是 {total}px：左格（我们）" + out[0] +
            " / 右格（猫头鹰）" + out[1] + "，零件正好多一倍")


@page("owl", 7)
def _(d, pal, img):
    """头能转到身子后面，差不多两百七十度 —— 一圈里的四分之三。"""
    cx, cy, R = S / 2, S / 2 + 30, 340
    d.pieslice([cx - R, cy - R, cx + R, cy + R], -90, 180,
               fill=pal["accent"], outline=pal["ink"], width=10)      # 转得到的 270°
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=pal["ink"], width=10)
    d.arc([cx - R - 60, cy - R - 60, cx + R + 60, cy + R + 60], -90, 170,
          fill=pal["ink"], width=10)
    t = math.radians(172)
    arrow(d, cx + (R + 60) * math.cos(math.radians(150)), cy + (R + 60) * math.sin(math.radians(150)),
          cx + (R + 60) * math.cos(t), cy + (R + 60) * math.sin(t), pal, w=10, head=30)
    ow, oh = place(img, asset("owl", 1), cx, cy, h=300)
    return (f"1 个整圆（半径 {R}px），转动的扇区正好 270°（整圈的 3/4），剩下 90° 空着；"
            f"外面 1 条同样 270° 的弧配 1 支箭头，中间 1 只猫头鹰（素材 {ow}×{oh}px）")


@page("owl", 8)
def _(d, pal):
    """它的血管比骨头洞细，旁边还有小口袋存着血。"""
    cx, cy = S / 2, S / 2
    ngon(d, cx, cy, 330, 8, pal, pal["bark"], w=10, rot=math.pi / 8)
    hole, vein, pocket = 170, 74, 58
    disc(d, cx, cy - 30, hole, pal["ground"], pal, w=9)
    disc(d, cx, cy - 30, vein, pal["accent"], pal, w=8)
    for s in (-1, 1):
        disc(d, cx + s * 195, cy + 140, pocket, pal["accent"], pal, w=8)
    return (f"1 节颈椎剖面（正八边形）：骨头洞直径 {2 * hole}px，里面的血管直径 {2 * vein}px"
            f"（不到洞的一半，四周还余 {hole - vein}px 能拧），旁边 2 个存血的小口袋"
            f"（直径 {2 * pocket}px）")


# ================================================================ whale 鲸鱼在水里怎么呼吸

@page("whale", 3)
def _(d, pal, img):
    """它和我们一样用肺，生下来就是小宝宝 —— 大小两条都得上来换气。"""
    sea = MARGIN + 110
    d.line([MARGIN, sea, S - MARGIN, sea], fill=pal["line"], width=12)
    a = asset("whale", 1)
    mw, mh = place(img, a, 330, 620, w=560)
    bw, bh = place(img, a, 810, 760, w=224)
    for x, y in ((330 - 560 * 0.30, 620 - mh * 0.45), (810 - 224 * 0.30, 760 - bh * 0.45)):
        arrow(d, x, y, x, sea + 18, pal, w=11, head=28)
    return (f"1 大 1 小两条鲸（素材，体长 {mw}px / {bw}px，大的正好是小的 2.5 倍），"
            f"各 1 支通到水面的呼吸箭头（都用肺），水面 1 条线")


@page("whale", 4)
def _(d, pal, img):
    """鱼长着鳃，鲸没有鳃 —— 它的鼻孔搬到了头顶上。"""
    out = []
    for (cx, cy, w_, h_), whale in zip(panel2(d, pal), (False, True)):
        if whale:
            ww, wh = place(img, asset("whale", 1), cx, cy, w=w_ * 0.88)
            bx, by = cx - ww * 0.30, cy - wh * 0.34
            disc(d, bx, by, 26, pal["accent"], pal, w=7)
            arrow(d, bx, by - 50, bx, by - 190, pal, w=10, head=26)
            out.append(f"1 条鲸（素材 {ww}×{wh}px），头顶 1 个喷气孔（直径 52px）+ 1 支向上的箭头，0 道鳃缝")
        else:
            d.ellipse([cx - w_ * 0.34, cy - h_ * 0.10, cx + w_ * 0.22, cy + h_ * 0.10],
                      fill=pal["soft"], outline=pal["ink"], width=8)
            poly(d, [(cx + w_ * 0.19, cy), (cx + w_ * 0.38, cy - h_ * 0.09),
                     (cx + w_ * 0.38, cy + h_ * 0.09)], pal, pal["soft"], 8)
            n = 3
            for i in range(n):
                gx = cx - w_ * 0.21 + i * 30
                d.arc([gx - 34, cy - h_ * 0.082, gx + 34, cy + h_ * 0.082], 250, 110,
                      fill=pal["ink"], width=8)
            disc(d, cx - w_ * 0.27, cy - h_ * 0.028, 11, pal["ink"], pal, w=0)
            out.append(f"1 条鱼，头侧 {n} 道鳃缝")
    return "两格等大：左格（鱼）" + out[0] + " / 右格（鲸）" + out[1]


@page("whale", 6)
def _(d, pal, img):
    """换气分两步：先把废气喷出去，再吸一大口新的。"""
    cy = S / 2 + 60
    xs, slot = lay(2)
    a = asset("whale", 1)
    sizes = [place(img, a, x, cy, w=slot * 0.74) for x in xs]
    arrow(d, xs[0] + slot * 0.40, cy, xs[1] - slot * 0.40, cy, pal, w=10, head=26)
    ww, wh = sizes[0]
    bx, by = xs[0] - ww * 0.30, cy - wh * 0.36
    k, spray = 5, 260
    for i in range(k):                                    # 第 1 步：喷出去的废气
        t = math.radians(-90 + (i - (k - 1) / 2) * 15)
        d.line([bx, by, bx + spray * math.cos(t), by + spray * math.sin(t)],
               fill=pal["soft"], width=12)
    ww2, wh2 = sizes[1]
    bx2, by2 = xs[1] - ww2 * 0.30, cy - wh2 * 0.36
    arrow(d, bx2, by2 - spray, bx2, by2 - 30, pal, w=16, head=40)
    return (f"2 步横排、中间 1 支箭头：第 1 步 1 条鲸喷气（{k} 条向上散开的气线，各长 {spray}px）/ "
            f"第 2 步同一条鲸吸气（1 支向下扎进喷气孔的粗箭头）")


@page("whale", 8)
def _(d, pal):
    """我憋一分钟，海豚十分钟，抹香鲸一个多小时。"""
    mins = (1, 10, 70)
    rows = [(m / mins[-1], k, t) for m, k, t in
            zip(mins, ("soft", "line", "accent"), ("我 1 分钟", "海豚 10 分钟", "抹香鲸 70 分钟"))]
    note = bars(d, pal, rows, h=104)
    full = S - 2 * MARGIN - 100
    return note + f"，严格按 1 : 10 : 70 的比例（1 分钟 = {full / mins[-1]:.1f}px）"


@page("whale", 10)
def _(d, pal):
    """它一次只睡半边脑子，另外半边替它守着。"""
    cx, cy, R = S / 2, S / 2 - 10, 300
    d.pieslice([cx - R, cy - R, cx + R, cy + R], 90, 270, fill=pal["accent"],
               outline=pal["ink"], width=9)
    d.pieslice([cx - R, cy - R, cx + R, cy + R], -90, 90, fill=pal["paper"],
               outline=pal["ink"], width=9)
    d.line([cx, cy - R, cx, cy + R], fill=pal["ink"], width=11)
    ey = cy + R + 110
    d.line([cx - 250, ey, cx - 90, ey], fill=pal["ink"], width=14)        # 闭着的那只
    disc(d, cx + 170, ey, 54, pal["paper"], pal, w=9)                     # 睁着的那只
    disc(d, cx + 170, ey, 20, pal["ink"], pal, w=0)
    return ("1 个脑子分成 2 半：左半填强调色（睡着的那半）/ 右半留白（醒着的那半），"
            "中间 1 条分界线；下面 1 只闭着的眼（1 条横线）+ 1 只睁着的眼（1 个圆）")


# ================================================================ spider 蜘蛛网是怎么织出来的
# 这本是这一批里几何最漂亮的：辐条几根、螺旋绕几圈全由参数决定，螺旋用极坐标算点。

SP_CX, SP_CY, SP_R, SP_HUB = S / 2, S / 2 + 10, 430, 26
SP_N = 34                       # 旁白说「数一数，三十多根」——三十四根，全书统一


@page("spider", 2)
def _(d, pal, img):
    """第一步放出一根丝，风一吹飘过去，粘在对面的树枝上 —— 三步。"""
    cy = S / 2
    note = steps(img, d, pal, "spider", [None, None, None], cy=cy)
    xs, slot = lay(3)
    half = slot * 0.36
    sag = 70
    for k, x in enumerate(xs):
        d.line([x - half, cy - 210, x - half, cy + 300], fill=pal["bark"], width=34)
        if k == 2:
            d.line([x + half, cy - 210, x + half, cy + 300], fill=pal["bark"], width=34)
        if k == 0:                                     # 刚放出来的一根丝，垂在自己这边
            d.line([(x - half, cy - 120), (x - half + 40, cy + 20), (x - half + 30, cy + 170)],
                   fill=pal["ink"], width=6, joint="curve")
            place(img, asset("spider", 1), x - half + 10, cy - 180, h=100)
        elif k == 1:                                   # 风把丝吹过去，还没搭上
            d.line([(x - half, cy - 120), (x, cy - 40), (x + half * 0.9, cy + 30)],
                   fill=pal["ink"], width=6, joint="curve")
            for i in range(3):
                arrow(d, x - half - 10, cy - 250 + i * 70, x + half * 0.8, cy - 250 + i * 70,
                      pal, w=7, head=20)
        else:                                          # 两端都粘住了，桥搭好
            d.line([(x - half, cy - 120), (x, cy - 120 + sag), (x + half, cy - 120)],
                   fill=pal["ink"], width=8, joint="curve")
    return (note + f"：第 1 格 1 只蜘蛛（素材）放出 1 根丝 / 第 2 格 3 支一样长的风箭头把丝吹过去 / "
            f"第 3 格 1 座搭好的桥（跨 {2 * half:.0f}px、中间下垂 {sag}px），两端各 1 根树枝")


@page("spider", 4)
def _(d, pal, img):
    """走到桥中间往下坠一根丝，三根丝聚在一起，网的中心就定了。"""
    bx0, bx1, by = MARGIN + 90, S - MARGIN - 90, 230
    hub = (S / 2, 560)
    leaf = (S / 2 + 30, S - MARGIN - 130)
    for x in (bx0, bx1):
        d.line([x, by - 140, x, S - MARGIN - 60], fill=pal["bark"], width=36)
    d.line([bx0, by, bx1, by], fill=pal["line"], width=5)          # 原来那座桥
    poly(d, [(leaf[0] - 150, leaf[1]), (leaf[0], leaf[1] - 70), (leaf[0] + 150, leaf[1]),
             (leaf[0], leaf[1] + 70)], pal, pal["soft"], 7)        # 下面的叶子
    ends = [(bx0, by), (bx1, by), leaf]
    lens = []
    for e in ends:
        d.line([hub[0], hub[1], e[0], e[1]], fill=pal["ink"], width=8)
        lens.append(math.hypot(e[0] - hub[0], e[1] - hub[1]))
    disc(d, hub[0], hub[1], 22, pal["accent"], pal, w=7)
    place(img, asset("spider", 1), hub[0], hub[1] - 20, h=120)
    return (f"1 个中心点，正好 {len(ends)} 根丝在这里汇合："
            f"2 根往上通到左右树枝（长 {lens[0]:.0f}px / {lens[1]:.0f}px），"
            f"1 根往下通到叶子（长 {lens[2]:.0f}px）；中心上 1 只蜘蛛（素材）")


@page("spider", 5)
def _(d, pal, img):
    """从中心到边上，一根又一根，数一数三十多根。"""
    cx, cy, R, n = SP_CX, SP_CY, SP_R, SP_N
    rim = [_spoke_pt(cx, cy, n, i, R) for i in range(n)]
    d.line(rim + [rim[0]], fill=pal["line"], width=6, joint="curve")   # 外框
    _spokes(d, pal, cx, cy, n, SP_HUB, R, w=5)
    disc(d, cx, cy, SP_HUB, pal["paper"], pal, w=6)
    sw, sh = place(img, asset("spider", 1), cx, cy, h=150)
    return (f"从 1 个中心均匀放射 {n} 根辐条，相邻两根夹角 {360 / n:.1f}°，"
            f"外端全落在半径 {R}px 的同一个圆上（外框把它们连起来）；中心 1 只蜘蛛（素材 {sw}×{sh}px）")


@page("spider", 6)
def _(d, pal, img):
    """辐条拉完，它从中心往外绕出一圈松松的丝，只当脚手架。"""
    cx, cy, n = SP_CX, SP_CY, SP_N
    R, turns, r0 = 400, 5, 60
    _spokes(d, pal, cx, cy, n, SP_HUB, SP_R, color=pal["line"], w=4)
    rr = [r0 + (R - r0) * i / turns for i in range(turns + 1)]
    pts = _spiral_pts(cx, cy, rr)
    d.line(pts, fill=pal["ink"], width=14, joint="curve")
    d.line(pts, fill=pal["soft"], width=8, joint="curve")
    disc(d, cx, cy, SP_HUB, pal["paper"], pal, w=6)
    place(img, asset("spider", 1), pts[-1][0], pts[-1][1], h=120)
    return (f"{n} 根辐条（淡色）+ 1 条从中心往外绕的临时螺旋：绕 {turns} 圈，"
            f"半径从 {r0}px 到 {R}px、圈距一律 {(R - r0) / turns:.0f}px（松），"
            f"拉直了长 {_plen(pts):.0f}px，点全由极坐标算出；蜘蛛（素材）停在最外那头")


@page("spider", 7)
def _(d, pal, img):
    """掉过头来从最外圈往里绕，这回的丝是粘的，一圈比一圈密。"""
    cx, cy, n = SP_CX, SP_CY, SP_N
    turns = 14
    rr, gaps = _shrinking_radii(420, 70, turns, ratio=0.42)
    _spokes(d, pal, cx, cy, n, SP_HUB, SP_R, color=pal["line"], w=4)
    pts = _spiral_pts(cx, cy, rr)
    d.line(pts, fill=pal["ink"], width=13, joint="curve")
    d.line(pts, fill=pal["accent"], width=7, joint="curve")
    disc(d, cx, cy, SP_HUB, pal["paper"], pal, w=6)
    place(img, asset("spider", 1), pts[0][0], pts[0][1], h=110)
    arrow(d, cx + 470 * math.cos(math.radians(-70)), cy + 470 * math.sin(math.radians(-70)),
          cx + 300 * math.cos(math.radians(-70)), cy + 300 * math.sin(math.radians(-70)),
          pal, w=9, head=24)
    return (f"{n} 根辐条 + 1 条从外往里绕的粘丝螺旋：绕 {turns} 圈，"
            f"圈距从最外圈 {gaps[0]:.1f}px 一路收到最里圈 {gaps[-1]:.1f}px（越往里越密），"
            f"半径 {rr[0]:.0f}px 收到 {rr[-1]:.0f}px，拉直了长 {_plen(pts):.0f}px，点全由极坐标算出；"
            f"外圈 1 支往里的箭头，蜘蛛（素材）在起点")


@page("spider", 8)
def _(d, pal, img):
    """辐条的丝不粘，绕圈的丝才粘 —— 蜘蛛只踩辐条走。"""
    cx, cy, n = SP_CX, SP_CY, SP_N
    turns = 8
    rr, gaps = _shrinking_radii(420, 90, turns, ratio=0.5)
    _spokes(d, pal, cx, cy, n, SP_HUB, SP_R, color=pal["ink"], w=7)     # 不粘：ink，细
    pts = _spiral_pts(cx, cy, rr)
    d.line(pts, fill=pal["ink"], width=20, joint="curve")
    d.line(pts, fill=pal["accent"], width=12, joint="curve")            # 粘：强调色，粗
    disc(d, cx, cy, SP_HUB, pal["paper"], pal, w=6)
    walk, steps_n = 9, 6
    for k in range(steps_n):
        r = 70 + k * (300 - 70) / (steps_n - 1)
        px, py = _spoke_pt(cx, cy, n, walk, r)
        disc(d, px, py, 15, pal["soft"], pal, w=5)
    sx, sy = _spoke_pt(cx, cy, n, walk, 350)
    place(img, asset("spider", 1), sx, sy, h=140)
    fx, fy = _spiral_pts(cx, cy, rr)[int(2.4 * 96)]
    place(img, asset("spider", 3), fx, fy, h=110)
    return (f"{n} 根辐条用 ink 画、线宽 7px（不粘）+ 1 条 {turns} 圈的螺旋用强调色画、线宽 12px（粘）；"
            f"蜘蛛（素材）落在第 {walk + 1} 根辐条上，这根辐条上 {steps_n} 个落脚点、螺旋上 0 个；"
            f"螺旋上另粘着 1 只苍蝇（素材）")


# ================================================================ giraffe 长颈鹿的脖子

@page("giraffe", 2)
def _(d, pal):
    """光是一个脖子就有两米多长，比爸爸站着还高。"""
    base = S - MARGIN - 40
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    ppm = 300
    neck, dad, me = 2.2, 1.8, 1.2
    nh = neck * ppm
    d.rounded_rectangle([230 - 60, base - nh, 230 + 60, base], radius=52,
                        fill=pal["accent"], outline=pal["ink"], width=9)
    _person(d, pal, 560, base, dad * ppm)
    _person(d, pal, 830, base, me * ppm)
    for h in (nh, dad * ppm, me * ppm):
        d.line([MARGIN, base - h, S - MARGIN, base - h], fill=pal["line"], width=4)
    return (f"同一条地线上三样东西：脖子 {neck} 米 = {nh:.0f}px / 爸爸 {dad} 米 = {dad * ppm:.0f}px / "
            f"我 {me} 米 = {me * ppm:.0f}px（1 米 = {ppm}px），"
            f"脖子比我高出 {(neck - me) * ppm:.0f}px，各高度上 1 条水平参照线")


@page("giraffe", 4)
def _(d, pal, img):
    """你摸摸自己的脖子，里面有七块骨头；长颈鹿的脖子里也正好是七块。"""
    bone = lie_flat(asset("giraffe", 2))
    n = 7
    out = []
    for (cx, cy, w_, h_), frac in zip(panel2(d, pal), (0.30, 0.86)):
        pitch = h_ * 0.115
        top = cy - pitch * (n - 1) / 2
        bw = bh = 0
        for i in range(n):
            bw, bh = place(img, bone, cx, top + i * pitch, w=w_ * frac)
        out.append(f"{n} 块颈椎（每块 {bw}×{bh}px，行距 {pitch:.0f}px）")
    return "两格等大，两边都是 7 块：左格（我）" + out[0] + " / 右格（长颈鹿）" + out[1]


@page("giraffe", 5)
def _(d, pal, img):
    """它的一块颈椎骨，差不多有我的一条胳膊那么长 —— 两条必须严格等长。"""
    ln = S - 2 * MARGIN - 160
    x0 = MARGIN + 80
    bw, bh = place(img, lie_flat(asset("giraffe", 2)), x0 + ln / 2, S / 2 - 180, w=ln)
    seg = (0.42, 0.40, 0.18)                      # 上臂 / 前臂 / 手掌，合计正好 1.0
    hts = (74, 60, 46)
    y = S / 2 + 200
    x = x0
    for f, hh in zip(seg, hts):
        d.rounded_rectangle([x, y - hh / 2, x + ln * f, y + hh / 2], radius=hh / 2,
                            fill=pal["soft"], outline=pal["ink"], width=8)
        x += ln * f
    for k in (seg[0], seg[0] + seg[1]):
        disc(d, x0 + ln * k, y, 30, pal["accent"], pal, w=7)
    for xx in (x0, x0 + ln):                      # 两端的对齐虚线
        for s_ in range(9):
            yy = S / 2 - 100 + s_ * 34
            d.line([xx, yy, xx, yy + 17], fill=pal["line"], width=5)
    return (f"上面 1 块横躺的颈椎骨（素材，长 {bw}px）/ 下面 1 条胳膊"
            f"（上臂 {ln * seg[0]:.0f}px + 前臂 {ln * seg[1]:.0f}px + 手掌 {ln * seg[2]:.0f}px "
            f"= {ln}px，2 个关节），两端各 1 条对齐虚线，两者长度严格相同")


@page("giraffe", 7)
def _(d, pal):
    """把血往上顶两米高，这股劲比我们要大上两三倍。"""
    note = bars(d, pal, [(1.00, "accent", "长颈鹿的心劲"), (0.40, "soft", "我们的心劲")], h=120)
    return note + "，长颈鹿那条正好是我们的 2.5 倍（旁白说的「两三倍」）"


@page("giraffe", 9)
def _(d, pal):
    """脖子里有一道道瓣膜，像一扇扇小门，把血挡住慢慢放。"""
    cx, half = S / 2 + 40, 95
    top, bot = MARGIN + 60, S - MARGIN - 60
    d.rounded_rectangle([cx - half, top, cx + half, bot], radius=44,
                        fill=pal["paper"], outline=pal["ink"], width=9)
    n = 7
    for i in range(n):
        y = top + (bot - top) * (i + 0.55) / n
        for s in (-1, 1):
            poly(d, [(cx + s * half, y - 36), (cx + s * half, y + 6),
                     (cx + s * half * 0.12, y + 44)], pal, pal["accent"], 7)
    arrow(d, cx - half - 110, top + 40, cx - half - 110, bot - 40, pal, w=12, head=32)
    return (f"1 根竖着的血管（宽 {2 * half}px、长 {bot - top}px），里面 {n} 道瓣膜、"
            f"每道 2 扇小门（共 {2 * n} 扇，间距 {(bot - top) / n:.0f}px），"
            f"旁边 1 支往下的血流箭头")
