#!/usr/bin/env python3
"""用 Qwen-Image-Edit 对一张成品页做一处小修改（比如去掉车头上模型自己画的笑脸），其余保持不变。

用法: python storybook/fix_edit.py <图片.png> "<英文修改指令>" [输出.png]
例:   python storybook/fix_edit.py storybook/out/bakeoff/digger_p03_restyle8_q3_k_m.png \
          "Remove the smiling face painted on the front of the yellow truck, leaving plain yellow metal with two round headlights."
不给输出路径时写到原图旁边的 <原名>_fix.png；原图不动。需要 ComfyUI 在 8188 上运行。
"""
import os, sys, shutil, time
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import edit_qwen as eq

eq.UNET = "qwen-image-edit-2511-Q3_K_M.gguf"
KEEP = " Keep everything else in the picture exactly the same: the same composition, colors, line work and style."

def main(src, instruction, dst=None):
    dst = dst or src.replace(".png", "_fix.png")
    name = "fix_" + os.path.basename(src)
    shutil.copy2(src, os.path.join(eq.INPUT, name))
    t0 = time.time()
    f = eq.submit("Picture 1 is a page from a children's picture book. " + instruction + KEEP, 1, "fix_" +
                  os.path.splitext(os.path.basename(src))[0], [name, name])
    shutil.copy2(os.path.join(eq.ROOT, "ComfyUI", "output", f[0]), dst)
    print(f"{dst}  {time.time() - t0:.0f}s")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(*sys.argv[1:4])
