import json, sys, os, time, uuid, urllib.request, shutil

ROOT = r"C:\FlowDev\githubdevitems\comfyUIItems"
API  = "http://127.0.0.1:8188"

def submit(prompt_text, seed, prefix):
    wf = json.load(open(os.path.join(ROOT, "workflows", "flux_schnell_validate.json"), encoding="utf-8"))
    wf["4"]["inputs"]["text"] = prompt_text
    wf["7"]["inputs"]["seed"] = seed
    wf["10"]["inputs"]["filename_prefix"] = prefix
    body = json.dumps({"prompt": wf, "client_id": str(uuid.uuid4())}).encode()
    req = urllib.request.Request(API + "/prompt", body, {"Content-Type": "application/json"})
    pid = json.load(urllib.request.urlopen(req))["prompt_id"]
    while True:
        h = json.load(urllib.request.urlopen(f"{API}/history/{pid}"))
        if pid in h:
            st = h[pid]["status"].get("status_str")
            if st != "success":
                raise RuntimeError(f"render failed: {json.dumps(h[pid]['status'])[:500]}")
            return [i["filename"] for o in h[pid]["outputs"].values() for i in o.get("images", [])]
        time.sleep(2)

def main(story_path):
    story = json.load(open(story_path, encoding="utf-8"))
    outdir = os.path.join(ROOT, "storybook", "out", story["slug"])
    os.makedirs(outdir, exist_ok=True)
    t0 = time.time()
    for p in story["pages"]:
        n = p["n"]
        prompt = f"{p['scene']} {story['style']}"
        seed = 2000 + n
        t = time.time()
        files = submit(prompt, seed, f"{story['slug']}_p{n:02d}")
        src = os.path.join(ROOT, "ComfyUI", "output", files[0])
        dst = os.path.join(outdir, f"page_{n:02d}.png")
        shutil.copy2(src, dst)
        print(f"page {n:02d}  seed {seed}  {time.time()-t:.1f}s  -> {dst}", flush=True)
    print(f"ALL {len(story['pages'])} pages in {time.time()-t0:.1f}s -> {outdir}")

if __name__ == "__main__":
    main(sys.argv[1])
