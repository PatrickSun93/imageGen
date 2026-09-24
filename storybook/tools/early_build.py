# Chinese + English web and print for the 5 early books (pages in out/<image_dir>)
import json, os, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
SB = r"C:\FlowDev\githubdevitems\comfyUIItems\storybook"; PY = r"C:\FlowDev\githubdevitems\comfyUIItems\venv\python.exe"
ENV = dict(os.environ, PYTHONIOENCODING="utf-8")
for s in sys.argv[1:]:
    st = json.load(open(os.path.join(SB, f"story_{s}.json"), encoding="utf-8"))
    web = os.path.join(SB, "out", f"web_{s}_v2"); os.makedirs(web, exist_ok=True)
    subprocess.run([PY, "pack_images.py", f"out/{st['image_dir']}", f"out/web_{s}_v2"], cwd=SB, env=ENV, check=True, stdout=subprocess.DEVNULL)
    with open(os.path.join(web, "index.html"), "w", encoding="utf-8") as h:
        subprocess.run([PY, "build_web.py", f"story_{s}.json", f"out/web_{s}_v2"], cwd=SB, env=ENV, check=True, stdout=h)
    r = subprocess.run([PY, "make_print.py", s], cwd=SB, env=ENV, capture_output=True, text=True, encoding="utf-8")
    print(s, "zh", r.stdout.splitlines()[0][:40] if r.returncode == 0 else r.stderr[-300:])
subprocess.run([PY, os.path.join(os.path.dirname(os.path.abspath(__file__)), "en_build.py")] + sys.argv[1:], env=ENV)
