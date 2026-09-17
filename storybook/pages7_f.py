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


# _tad()（圆身子 + 多边形尾巴拼出来的整只蝌蚪）已经删掉：
# 蝌蚪 p4 / p5 / p7 现在一律用素材（1 / 5 / 6 / 7 / 2），程序只管数目、尺寸和摆放。


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


def _fit(img, a, cx, cy, box_w=None, box_h=None, anchor="center"):
    """把素材放进一个格子：宽和高谁先顶到边就按谁缩放。

    素材还没出图，长宽比是未知数；凡是排成一行一列的（水桶、腹鳞、颈椎），
    只按宽度缩放就有可能纵向撑出格子、压到上下那一个。这里两边都卡住。
    """
    aw, ah = a.size
    s = min(box_w / aw if box_w else 1e9, box_h / ah if box_h else 1e9)
    return place(img, a, cx, cy, w=aw * s, anchor=anchor)


def _rows2(d, pal, gap=44):
    """上下两行等大的对比框，返回两个 (cx, cy, w, h) —— panel2 的竖版。

    两件要比的东西都又扁又长（蝌蚪的长宽比接近 4:1）时，左右分格先把宽度砍掉一半，
    再按长宽比把高度砍到一百出头，整格剩下的全是空白。上下分行反过来：
    宽度是整页的，高度才是被分掉的那一维，正好喂给扁长的东西。
    两行的 w、h 同出一份计算，所以「两行等大」和 panel2 一样是构造保证的。
    """
    h = (S - 2 * MARGIN - gap) / 2
    w = S - 2 * MARGIN
    boxes = []
    for i in range(2):
        cy = MARGIN + h / 2 + i * (h + gap)
        d.rounded_rectangle([MARGIN, cy - h / 2, S - MARGIN, cy + h / 2],
                            radius=18, fill=pal["paper"], outline=pal["ink"], width=6)
        boxes.append((S / 2, cy, w, h))
    return boxes


def _plen(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def _mid_x(a, frac):
    """素材在相对高度 frac 那一行上实体的中点，按素材宽度取比例。

    「树梢在哪儿」不该由我数像素：从素材自己的 alpha 上量那一行，丝就从真的枝头放出去。
    """
    w_, h_ = a.size
    y = max(0, min(h_ - 1, int(h_ * frac)))
    bb = a.getchannel("A").crop((0, y, w_, y + 1)).getbbox()
    return 0.5 if not bb else (bb[0] + bb[2]) / 2.0 / w_


def _bezier(p0, p1, p2, n=48):
    """二次贝塞尔，用来画飘过去的那根丝 —— 下垂多少写在控制点里，量得出来。"""
    pts = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        pts.append((u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
                    u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1]))
    return pts


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
    # 十一个桶共用同一个框，所以「我那一桶」和「它那十桶」一定一样大。
    # 框比槽宽多 2%：相邻两个桶轻微搭一点边，换来单个桶大出三成 —— 桶太小就数不清了。
    xs, slot = lay(5)
    box_w, box_h = slot * 1.02, 232
    bw, bh = _fit(img, b, S / 2, 268, box_w, box_h, anchor="bottom")
    d.line([MARGIN, 300, S - MARGIN, 300], fill=pal["line"], width=6)
    n = 0
    for r_ in range(2):
        for x in xs:
            _fit(img, b, x, 630 + r_ * 345, box_w, box_h, anchor="bottom")
            n += 1
    return (f"上面 1 个水桶（我一天喝的）/ 下面 {n} 个水桶（骆驼一口气，2 行 ×5），"
            f"11 个桶共用一个 {box_w:.0f}×{box_h}px 的框、实际一律 {bw}×{bh}px，"
            f"横向间距 {slot:.0f}px、行距 345px，中间 1 条分隔线")


@page("camel", 8)
def _(d, pal):
    """白天让身子先变热，热得受不了才出汗 —— 出汗线越高，汗越少。"""
    out = []
    for (cx, cy, w_, h_), (thr, drops) in zip(panel2(d, pal), ((0.30, 6), (0.72, 2))):
        x0, x1 = cx - w_ * 0.36, cx + w_ * 0.36
        base, top = cy + h_ * 0.30, cy - h_ * 0.38
        ty = base - (base - top) * thr
        d.line([x0, base, x1, base], fill=pal["line"], width=6)        # 起点（早上的体温）
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
    sw, sh = _fit(img, asset("snake", 1), S / 2, 290, S - 2 * MARGIN - 60, 380)
    # 旁白只说「一排」「一片挨着一片」，没点数目 —— 那就少放几片、每片放大：
    # 十四片时每片只有 63px 宽，看不出「又宽又扁、后边翘起来」。
    n = 5
    span = S - 2 * MARGIN - 40
    unit = span / n
    sc = asset("snake", 2)
    cw = ch = 0
    for i in range(n):
        cw, ch = _fit(img, sc, S / 2 - span / 2 + unit * (i + 0.5), 800, unit, 300)
    d.line([S / 2 - span / 2, 640, S / 2 + span / 2, 640], fill=pal["line"], width=5)
    return (f"上面 1 条蛇（素材1，{sw}×{sh}px）/ 下面 {n} 片腹鳞首尾相接铺满 {unit * n:.0f}px，"
            f"每片占 {unit:.0f}px 宽（实际 {cw}×{ch}px），一片挨着一片没有缝")


@page("snake", 4)
def _(d, pal, img):
    """鳞勾着地面，身子被推着往前 —— 每片鳞一支往后的小箭头，合起来一支往前的大箭头。"""
    base = 720
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=11)
    n = 5                                     # 旁白没点数目：八片 104px 太小，五片各大一半
    xs, slot = lay(n)
    sc = asset("snake", 2)
    sw = sh = 0
    for x in xs:
        sw, sh = _fit(img, sc, x, base, slot * 0.94, 230, anchor="bottom")
        arrow(d, x, base + 46, x - 86, base + 124, pal, w=8, head=24)   # 往后勾一下
    arrow(d, MARGIN + 120, 250, S - MARGIN - 120, 250, pal, w=14, head=36)  # 身子往前走
    return (f"地线上 {n} 片腹鳞（素材，各 {sw}×{sh}px、间距 {slot:.0f}px），"
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
def _(d, pal, img):
    """屁股后面先鼓出两个小包，小包慢慢伸长，变成两条后腿。"""
    # 蝌蚪是横着长的（素材长宽比接近 4:1），三只横排一格只有 244px 宽、66px 高。
    # 改成竖着排三行，每只能占满整页宽 —— 同样是 3 个阶段，单只大了三倍多。
    cys = (180, 512, 844)
    box_w, box_h = S - 2 * MARGIN - 60, 250   # 三行共用一个框，所以三只一样大
    plain, legged = asset("tadpole", 1), asset("tadpole", 5)
    sizes = [_fit(img, plain if i < 2 else legged, S / 2, y, box_w, box_h)
             for i, y in enumerate(cys)]
    bw, bh = sizes[1]
    r = max(16, bh * 0.13)
    # 小包鼓在「屁股后面」＝ 身子收进尾巴的那一段的两侧边上，不是背中央 ——
    # 第 3 行长出来的两条后腿也正是从这个位置伸出去的，两行对得上。
    for s in (-1, 1):                         # 第 2 行：2 个小包，数目由程序保证
        disc(d, S / 2 + bw * 0.03, cys[1] + s * bh * 0.30, r, pal["accent"], pal, w=7)
    for i in range(2):
        arrow(d, S / 2, cys[i] + box_h / 2 + 10, S / 2, cys[i + 1] - box_h / 2 - 10,
              pal, w=10, head=26)
    return (f"3 行竖排，共用一个 {box_w}×{box_h}px 的框：第 1 行 1 只光身子的蝌蚪"
            f"（素材1，{sizes[0][0]}×{sizes[0][1]}px，0 个包 0 条腿）/ 第 2 行同一个素材"
            f"另加 2 个小包（直径 {2 * r:.0f}px）/ 第 3 行 1 只已经长出 2 条后腿的蝌蚪"
            f"（素材5，{sizes[2][0]}×{sizes[2][1]}px），行间 2 支向下的箭头")


@page("tadpole", 5)
def _(d, pal, img):
    """后腿长好了前腿才长：先藏在皮里，忽然从两边顶出来。"""
    out = []
    boxes = _rows2(d, pal)                            # 蝌蚪又扁又长，上下分行才放得大
    for (cx, cy, w_, h_), outside in zip(boxes, (False, True)):
        # 下行的前腿是素材自己长的（素材6 四条腿）；上行前腿还没出来，
        # 藏在皮里的那两条只能由程序画 —— 虚线，2 条，每条 5 段。
        a = asset("tadpole", 6 if outside else 5)
        bw, bh = _fit(img, a, cx, cy, w_ * 0.94, h_ * 0.62)
        if outside:
            out.append(f"1 只四条腿的蝌蚪（素材6，{bw}×{bh}px），2 条前腿已经顶到身子外面")
        else:
            for s in (-1, 1):                         # 从头后面的「肩膀」往外斜着顶
                bx, by = cx - bw * 0.14, cy + s * bh * 0.10
                ex, ey = cx - bw * 0.27, cy + s * bh * 0.42
                for k in range(5):
                    t0, t1 = k / 5 + 0.04, (k + 1) / 5 - 0.04
                    d.line([bx + (ex - bx) * t0, by + (ey - by) * t0,
                            bx + (ex - bx) * t1, by + (ey - by) * t1],
                           fill=pal["ink"], width=7)
            out.append(f"1 只只长了后腿的蝌蚪（素材5，{bw}×{bh}px），另画 2 条藏在皮里的前腿"
                       f"（每条 5 段虚线，都落在身子的轮廓里）")
    return (f"两行等大（各 {boxes[0][2]:.0f}×{boxes[0][3]:.0f}px），两只都已经长好 2 条后腿："
            "上行 " + out[0] + " / 下行 " + out[1])


@page("tadpole", 7)
def _(d, pal, img):
    """鳃慢慢不见，身体里长出了肺，得浮到水面吸一口空气。"""
    out = []
    for (cx, cy, w_, h_), frog in zip(panel2(d, pal), (False, True)):
        wl = cy - h_ * 0.20
        d.line([cx - w_ * 0.46, wl, cx + w_ * 0.46, wl], fill=pal["line"], width=10)
        # 右格本来就该是青蛙，以前却还是同一只几何蝌蚪，只在肚子里加两个椭圆当肺。
        a = asset("tadpole", 2 if frog else 7)
        by = wl + h_ * (0.16 if frog else 0.34)        # 青蛙贴着水面，带鳃的蝌蚪整只在水下
        bw, bh = _fit(img, a, cx, by, w_ * 0.86, h_ * 0.44)
        if frog:                                       # 肺在身体里面，只能由程序画：2 个
            # 肺是长在胸口的一对小袋子，不是糊在肚皮上的两团 —— 往上挪到胸口、缩到原来一半
            ly = by - bh * 0.13
            lw_, lh_, off = bw * 0.055, bh * 0.10, bw * 0.085
            for s in (-1, 1):
                d.ellipse([cx + s * off - lw_, ly - lh_, cx + s * off + lw_, ly + lh_],
                          fill=pal["accent"], outline=pal["ink"], width=7)
                d.line([cx, ly - lh_ * 1.1, cx + s * off, ly - lh_ * 0.3],
                       fill=pal["ink"], width=10)
            d.line([cx, ly - lh_ * 2.2, cx, ly - lh_ * 1.0], fill=pal["ink"], width=12)
            arrow(d, cx, wl - 40, cx, wl - 190, pal, w=11, head=28)
            out.append(f"1 只青蛙（素材2，{bw}×{bh}px）浮到水面，胸口 2 个肺"
                       f"（各 {2 * lw_:.0f}×{2 * lh_:.0f}px）+ 1 根气管 + 1 支向上的吸气箭头")
        else:
            out.append(f"1 只带鳃的蝌蚪（素材7，{bw}×{bh}px）整只在水下，0 个肺")
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
    # 四格横着排，一格只剩 178px 宽，四只都小得看不清。改成 2×2 顺时针走一圈，
    # 同样是 4 格，单格能放到 330×290 —— 长腿那只现在是素材5，不用再手画后腿。
    box_w, box_h = 396, 300
    cxs, cys = (S / 2 - 248, S / 2 + 248), (300, 730)
    cells = [(cxs[0], cys[0], 3), (cxs[1], cys[0], 1),
             (cxs[1], cys[1], 5), (cxs[0], cys[1], 2)]
    sizes = [_fit(img, asset("tadpole", a), x, y, box_w, box_h) for x, y, a in cells]
    arrow(d, cxs[0] + box_w / 2 + 14, cys[0], cxs[1] - box_w / 2 - 14, cys[0],
          pal, w=10, head=26)                          # 卵 → 蝌蚪
    arrow(d, cxs[1], cys[0] + box_h / 2 + 14, cxs[1], cys[1] - box_h / 2 - 14,
          pal, w=10, head=26)                          # 蝌蚪 → 长腿蝌蚪
    arrow(d, cxs[1] - box_w / 2 - 14, cys[1], cxs[0] + box_w / 2 + 14, cys[1],
          pal, w=10, head=26)                          # 长腿蝌蚪 → 青蛙
    return (f"4 个模样排成 2×2 顺时针走一圈（左上卵 素材3 → 右上蝌蚪 素材1 → "
            f"右下长腿蝌蚪 素材5 → 左下青蛙 素材2），四格共用一个 {box_w}×{box_h}px 的框、"
            f"实际 " + " / ".join(f"{w}×{h}" for w, h in sizes) + "px，中间 3 支箭头，"
            "4 个模样是同一只")


# ================================================================ seaturtle 海龟怎么找回出生的那片海滩

@page("seaturtle", 3)
def _(d, pal, img):
    """用后脚挖坑，挖得比自己还深，再下一百多个蛋。"""
    sand = 330
    d.rectangle([MARGIN, sand, S - MARGIN, S - MARGIN], fill=pal["bark"],
                outline=pal["ink"], width=7)
    pit_w, depth = 610, 620
    px0 = S / 2 - pit_w / 2
    d.rounded_rectangle([px0, sand, px0 + pit_w, sand + depth], radius=70,
                        fill=pal["ground"], outline=pal["ink"], width=8)
    tw, th = _fit(img, asset("seaturtle", 1), S / 2, sand + 8, 430, 300, anchor="bottom")
    for seg in range(10):                              # 坑有多深：虚线量到坑底
        y = sand + 14 + seg * (depth - 20) / 10
        d.line([px0 - 100, y, px0 - 100, y + (depth - 20) / 20], fill=pal["line"], width=7)
    # 把龟自己的体长竖过来放在旁边，一眼看得出坑比它还深
    d.line([px0 - 50, sand, px0 - 50, sand + tw], fill=pal["accent"], width=14)
    # 「一百多个」是旁白点名的数目，所以还是一颗一颗摆 108 个 —— 只是每一颗
    # 从程序画的小白圆换成素材3（一颗真的海龟蛋），坑也放大了，单颗从 30px 长到 47px。
    # 摆成正正方方的 12×9 像张表格；单双行错开半格，看着才像一窝堆着的蛋，
    # 数目一点没变 —— 行数列数还是算出来的。
    egg = asset("seaturtle", 3)
    cols, rows_ = 12, 9
    pitch, rowh = 46, 41.4
    ex0 = S / 2 - (pitch * (cols - 1) + pitch / 2) / 2
    ey0 = sand + depth - 70 - rowh * (rows_ - 1)
    n = 0
    ew = eh = 0
    for r_ in range(rows_):
        for c_ in range(cols):
            ew, eh = _fit(img, egg, ex0 + c_ * pitch + (pitch / 2 if r_ % 2 else 0),
                          ey0 + r_ * rowh, pitch * 0.98, pitch * 1.06)
            n += 1
    return (f"沙面下 1 个坑，深 {depth}px，比上面那只龟的体长 {tw}px 还深；"
            f"坑里 {n} 个蛋（素材3，{rows_} 行 ×{cols} 列、单双行错开半格，"
            f"列距 {pitch}px、行距 {rowh:.0f}px，每颗 {ew}×{eh}px）")


@page("seaturtle", 4)
def _(d, pal, img):
    """沙子凉的时候孵出来多是男孩，热的时候多是女孩 —— 只有点的颜色数目不同。"""
    baby = asset("seaturtle", 2)
    # 旁白只说「多是男孩 / 多是女孩」，没点数目：六只 110px 太小，改成四只 2×2、每只放大一倍。
    out = []
    for (cx, cy, w_, h_), (sun, hot) in zip(panel2(d, pal), ((45, 1), (85, 3))):
        disc(d, cx, cy - h_ * 0.35, sun, pal["accent"] if sun > 60 else pal["paper"], pal, w=8)
        n = 4
        bw = bh = 0
        for i in range(n):
            r_, c_ = divmod(i, 2)
            bx = cx + (c_ - 0.5) * w_ * 0.46
            by = 520 + r_ * 240
            bw, bh = _fit(img, baby, bx, by, w_ * 0.42, 190)
            disc(d, bx, by + 118, 20, pal["accent"] if i < hot else pal["soft"], pal, w=5)
        out.append(f"太阳半径 {sun}px、{n} 只小龟（2 行 ×2 列，各 {bw}×{bh}px）、"
                   f"{hot} 个强调色点 + {n - hot} 个 soft 点")
    return "两格等大：左格（沙子凉，多是男孩）" + out[0] + " / 右格（沙子热，多是女孩）" + out[1]


@page("seaturtle", 7)
def _(d, pal, img):
    """爬这几分钟里，它们记下的是地下磁力的方向。"""
    sand = 560
    d.rectangle([MARGIN, sand, S - MARGIN, S - MARGIN], fill=pal["bark"],
                outline=pal["ink"], width=7)
    n = 3
    xs, slot = lay(n)                       # 以前按 4 槽排 3 只，宽度白白卡在 200px
    # 素材是俯视、头朝上的，顺时针转 90° 让它头朝右 —— 和上面那支路径箭头同一个方向
    baby = asset("seaturtle", 2).rotate(-90, expand=True)
    bw = bh = 0
    for i in range(n):
        bw, bh = _fit(img, baby, xs[i], sand - 25, slot * 0.90, 320, anchor="bottom")
    arrow(d, MARGIN + 120, 150, S - MARGIN - 120, 150, pal, w=12, head=32)
    k, ang, alen = 5, 20, 150
    ax, ay = alen * math.cos(math.radians(ang)) / 2, alen * math.sin(math.radians(ang)) / 2
    for i in range(k):
        x = MARGIN + 130 + i * (S - 2 * MARGIN - 260) / (k - 1)
        y = sand + 200
        arrow(d, x - ax, y + ay, x + ax, y - ay, pal, w=10, head=26)
    return (f"沙滩上 {n} 只小龟（素材2，各 {bw}×{bh}px、间距 {slot:.0f}px）朝同一个方向爬，"
            f"上面 1 支路径箭头；沙层下面 {k} 支磁力箭头，方向完全相同"
            f"（都倾斜 {ang}°、都长 {alen}px）")


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
            for s in (-1, 1):                          # 斜着看的那两个方向，一律打叉
                cross(d, cx + s * 193, base - 230, 48, pal)
            out.append("1 根管子 + 2 块卡住它的骨头 + 1 支只能朝正前的箭头 + 2 个叉")
    return "两格等大：左格（我们）" + out[0] + " / 右格（猫头鹰）" + out[1]


@page("owl", 6)
def _(d, pal, img):
    """它的脖子里藏着十四节骨头，我们只有七节。"""
    # 以前两摞塞进同样高的 700px：我们那摞每节 94px，猫头鹰那摞只有 47px —— 这一批最小的一处。
    # 改成两边**骨头一样大**、行数一样多，猫头鹰多出来的 7 节另起一列：
    # 「零件多一倍」就是右边整整多出一列，而不是同一节骨头被压扁一半。
    bone = asset("owl", 4)
    rows, pitch = 7, 111.0
    box_w, box_h = 202.0, pitch * 1.16         # 两格共用一个框，所以同一节骨头两边一样大
    out = []
    for (cx, cy, w_, h_), cols in zip(panel2(d, pal), (1, 2)):
        top = cy - pitch * (rows - 1) / 2
        bw = bh = 0
        for c_ in range(cols):
            for i in range(rows):
                bw, bh = _fit(img, bone, cx + (c_ - (cols - 1) / 2) * (box_w + 14),
                              top + i * pitch, box_w, box_h)
        out.append(f"{cols * rows} 节（{rows} 行 ×{cols} 列，每节 {bw}×{bh}px）")
    return (f"两格等大、两摞一样高（行距都是 {pitch:.0f}px、跨 {pitch * (rows - 1):.0f}px）、"
            f"骨头一样大（共用一个 {box_w:.0f}×{box_h:.0f}px 的框）：左格（我们）" + out[0] +
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
            ww, wh = _fit(img, asset("whale", 1), cx, cy, w_ * 0.88, h_ * 0.50)
            bx, by = cx - ww * 0.30, cy - wh * 0.34
            disc(d, bx, by, 26, pal["accent"], pal, w=7)
            arrow(d, bx, by - 50, bx, by - 190, pal, w=10, head=26)
            out.append(f"1 条鲸（素材1，{ww}×{wh}px），头顶 1 个喷气孔（直径 52px）"
                       f"+ 1 支向上的箭头，0 道鳃缝")
        else:
            # 以前这条鱼是椭圆身子 + 三点多边形尾巴 + 三段 arc 鳃缝 + 一个圆眼睛拼的。
            # 现在整条鱼是素材5，程序只做一件事：把鳃缝那一块圈出来。
            fw, fh = _fit(img, asset("whale", 5), cx, cy, w_ * 0.88, h_ * 0.50)
            gx = cx - fw * 0.22
            d.ellipse([gx - fw * 0.15, cy - fh * 0.44, gx + fw * 0.15, cy + fh * 0.44],
                      outline=pal["accent"], width=12)
            out.append(f"1 条鱼（素材5，{fw}×{fh}px），头后的鳃缝上套 1 个强调色的圈")
    return "两格等大：左格（鱼，有鳃）" + out[0] + " / 右格（鲸，没有鳃）" + out[1]


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

# 网的半径原来定在 430px，蜘蛛按真实比例只能画到 92～150px，六页都看不清它长什么样。
# 这本书讲的是「网是怎么织出来的」，网小一点不影响；蜘蛛看不清才影响 ——
# 所以半径收到 310px，蜘蛛一律提到 200px 以上。
SP_CX, SP_CY, SP_R, SP_HUB = S / 2, S / 2 + 10, 310, 24
SP_N = 34                       # 旁白说「数一数，三十多根」——三十四根，全书统一
SP_SPIDER = 205                 # 蜘蛛的统一尺寸框，全书六页一样大


@page("spider", 2)
def _(d, pal, img):
    """放出一根丝，风一吹飘过去，粘在对面的树枝上 —— 一座桥就搭好了。

    上一版把这句话拆成三格来画，结果是六棵小树、三支指向空白的粗箭头和几条断折线，
    蜘蛛还悬在树的上方，一根丝搭成一座桥这件事一点也看不出来。现在整页只画旁白点到的
    那几样：左右各 1 棵树、1 根从左边树梢飘到右边树梢的丝、1 支风向箭头、1 只站在左边
    树梢上的蜘蛛。树梢在哪儿是从素材 alpha 上量的（_mid_x），丝的两头就落在真的枝头上。
    """
    tree = asset("spider", 4)
    ground, xl, xr, f_top = S - MARGIN - 26, 240, 784, 0.14
    d.line([MARGIN, ground, S - MARGIN, ground], fill=pal["ink"], width=9)
    tw = th = 0
    for x in (xl, xr):
        tw, th = _fit(img, tree, x, ground, 400, 760, anchor="bottom")
    ytop = ground - th + f_top * th                    # 树梢那一行
    pl = (xl - tw / 2 + _mid_x(tree, f_top) * tw, ytop)
    pr = (xr - tw / 2 + _mid_x(tree, f_top) * tw, ytop)
    sag = 120
    silk = _bezier((pl[0] + 40, pl[1]), ((pl[0] + pr[0]) / 2, ytop + sag), pr)
    d.line(silk, fill=pal["ink"], width=7, joint="curve")
    disc(d, pr[0], pr[1], 15, pal["accent"], pal, w=6)  # 粘住对面枝头的那一点
    wy = 305
    arrow(d, MARGIN + 60, wy, S / 2 + 190, wy, pal, w=10, head=30)
    # 蜘蛛正压在树梢那一点上（素材是俯视的，压上去才像蹲在枝头，不能吊在树顶上方）
    sw, sh = _fit(img, asset("spider", 1), pl[0], pl[1], SP_SPIDER, SP_SPIDER)
    return (f"2 棵一样的树（素材4，各 {tw}×{th}px，都站在 y={ground} 的地线上，"
            f"树心相距 {xr - xl}px）；树梢取素材高度 {f_top * 100:.0f}% 那一行的中点，"
            f"两边树梢一样高（y={ytop:.0f}）。1 根丝从左边树梢飘到右边树梢："
            f"跨 {pr[0] - pl[0] - 40:.0f}px、中间最低比树梢低 {sag / 2:.0f}px、"
            f"拉直了长 {_plen(silk):.0f}px，右头 1 个圆点表示粘住了。"
            f"树梢上方 1 支从左往右的风箭头（y={wy}，长 {S / 2 + 190 - MARGIN - 60:.0f}px）。"
            f"1 只蜘蛛（素材1，{sw}×{sh}px）正压在左边树梢那一点上，丝就从它脚下出去")


@page("spider", 4)
def _(d, pal, img):
    """走到桥中间往下坠一根丝，三根丝聚在一起，网的中心就定了。"""
    bx0, bx1, by = MARGIN + 100, S - MARGIN - 100, 230
    hub = (S / 2, 560)
    leaf = (S / 2 + 40, S - MARGIN - 120)
    twig = asset("spider", 4)                                      # 两根树枝：素材4
    tw = th = 0
    for x in (bx0, bx1):
        tw, th = _fit(img, twig, x, 520, 130, 840)
    d.line([bx0, by, bx1, by], fill=pal["line"], width=5)          # 原来那座桥
    lw_, lh_ = _fit(img, asset("spider", 5), leaf[0], leaf[1], 330, 240)  # 下面的叶子：素材5
    ends = [(bx0, by), (bx1, by), leaf]
    lens = []
    for e in ends:
        d.line([hub[0], hub[1], e[0], e[1]], fill=pal["ink"], width=8)
        lens.append(math.hypot(e[0] - hub[0], e[1] - hub[1]))
    disc(d, hub[0], hub[1], 22, pal["accent"], pal, w=7)
    sw, sh = _fit(img, asset("spider", 1), hub[0], hub[1] - 110, SP_SPIDER, SP_SPIDER)
    return (f"1 个中心点，正好 {len(ends)} 根丝在这里汇合："
            f"2 根往上通到左右树枝（素材4，各 {tw}×{th}px，丝长 {lens[0]:.0f}px / "
            f"{lens[1]:.0f}px），1 根往下通到叶子（素材5，{lw_}×{lh_}px，丝长 {lens[2]:.0f}px）；"
            f"中心正上方 1 只蜘蛛（素材1，{sw}×{sh}px）")


@page("spider", 5)
def _(d, pal, img):
    """从中心到边上，一根又一根，数一数三十多根。"""
    cx, cy, R, n = SP_CX, SP_CY, SP_R, SP_N
    rim = [_spoke_pt(cx, cy, n, i, R) for i in range(n)]
    d.line(rim + [rim[0]], fill=pal["line"], width=6, joint="curve")   # 外框
    _spokes(d, pal, cx, cy, n, SP_HUB, R, w=5)
    disc(d, cx, cy, SP_HUB, pal["paper"], pal, w=6)
    # 蜘蛛放在一根辐条的外段上（正在往外拉这一根），不压住中心，中心的汇聚点还看得见
    px, py = _spoke_pt(cx, cy, n, 4, R * 0.74)
    sw, sh = _fit(img, asset("spider", 1), px, py, SP_SPIDER, SP_SPIDER)
    return (f"从 1 个中心均匀放射 {n} 根辐条，相邻两根夹角 {360 / n:.1f}°，"
            f"外端全落在半径 {R}px 的同一个圆上（外框把它们连起来）；"
            f"第 5 根辐条的 74% 处 1 只蜘蛛（素材1，{sw}×{sh}px）")


@page("spider", 6)
def _(d, pal, img):
    """辐条拉完，它从中心往外绕出一圈松松的丝，只当脚手架。"""
    cx, cy, n = SP_CX, SP_CY, SP_N
    R, turns, r0 = 290, 5, 44
    _spokes(d, pal, cx, cy, n, SP_HUB, SP_R, color=pal["ink"], w=4)
    rr = [r0 + (R - r0) * i / turns for i in range(turns + 1)]
    pts = _spiral_pts(cx, cy, rr)
    d.line(pts, fill=pal["ink"], width=14, joint="curve")
    d.line(pts, fill=pal["soft"], width=8, joint="curve")
    disc(d, cx, cy, SP_HUB, pal["paper"], pal, w=6)
    sw, sh = _fit(img, asset("spider", 1), pts[-1][0], pts[-1][1], SP_SPIDER, SP_SPIDER)
    return (f"{n} 根辐条（淡色）+ 1 条从中心往外绕的临时螺旋：绕 {turns} 圈，"
            f"半径从 {r0}px 到 {R}px、圈距一律 {(R - r0) / turns:.0f}px（松），"
            f"拉直了长 {_plen(pts):.0f}px，点全由极坐标算出；"
            f"蜘蛛（素材1，{sw}×{sh}px）停在最外那头")


@page("spider", 7)
def _(d, pal, img):
    """掉过头来从最外圈往里绕，这回的丝是粘的，一圈比一圈密。"""
    cx, cy, n = SP_CX, SP_CY, SP_N
    turns = 14
    rr, gaps = _shrinking_radii(300, 50, turns, ratio=0.42)
    _spokes(d, pal, cx, cy, n, SP_HUB, SP_R, color=pal["ink"], w=4)
    pts = _spiral_pts(cx, cy, rr)
    d.line(pts, fill=pal["ink"], width=13, joint="curve")
    d.line(pts, fill=pal["accent"], width=7, joint="curve")
    disc(d, cx, cy, SP_HUB, pal["paper"], pal, w=6)
    sw, sh = _fit(img, asset("spider", 1), pts[0][0], pts[0][1], SP_SPIDER, SP_SPIDER)
    arrow(d, cx + 380 * math.cos(math.radians(-70)), cy + 380 * math.sin(math.radians(-70)),
          cx + 300 * math.cos(math.radians(-70)), cy + 300 * math.sin(math.radians(-70)),
          pal, w=9, head=24)
    return (f"{n} 根辐条 + 1 条从外往里绕的粘丝螺旋：绕 {turns} 圈，"
            f"圈距从最外圈 {gaps[0]:.1f}px 一路收到最里圈 {gaps[-1]:.1f}px（越往里越密），"
            f"半径 {rr[0]:.0f}px 收到 {rr[-1]:.0f}px，拉直了长 {_plen(pts):.0f}px，点全由极坐标算出；"
            f"外圈 1 支往里的箭头，蜘蛛（素材1，{sw}×{sh}px）在起点")


@page("spider", 8)
def _(d, pal, img):
    """辐条的丝不粘，绕圈的丝才粘 —— 蜘蛛只踩辐条走，所以从不粘住自己。

    上一版蜘蛛落在半径 250px 的辐条上，可那一圈正是粘丝最密的地方：蜘蛛按全书统一的
    205px 摆，相邻两圈粘丝之间最宽只有 39px，怎么摆都压在橙色的粘丝上 —— 画出来的正好
    是这页要否定的事。整张网画在一页里，任何看得清的蜘蛛都塞不进两圈粘丝之间（网半径
    才 310px，里头要绕 8 圈），所以这一页改成网的一小块放大：圆心落在画外下方 130px，
    辐条的夹角还是按整张网的 34 根算，粘丝还是同一条越往里越密的螺旋，只是离得近了，
    两圈之间才腾得出地方，蜘蛛才真站得到辐条上。旁白没提的那只苍蝇去掉。
    """
    hx, hy, n = S / 2, S + 130, SP_N
    step = 2 * math.pi / n
    r_out, r_in, n_ring = hy - MARGIN, 300, 3
    rr, gaps = _shrinking_radii(r_out, r_in, n_ring, ratio=0.5)
    spokes = 0
    for i in range(-3, 4):                       # 直的、不粘：ink 细线
        a = -math.pi / 2 + i * step
        d.line([hx + r_in * 0.4 * math.cos(a), hy + r_in * 0.4 * math.sin(a),
                hx + r_out * math.cos(a), hy + r_out * math.sin(a)],
               fill=pal["ink"], width=7)
        spokes += 1
    for r in rr:                                 # 绕圈的、粘：强调色粗线
        # 角度开到 ±1.5rad：每一圈都从画面的边上出去，不会在半空里断掉
        arc = [(hx + r * math.sin(t * 0.015 - 1.5), hy - r * math.cos(t * 0.015 - 1.5))
               for t in range(201)]
        d.line(arc, fill=pal["ink"], width=20, joint="curve")
        d.line(arc, fill=pal["accent"], width=12, joint="curve")
    mids = [(rr[k] + rr[k + 1]) / 2 for k in range(len(rr) - 1)] + [r_in - 90]
    sw, sh = _fit(img, asset("spider", 1), hx, hy - mids[0], SP_SPIDER, SP_SPIDER)
    for r in mids[1:]:                           # 落脚点：全在辐条上，而且都在两圈粘丝正当中
        disc(d, hx, hy - r, 15, pal["soft"], pal, w=5)
    clear = min(abs(mids[0] - rr[0]), abs(mids[0] - rr[1])) - sh / 2
    return (f"网的一小块放大：圆心在画面下方 {hy - S:.0f}px 处（画外），"
            f"{spokes} 根直辐条从那里放射出来，夹角还是整张网的 360/{n}={360 / n:.1f}°，"
            f"用 ink 画、线宽 7px（不粘）；{len(rr)} 圈绕过来的粘丝用强调色画、线宽 12px，"
            f"圈距从外往里 {gaps[0]:.0f} / {gaps[1]:.0f} / {gaps[2]:.0f}px，越往里越密。"
            f"蜘蛛（素材1，{sw}×{sh}px）整只落在正中那根辐条上、正卡在最外两圈粘丝当中，"
            f"上下离粘丝各还有 {clear:.0f}px，一点也没碰着；同一根辐条上另有 "
            f"{len(mids) - 1} 个落脚点，个个也都在两圈粘丝正当中 —— 粘丝上 0 个。"
            f"整页没有苍蝇")


# ================================================================ giraffe 长颈鹿的脖子

@page("giraffe", 2)
def _(d, pal, img):
    """光是一个脖子就有两米多长，比爸爸站着还高。"""
    base = S - MARGIN - 40
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    ppm = 300
    neck, dad, me = 2.2, 1.8, 1.2
    nh = neck * ppm
    # 脖子以前是个 120×660px 的圆角矩形胶囊。现在是素材4（长颈鹿的头和脖子），
    # 高度仍然由程序说了算（2.2 米 = 660px，一米一米量得出来），宽度随素材去。
    a = asset("giraffe", 4)
    gw = max(1, round(a.width * nh / a.height))
    gx = MARGIN + 30 + gw / 2
    place(img, a, gx, base, h=nh, anchor="bottom")
    rest = max(260.0, S - MARGIN - 40 - (gx + gw / 2))     # 两个人分剩下的地方
    x_dad, x_me = gx + gw / 2 + rest * 0.34, gx + gw / 2 + rest * 0.76
    _person(d, pal, x_dad, base, dad * ppm)
    _person(d, pal, x_me, base, me * ppm)
    for h in (nh, dad * ppm, me * ppm):
        d.line([MARGIN, base - h, S - MARGIN, base - h], fill=pal["line"], width=4)
    return (f"同一条地线上三样东西：长颈鹿的头和脖子（素材4，{gw}×{nh:.0f}px）"
            f"{neck} 米 = {nh:.0f}px 高 / 爸爸 {dad} 米 = {dad * ppm:.0f}px / "
            f"我 {me} 米 = {me * ppm:.0f}px（1 米 = {ppm}px），"
            f"脖子比我高出 {(neck - me) * ppm:.0f}px，各高度上 1 条水平参照线")


@page("giraffe", 4)
def _(d, pal, img):
    """你摸摸自己的脖子，里面有七块骨头；长颈鹿的脖子里也正好是七块。"""
    bone = lie_flat(asset("giraffe", 2))
    n, small = 7, 0.46
    boxes = panel2(d, pal)
    w_, h_ = boxes[0][2], boxes[0][3]
    pitch = h_ * 0.132
    aw, ah = bone.size
    # 右格那块能放多大，由格宽和行距共同决定；左格一律取它的 small 倍 ——
    # 这样不论素材是宽是高，7 块都不会上下压在一起，长短差别也一定在。
    # 行距从 0.128 提到 0.132、单块从 0.88 倍行距放宽到 1.02（相邻两块轻微搭边，
    # 颈椎本来就是一节压着一节），左格的比例从 0.34 提到 0.46 —— 以前只有 32px 高。
    big = min(w_ * 0.92, pitch * 1.02 * aw / ah)
    out = []
    for (cx, cy, _w, _h), target in zip(boxes, (big * small, big)):
        top = cy - pitch * (n - 1) / 2
        bw = bh = 0
        for i in range(n):
            bw, bh = place(img, bone, cx, top + i * pitch, w=target)
        out.append(f"{n} 块颈椎（每块 {bw}×{bh}px，行距 {pitch:.0f}px）")
    return ("两格等大、7 行一一对齐，两边都是 7 块：左格（我）" + out[0] +
            " / 右格（长颈鹿）" + out[1] + f"，我那块是它的 {small:.2f} 倍长")


@page("giraffe", 5)
def _(d, pal, img):
    """它的一块颈椎骨，差不多有我的一条胳膊那么长 —— 两条必须严格等长。"""
    # 胳膊以前是三个圆角矩形 + 两个关节圆拼的，现在是素材5（小孩的一条胳膊）。
    # 「等长」是这一页唯一要保证的事：两件东西宽度都取同一个 ln，
    # 谁太高就把 ln 一起收窄（两件一起收，等长不会因此被破坏）。
    bone, arm = lie_flat(asset("giraffe", 2)), lie_flat(asset("giraffe", 5))
    cap = 300
    ln = round(min(S - 2 * MARGIN - 160,
                   cap * bone.width / bone.height, cap * arm.width / arm.height))
    x0 = (S - ln) / 2
    bw, bh = place(img, bone, S / 2, 320, w=ln)
    aw, ah = place(img, arm, S / 2, 720, w=ln)
    y1, y2 = 320 + bh / 2 + 14, 720 - ah / 2 - 14          # 两端的对齐虚线只走中间那一段
    segs = max(3, int((y2 - y1) / 34))
    step = max(12.0, (y2 - y1) / segs)
    for xx in (x0, x0 + ln):
        for s_ in range(segs):
            yy = y1 + s_ * step
            d.line([xx, yy, xx, yy + step * 0.55], fill=pal["line"], width=5)
    return (f"上面 1 块横躺的颈椎骨（素材2，{bw}×{bh}px）/ 下面 1 条平伸的胳膊"
            f"（素材5，{aw}×{ah}px），两者长度严格相同、都正好 {ln}px；"
            f"两端各 1 条对齐虚线（每条 {segs} 段）")


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
