# -*- coding: utf-8 -*-
"""第七批示意图页（1/5）：剑龙、甲龙、爪子、尾巴、手指、骨头里的空气、照顾宝宝、成群走。"""
from draw_diagrams import (S, MARGIN, page, asset, place, halo, lie_flat, poly, disc, arrow,
                           cross, lay, panel2, hbar, bands, cmp_len, cmp_count, bars,
                           timeline, steps, magnify)
from PIL import Image, ImageColor, ImageDraw
import math, random


# ---------------------------------------------------------------- 摆素材用的几样量具
# 素材的长宽比是模型给的，代码不知道。所以「摆哪儿」必须先算后画：先按框算出实际宽高，
# 再定坐标，最后才 place。只写 place(w=340) 的页，换一张竖素材就顶穿框顶。

def _fit(a, max_w, max_h):
    """把素材缩进 max_w × max_h 的框里，返回它实际会占的 (宽, 高)。

    两个方向各算一次、取小的那个。返回的是浮点数，用来先排版；真正的占位以 place 的返回为准。
    """
    s = min(max_w / a.width, max_h / a.height)
    return a.width * s, a.height * s


def _rgb(c):
    """调色板里存的是 "#2c2b23" 这样的字符串，halo() 要的是 (r, g, b)。"""
    return ImageColor.getrgb(c)


def _point_right(a):
    """把一头粗一头尖的素材翻成尖头朝右：哪半边实心面积大，哪半边就是根部。

    爪骨和爪鞘要按根部对齐着叠，可 lie_flat 只保证「躺平」，不保证朝哪头。
    先各自转正，再叠，才不会一根朝左一根朝右。
    """
    import numpy as np
    m = np.asarray(a.getchannel("A")) > 128
    half = m.shape[1] // 2
    return a.transpose(Image.FLIP_LEFT_RIGHT) if m[:, :half].sum() < m[:, half:].sum() else a


def _reach(a, x, y, ang, w, h, frac=0.86):
    """在放好的素材里，从 (x, y) 沿 ang 射出去，返回还留在素材实心部分里的最远长度。

    「三根指骨藏在翅膀里面」这种话不能靠我目测：翅膀是什么形状由模型定，
    所以直接拿素材自己的 alpha 逐根量，量到哪儿画到哪儿。x/y/w/h 都是贴上去以后的画面尺寸。
    """
    import numpy as np
    m = np.asarray(a.getchannel("A")) > 128
    ah, aw = m.shape
    t, step = 0.0, 6.0
    while t < max(w, h):
        nx, ny = x + (t + step) * math.cos(ang), y + (t + step) * math.sin(ang)
        ix, iy = int(nx * aw / w), int(ny * ah / h)
        if not (0 <= ix < aw and 0 <= iy < ah and m[iy, ix]):
            break
        t += step
    return t * frac


def _centroid(a, w, h):
    """素材实心部分的重心（贴上去以后的画面坐标）—— 一定落在素材里面，适合当引线的起点。"""
    import numpy as np
    m = np.asarray(a.getchannel("A")) > 128
    ys, xs = np.nonzero(m)
    if not len(xs):
        return w / 2, h / 2
    return xs.mean() / m.shape[1] * w, ys.mean() / m.shape[0] * h


def _nearest(a, w, h, tx, ty):
    """素材上离 (tx, ty) 最近的那个实心点（贴上去以后的画面坐标）。

    引线从这里出发才不会横穿整只恐龙——从重心出发的那条线，正好划过脑袋。
    """
    import numpy as np
    m = np.asarray(a.getchannel("A"))[::4, ::4] > 128
    ys, xs = np.nonzero(m)
    if not len(xs):
        return w / 2, h / 2
    px, py = xs / m.shape[1] * w, ys / m.shape[0] * h
    i = int(np.argmin((px - tx) ** 2 + (py - ty) ** 2))
    return float(px[i]), float(py[i])


def _extreme(a, w, h, side):
    """素材最左（side=-1）或最右（side=1）的那个实心点。

    「最外边那两根手指」在哪儿？张开的手，最外两根的指尖就是整张图最左和最右的实心像素，
    量出来比我按比例猜准得多。
    """
    import numpy as np
    m = np.asarray(a.getchannel("A")) > 128
    cols = np.nonzero(m.any(0))[0]
    c = cols[-1] if side > 0 else cols[0]
    rows = np.nonzero(m[:, c])[0]
    return c / m.shape[1] * w, rows.mean() / m.shape[0] * h


def _thick(a, h=None, w=None):
    """素材最粗的地方有多粗（缩放到目标尺寸以后的像素）：最大内切圆的直径。

    比外框宽度靠谱得多：钩爪弯成一个圈，外框跟铲爪一样宽，可它本身细得多。
    「又宽又钝」和「又细又尖」差多少，得量形状，不能量外框。
    """
    import numpy as np
    from scipy import ndimage
    m = np.asarray(a.getchannel("A")) > 128
    s = (h / a.height) if h else ((w / a.width) if w else 1.0)
    return 2 * ndimage.distance_transform_edt(m).max() * s


# ---------------------------------------------------------------- 这一批自己要用的小图元
# 只放通用图元里没有、而且这八本里反复出现的几样：爪、手、骨头、树、爆响星。

def _bone(d, cx, cy, L, pal, half=34, fill=None, soft=0, w=8):
    """一根立着的长骨：中间一段杆 + 两头各两个骨节。soft>0 时两头各盖一段软骨。"""
    F = fill if fill is not None else pal["paper"]
    d.rounded_rectangle([cx - half, cy - L / 2, cx + half, cy + L / 2], radius=half, fill=F,
                        outline=pal["ink"], width=w)
    for s in (-1, 1):
        for dx in (-1, 1):
            disc(d, cx + dx * half * 0.95, cy + s * L / 2, half * 1.05, F, pal, w=w)
    if soft:
        for s in (-1, 1):
            d.rounded_rectangle([cx - half * 1.9, cy + s * L / 2 - soft / 2,
                                 cx + half * 1.9, cy + s * L / 2 + soft / 2],
                                radius=soft / 2, fill=pal["accent"], outline=pal["ink"], width=6)
    return L


def _star(d, cx, cy, r, pal, n=10, inner=0.44, fill=None, w=7):
    """一个 n 角的爆响星。"""
    pts = []
    for i in range(2 * n):
        rr = r if i % 2 == 0 else r * inner
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    poly(d, pts, pal, fill if fill is not None else pal["accent"], w)
    return n


def _dash_v(d, x, y0, y1, pal, seg=18, gap=12, w=5, col=None):
    """一道竖的虚线，返回画了几段。"""
    n, y = 0, y0
    while y < y1:
        d.line([x, y, x, min(y + seg, y1)], fill=col or pal["line"], width=w)
        y += seg + gap
        n += 1
    return n


def _dash_h(d, y, x0, x1, pal, seg=22, gap=16, w=6, col=None):
    """一道横的虚线，返回画了几段。比高矮的页拿它当参考线：够不够得到，一眼看得出来。"""
    n, x = 0, x0
    while x < x1:
        d.line([x, y, min(x + seg, x1), y], fill=col or pal["line"], width=w)
        x += seg + gap
        n += 1
    return n


# ================================================================ stego 剑龙背上的板

@page("stego", 2)
def _(d, pal, img):
    """背上一共十七块板，沿着背脊一路排到尾巴根 —— 十七块就是十七块。"""
    # 十七块板，每块都要看得清（上一版每块只有 28～48px 宽，糊成一排小牙）。
    # 一行摆不下十七块 200px 的板，所以照尾巴那本的老办法折成两行：数目一块不少，
    # 板画大，相邻两块允许叠一点——真剑龙背上的板本来也是一块挨一块。
    n, per = 17, 9
    plate = asset("stego", 2)
    pw, ph = _fit(plate, 214, 330)
    # 两端的板是按中心摆的，所以起止点要让开半块板的宽度，不然最外两块有一半在页外
    x0, x1 = MARGIN + pw / 2 + 6, S - MARGIN - pw / 2 - 6
    step = (x1 - x0) / (per - 1)
    # 两行的高度按板的实际高度算：背脊线中间还要拱起 dip，不把它算进去，
    # 中间那几块板的尖就顶到页外了
    dip, between = 56, 130
    top = max(MARGIN + 8, (S - (2 * ph + between + dip)) / 2)
    bases = (top + dip + ph, top + dip + 2 * ph + between)
    got, k = [], 0
    for base in bases:
        cnt = min(per, n - k)
        # 背脊线只画到这一行最后一块板为止，两端各多伸 40px —— 多画的那一截会像根没来由的黑棍
        t_end = (cnt - 1) / (per - 1)
        spine = [(x0 - 40 + ((x1 - x0) * t_end + 80) * i / 40,
                  base - dip * math.sin(math.pi * t_end * i / 40)) for i in range(41)]
        d.line(spine, fill=pal["ink"], width=12, joint="curve")
        for i in range(cnt):
            t = i / (per - 1)
            got.append(place(img, plate, x0 + (x1 - x0) * t,
                             base - dip * math.sin(math.pi * t), w=pw, anchor="bottom"))
            k += 1
    arrow(d, x1 - 30, bases[0] + 54, x0 + 40, bases[1] - got[-1][1] - 34, pal, w=10, head=26)
    ow = got[0][0] - step
    return (f"2 段背脊线，沿线一共 {k} 块板（素材2）：上行 {per} 块 / 下行 {k - per} 块，"
            f"每块宽 {got[0][0]}px 高 {got[0][1]}px、中心距 {step:.0f}px —— 板比间距宽，"
            f"相邻两块叠 {ow:.0f}px（{ow / got[0][0] * 100:.0f}%，后一块压住前一块），"
            f"两行之间 1 支接着数下去的箭头")


@page("stego", 3)
def _(d, pal, img):
    """板不长在脊椎上：它们插在皮里，和脊椎之间还隔着一段空当。"""
    skin_top, skin_h = 560, 120
    n_p = 4
    px, pslot = lay(n_p)
    plate = asset("stego", 2)
    bury = 60                                  # 板底埋进皮里多深
    pw, ph = _fit(plate, pslot * 0.86, 430)
    got = []
    for x in px:
        # 先贴板、后画皮：皮这一条压住板的下半截，看着才是「插在皮里」而不是「立在皮上」
        got.append(place(img, plate, x, skin_top + bury, w=pw, anchor="bottom"))
    d.rectangle([MARGIN, skin_top, S - MARGIN, skin_top + skin_h],
                fill=pal["soft"], outline=pal["ink"], width=8)
    n_v = 9
    vy = skin_top + skin_h + 170
    xs, slot = lay(n_v)
    for x in xs:
        d.rounded_rectangle([x - slot * 0.34, vy - 48, x + slot * 0.34, vy + 48], radius=16,
                            fill=pal["bark"], outline=pal["ink"], width=6)
    clear = (vy - 48) - (skin_top + skin_h)
    arrow(d, S / 2, (skin_top + skin_h + vy - 48) / 2 - 8, S / 2, skin_top + skin_h + 6, pal, w=7, head=20)
    arrow(d, S / 2, (skin_top + skin_h + vy - 48) / 2 + 8, S / 2, vy - 54, pal, w=7, head=20)
    return (f"1 层皮（厚 {skin_h}px）+ 皮下 {n_v} 块脊椎骨 + 插在皮里的 {n_p} 块板"
            f"（素材2，每块宽 {got[0][0]}px 高 {got[0][1]}px、间距 {pslot:.0f}px，都小于间距不相碰）；"
            f"每块板的下端埋进皮里 {bury}px（被皮压住看不见）、离皮的底面还差 {skin_h - bury}px；"
            f"板底到脊椎 {clear + skin_h - bury}px，其中皮和脊椎之间空着的 {clear}px 由 2 支箭头标出，"
            f"没有一块板碰到脊椎")


@page("stego", 5)
def _(d, pal, img):
    """板是散热用的：热血流进板里，风一吹就凉，和汽车前面的水箱一个道理。"""
    n = 4
    boxes = panel2(d, pal)
    for (cx, cy, w_, h_), a in zip(boxes, (2, 3)):
        place(img, asset("stego", a), cx, cy - h_ * 0.06, h=h_ * 0.40, anchor="bottom")
        for i in range(n):                       # 两格一样多的风
            y = cy + h_ * 0.16 + i * 72
            arrow(d, cx - w_ * 0.40, y, cx + w_ * 0.22, y, pal, w=9, head=22)
    lx, ly, lw, lh = boxes[0]
    arrow(d, lx, ly + lh * 0.10, lx, ly - lh * 0.20, pal, w=13, head=30)
    return (f"左格 1 块板（素材2）+ 1 支往上流进板里的血 / 右格 1 个水箱（素材3）；"
            f"两格各 {n} 支一样长的风的箭头，两格等大")


@page("stego", 6)
def _(d, pal, img):
    """血一涌上去，板看着大了一圈 —— 板本身没变大，是外面多了一圈。"""
    halo, H = 44, 420
    boxes = panel2(d, pal)
    sizes = []
    for (cx, cy, w_, h_), hot in zip(boxes, (False, True)):
        w2, h2 = place(img, asset("stego", 2), cx, cy + h_ * 0.30, h=H, anchor="bottom")
        sizes.append((w2, h2))
        if hot:
            bx, by = cx, cy + h_ * 0.30
            poly_pts = [(bx - w2 / 2 - halo, by + halo), (bx, by - h2 - halo * 1.6),
                        (bx + w2 / 2 + halo, by + halo)]
            for a, b in zip(poly_pts, poly_pts[1:] + poly_pts[:1]):
                d.line([a, b], fill=pal["accent"], width=12)
            for k in range(3):                    # 涌上去的血
                arrow(d, bx - 120 + k * 120, by - 30, bx - 120 + k * 120, by - h2 * 0.62,
                      pal, w=10, head=24)
    return (f"左格 1 块板高 {sizes[0][1]}px（平时）/ 右格同一块板、同样高 {sizes[1][1]}px，"
            f"外面加 1 圈向外扩 {halo}px 的强调色轮廓 + 3 支涌上去的血；板本身一样大，是看着大了一圈")


@page("stego", 9)
def _(d, pal, img):
    """头很小，脑子只有核桃那么大。"""
    cx, cy = S / 2, S / 2 - 40
    stg = asset("stego", 1)
    w_, h_ = _fit(stg, S - 2 * MARGIN - 80, 620)      # 宽高都卡住，换张竖素材也不会顶穿
    w_, h_ = place(img, stg, cx, cy, w=w_)
    hx = cx - w_ / 2 + w_ * 0.09
    hy = cy - h_ / 2 + h_ * 0.66
    d.ellipse([hx - w_ * 0.075, hy - h_ * 0.13, hx + w_ * 0.075, hy + h_ * 0.13],
              outline=pal["accent"], width=12)
    nut = asset("stego", 4)
    nw, nh = _fit(nut, 300, 250)
    nx, ny = MARGIN + 40 + nw / 2, S - MARGIN - 20
    d.line([hx, hy + h_ * 0.13, nx, ny - nh], fill=pal["line"], width=6)
    nw, nh = place(img, nut, nx, ny, w=nw, anchor="bottom")
    return (f"1 只剑龙（素材1，宽 {w_}px）+ 1 个圈住小脑袋的圈（宽 {w_ * 0.15:.0f}px）+ "
            f"左下角 1 颗核桃（素材4，宽 {nw}px 高 {nh}px）+ 1 条把核桃和头连起来的引线")


@page("stego", 11)
def _(d, pal):
    """俯视：板不是两边对齐的，是左一块右一块错开着排。"""
    cx = S / 2
    y0, y1 = 140, 930
    poly(d, [(cx - 34, y0 - 40), (cx + 34, y0 - 40), (cx + 92, y0 + 120), (cx + 92, y1 - 140),
             (cx + 30, y1 + 30), (cx - 30, y1 + 30), (cx - 92, y1 - 140), (cx - 92, y0 + 120)],
         pal, pal["soft"], 9)
    n = 17
    step = (y1 - y0) / (n - 1)
    left = right = 0
    for i in range(n):
        y = y0 + step * i
        s = -1 if i % 2 == 0 else 1
        poly(d, [(cx + s * 80, y - step * 0.46), (cx + s * 235, y - step * 0.10),
                 (cx + s * 80, y + step * 0.46)], pal,
             pal["paper"] if s < 0 else pal["accent"], 7)
        left += s < 0
        right += s > 0
    return (f"1 个俯视的身体 + 左边 {left} 块 / 右边 {right} 块 = {left + right} 块板，"
            f"左右交错（同一高度上没有两块并排），行距 {step:.0f}px")


# ================================================================ ankylo 甲龙的尾巴锤

@page("ankylo", 2)
def _(d, pal, img):
    """从头到尾都盖着骨头板：背上、脖子上、连眼皮上都有。"""
    cx, cy = S / 2, S / 2 + 10
    w_, h_ = place(img, asset("ankylo", 1), cx, cy, w=S - 2 * MARGIN - 60)
    spots = [(0.60, 0.30), (0.32, 0.36), (0.10, 0.46)]     # 背 / 脖子 / 眼皮
    for sx, sy in spots:
        hx = cx - w_ / 2 + w_ * sx
        hy = cy - h_ / 2 + h_ * sy
        d.ellipse([hx - w_ * 0.085, hy - h_ * 0.12, hx + w_ * 0.085, hy + h_ * 0.12],
                  outline=pal["accent"], width=11)
    return (f"1 只甲龙（素材1，宽 {w_}px）+ {len(spots)} 个圈：背上 / 脖子上 / 眼皮上，"
            f"圈心间距 {w_ * 0.28:.0f}px 和 {w_ * 0.22:.0f}px，三个圈互不相碰")


@page("ankylo", 4)
def _(d, pal, img):
    """尾巴尖那个锤是两块骨头长在一起的，有西瓜那么大。"""
    base = S - MARGIN - 150
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    W = 340
    cw, ch = place(img, asset("ankylo", 2), MARGIN + 100 + W / 2, base, w=W, anchor="bottom")
    seg = _dash_v(d, MARGIN + 100 + W / 2, base - ch + 20, base - 20, pal,
                  seg=22, gap=16, w=7, col=pal["ink"])
    # 西瓜按锤实际量出来的宽度摆，「一样大」就不是我说了算，是同一个数
    mx = MARGIN + 100 + W + 70 + cw / 2
    mw, mh = place(img, asset("ankylo", 4), mx, base, w=cw, anchor="bottom")
    return (f"1 个尾锤（素材2，宽 {cw}px 高 {ch}px）+ 中间 1 道把它分成 2 块骨头的竖虚线（{seg} 段）"
            f"+ 右边 1 个西瓜（素材4，宽 {mw}px 高 {mh}px，宽度和锤一模一样），"
            f"两个站在同一条地线上，中心相距 {mx - (MARGIN + 100 + W / 2):.0f}px")


@page("ankylo", 6)
def _(d, pal, img):
    """一锤下去，追它的那只小腿骨就断了。"""
    d.arc([MARGIN + 30, 250, MARGIN + 720, 900], 200, 340, fill=pal["accent"], width=12)
    cw, chh = place(img, asset("ankylo", 2), MARGIN + 200, 430, w=300)
    bx, off = S / 2 + 230, 58
    poly(d, [(bx - 52, 250), (bx + 52, 250), (bx + 52, 520), (bx + 18, 545),
             (bx + 52, 568), (bx - 52, 568), (bx - 18, 542), (bx - 52, 518)],
         pal, pal["paper"], 9)
    for dx in (-1, 1):
        disc(d, bx + dx * 44, 250, 46, pal["paper"], pal, w=9)
    poly(d, [(bx + off - 52, 612), (bx + off - 18, 636), (bx + off + 52, 612),
             (bx + off + 52, 900), (bx + off - 52, 900)], pal, pal["paper"], 9)
    for dx in (-1, 1):
        disc(d, bx + off + dx * 44, 900, 46, pal["paper"], pal, w=9)
    for k in range(3):                           # 断口上的三道裂纹
        d.line([bx + 20 + k * 22, 575, bx + off - 30 + k * 22, 605], fill=pal["ink"], width=6)
    return (f"1 个甩过来的尾锤（素材2，宽 {cw}px）+ 1 道挥动的弧线 + 1 根断成 2 截的小腿骨"
            f"（断口上下错开 {off}px，3 道裂纹）")


@page("ankylo", 8)
def _(d, pal):
    """背上全是骨板，肚子一块也没有 —— 所以它从不翻身。"""
    n = 7
    for (cx, cy, w_, h_), armored in zip(panel2(d, pal), (True, False)):
        top = cy - h_ * 0.05
        d.rounded_rectangle([cx - w_ * 0.38, top - 64, cx + w_ * 0.38, top + 64], radius=60,
                            fill=pal["soft"] if armored else pal["paper"],
                            outline=pal["ink"], width=9)
        if armored:
            step = w_ * 0.68 / (n - 1)
            for i in range(n):
                disc(d, cx - w_ * 0.34 + i * step, top - 64, 24, pal["bark"], pal, w=6)
    return f"左格 1 段身体上 {n} 块骨板（间距 {(S - 2 * MARGIN - 44) / 2 * 0.68 / (n - 1):.0f}px）/ 右格同样大的 1 段身体、0 块骨板（肚子是软的），两格的身体一样大"


@page("ankylo", 10)
def _(d, pal, img):
    """一身盔甲加一把锤：上面是整只，下面是两个放大件。"""
    w_, h_ = place(img, asset("ankylo", 1), S / 2, 310, w=S - 2 * MARGIN - 180)
    rows, cols = 3, 4
    ax, ay = 270, 760
    d.rounded_rectangle([ax - 170, ay - 150, ax + 170, ay + 150], radius=40,
                        fill=pal["soft"], outline=pal["ink"], width=9)
    for r in range(rows):
        for c in range(cols):
            disc(d, ax - 120 + c * 80, ay - 100 + r * 100, 26, pal["bark"], pal, w=6)
    cw, ch = place(img, asset("ankylo", 2), 770, 920, h=300, anchor="bottom")
    d.line([S / 2 - 60, 310 + h_ * 0.30, ax, ay - 150], fill=pal["line"], width=6)
    d.line([S / 2 + w_ * 0.42, 310 + h_ * 0.22, 770, 920 - ch], fill=pal["line"], width=6)
    return (f"上面 1 只甲龙（素材1，宽 {w_}px）+ 下面 2 个放大件：左边 1 块盔甲"
            f"（{rows} 行 ×{cols} = {rows * cols} 个骨突）/ 右边 1 个尾锤（素材2，高 {ch}px），各 1 条引线")


# ================================================================ claws 恐龙的爪子

@page("claws", 2)
def _(d, pal, img):
    """我们看见的只是骨头，外面那层壳比骨头还长一截。"""
    # 壳套在骨头外面，可两张素材的姿势对不齐，硬叠出来是两件东西摞在一起。
    # 改成上下两行、根部（左端）对齐：长出来的那一截自己就跳出来，还能用虚线量给人看。
    x0 = MARGIN + 60
    sheath = _point_right(lie_flat(asset("claws", 4)))
    bone = _point_right(lie_flat(asset("claws", 2)))
    sy, by, frac = 320, 790, 0.70
    sw, sh = _fit(sheath, S - 2 * MARGIN - 140, 460)
    sw, sh = place(img, sheath, x0 + sw / 2, sy, w=sw)
    bw, bh = _fit(bone, sw * frac, 300)
    bw, bh = place(img, bone, x0 + bw / 2, by, w=bw)
    top, bot = sy - sh / 2 - 26, by + bh / 2 + 70
    d.line([x0, top, x0, bot], fill=pal["line"], width=6)          # 左端（根部）对齐线
    for x in (x0 + bw, x0 + sw):
        _dash_v(d, x, top, bot, pal, col=pal["ink"])
    arrow(d, x0 + bw + 12, bot - 30, x0 + sw - 12, bot - 30, pal, w=9, head=24)
    return (f"上行 1 层爪壳（素材4，长 {sw}px 高 {sh}px）/ 下行 1 根爪骨（素材2，长 {bw}px 高 {bh}px），"
            f"两件根部都顶在同 1 条左端对齐线上；两个尖端各 1 条竖虚线，"
            f"壳比骨头多伸出 {sw - bw}px（1 支箭头量的就是这一截），骨头只有壳的 {bw / sw * 100:.0f}%")


@page("claws", 3)
def _(d, pal, img):
    """镰刀龙的爪子，是所有恐龙里最长的一双手 —— 圈出来看。"""
    return magnify(img, d, pal, "claws", 1, (0.33, 0.62), r=0.10)


@page("claws", 5)
def _(d, pal, img):
    """脚上的爪：第二个脚趾翘着，挂着一只大钩子。"""
    gy = S - MARGIN - 60
    d.line([MARGIN, gy, S - MARGIN, gy], fill=pal["ink"], width=10)
    foot = asset("claws", 5)
    fw, fh = _fit(foot, 560, 700)
    fx = MARGIN + 40 + fw / 2
    fw, fh = place(img, foot, fx, gy, w=fw, anchor="bottom")         # 两趾踩在地线上
    hook = asset("claws", 8)
    hw, hh = _fit(hook, 250, 340)
    hx, hy = S - MARGIN - 30 - hw / 2, MARGIN + 60 + hh / 2
    # 引线从素材上离放大件最近的那个实心点起：从重心起的那条会横穿整只恐龙
    cxx, cyy = _nearest(foot, fw, fh, hx - (fx - fw / 2), hy - (gy - fh))
    d.line([fx - fw / 2 + cxx, gy - fh + cyy, hx - hw / 2, hy + hh / 2], fill=pal["line"], width=6)
    hw, hh = place(img, hook, hx, hy, w=hw)
    halo(img, hook, hx, hy, w=hw, color=_rgb(pal["accent"]), grow=12, width=8)
    return (f"1 条地线 + 1 只侧视的脚（素材5，宽 {fw}px 高 {fh}px，两趾踩在地线上、翘起的那趾挂着大钩爪）"
            f"+ 右上角同一只大钩爪的放大件（素材8，宽 {hw}px 高 {hh}px）+ 沿它轮廓的 1 圈强调线 + "
            f"1 条从脚连到放大件的引线")


@page("claws", 7)
def _(d, pal, img):
    """前面三根手指都带爪，三根能合到一起抓住东西。"""
    boxes = panel2(d, pal)
    cx0, cy0, w_, h_ = boxes[0]
    # 两只手画成一样高：同一只手的两个姿势，大小不该有差别
    H = min(_fit(asset("claws", k), w_ * 0.94, h_ * 0.62)[1] for k in (6, 7))
    ball = 180
    got = []
    for (cx, cy, w_, h_), a in zip(boxes, (6, 7)):
        im = asset("claws", a)
        if a == 7:
            # 球先画、手后贴：球心抬到手的上沿，下半个被手压住，才像抓在手里
            disc(d, cx, cy - H * 0.42, ball / 2, pal["accent"], pal, w=8)
        got.append(place(img, im, cx, cy, h=H))
    return (f"左格 1 只张开的三指手（素材6，宽 {got[0][0]}px）/ 右格同一只手合拢（素材7，宽 {got[1][0]}px）+ "
            f"1 个直径 {ball}px 的球画在手后面、被手压住一部分（抓在手里）；"
            f"两格等大，两只手一样高 {H:.0f}px，差别只在张开还是合拢")


@page("claws", 9)
def _(d, pal, img):
    """挖土的爪又宽又钝像把铲，抓肉的爪又细又尖像把钩。"""
    boxes = panel2(d, pal)
    cx0, cy0, w_, h_ = boxes[0]
    # 两只爪画成一样高，那么「谁更宽」量出来的就是爪本身的胖瘦，不是我缩放缩出来的
    H = min(_fit(asset("claws", k), w_ * 0.86, h_ * 0.50)[1] for k in (10, 8))
    got, th_ = [], []
    for (cx, cy, w_, h_), dig in zip(boxes, (True, False)):
        tool = asset("claws", 3 if dig else 2)
        tw, tht = _fit(tool, w_ * 0.66, h_ * 0.30)
        place(img, tool, cx, cy - h_ * 0.44 + tht / 2, w=tw)
        claw = asset("claws", 10 if dig else 8)
        got.append(place(img, claw, cx, cy + h_ * 0.44, h=H, anchor="bottom"))
        # 「粗细」量的是最大内切圆，不是外框：钩爪弯成一圈，外框跟铲爪一样宽，本身却细得多
        th_.append(_thick(claw, h=H))
    return (f"左格 1 把铲（素材3）+ 1 只又宽又钝的铲爪（素材10）/ "
            f"右格 1 根又细又尖的爪骨（素材2）+ 1 只钩爪（素材8）；"
            f"两只爪画成一样高 {H:.0f}px、脚底落在同一条高度上，"
            f"最粗的地方：铲爪 {th_[0]:.0f}px / 钩爪 {th_[1]:.0f}px，"
            f"铲爪粗 {th_[0] / th_[1]:.1f} 倍，两格等大")


@page("claws", 11)
def _(d, pal, img):
    """四种爪并排：钩的、抓的、挖的，还有干脆不用的。"""
    # 四只排成一行的话，格宽只有 241px，爪子就都缩到 216px 高、挤在页面底下一条。
    # 改成 2×2，每格宽一倍，爪子跟着大一倍，四只还是两两同基线、能直接比。
    xs, slot = lay(2)
    bases = (470, 962)
    ns, small = (8, 9, 10, 11), 0.33
    H = min(_fit(asset("claws", k), slot * 0.86, 400)[1] for k in ns[:3])
    got, th_ = [], []
    for i, (k, frac) in enumerate(zip(ns, (1, 1, 1, small))):
        x, base = xs[i % 2], bases[i // 2]
        got.append(place(img, asset("claws", k), x, base, h=H * frac, anchor="bottom"))
        th_.append(_thick(asset("claws", k), h=H * frac))
    for base in bases:
        d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    return (f"2 行 ×2 格，每行 1 条基线（格宽 {slot:.0f}px，每只在自己格子里居中）："
            f"1 只钩爪（素材8）/ 1 只抓握爪（素材9）/ 1 只铲爪（素材10）三只一样高 {H:.0f}px，"
            f"最粗的地方分别是 {th_[0]:.0f} / {th_[1]:.0f} / {th_[2]:.0f}px（钩最细、铲最粗）；"
            f"+ 1 只退化的小爪（素材11，高 {got[3][1]}px，只有前三只的 {small * 100:.0f}%）")


# ================================================================ tails 尾巴有什么用

@page("tails", 2)
def _(d, pal, img):
    """梁龙的尾巴是一节一节接起来的，八十二节。"""
    n, per = 82, 41
    tw, th = _fit(asset("tails", 1), S - 2 * MARGIN - 120, 300)     # 上一版只有 170px 高，太小
    w_, h_ = place(img, asset("tails", 1), S / 2, MARGIN + 30 + th / 2, w=tw)
    x0, x1 = MARGIN + 20, S - MARGIN - 20
    step = (x1 - x0) / per
    sw = step * 0.62
    h_top, h_end = 66, 10
    for i in range(n):
        r, c = divmod(i, per)
        x = x0 + step * (c + 0.5)
        cy = 500 + r * 300
        hh = h_top - (h_top - h_end) * i / (n - 1)
        d.rounded_rectangle([x - sw / 2, cy - hh / 2, x + sw / 2, cy + hh / 2],
                            radius=min(6, sw / 2), fill=pal["accent"] if i % 2 else pal["paper"],
                            outline=pal["ink"], width=3)
    arrow(d, x1 - 40, 560, x0 + 40, 700, pal, w=10, head=26)
    return (f"1 只梁龙（素材1，高 {h_}px）+ 它的尾巴拆成 {n} 节：上行 {per} 节、下行 {n - per} 节，"
            f"每节宽 {sw:.0f}px、中心距 {step:.1f}px（不重叠），高度从 {h_top}px 一路收细到 {h_end}px，"
            f"中间 1 支接着数下去的箭头")


@page("tails", 4)
def _(d, pal, img):
    """抬得起来是因为前后一样沉：头和脖子在前，尾巴在后，腿正好在中间。"""
    cx = S / 2
    w_, h_ = place(img, asset("tails", 1), cx, 290, w=S - 2 * MARGIN - 104)
    L = 380
    beam_y, gy = 700, 810
    d.line([cx - L, beam_y, cx + L, beam_y], fill=pal["ink"], width=14)
    poly(d, [(cx - 85, gy), (cx + 85, gy), (cx, beam_y)], pal, pal["accent"], 9)
    d.line([MARGIN, gy, S - MARGIN, gy], fill=pal["ink"], width=10)
    hbar(d, cx - L, 620, L, 56, pal, pal["soft"])
    hbar(d, cx, 620, L, 56, pal, pal["bark"])
    for s in (-1, 1):                                # 从头那头和尾那头各拉一条虚线下来
        _dash_v(d, cx + s * L, min(290 + h_ / 2 + 12, 560), 588, pal)
    return (f"1 只梁龙（素材1，宽 {w_}px）+ 下面 1 根架在支点上的横梁：左臂 {L}px（头和脖子）/ "
            f"右臂 {L}px（尾巴），两边严格等长，支点（1 个三角形）正在正中间，两端各 1 条虚线")


@page("tails", 6)
def _(d, pal, img):
    """尾巴里藏着一大块肉，一头连尾骨、一头连大腿，一使劲腿就往后蹬。"""
    base = S - MARGIN - 140
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    cx = S / 2
    w_, h_ = place(img, asset("tails", 2), cx, base, w=S - 2 * MARGIN - 60, anchor="bottom")
    top = base - h_
    ax, ay = cx - w_ / 2 + w_ * 0.74, top + h_ * 0.50      # 尾骨那一头
    bx, by = cx - w_ / 2 + w_ * 0.46, top + h_ * 0.74      # 大腿那一头
    poly(d, [(ax, ay - 46), (ax - w_ * 0.06, ay + 52), (bx + w_ * 0.04, by + 66),
             (bx - w_ * 0.03, by - 20), (ax - w_ * 0.12, ay - 70)],
         pal, pal["accent"], 8)
    mlen = math.hypot(ax - bx, ay - by)
    arrow(d, bx - w_ * 0.02, by + 90, bx + w_ * 0.16, by + 150, pal, w=12, head=30)
    return (f"1 只霸王龙（素材2，宽 {w_}px）+ 1 块从尾骨连到大腿的肌肉（1 个 5 边形，两头相距 {mlen:.0f}px）"
            f"+ 1 支往后蹬的箭头")


@page("tails", 8)
def _(d, pal, img):
    """尖上甩得那么快，也许真会啪的一声。"""
    ln = S - 2 * MARGIN - 180
    w_, h_ = place(img, lie_flat(asset("tails", 3)), S / 2 - 40, S / 2 + 40, w=ln)
    tipx = S / 2 - 40 + w_ / 2
    for k in range(3):                                # 尖上三道甩出来的弧
        r = 90 + k * 52
        d.arc([tipx - r, S / 2 + 40 - r, tipx + r, S / 2 + 40 + r], 300, 60,
              fill=pal["soft"], width=9)
    n = _star(d, tipx - 10, S / 2 - 200, 84, pal, n=10)
    return (f"1 根横躺的鞭子（素材3，长 {w_}px、高 {h_}px）+ 尖上 3 道弧线（半径 90/142/194px）"
            f"+ 1 个 {n} 角的爆响星（半径 84px）")


@page("tails", 11)
def _(d, pal):
    """尾巴有四样用处：撑着的、甩响的、打人的、管平衡的。"""
    xs, slot = lay(4)
    top, bot = 330, 760
    for k, x in enumerate(xs):
        tail = [(x - slot * 0.30, top), (x - slot * 0.04, top),
                (x + slot * 0.24, bot), (x + slot * 0.18, bot)]
        poly(d, tail, pal, pal["soft"], 8)
        tx, ty = x + slot * 0.21, bot - 6
        if k == 0:                                    # 撑在地上
            d.line([x - slot * 0.36, bot + 60, x + slot * 0.36, bot + 60],
                   fill=pal["ink"], width=10)
            d.line([tx, ty, tx, bot + 60], fill=pal["ink"], width=14)
        elif k == 1:                                  # 甩出响声
            for j in range(3):
                r = 46 + j * 34
                d.arc([tx - r, ty - r, tx + r, ty + r], 300, 60, fill=pal["accent"], width=8)
        elif k == 2:                                  # 尖上一个骨锤
            disc(d, tx, ty + 30, 56, pal["bark"], pal, w=9)
        else:                                         # 架在支点上
            poly(d, [(x - 50, bot + 70), (x + 50, bot + 70), (x, bot - 10)], pal, pal["accent"], 8)
            d.line([x - slot * 0.34, bot - 10, x + slot * 0.34, bot - 10], fill=pal["ink"], width=10)
    return (f"4 格并排（间距 {slot:.0f}px），每格 1 条一样的尾巴：第 1 条撑在地线上 / "
            f"第 2 条尖上 3 道甩响的弧 / 第 3 条尖上 1 个骨锤 / 第 4 条架在 1 个支点上")


# ================================================================ fingers 恐龙有几根手指

@page("fingers", 2)
def _(d, pal, img):
    """五根 → 三根 → 两根，一步一步少下去。"""
    marks = [(0.08, None, "最早"), (0.50, None, "后来"), (0.92, None, "再往后")]
    y = 700
    note = timeline(img, d, pal, "fingers", marks, y=y)
    x0, x1 = MARGIN + 50, S - MARGIN - 50
    ns = ((2, 5), (4, 3), (5, 2))                       # (素材号, 手指数)
    H = min(_fit(asset("fingers", a), 320, 560)[1] for a, _ in ns)
    got = []
    for (t, _a, _lab), (a, k) in zip(marks, ns):
        im = asset("fingers", a)
        w = im.width * H / im.height
        # 时间线两端的手会甩出画外，先算出宽度再把中心夹回页内
        cx = min(max(x0 + (x1 - x0) * t, MARGIN + w / 2), S - MARGIN - w / 2)
        got.append(place(img, im, cx, y - 44, h=H, anchor="bottom"))
        # 手指数是旁白点名的，交给素材就没人保证了：线下面再点 k 个点，数目由程序管
        dxs, dot = lay(k, width=min(w, 230), margin=0)
        for dx in dxs:
            disc(d, cx - min(w, 230) / 2 + dx, y + 64, 15, pal["accent"], pal, w=5)
    return (note + f"；线上 3 只手（素材2 / 4 / 5），一样高 {H:.0f}px、"
            f"宽 {got[0][0]}/{got[1][0]}/{got[2][0]}px，"
            f"每只手下面 1 排点标出手指数：从左到右 {ns[0][1]} 个 / {ns[1][1]} 个 / {ns[2][1]} 个点")


@page("fingers", 3)
def _(d, pal, img):
    """先没的是最外边那两根 —— 它们本来就又细又短。"""
    hand = asset("fingers", 2)
    hw, hh = _fit(hand, S - 2 * MARGIN - 120, S - 2 * MARGIN - 180)
    cx, cy = S / 2, S / 2 + 20
    hw, hh = place(img, hand, cx, cy, w=hw)
    # 叉不按比例猜：张开的手，最外两根的指尖就是整张素材最左、最右的实心点，直接量
    r = 54
    pts = []
    for side in (-1, 1):
        # 量到的是指尖最外那一点，叉心往里挪半个叉，整个叉才压在手指上而不是半个悬在外面
        ex, ey = _extreme(hand, hw, hh, side)
        pts.append((cx - hw / 2 + ex - side * r * 0.5, cy - hh / 2 + ey))
    for x, y in pts:
        cross(d, x, y, r, pal)
    return (f"1 只正面五指手（素材2，宽 {hw}px 高 {hh}px）+ 最外边 2 根手指上各 1 个叉"
            f"（半径 {r}px，叉心按素材最左 / 最右的实心点量出来，相距 {pts[1][0] - pts[0][0]:.0f}px"
            f" = 手宽的 {(pts[1][0] - pts[0][0]) / hw * 100:.0f}%），中间 3 根没有叉")


@page("fingers", 5)
def _(d, pal, img):
    """只剩两根，还长在一条很短的胳膊上，跟大脑袋比小得不像话。"""
    w_, h_ = place(img, asset("fingers", 1), S / 2, 700, h=600, anchor="bottom")
    top = 700 - h_
    for sx, sy, rx in ((0.22, 0.12, 0.13), (0.40, 0.44, 0.10)):      # 大脑袋 / 很短的前肢
        hx = S / 2 - w_ / 2 + w_ * sx
        hy = top + h_ * sy
        d.ellipse([hx - w_ * rx, hy - h_ * 0.09, hx + w_ * rx, hy + h_ * 0.09],
                  outline=pal["accent"], width=12)
    x0 = MARGIN + 60
    full = S - 2 * MARGIN - 120
    frac = 0.45
    hbar(d, x0, 810, full, 62, pal, pal["accent"])
    hbar(d, x0, 920, full * frac, 62, pal, pal["soft"])
    d.line([x0, 760, x0, 970], fill=pal["ink"], width=8)
    return (f"1 只霸王龙（素材1，高 {h_}px）+ 2 个圈（大脑袋 / 很短的前肢）+ 下面 2 根左端对齐的横条："
            f"脑袋 {full}px / 前肢 {full * frac:.0f}px（只有脑袋的 {frac * 100:.0f}%）")


@page("fingers", 7)
def _(d, pal):
    """第三根没有全没：肉里还埋着一小截骨头，外面看不出来。"""
    cx, cy = S / 2, 620
    d.rounded_rectangle([cx - 250, cy, cx + 250, cy + 250], radius=46,
                        fill=pal["soft"], outline=pal["ink"], width=9)
    for dx in (-140, 10):                                # 外面看得见的两根手指（皮）
        d.rounded_rectangle([dx + cx - 78, cy - 330, dx + cx + 78, cy + 40], radius=78,
                            fill=pal["soft"], outline=pal["ink"], width=9)
    L1 = 480
    for dx in (-140, 10):                                # 里面的两根长指骨
        d.rounded_rectangle([dx + cx - 34, cy - 300, dx + cx + 34, cy + L1 - 300], radius=34,
                            fill=pal["paper"], outline=pal["ink"], width=7)
    L2 = 150
    d.rounded_rectangle([cx + 160 - 34, cy + 60, cx + 160 + 34, cy + 60 + L2], radius=34,
                        fill=pal["accent"], outline=pal["ink"], width=7)
    return (f"1 只手的皮肤轮廓（外面只看得见 2 根手指）+ 里面 3 根指骨：2 根长 {L1}px 一直伸进手指，"
            f"第 3 根只有 {L2}px（前两根的 {L2 / L1 * 100:.0f}%），整根埋在手掌轮廓里、没有露出来")


@page("fingers", 9)
def _(d, pal, img):
    """一只手上摆着三样东西：一根钉、三个蹄，最外边那根还能弯过来夹树枝。"""
    base = S - MARGIN - 70
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    hand = asset("fingers", 6)
    hw, hh = _fit(hand, 620, 700)
    twig = asset("fingers", 7)
    tw, th = _fit(twig, 210, 560)
    over = tw * 0.30                               # 树枝压在手的外指底下，才像被夹住
    span = hw + tw - over
    hx = (S - span) / 2 + hw / 2                   # 手和树枝当成一组居中，别都挤在左边
    tx = hx + hw / 2 - over + tw / 2
    tx = min(tx, S - MARGIN - 20 - tw / 2)
    tw, th = place(img, twig, tx, base - 40, w=tw, anchor="bottom")
    hw, hh = place(img, hand, hx, base, w=hw, anchor="bottom")
    return (f"1 条地线 + 1 只禽龙的手（素材6，宽 {hw}px 高 {hh}px：钉、蹄、弯过来的外指都在素材里）"
            f"+ 1 根树枝（素材7，宽 {tw}px 高 {th}px），树枝先贴、手后贴，"
            f"两件横向重叠 {hx + hw / 2 - (tx - tw / 2):.0f}px（树枝的左边 {(hx + hw / 2 - (tx - tw / 2)) / tw * 100:.0f}% 被手压住 = 夹住）")


@page("fingers", 11)
def _(d, pal, img):
    """今天的鸟，翅膀里面还藏着三根手指。"""
    wing = asset("fingers", 8)
    ww, wh = _fit(wing, S - 2 * MARGIN - 40, S - 2 * MARGIN - 120)
    cx, cy = S / 2, S / 2 + 20
    ww, wh = place(img, wing, cx, cy, w=ww)
    left, top = cx - ww / 2, cy - wh / 2
    rx, ry = _centroid(wing, ww, wh)               # 根部取翅膀的重心，一定在翅膀里面
    angs = (-0.40, -0.12, 0.16)
    # 三根从同一个点出发会叠成一团乱线（上一版就是个「W」）：根部沿垂直方向各错开 70px，
    # 三根才是三根手指的样子
    perp = sum(angs) / 3 + math.pi / 2
    roots = [(rx + s * 70 * math.cos(perp), ry + s * 70 * math.sin(perp)) for s in (-1, 0, 1)]
    lens = [_reach(wing, x, y, a, ww, wh) for (x, y), a in zip(roots, angs)]
    # 骨头画在满是羽毛的底子上，不开一扇窗就只是三道白划痕：
    # 先盖一块半透明的浅色（等于把这一小片翅膀照透），骨头再画在窗上
    R = max(lens) + 80
    win = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(win).ellipse([left + rx - R * 0.40, top + ry - R * 0.60,
                                 left + rx + R * 0.96, top + ry + R * 0.60],
                                fill=tuple(_rgb(pal["paper"])) + (188,))
    img.paste(win, (0, 0), win)
    for (x, y), a, L in zip(roots, angs, lens):
        # 每根的长度是顺着这个方向量出来的「还在翅膀里面」的距离，所以指尖不会戳出轮廓。
        # 画法照 limb()：先描一道粗的墨线，再压一道细的填充线 —— 等于一根有描边的骨头
        x0, y0 = left + x, top + y
        x1, y1 = x0 + L * math.cos(a), y0 + L * math.sin(a)
        d.line([x0, y0, x1, y1], fill=pal["ink"], width=34)
        d.line([x0, y0, x1, y1], fill=pal["paper"], width=20)
        disc(d, x0, y0, 22, pal["paper"], pal, w=7)                 # 腕这一头的关节
        disc(d, x1, y1, 16, pal["paper"], pal, w=7)                 # 指尖那一头
    return (f"1 只张开的鸟翅膀（素材8，宽 {ww}px 高 {wh}px）+ 翅膀上 1 块半透明的窗"
            f"（{1.36 * R:.0f}×{1.20 * R:.0f}px，像照透了一样）+ 窗里 3 根手指骨"
            f"（长 {lens[0]:.0f} / {lens[1]:.0f} / {lens[2]:.0f}px，根部沿垂直方向各错开 70px、"
            f"两头各 1 个关节；每根的长度按素材自己的 alpha 量到轮廓内为止，3 根都埋在翅膀里面）")


# ================================================================ aircell 骨头里为什么有空气

@page("aircell", 2)
def _(d, pal):
    """锯开看：里面几乎是空的，只有薄薄的骨片横一道竖一道撑着。"""
    x0, x1 = MARGIN + 90, S - MARGIN - 90
    y0, y1 = S / 2 - 230, S / 2 + 230
    wall = 26
    d.rounded_rectangle([x0, y0, x1, y1], radius=64, fill=pal["paper"], outline=pal["ink"], width=14)
    d.rounded_rectangle([x0 + wall, y0 + wall, x1 - wall, y1 - wall], radius=48,
                        fill=pal["ground"], outline=pal["ink"], width=6)
    ix0, ix1 = x0 + wall, x1 - wall
    iy0, iy1 = y0 + wall, y1 - wall
    nv, nh = 7, 4
    for i in range(nv):
        x = ix0 + (ix1 - ix0) * (i + 1) / (nv + 1)
        d.line([x, iy0, x, iy1], fill=pal["soft"], width=9)
    for j in range(nh):
        y = iy0 + (iy1 - iy0) * (j + 1) / (nh + 1)
        d.line([ix0, y, ix1, y], fill=pal["soft"], width=9)
    return (f"1 根锯开的骨头：外壁厚 {wall}px，中间是空的；里面 {nh} 道横骨片 + {nv} 道竖骨片，"
            f"一共 {nh + nv} 道，围出 {(nh + 1) * (nv + 1)} 个小空格")


@page("aircell", 4)
def _(d, pal, img):
    """空的不等于不结实：自行车车架就是根空管子，照样压不弯。"""
    L = 180
    for (cx, cy, w_, h_), a in zip(panel2(d, pal), (1, 2)):
        place(img, asset("aircell", a), cx, cy + h_ * 0.32, h=h_ * 0.46, anchor="bottom")
        arrow(d, cx, cy - h_ * 0.42, cx, cy - h_ * 0.42 + L, pal, w=13, head=30)
    return (f"左格 1 根空心车架管（素材1）/ 右格 1 根空心骨头（素材2），两格等大，"
            f"各 1 支一样长（{L}px）从正上方往下压的箭头，两样都还是直的")


@page("aircell", 6)
def _(d, pal):
    """梁龙脖子里十五节这样的骨头，一节一节都是空的。"""
    n, r = 15, 27
    pts = []
    for i in range(n):
        t = i / (n - 1)
        x = 140 + 760 * t
        y = 810 - 620 * t + 90 * math.sin(math.pi * t)
        pts.append((x, y))
    d.line(pts, fill=pal["ink"], width=12, joint="curve")
    for x, y in pts:
        disc(d, x, y, r, pal["paper"], pal, w=8)
        disc(d, x, y, r * 0.56, pal["ground"], pal, w=5)
    sp = min(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))
    return (f"1 条脖子上 {n} 节骨头（每节直径 {2 * r}px、最小中心距 {sp:.0f}px，不重叠），"
            f"每节中间 1 个空洞，一共 {n} 个空洞")


@page("aircell", 8)
def _(d, pal, img):
    """肺后面连着一串气袋，气袋一点一点钻进骨头里去。"""
    cy = S / 2 + 20
    note = steps(img, d, pal, "aircell", [None, None, 2], cy=cy)
    xs, slot = lay(3)
    poly(d, [(xs[0] - 95, cy - 150), (xs[0] + 95, cy - 190), (xs[0] + 110, cy + 60),
             (xs[0], cy + 185), (xs[0] - 110, cy + 70)], pal, pal["accent"], 9)
    sacs = 5
    for k in range(sacs):
        disc(d, xs[1], cy - 176 + k * 88, 40, pal["paper"], pal, w=7)
        if k:
            d.line([xs[1], cy - 176 + (k - 1) * 88 + 40, xs[1], cy - 176 + k * 88 - 40],
                   fill=pal["ink"], width=7)
    return (note + f"：第 1 步 1 个肺 / 第 2 步 1 串 {sacs} 个气袋（竖着串起来，间距 88px）/ "
            f"第 3 步 1 根骨头（素材2）")


@page("aircell", 10)
def _(d, pal):
    """鳄鱼的骨头实心，鸟的空心，恐龙的跟鸟一样。"""
    xs, slot = lay(3)
    cy = S / 2
    R = min(slot * 0.38, 190)
    wall = 34
    for i, x in enumerate(xs):
        disc(d, x, cy, R, pal["bark"], pal, w=11)
        if i:
            disc(d, x, cy, R - wall, pal["ground"], pal, w=7)
    return (f"3 个并排的骨头横截面（直径都是 {2 * R:.0f}px、间距 {slot:.0f}px）："
            f"第 1 个实心（鳄鱼，整片填满）/ 第 2 个空心（鸟，壁厚 {wall}px）/ "
            f"第 3 个空心（恐龙），第 2、3 个的壁厚一模一样")


# ================================================================ mother 恐龙会照顾宝宝吗

@page("mother", 2)
def _(d, pal, img):
    """窝是个泥坑，蛋一个挨一个竖在坑里。"""
    nest = asset("mother", 2)
    nw, nh = _fit(nest, 830, 720)               # 只卡宽度的话，换一张竖素材窝就顶穿页面
    nw, nh = place(img, nest, S / 2, 950, w=nw, anchor="bottom")
    e = asset("mother", 3)
    # 上一版一排六个、每个才 150px，蛋小得看不清。旁白没点数目（「一个挨一个」），
    # 所以减个数、把单个放大：后排 4 + 前排 3，最小的一个也有 210px 高
    back, front, back_h, front_h = 4, 3, 210, 250
    step = nw * 0.70 / (back - 1)
    x0 = S / 2 - nw * 0.35
    got = []
    for k in range(back):                      # 后排先贴，前排压住它们的下半截，看着才是「在坑里」
        got.append(place(img, e, x0 + k * step, 950 - nh * 0.42, h=back_h, anchor="bottom"))
    for k in range(front):
        got.append(place(img, e, x0 + step * (k + 0.5), 950 - nh * 0.20, h=front_h, anchor="bottom"))
    return (f"1 个窝（素材2，宽 {nw}px 高 {nh}px）+ 里面 {back + front} 个竖着的蛋（素材3）："
            f"后排 {back} 个（高 {back_h}px、宽 {got[0][0]}px）+ 前排 {front} 个"
            f"（高 {front_h}px、宽 {got[-1][0]}px、左右各错开半格），两排的中心距都是 {step:.0f}px，"
            f"蛋比间距宽，相邻两个挨着叠 {got[0][0] - step:.0f}px —— 一个挨一个排在坑里")


@page("mother", 3)
def _(d, pal, img):
    """那么大的恐龙，下出来的蛋只有柚子那么点。"""
    # 蛋要按比例才叫「只有这么一点」，可按比例画出来就只有 130px、看不清。
    # 所以地线上仍是真比例的小蛋，右上角再挂一个同一个蛋的放大件，两者用引线连起来。
    base = S - MARGIN - 130
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    dh = 430
    dw, dh = place(img, asset("mother", 1), MARGIN + 40 + _fit(asset("mother", 1), 700, dh)[0] / 2,
                   base, h=dh, anchor="bottom")
    egg = asset("mother", 3)
    eh = round(dh * 0.30)
    ew, eh = _fit(egg, 150, eh)
    ex = S - MARGIN - 20 - ew / 2
    ew, eh = place(img, egg, ex, base, w=ew, anchor="bottom")
    halo(img, egg, ex, base, w=ew, color=_rgb(pal["accent"]), grow=12, width=7, anchor="bottom")
    bw, bh = _fit(egg, 300, 320)
    bx, by = S - MARGIN - 30 - bw / 2, MARGIN + 40 + bh / 2
    d.line([ex, base - eh - 26, bx, by + bh / 2 + 20], fill=pal["line"], width=6)
    bw, bh = place(img, egg, bx, by, w=bw)
    return (f"1 条地线上 1 只鸭嘴龙（素材1，宽 {dw}px 高 {dh}px）+ 1 个同比例的蛋"
            f"（素材3，高 {eh}px，只有恐龙的 {eh / dh * 100:.0f}%）+ 沿蛋轮廓的 1 圈强调线；"
            f"右上角 1 个同一个蛋的放大件（高 {bh}px，是地线上那个的 {bh / eh:.1f} 倍）+ 1 条引线")


@page("mother", 5)
def _(d, pal):
    """小恐龙的腿骨两头还是软的，走不了远路。"""
    L, soft = 520, 56
    for (cx, cy, w_, h_), baby in zip(panel2(d, pal), (True, False)):
        _bone(d, cx, cy, L, pal, half=40, soft=soft if baby else 0)
    return (f"左格 1 根小恐龙的腿骨（长 {L}px），两头各 1 段还没长结实的软骨（共 2 段，各厚 {soft}px）/ "
            f"右格 1 根一样长 {L}px 的腿骨，0 段软骨，两格等大")


@page("mother", 6)
def _(d, pal, img):
    """小牙已经磨平了一点 —— 牙被磨平，就是吃过东西。"""
    boxes = panel2(d, pal)
    cx0, cy0, w0, h0 = boxes[0]
    # 两排牙画成一样宽、牙床落在同一条高度上：那么两排高度之差，就是磨掉的那一截
    # 两件的取景不一样（素材6 模型画成了整张嘴），所以只敢保证「一样宽、底边落在同一条线上」。
    # 高度差在这里不是牙磨掉多少，是两张图裁的框不一样——真磨掉多少，只能由素材自己画出来。
    W = min(_fit(asset("mother", k), w0 * 0.86, h0 * 0.56)[0] for k in (5, 6))
    gum_y = cy0 + h0 * 0.30
    got = []
    for (cx, cy, w_, h_), a in zip(boxes, (5, 6)):
        got.append(place(img, asset("mother", a), cx, gum_y, w=W, anchor="bottom"))
    seg = _dash_h(d, gum_y + 24, MARGIN + 20, S - MARGIN - 20, pal, col=pal["accent"])
    return (f"左格 1 排没磨过的尖牙（素材5，宽 {got[0][0]}px 高 {got[0][1]}px）/ "
            f"右格同一排、尖被磨平（素材6，宽 {got[1][0]}px 高 {got[1][1]}px）；"
            f"两件一样宽 {W:.0f}px、底边都落在 y={gum_y:.0f} 这一条线上（1 条横虚线，{seg} 段，"
            f"横穿两格），两格等大 —— 尖和平的差别只来自素材本身")


@page("mother", 8)
def _(d, pal, img):
    """一大片窝排在一起，窝和窝之间正好空出一只大恐龙那么长。"""
    # 恐龙的长度 = 两窝之间的空当（旁白点名的那一条），所以把窝的间距拉大，
    # 恐龙才跟着变大：上一版 gap=220 画出来的恐龙只有 110px 高
    rows, cols, R = 3, 3, 44
    gap = 348
    step = 2 * R + gap
    x0, y0 = S / 2 - step, S / 2 - step
    for r in range(rows):
        for c in range(cols):
            x, y = x0 + c * step, y0 + r * step
            disc(d, x, y, R, pal["bark"], pal, w=9)
            disc(d, x, y, R * 0.56, pal["ground"], pal, w=6)
    w_, h_ = place(img, asset("mother", 1), x0 + step / 2, y0 + step, w=gap)
    return (f"俯视 {rows * cols} 个窝（{rows} 行 ×{cols}，窝直径 {2 * R}px、窝心间距 {step}px、"
            f"两窝之间空着 {gap}px）+ 1 只大恐龙（素材1，长 {w_}px 高 {h_}px）横在中排相邻两窝中间，"
            f"体长正好等于那 {gap}px —— 两头各顶到一个窝的边上")


@page("mother", 11)
def _(d, pal, img):
    """不守窝的一次下几十个，守窝的下得少，可是看得住。"""
    e = asset("mother", 3)
    boxes = panel2(d, pal)
    lx, ly, lw, lh = boxes[0]
    # 左格上一版 30 个蛋、每个 84px，小得像米粒。半格宽 460px 装不下几十个 140px 的蛋，
    # 所以隔行错半格、让它们互相叠着堆成一窝 —— 数目一个不少，单个大了 67%
    rows, cols, eh = 6, 4, 130
    sx, sy = lw * 0.20, lh * 0.156
    ew, eh = _fit(e, sx * 1.40, eh)             # 蛋再横也不许超过这个宽度，否则整堆挤出格子
    got = []
    for r in range(rows):
        for c in range(cols):
            # 隔行各错半格的一半，两行都还是居中的，整堆不会往一边挤出格子
            got.append(place(img, e, lx + (c - (cols - 1) / 2) * sx + (sx / 4) * (1 if r % 2 else -1),
                             ly - lh * 0.34 + r * sy, w=ew, anchor="bottom"))
    rx, ry, rw, rh = boxes[1]
    disc(d, rx, ry, 190, pal["bark"], pal, w=10)
    disc(d, rx, ry, 132, pal["ground"], pal, w=7)
    n2, R2, eh2 = 6, 130, 185
    ew2, eh2 = _fit(e, 190, eh2)                # 同理：圈上的蛋也得卡住宽度
    for k in range(n2):
        a = math.radians(k * 360 / n2 - 90)
        place(img, e, rx + R2 * math.cos(a), ry + R2 * math.sin(a) + eh2 / 2, w=ew2, anchor="bottom")
    n1 = rows * cols
    return (f"左格 {n1} 个蛋（{rows} 行 ×{cols}，各高 {got[0][1]}px 宽 {got[0][0]}px、列距 {sx:.0f}px、"
            f"行距 {sy:.0f}px、隔行错开，同排相邻两个叠 {got[0][0] - sx:.0f}px，堆成一堆）/ "
            f"右格 1 个窝 + {n2} 个蛋绕成 1 圈（各高 {eh2:.0f}px、圈半径 {R2}px、"
            f"圈上间距 {2 * math.pi * R2 / n2:.0f}px）；两格等大，左边是右边的 {n1 // n2} 倍")


# ================================================================ herd 它们为什么一起走

@page("herd", 2)
def _(d, pal, img):
    """最大的那个脚印比脸盆还大，盆放进去还空出一圈。"""
    tw, th = place(img, asset("herd", 3), S / 2, S / 2, w=790)
    bw, bh = place(img, asset("herd", 4), S / 2, S / 2, w=430)
    ring = (tw - bw) / 2
    return (f"1 个俯视的脚印（素材3，宽 {tw}px）+ 正中间 1 个脸盆（素材4，宽 {bw}px），"
            f"盆放进去四周还空出 {ring:.0f}px 一圈，脚印是盆的 {tw / bw:.1f} 倍宽")


@page("herd", 3)
def _(d, pal, img):
    """脚印有两种：大的是后脚，小的是前脚。"""
    a = asset("herd", 3)
    bw, bh = place(img, a, S / 2 - 220, S / 2, w=440)
    sw, sh = place(img, a, S / 2 + 300, S / 2, w=250)
    return (f"2 个脚印（同 1 个素材3）：左边大的宽 {bw}px（后脚）/ 右边小的宽 {sw}px（前脚），"
            f"大的是小的 {bw / sw:.1f} 倍，两个中心相距 520px、互不相碰")


@page("herd", 5)
def _(d, pal, img):
    """没有哪一串压在另一串上面 —— 谁也没踩着谁。"""
    a = asset("herd", 3)
    rows, per, gy, gx, jit = 4, 6, 205, 152, 22
    pw, ph = _fit(a, gx - 24, gy - 2 * jit - 10)       # 脚印宽必须小于间距，这两条线才咬得住
    got = []
    for r in range(rows):
        y = 165 + r * gy
        for i in range(per):
            got.append(place(img, a, MARGIN + 110 + i * gx, y + (jit if i % 2 else -jit), w=pw))
    return (f"{rows} 串平行的脚印（素材3），每串 {per} 个，一共 {rows * per} 个；"
            f"每个宽 {got[0][0]}px 高 {got[0][1]}px，行距 {gy}px、同串间距 {gx}px、"
            f"串内左右错开 ±{jit}px —— 行距减去错开还有 {gy - 2 * jit}px，都大于脚印本身，"
            f"没有任何两个压在一起")


@page("herd", 6)
def _(d, pal, img):
    """大脚印走在两边，小脚印夹在中间。"""
    a = asset("herd", 3)
    xs, slot = lay(4)
    per, gy = 4, 230
    big = _fit(a, slot * 0.86, gy - 16)[0]
    small = big * 0.56                            # 大小两档只差在 place 的缩放上，形状是同一张素材
    got = []
    for i, x in enumerate(xs):
        for k in range(per):
            got.append((i, place(img, a, x, 180 + k * gy, w=big if i in (0, 3) else small)))
    bw = got[0][1][0]
    sw = got[per][1][0]
    return (f"俯视 4 串脚印（同 1 个素材3），每串 {per} 个（共 {4 * per} 个）："
            f"外侧 2 串是大脚印（宽 {bw}px）/ 中间 2 串是小脚印（宽 {sw}px，是大的 {sw / bw * 100:.0f}%），"
            f"大的在外、小的在里；串距 {slot:.0f}px、行距 {gy}px，都大于脚印本身，互不相碰")


@page("herd", 8)
def _(d, pal, img):
    """量一量两个脚印中间隔多远，就知道它走得多快 —— 步距一样长。"""
    a = asset("herd", 3)
    n, step, jit = 5, 185, 40
    x0, y, my = MARGIN + 120, 400, 800
    pw, ph = _fit(a, step - 26, 180)
    got = []
    for i in range(n):
        got.append(place(img, a, x0 + i * step, y + (jit if i % 2 else -jit), w=pw))
        d.line([x0 + i * step, my - 34, x0 + i * step, my + 34], fill=pal["ink"], width=8)
        _dash_v(d, x0 + i * step, y + jit + ph / 2 + 16, my - 44, pal)
    for i in range(n - 1):
        arrow(d, x0 + i * step + 12, my, x0 + (i + 1) * step - 12, my, pal, w=7, head=18)
    return (f"1 串 {n} 个脚印（素材3，各宽 {got[0][0]}px 高 {got[0][1]}px，左右错开 ±{jit}px）"
            f"+ 下面 {n - 1} 段一样长的步距（各 {step}px，都大于脚印宽），"
            f"每个脚印下拉 1 条虚线到 {n} 道竖刻度上")


@page("herd", 10)
def _(d, pal, img):
    """一片树叶吃光了就往前挪一挪，再找一片。"""
    base = S - MARGIN - 50
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    t_full, t_bare = asset("herd", 5), asset("herd", 6)
    # 两棵树画成一样高：一棵有叶一棵光秃，差别只能来自素材本身，不能来自我缩放
    th = min(_fit(t, 300, 380)[1] for t in (t_full, t_bare))
    tree_base = 440
    tw1, th1 = place(img, t_full, 200, tree_base, h=th, anchor="bottom")
    tw2, th2 = place(img, t_bare, S - 200, tree_base, h=th, anchor="bottom")
    arrow(d, S - 200 - tw2 / 2 - 30, 260, 200 + tw1 / 2 + 30, 260, pal, w=12, head=30)
    big, small = asset("herd", 1), asset("herd", 2)
    ah, jh, gap = 300, 210, 40
    aw = big.size[0] * ah / big.size[1]
    jw = small.size[0] * jh / small.size[1]
    total = 2 * aw + jw + 2 * gap
    if total > S - 2 * MARGIN:                       # 素材太长就整队一起缩，绝不各缩各的
        k = (S - 2 * MARGIN) / total
        ah, jh, aw, jw, gap, total = ah * k, jh * k, aw * k, jw * k, gap * k, S - 2 * MARGIN
    x = (S - total) / 2
    for _ in range(2):
        aw, ah = place(img, big, x + aw / 2, base, h=ah, anchor="bottom")
        x += aw + gap
    jw, jh = place(img, small, x + jw / 2, base, h=jh, anchor="bottom")
    return (f"上面 2 棵一样高 {th1}px 的树：左边 1 棵有叶子的（素材5，宽 {tw1}px）/ "
            f"右边 1 棵光秃的（素材6，宽 {tw2}px）+ 1 支朝左（往下一片树去）的箭头；"
            f"下面地线上 3 只恐龙朝左走：2 只大的（素材1，各高 {ah:.0f}px、宽 {aw:.0f}px）+ "
            f"1 只小的（素材2，高 {jh:.0f}px、宽 {jw:.0f}px，是大的 {jh / ah * 100:.0f}%），"
            f"彼此隔开 {gap:.0f}px，整队宽 {total:.0f}px、居中放在地线上")
