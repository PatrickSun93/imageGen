# -*- coding: utf-8 -*-
"""measure: frames.py m slug_pNN ...   -> per edge: dark line span (<170, middle band) and paper-margin end (<225, full width)
   crop:    frames.py c slug_pNN=px ... -> keeps the original as _old/<name>_lightning8_framed.png, crops px all round"""
import os, shutil, sys
import numpy as np
from PIL import Image
B = r"C:\FlowDev\githubdevitems\comfyUIItems\storybook\out\bakeoff"
mode, items = sys.argv[1], sys.argv[2:]
for it in items:
    if mode == "m":
        g = np.asarray(Image.open(os.path.join(B, it + "_lightning8.png")).convert("L"), dtype=np.float32)
        H = g.shape[0]; band = slice(H // 2 - 150, H // 2 + 150)
        edges = {"T": (g[:120, band].mean(1), g[:120].mean(1)), "B": (g[::-1][:120, band].mean(1), g[::-1][:120].mean(1)),
                 "L": (g[band, :120].mean(0), g[:, :120].mean(0)), "R": (g[band, ::-1][:, :120].mean(0), g[:, ::-1][:, :120].mean(0))}
        out = []
        for k, (dark, full) in edges.items():
            d = [i for i in range(120) if dark[i] < 170]
            m = [i for i in range(120) if full[i] < 225]
            out.append(f"{k} dark {d[0] if d else '-'}..{d[-1] if d else '-'} margin {m[0] if m else '-'}")
        print(it, " | ".join(out))
    else:
        name, px = it.split("="); px = int(px)
        f = os.path.join(B, name + "_lightning8.png")
        old = os.path.join(B, "_old", name + "_lightning8_framed.png")
        if not os.path.exists(old):
            shutil.copy2(f, old)
        im = Image.open(old).convert("RGB"); W, H = im.size
        im.crop((px, px, W - px, H - px)).resize((W, H), Image.LANCZOS).save(f)
        print("cropped", name, px)
