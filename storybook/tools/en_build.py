# -*- coding: utf-8 -*-
"""English web book + print PDF for each slug (uses the Chinese book's pages in out/<slug>_qwen).
usage (any cwd): en_build.py [--noprint] slug ..."""
import os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
SB = r"C:\FlowDev\githubdevitems\comfyUIItems\storybook"
PY = r"C:\FlowDev\githubdevitems\comfyUIItems\venv\python.exe"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
args = [a for a in sys.argv[1:] if a != "--noprint"]
for slug in args:
    web = os.path.join(SB, "out", f"web_{slug}_en")
    os.makedirs(web, exist_ok=True)
    import json
    st = json.load(open(os.path.join(SB, f"story_{slug}_en.json"), encoding="utf-8"))
    src = st.get("image_dir") or f"{slug}_qwen"
    subprocess.run([PY, "pack_images.py", f"out/{src}", f"out/web_{slug}_en"], cwd=SB, env=ENV, check=True,
                   stdout=subprocess.DEVNULL)
    with open(os.path.join(web, "index.html"), "w", encoding="utf-8") as html:
        subprocess.run([PY, "build_web.py", f"story_{slug}_en.json", f"out/web_{slug}_en"], cwd=SB, env=ENV,
                       check=True, stdout=html)
    print(slug, "web", os.path.getsize(os.path.join(web, "index.html")) // 1024, "KB", flush=True)
    if "--noprint" not in sys.argv:
        r = subprocess.run([PY, "make_print.py", f"{slug}_en"], cwd=SB, env=ENV, capture_output=True, text=True,
                           encoding="utf-8")
        print(r.stdout.splitlines()[0] if r.returncode == 0 else r.stderr[-800:], flush=True)
