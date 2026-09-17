# -*- coding: utf-8 -*-
"""第七批示意图页（2/5）：怎么睡觉、打架、会不会游泳、最小的、羽毛、长帆、爬树、三个时代。"""
from draw_diagrams import (S, MARGIN, page, asset, place, lie_flat, poly, disc, arrow, cross,
                           lay, panel2, hbar, footprint, bands, cmp_len, cmp_height, cmp_count,
                           bars, timeline, steps, magnify)
import math, random


# ================================================================ dinosleep 恐龙怎么睡觉

@page("dinosleep", 2)
def _(d, pal, img):
    """寐龙不大，和一只鸭子差不多——两个站在同一条地线上比大小。"""
    base = S - MARGIN - 160
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    w1, h1 = place(img, asset("dinosleep", 1), S / 2 - 240, base, w=400, anchor="bottom")
    w2, h2 = place(img, asset("dinosleep", 2), S / 2 + 250, base, h=h1, anchor="bottom")
    return (f"站同一条地线：1 只蜷着的寐龙（宽 {w1}px、高 {h1}px）+ "
            f"1 只鸭子（缩到同样高 {h2}px、宽 {w2}px），差不多大")


@page("dinosleep", 3)
def _(d, pal, img):
    """睡姿的三处：腿收在身子下、尾巴绕过来、头掖进前肢——各圈一个。"""
    cx, cy = S / 2, S / 2 + 20
    w_, h_ = place(img, asset("dinosleep", 1), cx, cy, w=S - 2 * MARGIN - 180)
    x0, y0 = cx - w_ / 2, cy - h_ / 2
    spots = [(0.50, 0.82), (0.84, 0.46), (0.22, 0.44)]        # 腿 / 尾巴 / 头
    for sx, sy in spots:
        d.ellipse([x0 + w_ * (sx - 0.12), y0 + h_ * (sy - 0.16),
                   x0 + w_ * (sx + 0.12), y0 + h_ * (sy + 0.16)],
                  outline=pal["accent"], width=11)
    return (f"1 只蜷着睡的恐龙（宽 {w_}px、高 {h_}px）+ {len(spots)} 个圈："
            f"腿 1 个、尾巴 1 个、头 1 个")


@page("dinosleep", 5)
def _(d, pal):
    """头露在外面，呼出来的气就白白跑掉；头掖进去，气留在身子里。"""
    n = 4
    for i, (cx, cy, w_, h_) in enumerate(panel2(d, pal)):
        tuck = (i == 1)
        br = w_ * 0.30
        bx, by = cx, cy + h_ * 0.10
        disc(d, bx, by, br, pal["soft"], pal, w=9)                       # 身子
        hr = w_ * 0.15
        hy = by - br - hr * 0.72 if not tuck else by - br * 0.42
        disc(d, bx, hy, hr, pal["paper"], pal, w=9)                      # 头
        for j in range(n):
            a = math.radians(-150 + j * 40)
            if tuck:                                                     # 气往身子里收
                arrow(d, bx + (hr + 130) * math.cos(a), hy + (hr + 130) * math.sin(a),
                      bx + (hr + 24) * math.cos(a), hy + (hr + 24) * math.sin(a),
                      pal, w=8, head=22)
            else:                                                        # 气往外散
                arrow(d, bx + (hr + 24) * math.cos(a), hy + (hr + 24) * math.sin(a),
                      bx + (hr + 150) * math.cos(a), hy + (hr + 150) * math.sin(a),
                      pal, w=8, head=22)
    return (f"两格各 1 个身子 + 1 个头 + {n} 支气的箭头："
            f"左格头露在身子外、{n} 支箭头朝外散开；右格头掖进身子、{n} 支箭头朝里收回")


@page("dinosleep", 7)
def _(d, pal, img):
    """前后找到两只化石，睡觉的姿势一模一样。"""
    boxes = panel2(d, pal)
    got = []
    for cx, cy, w_, h_ in boxes:
        got.append(place(img, asset("dinosleep", 1), cx, cy, w=w_ * 0.82))
    return (f"左右两格等大（各 {boxes[0][2]:.0f}×{boxes[0][3]:.0f}px），各 1 只蜷着睡的恐龙，"
            f"都缩到宽 {got[0][0]}px、高 {got[0][1]}px，姿势一模一样")


@page("dinosleep", 8)
def _(d, pal, img):
    """小的能蜷成一团；大的蜷不起来，只能整个身子贴地趴着，头搁在前面。"""
    (lx, ly, lw, lh), (rx, ry, rw, rh) = panel2(d, pal)
    bl, br_ = ly + lh * 0.36, ry + rh * 0.36
    d.line([lx - lw * 0.42, bl, lx + lw * 0.42, bl], fill=pal["ink"], width=8)
    d.line([rx - rw * 0.42, br_, rx + rw * 0.42, br_], fill=pal["ink"], width=8)
    w_, h_ = place(img, asset("dinosleep", 1), lx, bl, w=lw * 0.70, anchor="bottom")
    bw, bh = rw * 0.76, rh * 0.15                                        # 又长又低的身子
    d.ellipse([rx - bw / 2, br_ - bh, rx + bw / 2, br_], fill=pal["soft"],
              outline=pal["ink"], width=9)
    poly(d, [(rx + bw / 2, br_ - bh * 0.7), (rx + bw / 2 + rw * 0.18, br_ - bh * 1.5),
             (rx + bw / 2 + rw * 0.17, br_)], pal, pal["soft"], 8)       # 尾巴
    disc(d, rx - bw / 2 - rw * 0.08, br_ - bh * 0.62, bh * 0.60, pal["paper"], pal, w=9)
    return (f"左格 1 只蜷成一团的（占地线以上 {h_}px 高、{w_}px 宽，又高又团）/ "
            f"右格 1 个整个贴在地线上的身子（长 {bw:.0f}px、只有 {bh:.0f}px 高），头搁在前面的地上")


@page("dinosleep", 10)
def _(d, pal):
    """眼睛周围那一圈小骨头：这圈骨头围出的孔大的，夜里也看得见。"""
    k = 14
    holes = []
    for i, (cx, cy, w_, h_) in enumerate(panel2(d, pal)):
        R = w_ * 0.34
        disc(d, cx, cy, R, pal["paper"], pal, w=8)
        for j in range(k):
            a = 2 * math.pi * j / k
            disc(d, cx + R * 0.80 * math.cos(a), cy + R * 0.80 * math.sin(a),
                 R * 0.15, pal["bark"], pal, w=5)
        hole = R * (0.30 if i == 0 else 0.56)
        disc(d, cx, cy, hole, pal["ink"], pal, w=0)
        holes.append(hole * 2)
    return (f"两格各 1 只眼睛，每只 {k} 块小骨头围成一圈；中间的孔左格 {holes[0]:.0f}px / "
            f"右格 {holes[1]:.0f}px（右边这只夜里看得见）")


# ================================================================ fight 打到一半被埋住了

@page("fight", 2)
def _(d, pal, img):
    """一只两条腿的伶盗龙，一只四条腿的原角龙，站在同一条地线上。"""
    base = S - MARGIN - 160
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    w1, h1 = place(img, asset("fight", 1), MARGIN + 20 + 220, base, w=440, anchor="bottom")
    w2, h2 = place(img, asset("fight", 2), S - MARGIN - 20 - 200, base, w=400, anchor="bottom")
    return (f"站同一条地线的 2 只：左边 1 只两条腿的（宽 {w1}px、高 {h1}px）/ "
            f"右边 1 只四条腿的（宽 {w2}px、高 {h2}px），中间留 "
            f"{(S - MARGIN - 20 - 200 - w2 / 2) - (MARGIN + 20 + 220 + w1 / 2):.0f}px 不相碰")


@page("fight", 3)
def _(d, pal):
    """后脚上那根大爪子：平时翘着不落地，要用的时候才扳下来。"""
    degs, gaps, L = (-70, 64), [], 0
    for i, (cx, cy, w_, h_) in enumerate(panel2(d, pal)):
        base = cy + h_ * 0.30
        d.line([cx - w_ * 0.40, base, cx + w_ * 0.40, base], fill=pal["ink"], width=8)
        kx, ky = cx - w_ * 0.14, base - h_ * 0.27                        # 脚踝
        d.line([kx, base - h_ * 0.56, kx, ky], fill=pal["ink"], width=20)  # 小腿
        d.rounded_rectangle([kx - w_ * 0.07, ky, kx + w_ * 0.34, base], radius=20,
                            fill=pal["soft"], outline=pal["ink"], width=7)  # 脚板踩地
        a = math.radians(degs[i])
        L = h_ * 0.30
        tx, ty = kx + L * math.cos(a), ky + L * math.sin(a)
        rad = h_ * 0.042
        px, py = -math.sin(a) * rad, math.cos(a) * rad
        poly(d, [(kx + px, ky + py), (tx, ty), (kx - px, ky - py)], pal, pal["accent"], 6)
        gaps.append(base - ty)
    return (f"两格各 1 条腿 + 1 根一样长的大爪子（长 {L:.0f}px）："
            f"左格爪子翘起 {abs(degs[0])}°、尖离地 {gaps[0]:.0f}px；"
            f"右格爪子扳下 {degs[1]}°、尖离地只剩 {gaps[1]:.0f}px")


@page("fight", 4)
def _(d, pal, img):
    """那根大爪子卡在原角龙脖子那块地方——圈出脖子。"""
    return magnify(img, d, pal, "fight", 2, (0.24, 0.34))


@page("fight", 6)
def _(d, pal, img):
    """一个钩着脖子，一个咬着胳膊，两处咬扣各圈一个，谁也不松开。"""
    base = S - MARGIN - 170
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    w1, h1 = place(img, asset("fight", 1), S / 2 - 230, base, w=440, anchor="bottom")
    w2, h2 = place(img, asset("fight", 2), S / 2 + 235, base, w=420, anchor="bottom")
    grips = [(S / 2 + 10, base - h2 * 0.86), (S / 2 - 10, base - h2 * 0.30)]
    for gx, gy in grips:
        d.ellipse([gx - 45, gy - 45, gx + 45, gy + 45], outline=pal["accent"], width=12)
    gap = (S / 2 + 235 - w2 / 2) - (S / 2 - 230 + w1 / 2)
    return (f"2 只面对面站在同一条地线上（宽 {w1}px / {w2}px，中间还留 {gap:.0f}px 不重叠）+ "
            f"{len(grips)} 个圈：上面 1 个圈住脖子、下面 1 个圈住胳膊")


@page("fight", 8)
def _(d, pal, img):
    """沙子一层一层盖下来，打架的样子原封不动压在最底下。"""
    n = 5
    note = bands(d, pal, n)
    h = (S - 2 * MARGIN - 80) / n
    floor = MARGIN + 40 + n * h - h * 0.12
    place(img, asset("fight", 1), S / 2 - 150, floor, w=250, anchor="bottom")
    place(img, asset("fight", 2), S / 2 + 150, floor, w=240, anchor="bottom")
    return note + f"；最下面那层里 2 只打架的恐龙（宽 250px / 240px），头上压着 {n - 1} 层沙"


@page("fight", 10)
def _(d, pal, img):
    """伶盗龙其实不大，只有火鸡那么高——两只缩到一样高，站同一条地线。"""
    base = S - MARGIN - 160
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    w1, h1 = place(img, asset("fight", 1), MARGIN + 20 + 230, base, w=460, anchor="bottom")
    w2, h2 = place(img, asset("fight", 3), S - MARGIN - 190, base, h=h1, anchor="bottom")
    return (f"站同一条地线：1 只伶盗龙（宽 {w1}px、高 {h1}px）+ 1 只火鸡"
            f"（缩到同样高 {h2}px、宽 {w2}px），站直了一样高")


# ================================================================ dinoswim 恐龙会游泳吗

@page("dinoswim", 2)
def _(d, pal, img):
    """整只脚踩出来的脚印又深又宽；划痕只有爪尖那么窄。"""
    (lx, ly, lw, lh), (rx, ry, rw, rh) = panel2(d, pal)
    w1, h1 = place(img, asset("dinoswim", 2), lx, ly, w=lw * 0.80)
    w2, h2 = place(img, asset("dinoswim", 3), rx, ry, w=rw * 0.36)
    return (f"两格等大（各 {lw:.0f}×{lh:.0f}px）：左格 1 个整脚踩的脚印（宽 {w1}px）/ "
            f"右格 1 组爪尖划痕（宽 {w2}px，只有脚印的 {w2 / max(w1, 1) * 100:.0f}%）")


@page("dinoswim", 4)
def _(d, pal):
    """河底的划痕：每一组三条，又细又直，一组接着一组排成长长的一串。"""
    g, k = 6, 3
    xs, slot = lay(g)
    intra = slot * 0.17
    for x in xs:
        for j in range(k):
            dx = (j - 1) * intra
            d.line([x + dx, S / 2 - 160, x + dx + 26, S / 2 + 160], fill=pal["ink"], width=12)
    return (f"{g} 组划痕排成一串，每组 {k} 条平行的细线，一共 {g * k} 道；"
            f"组内间距 {intra:.0f}px、组与组之间 {slot:.0f}px")


@page("dinoswim", 6)
def _(d, pal, img):
    """水比它的腿还深，一直没到肚子，脚只能用爪尖点着走。"""
    base = S - MARGIN - 90
    w_, h_ = place(img, asset("dinoswim", 1), S / 2, base, w=700, anchor="bottom")
    belly, hip = base - h_ * 0.52, base - h_ * 0.40
    d.line([MARGIN, belly, S - MARGIN, belly], fill=pal["line"], width=10)
    for i in range(4):
        y = belly + 46 + i * 46
        for j in range(5):
            x = MARGIN + 40 + j * 190 + (i % 2) * 70
            d.line([x, y, x + 100, y], fill=pal["line"], width=6)
    for seg in range(4):
        x = MARGIN + 20 + seg * 70
        d.line([x, hip, x + 34, hip], fill=pal["ink"], width=5)
    arrow(d, MARGIN + 70, belly, MARGIN + 70, base, pal, w=8, head=22)
    return (f"1 只恐龙（高 {h_}px）站在地线上：水面画在它高度的 52% 处（没到肚子），"
            f"水深 {h_ * 0.52:.0f}px，比腿（{h_ * 0.40:.0f}px）还深 {h_ * 0.12:.0f}px")


@page("dinoswim", 8)
def _(d, pal):
    """岸上一步就是一步；水里蹬一下滑出去好远，两组划痕隔得很开。"""
    (lx, ly, lw, lh), (rx, ry, rw, rh) = panel2(d, pal)
    n, m = 5, 3
    gl = lh * 0.14
    for i in range(n):
        footprint(d, lx, ly - lh * 0.30 + i * gl, 74, pal)
    gr = rh * 0.30
    for i in range(m):
        y = ry - rh * 0.32 + i * gr
        for j in range(3):
            d.line([rx - 62 + j * 46, y, rx - 42 + j * 46, y + 72], fill=pal["ink"], width=11)
    return (f"左格 {n} 个脚印，中心间距 {gl:.0f}px / 右格 {m} 组划痕（每组 3 条），"
            f"中心间距 {gr:.0f}px，是左格的 {gr / gl:.1f} 倍")


@page("dinoswim", 11)
def _(d, pal):
    """泥后来干了，上面一层一层压上去，最底下那几道爪印留到今天。"""
    n, k = 5, 3
    note = bands(d, pal, n, mark=n - 1)
    h = (S - 2 * MARGIN - 80) / n
    y = MARGIN + 40 + (n - 0.5) * h
    for j in range(k):
        d.line([S / 2 - 130 + j * 118, y - 32, S / 2 - 88 + j * 118, y + 32],
               fill=pal["ink"], width=14)
    return note + f"；最下面那层里 {k} 道爪印，上面压着 {n - 1} 层"


# ================================================================ tiny 最小的恐龙有多小

@page("tiny", 2)
def _(d, pal, img):
    """它跟一只鸽子差不多——两个并排站在同一条地线上。"""
    base = S - MARGIN - 170
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    w1, h1 = place(img, asset("tiny", 1), MARGIN + 20 + 215, base, w=430, anchor="bottom")
    w2, h2 = place(img, asset("tiny", 2), S - MARGIN - 210, base, h=h1, anchor="bottom")
    return (f"站同一条地线：1 只小恐龙（宽 {w1}px、高 {h1}px）+ 1 只鸽子"
            f"（缩到同样高 {h2}px、宽 {w2}px），一样高、鸽子胖一圈")


@page("tiny", 3)
def _(d, pal, img):
    """放在秤上：鸡蛋那头沉下去，恐龙那头翘起来。"""
    cx, cy = S / 2, S / 2 + 60
    deg, arm = 12, 330
    t = math.radians(deg)
    lx, ly = cx - arm * math.cos(t), cy - arm * math.sin(t)
    rx, ry = cx + arm * math.cos(t), cy + arm * math.sin(t)
    poly(d, [(cx - 74, cy + 250), (cx + 74, cy + 250), (cx, cy)], pal, pal["bark"], 8)
    d.line([lx, ly, rx, ry], fill=pal["ink"], width=18)
    for px, py in ((lx, ly), (rx, ry)):
        d.line([px, py, px, py + 58], fill=pal["ink"], width=8)
        d.rounded_rectangle([px - 96, py + 58, px + 96, py + 90], radius=14,
                            fill=pal["soft"], outline=pal["ink"], width=7)
    dw, dh = place(img, asset("tiny", 1), lx, ly + 58, w=240, anchor="bottom")
    ew, eh = place(img, asset("tiny", 3), rx, ry + 58, h=150, anchor="bottom")
    return (f"1 副天平，横梁向鸡蛋那头倾斜 {deg}°、两盘差 {2 * arm * math.sin(t):.0f}px："
            f"左盘 1 只恐龙（高 {dh}px）翘起来 / 右盘 1 个鸡蛋（高 {eh}px）沉下去")


@page("tiny", 5)
def _(d, pal, img):
    """脑袋比核桃大不了多少；嘴里的牙细得像针尖，一根一根排得很密。"""
    base = S / 2 - 40
    w_, h_ = place(img, asset("tiny", 1), 280, base, h=300, anchor="bottom")
    hx, hy = 280 - w_ / 2 + w_ * 0.13, base - h_ + h_ * 0.13
    r = h_ * 0.13
    d.ellipse([hx - r, hy - r, hx + r, hy + r], outline=pal["accent"], width=10)
    nw, nh = place(img, asset("tiny", 4), 762, hy, h=2 * r)
    for y in (hy - r, hy + r):
        for seg in range(4):
            x = 530 + seg * 90
            d.line([x, y, x + 45, y], fill=pal["line"], width=5)
    k = 18
    gy, span = S - MARGIN - 190, 600
    step = span / (k - 1)
    d.line([S / 2 - span / 2, gy, S / 2 + span / 2, gy], fill=pal["ink"], width=12)
    for i in range(k):
        x = S / 2 - span / 2 + i * step
        poly(d, [(x - 7, gy), (x + 7, gy), (x, gy + 95)], pal, pal["paper"], 4)
    return (f"1 个圈住脑袋的圈（直径 {2 * r:.0f}px）+ 旁边 1 个核桃（高 {nh}px），"
            f"上下两条虚线说明一样大；下面 1 条牙床上 {k} 颗针尖牙，间距 {step:.0f}px")


@page("tiny", 7)
def _(d, pal):
    """最大的三十米，它连半米都不到——同样长的一条切成六十二格，它只占一格。"""
    k = 62
    x0, full = MARGIN + 50, S - 2 * MARGIN - 100
    hbar(d, x0, S / 2 - 150, full, 110, pal, pal["accent"])
    cell, y = full / k, S / 2 + 150
    for i in range(k):
        d.rectangle([x0 + i * cell, y - 56, x0 + (i + 1) * cell, y + 56],
                    fill=pal["accent"] if i == 0 else pal["paper"], outline=pal["ink"], width=2)
    for x in (x0, x0 + full):
        d.line([x, S / 2 - 260, x, S / 2 + 260], fill=pal["ink"], width=8)
    return (f"上条 1 根（最大的恐龙）长 {full}px；下面同样长的一条切成 {k} 格，"
            f"每格 {cell:.1f}px，只有第 1 格填了强调色（这一只），两端有对齐线")


@page("tiny", 10)
def _(d, pal, img):
    """一窝蛋挨着围成一圈，刚好放满一只手心。"""
    k, R = 7, 250
    cx, cy = S / 2, S / 2 + 20
    disc(d, cx, cy, R + 110, pal["soft"], pal, w=12)
    eh = 0
    for i in range(k):
        a = 2 * math.pi * i / k - math.pi / 2
        _w, eh = place(img, asset("tiny", 3), cx + R * math.cos(a), cy + R * math.sin(a), h=185)
    return (f"1 只手心（圆，直径 {2 * (R + 110)}px）里 {k} 个蛋围成一圈，圈半径 {R}px，"
            f"每个蛋高 {eh}px、相邻中心间距 {2 * R * math.sin(math.pi / k):.0f}px")


# ================================================================ feather 长羽毛的恐龙

@page("feather", 2)
def _(d, pal, img):
    """最早的羽毛不是一片，是一根丝。"""
    (lx, ly, lw, lh), (rx, ry, rw, rh) = panel2(d, pal)
    w1, h1 = place(img, lie_flat(asset("feather", 3)), lx, ly, w=lw * 0.86)
    cross(d, lx, ly, min(lw, lh) * 0.30, pal, w=16)
    w2, h2 = place(img, asset("feather", 1), rx, ry, h=rh * 0.72)
    return (f"两格等大：左格 1 片摆平的羽毛（长 {w1}px）上打 1 个大叉（不是这样）/ "
            f"右格 1 根细丝（高 {h2}px）")


@page("feather", 4)
def _(d, pal):
    """一根丝从根上分了叉，一根变成好几根，聚成一小簇。"""
    k, L, deg = 6, 420, 13
    base = S / 2 + 300
    d.line([S / 2 - 250, base, S / 2 - 250, base - L], fill=pal["ink"], width=14)
    for i in range(k):
        a = math.radians(-90 + (i - (k - 1) / 2) * deg)
        d.line([S / 2 + 250, base, S / 2 + 250 + L * math.cos(a), base + L * math.sin(a)],
               fill=pal["ink"], width=12)
    arrow(d, S / 2 - 110, base - L / 2, S / 2 + 110, base - L / 2, pal, w=10, head=28)
    return (f"左边 1 根直丝（长 {L}px）/ 右边 1 簇 {k} 根从同一个根部分出来"
            f"（每根都是 {L}px，相邻夹角 {deg}°）+ 中间 1 支箭头")


@page("feather", 5)
def _(d, pal, img):
    """一根丝 → 一小簇 → 中间长出梗、两边排开细丝的一整片。"""
    return steps(img, d, pal, "feather", [1, 2, 3])


@page("feather", 7)
def _(d, pal):
    """胳膊上的羽毛一排排开，越靠外越长，合起来像一把扇子。"""
    k = 10
    hx, hy = MARGIN + 182, S - MARGIN - 120
    a0, a1, L0, dL = -105, -20, 280, 40
    for i in range(k):
        a = math.radians(a0 + (a1 - a0) * i / (k - 1))
        L = L0 + i * dL
        ex, ey = hx + L * math.cos(a), hy + L * math.sin(a)
        mx, my = hx + L * 0.45 * math.cos(a), hy + L * 0.45 * math.sin(a)
        nx, ny = -math.sin(a) * 26, math.cos(a) * 26
        poly(d, [(hx, hy), (mx + nx, my + ny), (ex, ey), (mx - nx, my - ny)],
             pal, pal["soft"], 5)
        d.line([hx, hy, ex, ey], fill=pal["ink"], width=5)
    return (f"1 把扇子：{k} 根羽毛从同一个根排开，角度从 {a0}° 到 {a1}°"
            f"（每根差 {(a1 - a0) / (k - 1):.1f}°），长度从 {L0}px 一根比一根长到 "
            f"{L0 + (k - 1) * dL}px，越靠外越长")


@page("feather", 10)
def _(d, pal, img):
    """恐龙的羽毛和今天鸟的羽毛并在一起，几乎分不出来。"""
    a = lie_flat(asset("feather", 3))
    aw, ah = a.size
    ln = min(S - 2.0 * MARGIN - 150, 250.0 * aw / ah)   # 厚度封在 250px 内，两根不会压到
    x0 = (S - ln) / 2
    w1, h1 = place(img, a, x0 + ln / 2, S / 2 - 170, w=ln)
    w2, h2 = place(img, a, x0 + ln / 2, S / 2 + 170, w=ln)
    for x in (x0, x0 + ln):
        for seg in range(11):
            y = S / 2 - 330 + seg * 46
            d.line([x, y, x, y + 24], fill=pal["line"], width=5)
    return (f"上下 2 根摆平的羽毛，都缩到长 {w1}px / {w2}px（厚 {h1}px / {h2}px），"
            f"两端各 1 条对齐虚线，长短一模一样")


# ================================================================ sail 背上长帆的恐龙

@page("sail", 2)
def _(d, pal, img):
    """帆顶比一扇门还高——门和棘龙站在同一条地线上。"""
    base = S - MARGIN - 120
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    dw, dh = place(img, asset("sail", 1), MARGIN + 370, base, w=660, anchor="bottom")
    ww, wh = place(img, asset("sail", 3), S - MARGIN - 110, base, h=dh * 0.78, anchor="bottom")
    for seg in range(7):
        x = MARGIN + 40 + seg * 130
        d.line([x, base - wh, x + 60, base - wh], fill=pal["line"], width=6)
    return (f"1 只棘龙（宽 {dw}px、高 {dh}px）+ 1 扇门（高 {wh}px，只有它的 78%），"
            f"站同一条地线；门顶那条虚线离帆顶还差 {dh - wh}px")


@page("sail", 3)
def _(d, pal, img):
    """帆是骨头撑起来的：每一节脊椎骨往上长出一根长棒，一根挨着一根。"""
    k = 11
    spine = S - MARGIN - 210
    xs, slot = lay(k)
    a = asset("sail", 2)
    aw, ah = a.size
    hmax = min(520.0, slot * 0.78 * ah / aw)        # 最高的一根也不许比槽宽
    hs = []
    for i, x in enumerate(xs):
        t = 1 - abs(i - (k - 1) / 2) / ((k - 1) / 2)
        _w, h_ = place(img, a, x, spine, h=hmax * (0.40 + 0.60 * t), anchor="bottom")
        hs.append(h_)
    d.line([MARGIN + 30, spine, S - MARGIN - 30, spine], fill=pal["ink"], width=16)
    return (f"1 条脊椎线上 {k} 根长棒，一根挨着一根，中心间距 {slot:.0f}px；"
            f"中间最长 {max(hs)}px、两端最短 {min(hs)}px")


@page("sail", 4)
def _(d, pal, img):
    """别的恐龙那根棒只有短短一截，棘龙的这一根长得吓人。"""
    return cmp_height(img, d, pal, "sail", [(2, 120, S / 2 - 230), (2, 620, S / 2 + 230)])


@page("sail", 7)
def _(d, pal):
    """血一涌上帆，帆就变红；远远看过去，那个身子好像又大了一圈。"""
    sw = sh = 0
    for i, (cx, cy, w_, h_) in enumerate(panel2(d, pal)):
        hw, hh = w_ * 0.36, h_ * 0.30
        sw, sh = hw * 2, hh * 2
        sail = [(cx - hw, cy + hh), (cx - hw * 0.55, cy - hh),
                (cx + hw * 0.55, cy - hh), (cx + hw, cy + hh)]
        if i == 1:
            poly(d, [(cx + (x - cx) * 1.15, cy + (y - cy) * 1.15) for x, y in sail],
                 pal, pal["paper"], 6)
        poly(d, sail, pal, pal["accent"] if i else pal["soft"], 8)
        for j in range(5):
            x = cx - hw * 0.60 + j * hw * 0.30
            d.line([x, cy + hh, x, cy - hh * 0.80], fill=pal["ink"], width=5)
    return (f"两格各 1 面一样大的帆（宽 {sw:.0f}px、高 {sh:.0f}px）、各 5 根撑棒："
            f"左格填浅色 / 右格填强调色，外面还多一圈放大 15% 的轮廓")


@page("sail", 10)
def _(d, pal, img):
    """从鼻子到尾巴尖十五米，两辆小汽车接起来还不够。"""
    span, n = 860, 2
    x0 = (S - span) / 2
    w_, h_ = place(img, asset("sail", 1), S / 2, 360, w=span)
    car = span * 0.425                      # 两辆合起来只有它的 85%
    for i in range(n):
        cx, cy = x0 + car * (i + 0.5), 830
        h = car * 0.24
        d.rounded_rectangle([cx - car / 2 + 8, cy - h * 0.5, cx + car / 2 - 8, cy + h * 0.7],
                            radius=car * 0.06, fill=pal["paper"], outline=pal["ink"], width=7)
        poly(d, [(cx - car * 0.20, cy - h * 0.5), (cx - car * 0.09, cy - h * 1.25),
                 (cx + car * 0.13, cy - h * 1.25), (cx + car * 0.22, cy - h * 0.5)],
             pal, pal["soft"], 7)
        for dx in (-car * 0.27, car * 0.27):
            disc(d, cx + dx, cy + h * 0.7, car * 0.075, pal["bark"], pal, w=6)
    for x in (x0, x0 + span):
        for seg in range(6):
            y = 620 + seg * 18
            d.line([x, y, x, y + 9], fill=pal["line"], width=5)
    return (f"上面 1 只棘龙体长 {w_}px；下面 {n} 辆小汽车首尾相接合计 {n * car:.0f}px"
            f"（只有它的 {n * car / span * 100:.0f}%，还差 {span - n * car:.0f}px），两端有对齐线")


# ================================================================ climb 会爬树的恐龙

@page("climb", 2)
def _(d, pal, img):
    """从头到尾巴尖只有乌鸦那么长——上下两行严格等长。"""
    return cmp_len(img, d, pal, "climb", 1, 2, n_b=1, span=500, ay=310, by=740)


@page("climb", 4)
def _(d, pal, img):
    """四条腿上都长着长羽毛：前面两片，后面还有两片——圈出四处。"""
    cx, cy = S / 2, S / 2 + 20
    w_, h_ = place(img, asset("climb", 1), cx, cy, w=S - 2 * MARGIN - 120)
    x0, y0 = cx - w_ / 2, cy - h_ / 2
    spots = [(0.26, 0.46), (0.44, 0.76), (0.62, 0.46), (0.80, 0.76)]
    for sx, sy in spots:
        d.ellipse([x0 + w_ * (sx - 0.08), y0 + h_ * (sy - 0.13),
                   x0 + w_ * (sx + 0.08), y0 + h_ * (sy + 0.13)],
                  outline=pal["accent"], width=11)
    return (f"1 只小盗龙（宽 {w_}px、高 {h_}px）+ {len(spots)} 个圈："
            f"前面 2 个、后面 2 个，四个圈互不相碰")


@page("climb", 6)
def _(d, pal):
    """爬树的爪子弯得厉害，地上跑的直一些，小盗龙的很弯。"""
    degs = (125, 45, 118)
    xs, slot = lay(3)
    R = 150
    for x, deg in zip(xs, degs):
        sx, sy = x - slot * 0.22, S / 2 - 130
        ccx, ccy = sx, sy + R
        pts = [(ccx + R * math.sin(math.radians(t)), ccy - R * math.cos(math.radians(t)))
               for t in range(0, deg + 1, 4)]
        for i in range(len(pts) - 1):
            d.line([pts[i], pts[i + 1]], fill=pal["ink"],
                   width=max(5, int(26 - 20 * i / (len(pts) - 1))))
        disc(d, sx, sy, 22, pal["soft"], pal, w=7)
    return (f"3 只爪子并排（半径都是 {R}px），弯过的角度分别是 "
            f"{degs[0]}° / {degs[1]}° / {degs[2]}°：爬树的最弯，地上跑的最直，"
            f"小盗龙的和爬树的差不多弯")


@page("climb", 8)
def _(d, pal, img):
    """从十米高的树上跳，飘出去二三十米；树再高一点，就飘得更远。"""
    k = 21.6                                     # 每米多少像素
    base = S - MARGIN - 70
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    trunk = asset("climb", 3)
    tops, hs = [], []
    for m, x, far in ((15, MARGIN + 60, 37), (10, MARGIN + 155, 25)):
        _w, h_ = place(img, trunk, x, base, h=m * k, anchor="bottom")
        hs.append(h_)
        tops.append((x, base - h_, far))
    for x, y, far in tops:
        x1 = MARGIN + far * k
        for s in range(0, 22, 2):
            t0, t1 = s / 22.0, (s + 1) / 22.0
            d.line([x + (x1 - x) * t0, y + (base - y) * (t0 ** 1.7),
                    x + (x1 - x) * t1, y + (base - y) * (t1 ** 1.7)],
                   fill=pal["line"], width=7)
    return (f"地线上 2 棵树（比例尺 {k} px/米）：15 米高 {hs[0]}px / 10 米高 {hs[1]}px；"
            f"2 条滑行虚线分别落在 37 米（{37 * k:.0f}px）和 25 米（{25 * k:.0f}px）处，"
            f"树高的那条飘得远")


@page("climb", 11)
def _(d, pal, img):
    """地上跑的个个又大又凶，它搬到别人上不去的高处。"""
    base = S - MARGIN - 60
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    tw, th = place(img, asset("climb", 3), MARGIN + 150, base, h=760, anchor="bottom")
    dw, dh = place(img, asset("climb", 1), MARGIN + 150 + tw / 2 + 120, base - th * 0.80, w=220)
    n, s = 3, 170
    for i in range(n):
        footprint(d, S / 2 + 90 + i * 150, base - 80, s, pal)
    return (f"1 棵树（高 {th}px），小盗龙（宽 {dw}px、高 {dh}px）停在树高的 80% 处；"
            f"地面上 {n} 个大脚印（各 {s}px、高 {s * 1.05:.0f}px，中心间距 150px），"
            f"一个脚印就比它整只还大")


# ================================================================ eras 恐龙住了一亿六千万年

@page("eras", 2)
def _(d, pal, img):
    """一亿六千万年分成三段：三叠纪、侏罗纪、白垩纪，一段比一段长。"""
    segs = [51, 56, 79]
    tot = float(sum(segs))
    cuts, acc = [0.0], 0.0
    for s in segs:
        acc += s / tot
        cuts.append(acc)
    y = S / 2 + 80
    note = timeline(img, d, pal, "eras", [(c, None, f"第 {i + 1} 道刻度")
                                          for i, c in enumerate(cuts)], y=y)
    x0, x1 = MARGIN + 50, S - MARGIN - 50
    fills = (pal["soft"], pal["bark"], pal["accent"])
    for i in range(len(segs)):
        d.rounded_rectangle([x0 + (x1 - x0) * cuts[i] + 6, y + 60,
                             x0 + (x1 - x0) * cuts[i + 1] - 6, y + 150],
                            radius=16, fill=fills[i], outline=pal["ink"], width=6)
    return note + ("；线下 3 条色块：长度依次 " +
                   " / ".join(f"{(x1 - x0) * (cuts[i + 1] - cuts[i]):.0f}px" for i in range(3)) +
                   f"（{segs[0]} / {segs[1]} / {segs[2]}），一段比一段长")


@page("eras", 4)
def _(d, pal):
    """那时候地上别的爬行动物又大又多，恐龙只是小小一群。"""
    big, small, bs, ss = 0, 4, 105, 52
    for r in range(3):
        for c in range(5 if r < 2 else 4):
            footprint(d, MARGIN + 110 + c * 190, MARGIN + 130 + r * 190, bs, pal, pal["bark"])
            big += 1
    for i in range(small):
        footprint(d, S / 2 + 150 + (i % 2) * 90, S - MARGIN - 190 + (i // 2) * 90,
                  ss, pal, pal["accent"])
    return (f"{big} 个大脚印（各 {bs}px，5+5+4 三行铺开）+ {small} 个小脚印挤在一角"
            f"（各 {ss}px）：大的又大又多，小的又小又少")


@page("eras", 6)
def _(d, pal, img):
    """最早的那种小恐龙站在它脚边，只到它的膝盖。"""
    frac = 0.26
    base = S - MARGIN - 110
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    bw, bh = place(img, asset("eras", 2), S / 2 + 130, base, w=620, anchor="bottom")
    knee = base - bh * frac
    sw, sh = place(img, asset("eras", 1), MARGIN + 110, base, h=bh * frac, anchor="bottom")
    for seg in range(5):
        x = MARGIN + 30 + seg * 60
        d.line([x, knee, x + 30, knee], fill=pal["line"], width=6)
    return (f"1 只蜥脚类（宽 {bw}px、高 {bh}px）+ 1 只早期小恐龙（高 {sh}px，"
            f"正好是它的 {frac * 100:.0f}%），站同一条地线，膝盖那条虚线落在小恐龙头顶")


@page("eras", 8)
def _(d, pal, img):
    """剑龙先走，八千万年以后霸王龙才出来，两个没见过面。"""
    t0, t1 = 0.15, 0.85
    note = timeline(img, d, pal, "eras", [(t0, 4, "剑龙"), (t1, 3, "霸王龙")])
    return note + (f"；两个刻度隔着整条线的 {(t1 - t0) * 100:.0f}%（八千万年），"
                   f"两只素材各 250px 宽、中间不相碰")


@page("eras", 9)
def _(d, pal, img):
    """剑龙到霸王龙隔八千万年，霸王龙到我们只隔六千六百万年，后一段更短。"""
    a, b = 80.0, 66.0
    t0, t2 = 0.15, 0.90
    t1 = t0 + (t2 - t0) * a / (a + b)
    note = timeline(img, d, pal, "eras",
                    [(t0, 4, "剑龙"), (t1, 3, "霸王龙"), (t2, None, "我们")])
    return note + (f"；左段 {(t1 - t0) * 100:.0f}%（八千万年）比右段 {(t2 - t1) * 100:.0f}%"
                   f"（六千六百万年）长，霸王龙这一刻度离右端更近")


@page("eras", 10)
def _(d, pal, img):
    """三个时代各挑一只，按同一个比例尺排在一条地线上。"""
    k, gap = 21.0, 50
    items = [(1, 2.0), (2, 25.0), (3, 12.0)]
    base = S - MARGIN - 90
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    total = sum(m * k for _a, m in items) + gap * (len(items) - 1)
    x = (S - total) / 2
    out = []
    for a, m in items:
        w_, h_ = place(img, asset("eras", a), x + m * k / 2, base, w=m * k, anchor="bottom")
        out.append(f"素材{a}（{m:.0f} 米）→ 宽 {w_}px、高 {h_}px")
        if a == 1:                                  # 最小的那只太小，圈出来才找得着
            ex, ey, er = x + m * k / 2, base - 55, 58
            d.ellipse([ex - er, ey - er, ex + er, ey + er], outline=pal["accent"], width=10)
        x += m * k + gap
    return (f"同一个比例尺 {k:.0f} px/米，{len(items)} 只按体长排在一条地线上、"
            f"间距 {gap}px 互不相碰：" + " / ".join(out) +
            f"，一行总宽 {total:.0f}px，最小的那只外面加了 1 个直径 116px 的圈")
