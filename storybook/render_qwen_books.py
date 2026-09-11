#!/usr/bin/env python3
"""整本出图（Qwen 路线）：有他的页用 Qwen-Image-Edit Q3 + 两张照片，其他页用 Qwen-Image-2512 Lightning 8 步。

用法: python storybook/render_qwen_books.py <照片1> <照片2> <slug> [<slug> ...]
  照片放在 ComfyUI/input/ 里，这里只写文件名。
  顺序：先画所有书没有他的页（文生图），再换一次模型画有他的页（Edit）。
  story JSON 里写了 "restyle_ref": <页码> 的书，没有他的页再多一步：用 Edit 模型把文生图那张
  照这一页（必须是有他的页）的画风重画（edit_qwen.py --restyle）。印刷类画风（孔版、复古网点）
  的文生图容易画成加了滤镜的照片，这一步把整本书拉回同一个画风。
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
INPUT = os.path.join(ROOT, "ComfyUI", "input")
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

def bake(slug, n, kind):
    return os.path.join(BAKE, f"{slug}_p{n:02d}_{kind}.png")

def page_file(slug, st, p):
    """这一页最终用哪张图。"""
    if p["has_boy"]:
        return bake(slug, p["n"], "edit8v2_q3_k_m")
    if st.get("restyle_ref"):
        return bake(slug, p["n"], "restyle8_q3_k_m")
    return bake(slug, p["n"], "lightning8")

def main(ref1, ref2, slugs):
    stories = {s: json.load(open(os.path.join(SB, f"story_{s}.json"), encoding="utf-8")) for s in slugs}
    target = lambda s, p: f"storybook/story_{s}.json:{p['n']}"

    # 1. 文生图：没有他的页，最终图和文生图底稿都还没有的
    t2i = [target(s, p) for s, st in stories.items() for p in st["pages"]
           if not p["has_boy"] and not os.path.exists(page_file(s, st, p))
           and not os.path.exists(bake(s, p["n"], "lightning8"))]
    if t2i:
        print(f"文生图：{len(t2i)} 张", flush=True)
        free()
        print("t2i 退出码", run([os.path.join(SB, "bakeoff_qwen.py"), "lightning8"] + t2i))

    # 2. Edit：有他的页
    boy = [target(s, p) for s, st in stories.items() for p in st["pages"]
           if p["has_boy"] and not os.path.exists(page_file(s, st, p))]
    restyle = {s: [target(s, p) for p in st["pages"] if not p["has_boy"] and not os.path.exists(page_file(s, st, p))]
               for s, st in stories.items() if st.get("restyle_ref")}
    restyle = {s: t for s, t in restyle.items() if t}
    if boy or restyle:
        free()
    if boy:
        print(f"有他的页：{len(boy)} 张", flush=True)
        print("edit 退出码", run([os.path.join(SB, "edit_qwen.py"), "--v2", f"--unet={EDIT_UNET}", ref1, ref2] + boy))

    # 3. Edit：照本书样板页重画（同一个模型，不用换）
    for s, targets in restyle.items():
        n = stories[s]["restyle_ref"]
        ref = bake(s, n, "edit8v2_q3_k_m")
        if not os.path.exists(ref):
            print(f"{s}: 样板页 p{n} 还没画出来，跳过重画", flush=True)
            continue
        style_name = f"style_{s}_p{n:02d}.png"
        shutil.copy2(ref, os.path.join(INPUT, style_name))
        print(f"{s}：照第 {n} 页重画 {len(targets)} 张", flush=True)
        print("restyle 退出码", run([os.path.join(SB, "edit_qwen.py"), "--restyle", f"--unet={EDIT_UNET}",
                                    "unused.png", style_name] + targets))

    # 4. 拼书、联系表、网页
    for s, st in stories.items():
        dst = os.path.join(OUT, f"{s}_qwen")
        os.makedirs(dst, exist_ok=True)
        missing = []
        for p in st["pages"]:
            f = page_file(s, st, p)
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
