"""Render story pages on Qwen-Image-2512 and set them beside the existing Flux page.

usage: bakeoff_qwen.py <lightning8|full50> <story.json>:<page> [<story.json>:<page> ...]
       bakeoff_qwen.py compose <story.json>:<page> ...      (only rebuild the comparison sheets)
"""
import json, os, sys, time, uuid, urllib.request, shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = r"C:\FlowDev\githubdevitems\comfyUIItems"
API  = "http://127.0.0.1:8188"
WF   = os.path.join(ROOT, "workflows", "qwen_image_2512.json")
OUT  = os.path.join(ROOT, "storybook", "out", "bakeoff")
NEG  = ("character sheet, model sheet, multiple views, grid, collage, text, watermark, signature, "
        "blurry, deformed hands, extra fingers, photorealistic face")
# lightning8: distilled 8-step LoRA at CFG 1 (negative ignored); full50: the base model with real CFG and the negative
MODES = {"lightning8": dict(lora=True, steps=8, cfg=1.0), "full50": dict(lora=False, steps=50, cfg=4.0)}

def page_prompt(story, p):
    if "prompt" in p:
        text = p["prompt"]
    else:
        text = f"{story['style']}, {p['scene']}"
    # Qwen has no ohwx LoRA: drop the trigger and let it draw a generic boy
    return text.replace("ohwx boy, ", "a little asian boy, ", 1)

def submit(prompt, negative, seed, prefix, mode):
    wf = json.load(open(WF, encoding="utf-8"))
    m = MODES[mode]
    wf["4"]["inputs"]["text"] = prompt
    wf["8"]["inputs"]["text"] = negative
    wf["7"]["inputs"].update(seed=seed, steps=m["steps"], cfg=m["cfg"])
    wf["10"]["inputs"]["filename_prefix"] = prefix
    if not m["lora"]:
        del wf["11"]
        wf["12"]["inputs"]["model"] = ["1", 0]
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

def targets(args):
    for a in args:
        path, n = a.rsplit(":", 1)
        story = json.load(open(os.path.join(ROOT, path), encoding="utf-8"))
        yield story, next(p for p in story["pages"] if p["n"] == int(n))

def compose(story, p):
    n, slug = p["n"], story["slug"]
    cells = [("Flux dev + LoRA", os.path.join(ROOT, "storybook", "out", slug + "_lora", f"page_{n:02d}.png"))]
    cells += [(f"Qwen {m}", os.path.join(OUT, f"{slug}_p{n:02d}_{m}.png")) for m in MODES]
    cells = [(label, f) for label, f in cells if os.path.exists(f)]
    if len(cells) < 2:
        return None
    S, H = 640, 44
    sheet = Image.new("RGB", (S * len(cells), S + H), "white")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype("arial.ttf", 26)
    for i, (label, f) in enumerate(cells):
        sheet.paste(Image.open(f).convert("RGB").resize((S, S), Image.LANCZOS), (i * S, H))
        draw.text((i * S + 12, 8), label, fill="black", font=font)
    dst = os.path.join(OUT, f"cmp_{slug}_p{n:02d}.png")
    sheet.save(dst)
    return dst

def main(mode, args):
    os.makedirs(OUT, exist_ok=True)
    for story, p in targets(args):
        n, slug = p["n"], story["slug"]
        if mode != "compose":
            # the job's negative already starts with NEG; add the page's own extra negatives on top
            neg = ", ".join(x for x in [story.get("negative") or NEG, p.get("negative_extra", "")] if x)
            seed = p.get("seed", story.get("seed_base", 2000) + n)   # same seed as the Flux page it is compared with
            t = time.time()
            # ComfyUI 偶尔在 CLIPTextEncode 上报 HostBuffer.read_file_slice failed（读模型
            # 文件失败，和提示词无关，重来一次就好）。以前这里直接抛出去，一张图的偶发
            # 失败会把整批剩下的几百张全废掉——2026-09-16 一晚上栽了四次。改成本地重试。
            for attempt in range(1, 4):
                try:
                    f = submit(page_prompt(story, p), neg, seed,
                               f"bake_{slug}_p{n:02d}_{mode}", mode)
                    break
                except Exception as e:
                    print(f"{slug} p{n:02d} 第 {attempt} 次失败：{str(e)[:120]}", flush=True)
                    if attempt == 3:
                        print(f"{slug} p{n:02d} 三次都失败，跳过", flush=True)
                        f = None
                        break
                    time.sleep(20)
            if f is None:
                continue
            shutil.copy2(os.path.join(ROOT, "ComfyUI", "output", f[0]), os.path.join(OUT, f"{slug}_p{n:02d}_{mode}.png"))
            print(f"{slug} p{n:02d} {mode} {time.time()-t:.0f}s", flush=True)
        print("sheet:", compose(story, p), flush=True)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
