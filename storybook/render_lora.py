import json, sys, os, time, uuid, urllib.request, shutil
ROOT = r"C:\FlowDev\githubdevitems\comfyUIItems"
API  = "http://127.0.0.1:8188"
TRIGGER = "ohwx boy"
LORA = "son_ohwx_flux_v1-step00001000.safetensors"

def submit(wf_path, prompt_text, seed, prefix, strength, negative=""):
    wf = json.load(open(wf_path, encoding="utf-8"))
    wf["4"]["inputs"]["text"] = prompt_text
    # recorded for completeness only: at CFG 1.0 Flux dev never runs the negative branch
    wf["8"]["inputs"]["text"] = negative
    wf["7"]["inputs"]["seed"] = seed
    wf["10"]["inputs"]["filename_prefix"] = prefix
    if strength:
        wf["11"]["inputs"]["lora_name"] = LORA
        wf["11"]["inputs"]["strength_model"] = strength
    else:
        # page without the boy: cut the LoRA out of the graph so it renders as plain Flux
        del wf["11"]
        wf["7"]["inputs"]["model"] = ["1", 0]
    b = json.dumps({"prompt": wf, "client_id": str(uuid.uuid4())}).encode()
    pid = json.load(urllib.request.urlopen(urllib.request.Request(
        API+"/prompt", b, {"Content-Type":"application/json"})))["prompt_id"]
    while True:
        h = json.load(urllib.request.urlopen(f"{API}/history/{pid}"))
        if pid in h:
            if h[pid]["status"].get("status_str") != "success":
                raise RuntimeError(json.dumps(h[pid]["status"])[:400])
            return [i["filename"] for o in h[pid]["outputs"].values() for i in o.get("images",[])]
        time.sleep(2)

def main(story_path, only):
    story = json.load(open(story_path, encoding="utf-8"))
    wf_path = os.path.join(ROOT, story.get("workflow", "workflows/flux_dev_lora.json"))
    # the colophon's strength is the one actually rendered with, so the book can't misreport it
    strength = story["colophon"]["strength"]
    seed_base = story.get("seed_base", 2000)
    outdir = os.path.join(ROOT,"storybook","out", story["slug"]+"_lora"); os.makedirs(outdir, exist_ok=True)
    pages = [p for p in story["pages"] if not only or p["n"] in only]
    t0=time.time()
    for p in pages:
        n=p["n"]
        if "prompt" in p:
            prompt = p["prompt"]   # already assembled on the Mac side: use it verbatim
        elif p["has_boy"]:
            prompt = ", ".join(x for x in [TRIGGER, story.get("character"), story["style"], p["scene"]] if x)
        else:
            prompt = ", ".join(x for x in [story["style"], p["scene"]] if x)
        negative = ", ".join(x for x in [story.get("negative", ""), p.get("negative_extra", "")] if x)
        t=time.time()
        f=submit(wf_path, prompt, seed_base+n, f"{story['slug']}_p{n:02d}", strength if p["has_boy"] else 0,
                 negative)
        shutil.copy2(os.path.join(ROOT,"ComfyUI","output",f[0]), os.path.join(outdir,f"page_{n:02d}.png"))
        print(f"page {n:02d} seed {seed_base+n} {'[boy]' if p['has_boy'] else '[no boy]'} {time.time()-t:.0f}s", flush=True)
    print(f"{len(pages)} pages in {time.time()-t0:.0f}s -> {outdir}")

if __name__ == "__main__":
    # render_lora.py story.json [page ...]   -- page numbers re-render just those pages
    main(sys.argv[1], {int(a) for a in sys.argv[2:]})
