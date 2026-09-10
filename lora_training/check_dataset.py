#!/usr/bin/env python3
"""检查 LoRA 训练素材质量。用法：python check_dataset.py raw/"""
import sys, os, glob
from collections import Counter
try:
    from PIL import Image
except ImportError:
    sys.exit("需要 Pillow：ComfyUI/venv/bin/pip install pillow")

d = sys.argv[1] if len(sys.argv) > 1 else "raw"
files = sorted(sum([glob.glob(os.path.join(d, e)) for e in
                    ("*.jpg","*.jpeg","*.png","*.JPG","*.JPEG","*.PNG","*.heic","*.HEIC")], []))
if not files:
    sys.exit(f"{d}/ 里没有图片。把照片放进去再跑。")

print(f"共 {len(files)} 张\n")
small, sizes, ratios = [], [], Counter()
for f in files:
    try:
        im = Image.open(f); w, h = im.size
    except Exception as e:
        print(f"  ⚠️  {os.path.basename(f)} 读不了: {e}"); continue
    sizes.append((w, h, f))
    if min(w, h) < 1024: small.append((os.path.basename(f), w, h))
    r = round(w/h, 2)
    ratios[("竖图" if r < 0.9 else "横图" if r > 1.1 else "方图")] += 1

print("=== 数量 ===")
n = len(files)
print(f"  {n} 张 —— " + ("✅ 合适（15~30 最佳）" if 15 <= n <= 30
      else "⚠️ 偏少，建议补到 15 张以上" if n < 15
      else "⚠️ 偏多，30 张以内就够，多了容易过拟合"))

print("\n=== 分辨率 ===")
if small:
    print(f"  ⚠️ {len(small)} 张短边小于 1024，训练时会被放大，细节会糊：")
    for nm, w, h in small[:5]: print(f"      {nm}  {w}×{h}")
else:
    print("  ✅ 全部短边 ≥1024")

print("\n=== 构图比例 ===")
for k, v in ratios.items(): print(f"  {k}: {v} 张")
if len(ratios) == 1:
    print("  ⚠️ 全是同一种比例，建议混一些不同构图")

print("\n=== 还需要你自己确认的（脚本查不了）===")
print("  □ 角度：正脸/侧脸/3-4 侧都有吗？")
print("  □ 表情：至少 3~4 种不同表情？")
print("  □ 背景：够多样吗？（全同一背景 = 背景会被学进 LoRA）")
print("  □ 衣服：别全是同一件")
print("  □ 遮挡：有没有墨镜、口罩、手挡脸的")
print("  □ 其他人：照片里最好只有你一个人")
