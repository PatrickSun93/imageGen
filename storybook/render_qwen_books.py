#!/usr/bin/env python3
"""整本出图（Qwen 路线）：有他的页用 Qwen-Image-Edit Q3 + 两张照片，其他页用 Qwen-Image-2512 Lightning 8 步。

用法: python storybook/render_qwen_books.py <照片1> <照片2> <slug> [<slug> ...]
  照片放在 ComfyUI/input/ 里，这里只写文件名。
  先把所有书有他的页一次画完，再换模型画其他页（整批只换一次模型）。
  out/bakeoff/ 里已经有的页直接跳过，所以中断后重跑就能续上；想重画某页，先删掉那张图。
  每本画完：拼到 out/<slug>_qwen/，水墨风的书自动去印章（clean_seal.py），
  出联系表 out/<slug>_qwen_sheet.png，打包网页 out/web_<slug>/index.html。
"""
import os, sys, json, glob, shutil, subprocess, urllib.request
sys.stdout.reconfigure(encoding="utf-8")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SB = os.path.join(ROOT, "storybook")
OUT = os.path.join(SB, "out")
BAKE = os.path.join(OUT, "bakeoff")
EDIT_UNET = "qwen-image-edit-2511-Q3_K_M.gguf"
PY = sys.executable
ENV = {**os.environ, "PYTHONIOENCODING": "utf-8"}   # 子进程输出重定向到文件时也能打中文

def run(args, cwd=ROOT, out=None):
    """out 给了就把 stdout 写进去（网页），报错照样进日志。"""
    sys.stdout.flush()
    return subprocess.run([PY] + args, cwd=cwd, env=ENV, stdout=out or sys.stdout,
                          stderr=sys.stdout if out else subprocess.STDOUT).returncode

def free():
    try:
        urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:8188/free", json.dumps(
            {"unload_models": True, "free_memory": True}).encode(), {"Content-Type": "application/json"}))
    except Exception as e:
        print("free 失败:", e)

def page_file(slug, p):
    kind = "edit8v2_q3_k_m" if p["has_boy"] else "lightning8"
    return os.path.join(BAKE, f"{slug}_p{p['n']:02d}_{kind}.png")

def main(ref1, ref2, slugs):
    stories = {s: json.load(open(os.path.join(SB, f"story_{s}.json"), encoding="utf-8")) for s in slugs}
    def todo(boy):
        return [f"storybook/story_{s}.json:{p['n']}" for s, st in stories.items() for p in st["pages"]
                if p["has_boy"] == boy and not os.path.exists(page_file(s, p))]

    boy = todo(True)
    if boy:
        print(f"有他的页：{len(boy)} 张", flush=True)
        free()
        print("edit 退出码", run([os.path.join(SB, "edit_qwen.py"), "--v2", f"--unet={EDIT_UNET}", ref1, ref2] + boy))
    rest = todo(False)
    if rest:
        print(f"其他页：{len(rest)} 张", flush=True)
        free()
        print("t2i 退出码", run([os.path.join(SB, "bakeoff_qwen.py"), "lightning8"] + rest))

    for s, st in stories.items():
        dst = os.path.join(OUT, f"{s}_qwen")
        os.makedirs(dst, exist_ok=True)
        missing = []
        for p in st["pages"]:
            f = page_file(s, p)
            if os.path.exists(f):
                shutil.copy2(f, os.path.join(dst, f"page_{p['n']:02d}.png"))
            else:
                missing.append(p["n"])
        if "ink wash" in st["style"]:
            run(["clean_seal.py"] + sorted(glob.glob(os.path.join(dst, "page_*.png"))), cwd=SB)
        run(["contact_sheet.py", f"out/{s}_qwen", f"out/{s}_qwen_sheet.png"], cwd=SB)
        web = os.path.join(OUT, f"web_{s}")
        run(["pack_images.py", f"out/{s}_qwen", f"out/web_{s}"], cwd=SB)
        with open(os.path.join(web, "index.html"), "w", encoding="utf-8") as html:
            run(["build_web.py", f"story_{s}.json", f"out/web_{s}"], cwd=SB, out=html)
        print(f"{s}: 缺页 {missing or '无'}，网页 out/web_{s}/index.html", flush=True)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2], sys.argv[3:])
