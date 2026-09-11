#!/usr/bin/env python3
"""涂掉水墨风页面角落里模型自己加的红色印章（Qwen 画水墨淡彩时常在右下角、有时两个角都盖一个假章）。

用法: python clean_seal.py [--out=<目录>] <图片> [<图片> ...]
      默认原地修改，原图先备份到同目录的 _orig/ 里。
只看四个角各 12% 的方块。角里偏粉红的像素按连通块分开看：够大（≥30 像素）又紧凑（不超过角落的 60%）
的块当作印章，用四周的纸色盖掉；零星的小点和大片的暖色晕染都不动。
"""
import sys, os, shutil
import numpy as np
from PIL import Image
from scipy import ndimage
sys.stdout.reconfigure(encoding="utf-8")

def clean(path, out=None):
    im = np.asarray(Image.open(path).convert("RGB")).astype(np.int32)
    h, w, _ = im.shape
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    # 淡印章只比米色纸 r-g 高 10～25（纸本身 r-g≈4、g-b≈16）；g-b 小是粉红的特征，用来排除黄色晕染
    red = (r > 140) & (r - g > 12) & (r - b > 20) & (g - b < 30)
    s = int(min(h, w) * 0.12)
    found = []
    # 只看下面两个角：假章都盖在下角；上角常有天空和阳光的暖色，会误判
    for y0, x0 in [(h - s, w - s), (h - s, 0)]:
        m = red[y0:y0 + s, x0:x0 + s]
        if m.sum() < 30:
            continue
        # 印章的笔画是断开的细线，先膨胀几像素再分块，同一枚章才会连成一块
        labels, n = ndimage.label(ndimage.binary_dilation(m, iterations=3))
        for i in range(1, n + 1):
            ys, xs = np.nonzero((labels == i) & m)
            if len(ys) < 30:
                continue
            if np.ptp(ys) > s * 0.6 or np.ptp(xs) > s * 0.6:   # 印章约 50px 见方；更大的是画面里的暖色，不动
                continue
            pad = 6
            Y1, Y2 = max(y0 + ys.min() - pad, 0), min(y0 + ys.max() + pad + 1, h)
            X1, X2 = max(x0 + xs.min() - pad, 0), min(x0 + xs.max() + pad + 1, w)
            ring = np.concatenate([a.reshape(-1, 3) for a in (
                im[max(Y1 - 8, 0):Y1, X1:X2], im[Y2:Y2 + 8, X1:X2], im[Y1:Y2, max(X1 - 8, 0):X1], im[Y1:Y2, X2:X2 + 8])
                if a.size])
            # 真章盖在空白纸上：四周至少四分之三是亮纸（允许几粒墨点）；画面里的暖色块四周是颜料，不算
            if np.percentile(ring.mean(axis=1), 25) < 200:
                continue
            im[Y1:Y2, X1:X2] = np.median(ring, axis=0)
            found.append((int(X1), int(Y1), int(X2), int(Y2)))
    if not found:
        print(f"{path}: 没有印章")
        return False
    if out:
        dst = os.path.join(out, os.path.basename(path))
    else:
        keep = os.path.join(os.path.dirname(path) or ".", "_orig")
        os.makedirs(keep, exist_ok=True)
        if not os.path.exists(os.path.join(keep, os.path.basename(path))):
            shutil.copy2(path, keep)
        dst = path
    Image.fromarray(im.astype(np.uint8)).save(dst)
    print(f"{path}: 涂掉 {len(found)} 处 {found} → {dst}")
    return True

if __name__ == "__main__":
    args, out = sys.argv[1:], None
    if args and args[0].startswith("--out="):
        out = args.pop(0)[6:]
        os.makedirs(out, exist_ok=True)
    for p in args:
        clean(p, out)
