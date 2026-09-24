# -*- coding: utf-8 -*-
"""Crop a drawn frame border off bakeoff pages. usage: unframe.py [--dry] slug:n,n ...
Per edge: scan the first 70 px for a line (more than half the pixels darker than THR),
follow it to its inner side, cut 8 px past it; then scale back to the original size.
The original is kept as out/bakeoff/_old/<name>_framed.png."""
import os, shutil, sys
import numpy as np
from PIL import Image
BAKE = r"C:\FlowDev\githubdevitems\comfyUIItems\storybook\out\bakeoff"
THR, SCAN, PAD = 175, 70, 8
dry = "--dry" in sys.argv


def edge(lines):
    """lines: dark fraction per row/col from the edge inwards; returns how much to cut."""
    for i in range(SCAN):
        if lines[i] > 0.5:
            if i and lines[:i].max() > 0.3:
                return 0                      # something drawn outside it: not a frame
            j = i
            while j + 1 < len(lines) and lines[j + 1] > 0.5 and j - i < 12:
                j += 1
            if j - i < 12:
                return j + 1 + PAD            # a thin line
            if i >= 5:
                return i + 6 + PAD            # inset picture with dark content right inside the line
            return 0                          # dark content running off the edge (grass, a trunk)
    return 0


for a in [x for x in sys.argv[1:] if x != "--dry"]:
    slug, ns = a.split(":")
    for n in ns.split(","):
        f = os.path.join(BAKE, f"{slug}_p{int(n):02d}_lightning8.png")
        im = Image.open(f).convert("RGB")
        g = np.asarray(im.convert("L")) < THR
        rows, cols = g.mean(axis=1), g.mean(axis=0)
        t, b = edge(rows), edge(rows[::-1])
        l, r = edge(cols), edge(cols[::-1])
        W, H = im.size
        print(f"{slug} p{n}: top {t} bottom {b} left {l} right {r}")
        if dry or not (t or b or l or r):
            continue
        old = os.path.join(BAKE, "_old", f"{slug}_p{int(n):02d}_lightning8_framed.png")
        os.makedirs(os.path.dirname(old), exist_ok=True)
        if not os.path.exists(old):
            shutil.copy2(f, old)
        x0, y0, x1, y1 = l, t, W - r, H - b
        s = min(x1 - x0, y1 - y0)                  # keep it square: trim the longer side evenly
        x0 += (x1 - x0 - s) // 2
        y0 += (y1 - y0 - s) // 2
        im.crop((x0, y0, x0 + s, y0 + s)).resize((W, H), Image.LANCZOS).save(f)
