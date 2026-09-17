# -*- coding: utf-8 -*-
"""第七批示意图页（1/5）：剑龙、甲龙、爪子、尾巴、手指、骨头里的空气、照顾宝宝、成群走。"""
from draw_diagrams import (S, MARGIN, page, asset, place, lie_flat, poly, disc, arrow, cross,
                           lay, panel2, hbar, footprint, bands, cmp_len, cmp_height, cmp_count,
                           bars, timeline, steps, magnify)
import math, random


# ---------------------------------------------------------------- 这一批自己要用的小图元
# 只放通用图元里没有、而且这八本里反复出现的几样：爪、手、骨头、树、爆响星。

def _claw(d, x, y, L, ang, pal, fill=None, curve=0.9, thick=0.30, w=7, n=16):
    """一只爪：从 (x, y) 出发，长 L，起始方向 ang（弧度），curve 越大越弯，thick 是根部半宽比。

    长度和弯度都是参数，所以「宽钝的铲爪」和「细尖的钩爪」差多少是算出来的，不是画出来的。
    返回爪尖坐标。
    """
    outer, inner = [], []
    tip = (x, y)
    for i in range(n + 1):
        t = i / n
        a = ang + curve * t
        px, py = x + L * t * math.cos(a), y + L * t * math.sin(a)
        th = thick * L * (1 - t) ** 1.1
        outer.append((px + th * math.cos(a - math.pi / 2), py + th * math.sin(a - math.pi / 2)))
        inner.append((px + th * math.cos(a + math.pi / 2), py + th * math.sin(a + math.pi / 2)))
        tip = (px, py)
    poly(d, outer + inner[::-1], pal, fill if fill is not None else pal["paper"], w)
    return tip


def _claw_span(L, ang, curve, n=16):
    """一只爪横向占多宽（返回相对起点的 (最左, 最右)）。

    弯爪的爪尖会甩出去很远：curve=1.3 的爪，尖端几乎横在起点右边一整个 L。
    并排画几只爪时先用这个把每只在自己格子里摆正，不然右边那只会甩进隔壁格。
    """
    xs = [L * (i / n) * math.cos(ang + curve * i / n) for i in range(n + 1)]
    return min(xs), max(xs)


def _hand(d, cx, cy_palm, W, pal, n, lens=None, widths=None, fill=None, claw=0.0):
    """一只正面的手：手掌 + n 根手指。lens/widths 给每根的相对长短和粗细。

    手指先画、手掌后画压住指根 —— 反过来画的话，每根手指的下端会有一道横线穿过手掌。
    返回每根手指的 (x, 指尖y, 半宽, 长度)。
    """
    lens = list(lens or [1.0] * n)
    widths = list(widths or [1.0] * n)
    pw = W * 0.72
    base = W * 0.62
    slot = pw / n
    out = []
    for i in range(n):
        x = cx - pw / 2 + slot * (i + 0.5)
        hw = slot * 0.32 * widths[i]
        L = base * lens[i]
        d.rounded_rectangle([x - hw, cy_palm - L, x + hw, cy_palm + W * 0.10], radius=hw,
                            fill=fill if fill is not None else pal["paper"],
                            outline=pal["ink"], width=6)
        if claw:
            poly(d, [(x - hw, cy_palm - L), (x, cy_palm - L - base * claw), (x + hw, cy_palm - L)],
                 pal, pal["accent"], 5)
        out.append((x, cy_palm - L, hw, L))
    d.rounded_rectangle([cx - pw / 2 - W * 0.04, cy_palm, cx + pw / 2 + W * 0.04,
                         cy_palm + W * 0.46], radius=W * 0.10,
                        fill=fill if fill is not None else pal["paper"],
                        outline=pal["ink"], width=8)
    return out


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


def _tree(d, cx, base, h, pal, leaves=12, cols=6):
    """一棵树：树干 + 两根枝 + 正好 leaves 片叶子（排成 cols 列几行，片数由参数保证）。"""
    d.rounded_rectangle([cx - h * 0.055, base - h * 0.55, cx + h * 0.055, base],
                        radius=h * 0.03, fill=pal["bark"], outline=pal["ink"], width=7)
    for s in (-1, 1):
        d.line([cx, base - h * 0.50, cx + s * h * 0.26, base - h * 0.80],
               fill=pal["ink"], width=10)
    k = 0
    rows = math.ceil(leaves / cols) if leaves else 0
    for r in range(rows):
        for c in range(cols):
            if k >= leaves:
                break
            lx = cx - h * 0.30 + c * (h * 0.60 / max(1, cols - 1))
            ly = base - h * 0.98 + r * h * 0.155
            d.ellipse([lx - h * 0.042, ly - h * 0.028, lx + h * 0.042, ly + h * 0.028],
                      fill=pal["soft"], outline=pal["ink"], width=4)
            k += 1
    return leaves


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


# ================================================================ stego 剑龙背上的板

@page("stego", 2)
def _(d, pal, img):
    """背上一共十七块板，沿着背脊一路排到尾巴根 —— 十七块就是十七块。"""
    n = 17
    x0, x1 = MARGIN + 50, S - MARGIN - 50
    step = (x1 - x0) / (n - 1)
    plate = asset("stego", 2)
    spine = [(x0 + (x1 - x0) * i / 60, 760 - 150 * math.sin(math.pi * i / 60)) for i in range(61)]
    d.line(spine, fill=pal["ink"], width=12, joint="curve")
    ws = []
    for i in range(n):
        t = i / (n - 1)
        x = x0 + (x1 - x0) * t
        y = 760 - 150 * math.sin(math.pi * t)
        # 每块的宽度都小于间距，所以相邻两块一定不会叠在一起
        w_, h_ = place(img, plate, x, y + 14, w=step * 0.88 * (0.58 + 0.42 * math.sin(math.pi * t)),
                       anchor="bottom")
        ws.append((w_, h_))
    return (f"1 条背脊线 + 沿线 {n} 块板（素材2），间距 {step:.0f}px、每块宽 {ws[0][0]}～{ws[n // 2][0]}px"
            f"（都小于间距，没有两块重叠），最高的一块 {max(h for _, h in ws)}px 在正中间")


@page("stego", 3)
def _(d, pal):
    """板不长在脊椎上：它们插在皮里，和脊椎之间还隔着一段空当。"""
    skin_top, skin_h = 520, 120
    d.rectangle([MARGIN, skin_top, S - MARGIN, skin_top + skin_h],
                fill=pal["soft"], outline=pal["ink"], width=8)
    n_v = 9
    vy = skin_top + skin_h + 190
    xs, slot = lay(n_v)
    for x in xs:
        d.rounded_rectangle([x - slot * 0.34, vy - 48, x + slot * 0.34, vy + 48], radius=16,
                            fill=pal["bark"], outline=pal["ink"], width=6)
    n_p = 5
    px, pslot = lay(n_p)
    for x in px:
        # 板底扎进皮里（比皮底还高 14px），所以是「插在皮里」而不是「立在皮上」
        poly(d, [(x - 72, skin_top + skin_h - 14), (x, skin_top - 300), (x + 72, skin_top + skin_h - 14)],
             pal, pal["paper"], 8)
    clear = (vy - 48) - (skin_top + skin_h)
    arrow(d, S / 2, (skin_top + skin_h + vy - 48) / 2 - 8, S / 2, skin_top + skin_h + 6, pal, w=7, head=20)
    arrow(d, S / 2, (skin_top + skin_h + vy - 48) / 2 + 8, S / 2, vy - 54, pal, w=7, head=20)
    return (f"1 层皮（厚 {skin_h}px）+ 皮下 {n_v} 块脊椎骨 + 插在皮里的 {n_p} 块板（每块底宽 144px、"
            f"间距 {pslot:.0f}px）；板底和脊椎之间空着 {clear}px，没有一块碰到脊椎")


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
    w_, h_ = place(img, asset("stego", 1), cx, cy, w=S - 2 * MARGIN - 80)
    hx = cx - w_ / 2 + w_ * 0.09
    hy = cy - h_ / 2 + h_ * 0.66
    d.ellipse([hx - w_ * 0.075, hy - h_ * 0.13, hx + w_ * 0.075, hy + h_ * 0.13],
              outline=pal["accent"], width=12)
    nr = 48
    nx, ny = MARGIN + 150, S - MARGIN - 110
    d.line([hx, hy + h_ * 0.13, nx, ny - nr], fill=pal["line"], width=6)
    disc(d, nx, ny, nr, pal["bark"], pal, w=9)
    d.line([nx, ny - nr, nx, ny + nr], fill=pal["ink"], width=6)   # 核桃的那道缝
    return (f"1 只剑龙（素材1，宽 {w_}px）+ 1 个圈住小脑袋的圈 + 左下角 1 颗核桃"
            f"（直径 {2 * nr}px）+ 1 条把核桃和头连起来的引线")


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
    mr = W / 2
    mx = MARGIN + 100 + W + 70 + mr
    disc(d, mx, base - mr, mr, pal["soft"], pal, w=10)
    for a in (0.28, 0.60, 0.88):                 # 西瓜的条纹：三道同心的竖椭圆
        d.ellipse([mx - mr * a, base - 2 * mr, mx + mr * a, base], outline=pal["ink"], width=7)
    return (f"1 个尾锤（素材2，宽 {cw}px 高 {ch}px）+ 中间 1 道把它分成 2 块骨头的竖虚线（{seg} 段）"
            f"+ 右边 1 个同样宽 {2 * mr:.0f}px 的西瓜（3 道条纹），两个站在同一条地线上，中心相距 {mx - (MARGIN + 100 + W / 2):.0f}px")


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
    full = S - 2 * MARGIN - 120
    x0, cy = MARGIN + 60, S / 2
    bl = full * 0.70
    bw, bh = place(img, lie_flat(asset("claws", 2)), x0 + bl / 2, cy, w=bl)
    # 壳的轮廓按骨头量出来的实际高度画，保证一定包得住，尖端再往前伸一截
    pts = [(x0 - 24, cy - bh / 2 - 26), (x0 + full, cy - 18),
           (x0 + full, cy + 18), (x0 - 24, cy + bh / 2 + 26)]
    for a, b in zip(pts, pts[1:] + pts[:1]):
        d.line([a, b], fill=pal["accent"], width=11)
    return (f"1 层爪壳的轮廓（长 {full}px）+ 里面 1 根横躺的爪骨（素材2，长 {bw}px、高 {bh}px），"
            f"壳比骨头多伸出 {full - bw:.0f}px，骨头只有壳的 {bw / full * 100:.0f}%")


@page("claws", 3)
def _(d, pal, img):
    """镰刀龙的爪子，是所有恐龙里最长的一双手 —— 圈出来看。"""
    return magnify(img, d, pal, "claws", 1, (0.33, 0.62), r=0.10)


@page("claws", 5)
def _(d, pal):
    """脚上的爪：第二个脚趾翘着，挂着一只大钩子。"""
    gy = 780
    d.line([MARGIN, gy, S - MARGIN, gy], fill=pal["ink"], width=10)
    ax, ay = 660, 500                                               # 踝
    mx, my = 570, 690                                               # 跖骨下端，三根趾都从这里分出去
    d.line([720, 170, ax, ay], fill=pal["ink"], width=48)           # 小腿
    d.line([ax, ay, mx, my], fill=pal["ink"], width=38)             # 跖骨
    small, big, lift = 64, 210, 150
    for tx in (340, 455):                                           # 两根踩在地上的趾：趾尖正好落在地线上
        d.line([mx, my, tx, gy], fill=pal["ink"], width=28)
        _claw(d, tx, gy, small, math.pi - 0.22, pal, pal["paper"], curve=0.55, thick=0.34)
    hx, hy = mx - 200, gy - lift                                    # 第二趾翘起来离地
    d.line([mx, my, hx, hy], fill=pal["ink"], width=28)
    _claw(d, hx, hy, big, 3.30, pal, pal["accent"], curve=1.10, thick=0.28)
    return (f"1 只侧视的脚：3 根脚趾，2 根的趾尖正好落在地线上（爪长 {small}px），"
            f"第 2 根翘起来离地 {lift}px、挂着 1 只大钩爪（长 {big}px，是另外两只的 {big / small:.1f} 倍）")


@page("claws", 7)
def _(d, pal):
    """前面三根手指都带爪，三根能合到一起抓住东西。"""
    n = 3
    tip_sp = []
    for (cx, cy, w_, h_), closed in zip(panel2(d, pal), (False, True)):
        palm_y = cy + h_ * 0.16
        L = h_ * 0.26
        # 左右两根的弯度取相反的符号，三根才是对称的一把
        spec = ((-1.35, 0.20), (-1.57, 0.0), (-1.79, -0.20)) if closed else                ((-1.95, -0.22), (-1.57, 0.0), (-1.19, 0.22))
        if closed:
            disc(d, cx, palm_y - L * 0.92, 54, pal["accent"], pal, w=8)
        tips = []
        for k, (a, cv) in enumerate(spec):
            x = cx + (k - 1) * w_ * 0.16
            tips.append(_claw(d, x, palm_y, L, a, pal, pal["soft"], curve=cv, thick=0.16))
        d.rounded_rectangle([cx - w_ * 0.26, palm_y, cx + w_ * 0.26, palm_y + h_ * 0.16],
                            radius=42, fill=pal["paper"], outline=pal["ink"], width=9)
        tip_sp.append(abs(tips[2][0] - tips[0][0]))
    return (f"左格 1 只手 {n} 根张开的爪（爪尖相距 {tip_sp[0]:.0f}px）/ 右格同样 {n} 根合拢，"
            f"爪尖收到相距 {tip_sp[1]:.0f}px，三只一起抓住中间 1 个直径 108px 的东西；两格等大、爪数一样")


@page("claws", 9)
def _(d, pal, img):
    """挖土的爪又宽又钝像把铲，抓肉的爪又细又尖像把钩。"""
    wide, thin = 0.42, 0.13
    for (cx, cy, w_, h_), dig in zip(panel2(d, pal), (True, False)):
        place(img, asset("claws", 3 if dig else 2), cx, cy - h_ * 0.30, h=h_ * 0.30)
        _claw(d, cx - (140 if dig else 90), cy + h_ * 0.30, h_ * 0.34,
              -1.15 if dig else -1.35, pal,
              pal["bark"] if dig else pal["accent"],
              curve=0.35 if dig else 1.05, thick=wide if dig else thin)
    return (f"左格 1 把铲（素材3）+ 1 只又宽又钝的爪（根部半宽是长度的 {wide * 100:.0f}%、弯 0.35 弧度）/ "
            f"右格 1 只又细又尖的爪骨（素材2）+ 1 只钩（根部半宽只有长度的 {thin * 100:.0f}%、弯 1.05 弧度），"
            f"左边那只比右边粗 {wide / thin:.1f} 倍，两格等大")


@page("claws", 11)
def _(d, pal):
    """四种爪并排：钩的、抓的、挖的，还有干脆不用的。"""
    xs, slot = lay(4)
    cy = 660
    ang = -1.95
    specs = [(270, 1.30, 0.13, "accent"), (270, 0.70, 0.20, "soft"),
             (270, 0.30, 0.42, "bark"), (88, 0.55, 0.26, "paper")]
    wide = 0
    for x, (L, cv, th, key) in zip(xs, specs):
        lo, hi = _claw_span(L, ang, cv)
        ox = x - (lo + hi) / 2                        # 每只爪在自己格子里居中
        wide = max(wide, hi - lo)
        d.line([ox - 66, cy + 40, ox + 66, cy + 40], fill=pal["ink"], width=26)   # 指根
        _claw(d, ox, cy + 30, L, ang, pal, pal[key], curve=cv, thick=th)
    return (f"4 种爪并排（格宽 {slot:.0f}px，每只按自己的横向占位居中，最宽的一只占 {wide:.0f}px）："
            f"1 只钩（长 270px、弯 1.30）/ 1 只抓（长 270px、弯 0.70）/ "
            f"1 只铲（长 270px、弯 0.30、根部最粗）/ 1 只退化的小短爪（只有 88px，是前三只的 33%）")


# ================================================================ tails 尾巴有什么用

@page("tails", 2)
def _(d, pal, img):
    """梁龙的尾巴是一节一节接起来的，八十二节。"""
    n, per = 82, 41
    w_, h_ = place(img, asset("tails", 1), S / 2, 150, h=170)
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
    note = timeline(img, d, pal, "fingers", marks, y=670)
    x0, x1 = MARGIN + 50, S - MARGIN - 50
    ns = (5, 3, 2)
    for (t, _a, _lab), n in zip(marks, ns):
        _hand(d, x0 + (x1 - x0) * t, 460, 215, pal, n)
    return note + f"；线上 3 只手，从左到右 {ns[0]} 根 / {ns[1]} 根 / {ns[2]} 根手指"


@page("fingers", 3)
def _(d, pal):
    """先没的是最外边那两根 —— 它们本来就又细又短。"""
    W, cx, cy = 640, S / 2, 660
    lens = [0.42, 1.00, 1.06, 1.00, 0.42]
    fs = _hand(d, cx, cy, W, pal, 5, lens=lens, widths=[0.45, 1, 1, 1, 0.45])
    for i in (0, 4):
        cross(d, fs[i][0], fs[i][1] - 76, 46, pal)
    inner = fs[2][3]
    outer = fs[0][3]
    return (f"1 只手 5 根手指：中间 3 根长 {inner:.0f}px、最外边 2 根只有 {outer:.0f}px"
            f"（是中间那几根的 {outer / inner * 100:.0f}%）、也只有一半粗；最外边 2 根各画 1 个叉")


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
def _(d, pal):
    """一只手上摆着三样东西：一根钉、三个蹄，最外边那根还能弯过来夹树枝。"""
    cx, cy = S / 2 - 60, 580
    d.rounded_rectangle([cx - 250, cy, cx + 250, cy + 230], radius=44,
                        fill=pal["paper"], outline=pal["ink"], width=9)
    spike = 300
    poly(d, [(cx - 200 - 44, cy + 10), (cx - 200, cy - spike), (cx - 200 + 44, cy + 10)],
         pal, pal["accent"], 8)
    hoof_w, hoof_l = 44, 230
    for i in range(3):
        x = cx - 100 + i * 100
        d.rounded_rectangle([x - hoof_w, cy - hoof_l, x + hoof_w, cy + 10], radius=hoof_w,
                            fill=pal["paper"], outline=pal["ink"], width=7)
        disc(d, x, cy - hoof_l, hoof_w * 1.02, pal["bark"], pal, w=7)
    twig_x = cx + 350
    d.rounded_rectangle([twig_x - 26, cy - 320, twig_x + 26, cy + 120], radius=26,
                        fill=pal["bark"], outline=pal["ink"], width=7)
    _claw(d, cx + 200, cy, 190, -1.30, pal, pal["soft"], curve=1.45, thick=0.19)
    return (f"1 只手 5 根指：1 根钉子（尖，长 {spike}px）+ 3 个蹄（钝，各宽 {2 * hoof_w}px、长 {hoof_l}px、"
            f"间距 100px）+ 最外边 1 根弯过来（弯 1.45 弧度）夹住 1 根树枝")


@page("fingers", 11)
def _(d, pal):
    """今天的鸟，翅膀里面还藏着三根手指。"""
    cx, cy = S / 2, S / 2 + 40
    wing = [(cx - 390, cy + 70), (cx - 310, cy - 130), (cx - 60, cy - 230), (cx + 220, cy - 200),
            (cx + 390, cy - 60), (cx + 300, cy + 100), (cx + 40, cy + 180), (cx - 230, cy + 170)]
    poly(d, wing, pal, pal["soft"], 10)
    lens = (380, 440, 300)
    for a, L in zip((-0.30, -0.12, 0.08), lens):
        _claw(d, cx - 150, cy + 30, L, a, pal, pal["paper"], curve=0.10, thick=0.09)
    return (f"1 只翅膀的轮廓 + 里面 3 根手指骨（长 {lens[0]} / {lens[1]} / {lens[2]}px，"
            f"从同一个根部散开，全都包在翅膀轮廓里面）")


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
    nw, nh = place(img, asset("mother", 2), S / 2, 950, w=830, anchor="bottom")
    e = asset("mother", 3)
    per, back_h, front_h = 6, 150, 178
    step = nw * 0.70 / (per - 1)
    x0 = S / 2 - nw * 0.35
    for k in range(per):                       # 后排先贴，前排压住它们的下半截，看着才是「在坑里」
        place(img, e, x0 + k * step, 950 - nh * 0.42, h=back_h, anchor="bottom")
    for k in range(per):
        place(img, e, x0 + step * 0.5 + (k - 0.5) * step, 950 - nh * 0.22, h=front_h, anchor="bottom")
    return (f"1 个窝（素材2，宽 {nw}px）+ 里面 {2 * per} 个竖着的蛋（素材3）："
            f"后排 {per} 个（高 {back_h}px）+ 前排 {per} 个（高 {front_h}px、左右各错开半格），"
            f"每排间距 {step:.0f}px，一个挨一个排在坑里")


@page("mother", 3)
def _(d, pal, img):
    """那么大的恐龙，下出来的蛋只有柚子那么点。"""
    return cmp_height(img, d, pal, "mother",
                      [(1, 370, S / 2 - 120), (3, 130, S / 2 + 380)])


@page("mother", 5)
def _(d, pal):
    """小恐龙的腿骨两头还是软的，走不了远路。"""
    L, soft = 520, 56
    for (cx, cy, w_, h_), baby in zip(panel2(d, pal), (True, False)):
        _bone(d, cx, cy, L, pal, half=40, soft=soft if baby else 0)
    return (f"左格 1 根小恐龙的腿骨（长 {L}px），两头各 1 段还没长结实的软骨（共 2 段，各厚 {soft}px）/ "
            f"右格 1 根一样长 {L}px 的腿骨，0 段软骨，两格等大")


@page("mother", 6)
def _(d, pal):
    """小牙已经磨平了一点 —— 牙被磨平，就是吃过东西。"""
    n, sharp, worn = 6, 230, 150
    for (cx, cy, w_, h_), is_worn in zip(panel2(d, pal), (False, True)):
        gum_y = cy + 40
        step = w_ * 0.68 / (n - 1)
        for i in range(n):
            x = cx - w_ * 0.34 + i * step
            if is_worn:
                poly(d, [(x - 26, gum_y), (x - 13, gum_y - worn), (x + 13, gum_y - worn),
                         (x + 26, gum_y)], pal, pal["paper"], 7)
            else:
                poly(d, [(x - 26, gum_y), (x, gum_y - sharp), (x + 26, gum_y)],
                     pal, pal["paper"], 7)
        d.rounded_rectangle([cx - w_ * 0.42, gum_y, cx + w_ * 0.42, gum_y + 120], radius=32,
                            fill=pal["soft"], outline=pal["ink"], width=8)
    return (f"左格 {n} 颗没磨过的尖牙（尖高 {sharp}px）/ 右格同样 {n} 颗、尖被磨平"
            f"（只剩 {worn}px，削掉了 {sharp - worn}px），两格牙数一样、牙宽都是 52px")


@page("mother", 8)
def _(d, pal, img):
    """一大片窝排在一起，窝和窝之间正好空出一只大恐龙那么长。"""
    rows, cols, R = 3, 3, 48
    gap = 220
    step = 2 * R + gap
    x0, y0 = S / 2 - step, 230
    for r in range(rows):
        for c in range(cols):
            x, y = x0 + c * step, y0 + r * step
            disc(d, x, y, R, pal["bark"], pal, w=9)
            disc(d, x, y, R * 0.56, pal["ground"], pal, w=6)
    w_, h_ = place(img, asset("mother", 1), x0 + step / 2, y0, w=gap)
    return (f"俯视 {rows * cols} 个窝（{rows} 行 ×{cols}，窝直径 {2 * R}px、窝心间距 {step}px）+ "
            f"1 只大恐龙（素材1）横在上排相邻两窝中间，体长 {w_}px 正好等于两窝之间空着的 {gap}px")


@page("mother", 11)
def _(d, pal, img):
    """不守窝的一次下几十个，守窝的下得少，可是看得住。"""
    e = asset("mother", 3)
    boxes = panel2(d, pal)
    lx, ly, lw, lh = boxes[0]
    rows, cols, eh = 5, 6, 84
    step = lw * 0.84 / cols
    for r in range(rows):
        for c in range(cols):
            place(img, e, lx - lw * 0.42 + step * (c + 0.5), ly - lh * 0.28 + r * 118,
                  h=eh, anchor="bottom")
    rx, ry, rw, rh = boxes[1]
    disc(d, rx, ry, 190, pal["bark"], pal, w=10)
    disc(d, rx, ry, 132, pal["ground"], pal, w=7)
    n2, R2, eh2 = 6, 132, 140
    for k in range(n2):
        a = math.radians(k * 360 / n2 - 90)
        place(img, e, rx + R2 * math.cos(a), ry + R2 * math.sin(a) + eh2 / 2, h=eh2, anchor="bottom")
    return (f"左格 {rows * cols} 个蛋（{rows} 行 ×{cols}，各高 {eh}px、间距 {step:.0f}px）/ "
            f"右格 1 个窝 + {n2} 个蛋绕成 1 圈（各高 {eh2}px、圈半径 {R2}px、圈上间距 {2 * math.pi * R2 / n2:.0f}px），"
            f"两格等大，左边是右边的 {rows * cols // n2} 倍")


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
def _(d, pal):
    """没有哪一串压在另一串上面 —— 谁也没踩着谁。"""
    rows, per, s, gy, gx = 4, 6, 92, 196, 152
    for r in range(rows):
        y = 180 + r * gy
        for i in range(per):
            footprint(d, MARGIN + 110 + i * gx, y + (26 if i % 2 else -26), s, pal,
                      pal["bark"] if r % 2 else pal["soft"])
    return (f"{rows} 串平行的脚印，每串 {per} 个，一共 {rows * per} 个；"
            f"行距 {gy}px、同串间距 {gx}px，都大于脚印宽 {s}px，没有任何两个压在一起")


@page("herd", 6)
def _(d, pal):
    """大脚印走在两边，小脚印夹在中间。"""
    xs = (150, 400, 650, 890)
    per, big, small = 5, 132, 76
    for i, x in enumerate(xs):
        s = big if i in (0, 3) else small
        for k in range(per):
            footprint(d, x, 180 + k * 166, s, pal, pal["bark"] if i in (0, 3) else pal["soft"])
    return (f"俯视 {len(xs)} 串脚印，每串 {per} 个（共 {len(xs) * per} 个）："
            f"外侧 2 串是大脚印（宽 {big}px）/ 中间 2 串是小脚印（宽 {small}px），"
            f"大的在外、小的在里，串距 250px")


@page("herd", 8)
def _(d, pal):
    """量一量两个脚印中间隔多远，就知道它走得多快 —— 步距一样长。"""
    n, step, s = 5, 190, 110
    x0, y, my = MARGIN + 130, 420, 780
    for i in range(n):
        footprint(d, x0 + i * step, y + (40 if i % 2 else -40), s, pal, pal["bark"])
        d.line([x0 + i * step, my - 34, x0 + i * step, my + 34], fill=pal["ink"], width=8)
        _dash_v(d, x0 + i * step, y + 110, my - 44, pal)
    for i in range(n - 1):
        arrow(d, x0 + i * step + 12, my, x0 + (i + 1) * step - 12, my, pal, w=7, head=18)
    return (f"1 串 {n} 个脚印（宽 {s}px）+ 下面 {n - 1} 段一样长的步距（各 {step}px），"
            f"每个脚印下拉 1 条虚线到 {n} 道竖刻度上")


@page("herd", 10)
def _(d, pal, img):
    """一片树叶吃光了就往前挪一挪，再找一片。"""
    base = S - MARGIN - 50
    d.line([MARGIN, base, S - MARGIN, base], fill=pal["ink"], width=10)
    full, bare = 12, 0
    _tree(d, 175, 350, 250, pal, leaves=full)
    _tree(d, 850, 350, 250, pal, leaves=bare)
    arrow(d, 640, 250, 370, 250, pal, w=12, head=30)
    big, small = asset("herd", 1), asset("herd", 2)
    ah, jh, gap = 165, 108, 40
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
    return (f"上面 2 棵树：左边 1 棵还满着的（{full} 片叶子）/ 右边 1 棵吃光的（{bare} 片叶子）"
            f"+ 1 支朝左（往下一片树去）的箭头；下面地线上 3 只恐龙朝左走："
            f"2 只大的（素材1，各高 {ah}px、宽 {aw}px）+ 1 只小的（素材2，高 {jh}px、宽 {jw}px），"
            f"彼此隔开 {gap:.0f}px，整队宽 {total:.0f}px、居中放在地线上")
