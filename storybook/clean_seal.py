#!/usr/bin/env python3
"""涂掉水墨风页面角落里模型自己加的红色印章（Qwen 画水墨淡彩时常在右下角盖一个假章）。

用法: python clean_seal.py [--out=<目录>] <图片> [<图片> ...]
      默认原地修改，原图先备份到同目录的 _orig/ 里。
只看四个角各 12% 的方块；红色块太大（占角落 80% 以上）就当作画面内容，不动。
"""
import sys, os, shutil
import numpy as np
from PIL import Image
sys.stdout.reconfigure(encoding="utf-8")

def clean(path, out=None):
    im = np.asarray(Image.open(path).convert("RGB")).astype(np.int32)
    h, w, _ = im.shape
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    red = (r > 140) & (r - g > 22) & (r - b > 30)   # 淡印章只有 r-g≈30，所以阈值放得很宽，只在角落里用
    s = int(min(h, w) * 0.12)
    found = []
    for y0, x0 in [(h - s, w - s), (h - s, 0), (0, w - s), (0, 0)]:
        m = red[y0:y0 + s, x0:x0 + s]
        if m.sum() < 30:
            continue
        ys, xs = np.nonzero(m)
        if np.ptp(ys) > s * 0.8 or np.ptp(xs) > s * 0.8:
            continue
        pad = 6
        Y1, Y2 = max(y0 + ys.min() - pad, 0), min(y0 + ys.max() + pad + 1, h)
        X1, X2 = max(x0 + xs.min() - pad, 0), min(x0 + xs.max() + pad + 1, w)
        ring = np.concatenate([a.reshape(-1, 3) for a in (
            im[max(Y1 - 8, 0):Y1, X1:X2], im[Y2:Y2 + 8, X1:X2], im[Y1:Y2, max(X1 - 8, 0):X1], im[Y1:Y2, X2:X2 + 8])
            if a.size])
        im[Y1:Y2, X1:X2] = np.median(ring, axis=0)
        found.append((X1, Y1, X2, Y2))
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
