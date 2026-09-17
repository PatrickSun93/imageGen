# -*- coding: utf-8 -*-
"""第七批示意图页（2/5）：怎么睡觉、打架、会不会游泳、最小的、羽毛、长帆、爬树、三个时代。"""
from draw_diagrams import (S, MARGIN, page, asset, place, lie_flat, halo, disc, arrow, cross,
                           lay, panel2, hbar, bands, cmp_len, cmp_height, timeline, steps,
                           magnify)
from PIL import Image, ImageColor
import math, random


# ---------------------------------------------------------------- 本页文件的三个小助手
# 素材的长宽比要等 GPU 跑完才知道。写死 w=250 这类数字，扁的东西就只剩一百多像素高
# （eras 8/9 栽在这上面），细长的东西又会冲出画面。所以这一批全部改成「塞进一个框」。

def _box(a, bw, bh):
    """按长宽比把素材塞进 bw×bh 的框，返回交给 place 的那一个关键字（w= 或 h=）。"""
    return dict(w=bw) if a.width / a.height >= bw / bh else dict(h=bh)


def _rgb(c):
    """调色板里是 '#rrggbb' 字符串，halo/silhouette 要的是三元组。"""
    return ImageColor.getrgb(c)


def _upright(a, deg):
    """把斜着画的素材扶正：逆时针转 deg°，再裁回外框。

    lie_flat 只管「最扁」，管不了哪头朝上——爪子、羽毛这种有根有尖的东西，
    得按它自己画的倾角扶正，根才会落在外框底边中点上，_turn 才转得对。
    """
    r = a.rotate(deg, expand=True, resample=Image.BICUBIC)
    bb = r.getchannel("A").getbbox()
    return r.crop(bb) if bb else r


def _turn(img, a, x, y, deg, h=None, w=None):
    """素材缩放后绕**自己底边中点**转 deg°（正数向右倒），根部落在 (x, y)。

    扇形排开的羽毛、翘起／扳下的镰刀爪，以前都是拿多边形现拼的——菱形不是羽毛，
    三角形不是爪子。用真素材就得能绕根部转：PIL 的 rotate 绕的是图心，这里把
    底边中点转过去的偏移算回来，所以根部永远咬在 (x, y) 上，角度仍由参数保证。

    返回转**之前**的 (宽, 高)：构造清单要的是「这根多长」，不是转完外框多大。
    """
    aw, ah = a.size
    s = (h / ah) if h else ((w / aw) if w else 1.0)
    nw, nh = max(1, round(aw * s)), max(1, round(ah * s))
    r = a.resize((nw, nh), Image.LANCZOS).rotate(-deg, expand=True, resample=Image.BICUBIC)
    t = math.radians(-deg)
    ox, oy = nh / 2 * math.sin(t), nh / 2 * math.cos(t)
    img.paste(r, (round(x - ox - r.width / 2), round(y - oy - r.height / 2)), r)
    return nw, nh


def _tl(img, d, pal, book, marks, y=None, bw=400, bh=320):
    """本地时间线。draw_diagrams.timeline 把素材写死成 w=250，扁身的恐龙只剩 150px 高；
    这里改成塞进 bw×bh 的框，刻度位置和个数仍由 marks 保证。"""
    y = y if y is not None else S / 2 + 110
    x0, x1 = MARGIN + 50, S - MARGIN - 50
    d.line([x0, y, x1, y], fill=pal["ink"], width=12)
    out = []
    for t, a, lab in marks:
        mx = x0 + (x1 - x0) * t
        d.line([mx, y - 26, mx, y + 26], fill=pal["ink"], width=10)
        if a:
            im = asset(book, a)
            w_, h_ = place(img, im, mx, y - 40, anchor="bottom", **_box(im, bw, bh))
            out.append(f"{lab}（素材{a}）在 {t * 100:.0f}%、{w_}×{h_}px")
        else:
            out.append(f"{lab} 在 {t * 100:.0f}%")
    return f"1 条时间线，{len(marks)} 个刻度：" + " / ".join(out)


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
    bl, br_ = ly + lh * 0.34, ry + rh * 0.34
    d.line([lx - lw * 0.42, bl, lx + lw * 0.42, bl], fill=pal["ink"], width=8)
    d.line([rx - rw * 0.42, br_, rx + rw * 0.42, br_], fill=pal["ink"], width=8)
    a1, a4 = asset("dinosleep", 1), asset("dinosleep", 4)
    w1, h1 = place(img, a1, lx, bl, anchor="bottom", **_box(a1, lw * 0.88, lh * 0.60))
    w2, h2 = place(img, a4, rx, br_, anchor="bottom", **_box(a4, rw * 0.96, rh * 0.60))
    return (f"左右两格等大（各 {lw:.0f}×{lh:.0f}px）、地线一样高：左格 1 只蜷成一团的"
            f"（素材1，{w1}×{h1}px，高是宽的 {h1 / w1:.2f} 倍）/ 右格 1 只整个贴地趴着的"
            f"大恐龙（素材4，{w2}×{h2}px，高是宽的 {h2 / w2:.2f} 倍，肚子压在地线上、"
            f"头搁在前面）——"
            f"{'趴着' if h2 / w2 < h1 / w1 else '蜷着'}的那只更扁")


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
def _(d, pal, img):
    """后脚上那根大爪子：平时翘着不落地，要用的时候才扳下来。"""
    degs, gaps, L = (20, 154), [], 0            # 离竖直方向的角度：尖朝上翘 / 尖朝下扳
    f0 = asset("fight", 5)
    # 素材上沿把身子和尾巴齐齐切掉，抠出来是一块硬邦邦的方角——切掉上面三成，
    # 只留小腿和脚板，这一页要的本来也就是脚
    foot = f0.crop((0, int(f0.height * 0.30), f0.width, f0.height))
    claw = _upright(asset("fight", 4), 45)      # 素材是斜着画的，先扶正成根在下、尖朝上
    # 脚是横宽的，配 844px 高的标准格子上面空一大片；格子压矮一点，脚才填得满
    for i, (cx, cy, w_, h_) in enumerate(panel2(d, pal, top=330)):
        base = cy + h_ * 0.30
        d.line([cx - w_ * 0.40, base, cx + w_ * 0.40, base], fill=pal["ink"], width=8)
        fx = cx + w_ * 0.04
        fw, fh = place(img, foot, fx, base, anchor="bottom", **_box(foot, w_ * 0.94, h_ * 0.66))
        kx, ky = fx - fw * 0.20, base - fh * 0.56                        # 内趾的根，咬在脚踝前面
        L = fh * 0.55                                                    # 扳下来正好够着地，不穿过地线
        _turn(img, claw, kx, ky, degs[i], h=L)                           # 整根爪子按角度转
        gaps.append(base - (ky - L * math.cos(math.radians(degs[i]))))   # 爪尖离地
    return (f"两格各 1 只后脚（素材5，{fw}×{fh}px）+ 1 根一样长的大爪子"
            f"（素材4，长 {L:.0f}px，根部咬在脚踝上）："
            f"左格爪子离竖直方向 {degs[0]}°（尖朝上翘着）、尖离地 {gaps[0]:.0f}px；"
            f"右格 {degs[1]}°（尖朝下扳着）、尖离地只剩 {gaps[1]:.0f}px")


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
    n = 4                                   # 5 层时每层只有 177px 高，恐龙缩到 160px——层数少一层，恐龙就装得下
    h = (S - 2 * MARGIN) / n
    note = bands(d, pal, n, top=MARGIN, h=h)
    floor = MARGIN + n * h - h * 0.10
    got = []
    for a_, x in ((1, S / 2 - 235), (2, S / 2 + 235)):
        a = asset("fight", a_)
        got.append(place(img, a, x, floor, anchor="bottom", **_box(a, 440, h * 0.84)))
    return (note + f"；最下面那层（高 {h:.0f}px）里 2 只打架的恐龙（素材1 {got[0][0]}×{got[0][1]}px / "
            f"素材2 {got[1][0]}×{got[1][1]}px，各封顶 440px 宽、中心相距 470px，不重叠），"
            f"头上压着 {n - 1} 层沙")


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
def _(d, pal, img):
    """河底的划痕：每一组三条，又细又直，一组接着一组排成长长的一串。"""
    g, k = 6, 3
    xs, slot = lay(g)
    a = asset("dinoswim", 3)                       # 素材本身就是三道平行的沟
    y0, dy = 760, 96                               # 斜着排成一串，比横平的一条更像趟过去的痕
    w_ = h_ = 0
    for i, x in enumerate(xs):
        w_, h_ = place(img, a, x, y0 - i * dy, **_box(a, slot * 0.92, S * 0.5))
    return (f"{g} 组划痕（素材3，每组就是三道平行的沟）斜着排成一串，一共 {g * k} 道；"
            f"每组 {w_}×{h_}px，横向中心间距 {slot:.0f}px、纵向 {dy}px，组与组不重叠")


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
def _(d, pal, img):
    """岸上一步就是一步；水里蹬一下滑出去好远，两组划痕隔得很开。"""
    (lx, ly, lw, lh), (rx, ry, rw, rh) = panel2(d, pal)
    n, m = 4, 3
    fp, sc = asset("dinoswim", 2), asset("dinoswim", 3)
    gl, gr = lh * 0.22, rh * 0.37
    fw = fh = sw = sh = 0
    for i in range(n):
        fw, fh = place(img, fp, lx, ly - gl * (n - 1) / 2 + i * gl,
                       **_box(fp, lw * 0.56, gl * 0.92))
    for i in range(m):
        sw, sh = place(img, sc, rx, ry - gr * (m - 1) / 2 + i * gr,
                       **_box(sc, rw * 0.60, gr * 0.62))
    return (f"左右两格等大（各 {lw:.0f}×{lh:.0f}px）：左格 {n} 个整脚脚印（素材2，各 {fw}×{fh}px），"
            f"中心间距 {gl:.0f}px / 右格 {m} 组爪尖划痕（素材3，每组三道，各 {sw}×{sh}px），"
            f"中心间距 {gr:.0f}px —— 是左格的 {gr / gl:.1f} 倍，水里那一步迈得远")


@page("dinoswim", 11)
def _(d, pal, img):
    """泥后来干了，上面一层一层压上去，最底下那几道爪印留到今天。"""
    n, k, step = 4, 3, 230
    h = (S - 2 * MARGIN) / n
    note = bands(d, pal, n, mark=n - 1, top=MARGIN, h=h)
    y = MARGIN + (n - 0.5) * h
    a = asset("dinoswim", 3)
    w_ = h_ = 0
    for j in range(k):
        w_, h_ = place(img, a, S / 2 + (j - 1) * step, y, **_box(a, step * 0.80, h * 0.72))
    return (note + f"；最下面那层（高 {h:.0f}px）里 {k} 组爪印（素材3，每组三道、共 {k * 3} 道，"
            f"各 {w_}×{h_}px、中心间距 {step}px），上面压着 {n - 1} 层")


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
    sc = asset("tiny", 5)
    base = S - MARGIN - 34
    sw, sh = place(img, sc, S / 2, base, anchor="bottom", **_box(sc, S - 2 * MARGIN - 80, 560))
    x0, top = S / 2 - sw / 2, base - sh
    # 素材自己就是斜的：左盘低（沉）、右盘高（翘）。程序只管把谁放哪一盘。
    lowx, lowy = x0 + sw * 0.15, top + sh * 0.72
    hix, hiy = x0 + sw * 0.82, top + sh * 0.51
    egg, dino = asset("tiny", 3), asset("tiny", 1)
    ew, eh = place(img, egg, lowx, lowy, h=230, anchor="bottom")
    dw, dh = place(img, dino, hix, hiy, h=210, anchor="bottom")
    return (f"1 副天平（素材5，{sw}×{sh}px，横梁自己是斜的：左盘低、右盘高）："
            f"沉下去的那一盘（在它宽度的 15% 处）放 1 个鸡蛋（{ew}×{eh}px）/ "
            f"翘起来的那一盘（82% 处）放 1 只小恐龙（{dw}×{dh}px），"
            f"两个落脚点差 {lowy - hiy:.0f}px —— 鸡蛋那头沉")


@page("tiny", 5)
def _(d, pal, img):
    """脑袋比核桃大不了多少；嘴里的牙细得像针尖，一根一根排得很密。"""
    a, nut = asset("tiny", 1), asset("tiny", 4)
    base, top, gap = 730, MARGIN + 30, 70
    ra, rn = a.width / a.height, nut.width / nut.height
    # 核桃要和脑袋一样大，脑袋又是整只的 26%——两件并排不许相碰，高度就只能算出来
    hh = min(base - top, (S - 2 * MARGIN - gap) / (ra + 0.26 * rn))
    w_, h_ = place(img, a, MARGIN + hh * ra / 2, base, h=hh, anchor="bottom")
    hx, hy, r = MARGIN + w_ * 0.13, base - h_ + h_ * 0.13, h_ * 0.13
    d.ellipse([hx - r, hy - r, hx + r, hy + r], outline=pal["accent"], width=10)
    nw, nh = place(img, nut, S - MARGIN - r * rn, hy, h=2 * r)
    for y in (hy - r, hy + r):
        x = hx + r + 16
        while x < S - MARGIN - nw - 12:
            d.line([x, y, x + 34, y], fill=pal["line"], width=5)
            x += 56
    k, gy, span = 18, 838, 700
    step = span / (k - 1)
    fang = asset("tiny", 6)
    fh = min(145.0, step * 0.96 * fang.height / fang.width)
    fw = round(fang.width * fh / fang.height)
    d.line([S / 2 - span / 2, gy, S / 2 + span / 2, gy], fill=pal["ink"], width=12)
    for i in range(k):
        place(img, fang, S / 2 - span / 2 + i * step, gy + fh / 2, h=fh)
    return (f"1 只小恐龙（素材1，{w_}×{h_}px）+ 头上 1 个圈（直径 {2 * r:.0f}px）+ "
            f"右边 1 个核桃（素材4，{nw}×{nh}px，和这个圈一样大）+ 中间上下 2 条对齐虚线；"
            f"下面 1 条牙床上 {k} 颗针尖牙（素材6，各 {fw}×{fh:.0f}px），"
            f"中心间距 {step:.1f}px、相邻只空 {step - fw:.0f}px —— 排得很密")


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
    hand, egg = asset("tiny", 7), asset("tiny", 3)
    hw, hh = place(img, hand, S / 2, S / 2, **_box(hand, S - 2 * MARGIN, S - 2 * MARGIN))
    x0, y0 = S / 2 - hw / 2, S / 2 - hh / 2
    cx, cy = x0 + hw * 0.46, y0 + hh * 0.63              # 手心那块凹的正中
    k, eh = 7, 200
    ew = round(egg.width * eh / egg.height)
    R = (ew + 8) / (2 * math.sin(math.pi / k))           # 圈的大小由蛋的宽度倒推——刚好挨着
    for i in range(k):
        a = 2 * math.pi * i / k - math.pi / 2
        place(img, egg, cx + R * math.cos(a), cy + R * math.sin(a), h=eh)
    return (f"1 只摊开的手心（素材7，{hw}×{hh}px）+ 手心那块凹处 {k} 个蛋（素材3，各 {ew}×{eh}px）"
            f"围成 1 圈：圈半径 {R:.0f}px，相邻中心间距 {ew + 8}px、边缘只空 8px —— 挨着围满一圈")


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
def _(d, pal, img):
    """一根丝从根上分了叉，一根变成好几根，聚成一小簇。"""
    L, base = 430, S / 2 + 300
    # 单根丝是竖着画的，一簇是斜躺着画的——不扶正就成了「一根立着、一簇倒着」
    one, tuft = asset("feather", 1), _upright(asset("feather", 2), 58)
    w1, h1 = place(img, one, 215, base, h=L, anchor="bottom")
    w2, h2 = place(img, tuft, 775, base, h=L, anchor="bottom")
    arrow(d, 215 + w1 / 2 + 40, base - L / 2, 775 - w2 / 2 - 40, base - L / 2, pal, w=10, head=28)
    return (f"左边 1 根丝（素材1，{w1}×{h1}px）/ 右边 1 簇（素材2，{w2}×{h2}px，"
            f"好几根从同一个根聚起来）+ 中间 1 支箭头：两边脚底在同一条线上、"
            f"缩到同样高 {L}px，簇比单根宽 {w2 - w1}px")


@page("feather", 5)
def _(d, pal, img):
    """一根丝 → 一小簇 → 中间长出梗、两边排开细丝的一整片。"""
    return steps(img, d, pal, "feather", [1, 2, 3])


@page("feather", 7)
def _(d, pal, img):
    """胳膊上的羽毛一排排开，越靠外越长，合起来像一把扇子。"""
    k = 10
    feat = _upright(asset("feather", 3), 44)        # 素材斜着画，先扶成羽根在下
    hx, hy = MARGIN + 205, S - MARGIN - 105
    d0, d1, L0, dL = -15, 70, 250, 38
    for i in range(k):
        _turn(img, feat, hx, hy, d0 + (d1 - d0) * i / (k - 1), h=L0 + i * dL)
    disc(d, hx, hy, 26, pal["soft"], pal, w=8)
    return (f"1 把扇子：{k} 根羽毛（素材3）从同一个根排开，离竖直方向 {d0}° 到 {d1}°"
            f"（相邻差 {(d1 - d0) / (k - 1):.1f}°），长度从 {L0}px 一根比一根长到 "
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
    # 11 根时槽只有 88px 宽，这根素材长宽比 1:2.7，最高的一根也只剩 183px、最短 73px。
    # 帆是一排挨着的骨棒，少两根、让相邻的略叠一点，每一根就都看得清了。
    k = 9
    spine = S - MARGIN - 210
    xs, slot = lay(k)
    a = asset("sail", 2)
    aw, ah = a.size
    hmax = min(660.0, slot * 1.25 * ah / aw)
    hs = []
    for i, x in enumerate(xs):
        t = 1 - abs(i - (k - 1) / 2) / ((k - 1) / 2)
        _w, h_ = place(img, a, x, spine, h=hmax * (0.62 + 0.38 * t), anchor="bottom")
        hs.append(h_)
    d.line([MARGIN + 30, spine, S - MARGIN - 30, spine], fill=pal["ink"], width=16)
    return (f"1 条脊椎线上 {k} 根长棒（素材2），一根挨着一根，中心间距 {slot:.0f}px；"
            f"中间最长 {max(hs)}px、两端最短 {min(hs)}px，都从脊椎线上往上长")


@page("sail", 4)
def _(d, pal, img):
    """别的恐龙那根棒只有短短一截，棘龙的这一根长得吓人。"""
    note = cmp_height(img, d, pal, "sail", [(2, 230, S / 2 - 230), (2, 760, S / 2 + 230)])
    return note + "；两根是同一个素材（同一节脊椎骨上的长棒），右边这根是左边的 3.3 倍高"


@page("sail", 7)
def _(d, pal, img):
    """血一涌上帆，帆就变红；远远看过去，那个身子好像又大了一圈。"""
    boxes = panel2(d, pal)
    _cx, _cy, w_, h_ = boxes[0]
    a = [asset("sail", 5), asset("sail", 6)]
    bw, bh = w_ * 0.78, h_ * 0.70
    hh = min(bh, min(bw * x.height / x.width for x in a))   # 同一个高度，两格才是「一样大」
    out = []
    for i, (cx, cy, _w, _h) in enumerate(boxes):
        if i == 1:                          # 涨红那只沿自己的轮廓加一圈：远看「又大了一圈」
            halo(img, a[i], cx, cy, h=hh, color=_rgb(pal["accent"]), grow=22, width=11)
        out.append(place(img, a[i], cx, cy, h=hh))
    return (f"左右两格等大（各 {w_:.0f}×{h_:.0f}px），各 1 只背上长帆的恐龙、都缩到同样高 {hh:.0f}px："
            f"左格帆是浅色的（素材5，宽 {out[0][0]}px）/ 右格帆涨红了（素材6，宽 {out[1][0]}px），"
            f"右边这只外面还沿着它自己的轮廓描了 1 圈强调线（离轮廓 22px、线宽 11px）")


@page("sail", 10)
def _(d, pal, img):
    """从鼻子到尾巴尖十五米，两辆小汽车接起来还不够。"""
    n = 2
    a1, car_a = asset("sail", 1), asset("sail", 4)
    span = min(860.0, (610 - MARGIN) * a1.width / a1.height)   # 体长封顶，也不许顶出上边
    x0 = (S - span) / 2
    w_, h_ = place(img, a1, S / 2, 640, w=span, anchor="bottom")
    car = span * 0.425                      # 两辆合起来只有它的 85%
    cw = ch = 0
    for i in range(n):
        cw, ch = place(img, car_a, x0 + car * (i + 0.5), 950, w=car, anchor="bottom")
    for x in (x0, x0 + span):
        for seg in range(6):
            y = 662 + seg * 18
            d.line([x, y, x, y + 9], fill=pal["line"], width=5)
    return (f"上面 1 只棘龙体长 {w_}px（高 {h_}px）；下面 {n} 辆小汽车（素材4，各 {cw}×{ch}px）"
            f"首尾相接合计 {n * car:.0f}px（只有它的 {n * car / span * 100:.0f}%，"
            f"还差 {span - n * car:.0f}px），两端有对齐线")


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
def _(d, pal, img):
    """爬树的爪子弯得厉害，地上跑的直一些，小盗龙的很弯。"""
    ns = (5, 6, 5)                       # 弯钩 / 近乎笔直 / 弯钩（小盗龙的和爬树的同一个素材）
    xs, slot = lay(3)
    Lm, out = 280, []
    for x, n in zip(xs, ns):
        im = asset("climb", n)
        out.append(place(img, im, x, S / 2, **(dict(w=Lm) if im.width >= im.height else dict(h=Lm))))
    return (f"3 只爪子并排（中心间距 {slot:.0f}px，最长的一边都缩到 {Lm}px）："
            f"左 1 只弯钩爪（素材5，{out[0][0]}×{out[0][1]}px）/ "
            f"中 1 只近乎笔直的爪（素材6，{out[1][0]}×{out[1][1]}px）/ "
            f"右 1 只还是弯钩爪（素材5，和左边同一个素材、一样弯，{out[2][0]}×{out[2][1]}px）"
            f"——爬树的最弯、地上跑的最直、小盗龙的和爬树的一样弯")


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
    tree, a1, fp = asset("climb", 3), asset("climb", 1), asset("climb", 7)
    tx = MARGIN + 250
    tw, th = place(img, tree, tx, base, anchor="bottom", **_box(tree, 480, 600))
    dw, dh = place(img, a1, tx + tw / 2 + 110, base - th * 0.80, **_box(a1, 180, 180))
    # 脚印一定要比整只小盗龙大：高度直接按它的 1.3 倍算，不是写死一个数
    fh = dh * 1.30
    fw = fp.width * fh / fp.height
    n, step = 3, fw + 26
    x0 = S - MARGIN - 20 - (n - 1) * step - fw / 2
    for i in range(n):
        place(img, fp, x0 + i * step, base - 100, h=fh)
    return (f"1 棵树（素材3，{tw}×{th}px），1 只小盗龙（素材1，{dw}×{dh}px）停在树高的 80% 处；"
            f"地面上 {n} 个大脚印（素材7，各 {fw:.0f}×{fh:.0f}px，中心间距 {step:.0f}px 不重叠）——"
            f"1 个脚印高 {fh:.0f}px，比整只小盗龙（高 {dh}px）还大")


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
def _(d, pal, img):
    """那时候地上别的爬行动物又大又多，恐龙只是小小一群。"""
    a5, a6 = asset("eras", 5), asset("eras", 6)     # 五趾爬行动物 / 三趾恐龙
    big, small = 0, 4
    bw = bh = sw = sh = 0
    for r in range(3):
        for c in range(5 if r < 2 else 4):
            bw, bh = place(img, a5, MARGIN + 115 + c * 190, MARGIN + 140 + r * 190,
                           **_box(a5, 168, 168))
            big += 1
    for i in range(small):
        sw, sh = place(img, a6, S / 2 + 170 + (i % 2) * 105,
                       S - MARGIN - 190 + (i // 2) * 105, **_box(a6, 92, 92))
    return (f"{big} 个五趾爬行动物脚印（素材5，各 {bw}×{bh}px，5+5+4 三行铺开、中心间距 190px）+ "
            f"{small} 个三趾恐龙脚印（素材6，各 {sw}×{sh}px，挤在右下角 2×2、中心间距 105px）："
            f"大的又大又多（{big} 个），小的又小又少（{small} 个），"
            f"单个面积只有大的 {sw * sh / max(bw * bh, 1) * 100:.0f}%")


@page("eras", 6)
def _(d, pal, img):
    """最早的那种小恐龙站在它脚边，只到它的膝盖。"""
    frac = 0.30                              # 膝盖在它整高的 30% 处
    base = S - MARGIN - 90
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    big, small = asset("eras", 2), asset("eras", 1)
    # 大的这只顶到画面上沿才够高，小的才有 200px 以上——所以按高度摆，不写死宽度
    hb = min(base - MARGIN - 30, (S - 2 * MARGIN - 40) * big.height / big.width)
    bw, bh = place(img, big, S - MARGIN - 40 - hb * big.width / big.height / 2, base,
                   h=hb, anchor="bottom")
    knee = base - bh * frac
    sw, sh = place(img, small, MARGIN + 200, base, h=bh * frac, anchor="bottom")
    for seg in range(6):
        x = MARGIN + 20 + seg * 62
        d.line([x, knee, x + 32, knee], fill=pal["line"], width=6)
    return (f"1 只蜥脚类（素材2，{bw}×{bh}px）+ 1 只早期小恐龙（素材1，{sw}×{sh}px，"
            f"高正好是它的 {frac * 100:.0f}%），站同一条地线、小的站在大的脚边，"
            f"膝盖那条虚线（离地 {bh * frac:.0f}px）落在小恐龙头顶")


@page("eras", 8)
def _(d, pal, img):
    """剑龙先走，八千万年以后霸王龙才出来，两个没见过面。"""
    t0, t1 = 0.18, 0.78
    note = _tl(img, d, pal, "eras", [(t0, 4, "剑龙"), (t1, 3, "霸王龙")], bw=400, bh=330)
    return note + (f"；两个刻度隔着整条线的 {(t1 - t0) * 100:.0f}%（八千万年）、"
                   f"中心相距 {(t1 - t0) * (S - 2 * MARGIN - 100):.0f}px，"
                   f"两只各封顶 400×330px，中间不相碰")


@page("eras", 9)
def _(d, pal, img):
    """剑龙到霸王龙隔八千万年，霸王龙到我们只隔六千六百万年，后一段更短。"""
    a, b = 80.0, 66.0
    t0, t2 = 0.15, 0.90
    t1 = t0 + (t2 - t0) * a / (a + b)
    note = _tl(img, d, pal, "eras",
               [(t0, 4, "剑龙"), (t1, 3, "霸王龙"), (t2, None, "我们")], bw=340, bh=300)
    return note + (f"；左段 {(t1 - t0) * 100:.0f}%（八千万年）比右段 {(t2 - t1) * 100:.0f}%"
                   f"（六千六百万年）长，霸王龙这一刻度离右端更近")


@page("eras", 10)
def _(d, pal, img):
    """三个时代各挑一只，按同一个比例尺排在一条地线上。"""
    # 2 米和 25 米差 12.5 倍：一条地线上按同一把尺排，最小的那只只有 44px 宽，怎么都找不着。
    # 所以地线抬到 742，下面空出一条，另放一只放大的——并在清单里写明这一只没按尺。
    k, gap = 22.0, 40
    items = [(1, 2.0), (2, 25.0), (3, 12.0)]
    base = 742
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    small = asset("eras", 1)
    total = sum(m * k for _a, m in items) + gap * (len(items) - 1)
    x = (S - total) / 2
    out, tw, th, tx = [], 0, 0, 0.0
    for a, m in items:
        w_, h_ = place(img, asset("eras", a), x + m * k / 2, base, w=m * k, anchor="bottom")
        out.append(f"素材{a}（{m:.0f} 米）→ {w_}×{h_}px")
        if a == 1:
            tx, tw, th = x + m * k / 2, w_, h_
            halo(img, small, tx, base, w=m * k, anchor="bottom",
                 color=_rgb(pal["accent"]), grow=14, width=7)
        x += m * k + gap
    bx, by, bh_ = 810, 970, 210
    bw_, _ = place(img, small, bx, by, h=bh_, anchor="bottom")
    halo(img, small, bx, by, h=bh_, anchor="bottom", color=_rgb(pal["accent"]), grow=14, width=7)
    d.line([tx - tw / 2, base + 2, bx - bw_ / 2, by - bh_], fill=pal["line"], width=5)
    d.line([tx + tw / 2, base + 2, bx + bw_ / 2, by], fill=pal["line"], width=5)
    return (f"同一个比例尺 {k:.0f} px/米，{len(items)} 只按体长排在地线上、间距 {gap}px 互不相碰："
            + " / ".join(out) + f"，一行总宽 {total:.0f}px。最小的那只按尺只有 {tw}×{th}px，"
            f"沿轮廓描了 1 圈强调线；地线下面另放 1 只放大到 {bw_}×{bh_}px 的同一个素材"
            f"（放大 {bh_ / max(th, 1):.1f} 倍，**这一只没按尺**），2 条引线连回按尺的那只")
