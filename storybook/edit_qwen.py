"""Render pages that show the boy with Qwen-Image-Edit-2511, using his photos as references instead of a LoRA.

usage: edit_qwen.py <ref1.png> <ref2.png> <story.json>:<page> [<story.json>:<page> ...]
       (ref files must already be in ComfyUI/input)
"""
import json, os, sys, time, uuid, urllib.request, shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = r"C:\FlowDev\githubdevitems\comfyUIItems"
API  = "http://127.0.0.1:8188"
WF   = os.path.join(ROOT, "workflows", "qwen_image_edit_2511_ref.json")
OUT  = os.path.join(ROOT, "storybook", "out", "bakeoff")
# tells the edit model who the boy is and that the result is a painting, not a retouched photo
LEAD = ("A new children's book illustration, not a photo. The little boy in it is the child shown in image 1 "
        "and image 2: keep his face, eyes, hair and proportions, but draw him in the illustration style described. ")

def page_prompt(story, p):
    if "prompt" in p:
        body = p["prompt"]
    else:
        body = ", ".join(x for x in ["ohwx boy", story.get("character"), story["style"], p["scene"]] if x)
    return LEAD + body.replace("ohwx boy, ", "", 1)

def submit(prompt, seed, prefix, refs):
    wf = json.load(open(WF, encoding="utf-8"))
    wf["20"]["inputs"]["image"], wf["21"]["inputs"]["image"] = refs
    wf["4"]["inputs"]["prompt"] = prompt
    wf["7"]["inputs"]["seed"] = seed
    wf["10"]["inputs"]["filename_prefix"] = prefix
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

def compose(slug, n, refs, edit_img):
    cells = [("reference photo", os.path.join(ROOT, "ComfyUI", "input", refs[0])),
             ("Flux dev + LoRA", os.path.join(ROOT, "storybook", "out", slug + "_lora", f"page_{n:02d}.png")),
             ("Qwen Edit 8-step", edit_img)]
    cells = [(label, f) for label, f in cells if os.path.exists(f)]
    S, H = 640, 44
    sheet = Image.new("RGB", (S * len(cells), S + H), "white")
    draw = ImageDraw.Draw(sheet); font = ImageFont.truetype("arial.ttf", 26)
    for i, (label, f) in enumerate(cells):
        im = Image.open(f).convert("RGB")
        im.thumbnail((S, S), Image.LANCZOS)
        sheet.paste(im, (i * S + (S - im.width) // 2, H + (S - im.height) // 2))
        draw.text((i * S + 12, 8), label, fill="black", font=font)
    dst = os.path.join(OUT, f"cmp_edit_{slug}_p{n:02d}.png"); sheet.save(dst)
    return dst

def main(refs, targets):
    os.makedirs(OUT, exist_ok=True)
    for t in targets:
        path, n = t.rsplit(":", 1); n = int(n)
        story = json.load(open(os.path.join(ROOT, path), encoding="utf-8"))
        p = next(x for x in story["pages"] if x["n"] == n)
        slug = story["slug"]; seed = p.get("seed", story.get("seed_base", 2000) + n)
        t0 = time.time()
        f = submit(page_prompt(story, p), seed, f"edit_{slug}_p{n:02d}", refs)
        dst = os.path.join(OUT, f"{slug}_p{n:02d}_edit8.png")
        shutil.copy2(os.path.join(ROOT, "ComfyUI", "output", f[0]), dst)
        print(f"{slug} p{n:02d} edit8 {time.time()-t0:.0f}s  sheet: {compose(slug, n, refs, dst)}", flush=True)

if __name__ == "__main__":
    main(sys.argv[1:3], sys.argv[3:])
