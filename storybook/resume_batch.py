"""resume_batch.py <logfile> <slug> [<slug> ...]

Runs as a detached process so a low-memory kill of the harness task can't stop it.
Waits for ComfyUI's queue to drain, recovers pages ComfyUI already rendered, renders the rest.
"""
import json, os, sys, time, glob, shutil, subprocess, urllib.request

ROOT = r"C:\FlowDev\githubdevitems\comfyUIItems"
API = "http://127.0.0.1:8188"
log_f = open(sys.argv[1], "a", buffering=1, encoding="utf-8")

def log(msg):
    log_f.write(time.strftime("%H:%M:%S ") + msg + "\n")

def queue_len():
    d = json.load(urllib.request.urlopen(API + "/queue"))
    return len(d["queue_running"]) + len(d["queue_pending"])

log("started; waiting for ComfyUI queue to drain")
while queue_len():
    time.sleep(5)

for slug in sys.argv[2:]:
    out = os.path.join(ROOT, "storybook", "out", slug + "_lora")
    os.makedirs(out, exist_ok=True)
    missing = []
    for n in range(1, 11):
        dst = os.path.join(out, f"page_{n:02d}.png")
        if os.path.exists(dst):
            continue
        done = sorted(glob.glob(os.path.join(ROOT, "ComfyUI", "output", f"{slug}_p{n:02d}_*.png")))
        if done:
            shutil.copy2(done[-1], dst)
            log(f"{slug} p{n:02d} recovered from {os.path.basename(done[-1])}")
        else:
            missing.append(n)
    if missing:
        log(f"{slug}: rendering pages {missing}")
        r = subprocess.run([sys.executable, os.path.join(ROOT, "storybook", "render_lora.py"),
                            os.path.join(ROOT, "storybook", "render_jobs", slug + ".json")] + [str(n) for n in missing],
                           stdout=log_f, stderr=subprocess.STDOUT, cwd=ROOT)
        log(f"{slug}: exit {r.returncode}")
log("ALL DONE")
