"""Render pages that show the boy with Qwen-Image-Edit-2511, using his photos as references instead of a LoRA.

usage: edit_qwen.py [--v2] [--style|--restyle] [--unet=<file>] <ref1.png> <ref2.png> <story.json>:<page> [...]
       (ref files must already be in ComfyUI/input; --v2 uses the short "Picture 1 / Picture 2" instruction)
       Pages without the boy (Qwen-Image text-to-image drifts to near-photo detail on print styles):
       --style:   ref1/ref2 are finished pages of the same book, used as an art-style sample.
                  Output <slug>_pNN_style8[_quant].png
       --restyle: Picture 1 = this page's text-to-image render (out/bakeoff/<slug>_pNN_lightning8.png, copied into
                  ComfyUI/input automatically; ref1 is ignored), Picture 2 = ref2, a finished page of the same book.
                  Keeps the composition of the text-to-image page and the look of the book page.
                  Output <slug>_pNN_restyle8[_quant].png
"""
import json, os, sys, time, uuid, urllib.request, shutil
from PIL import Image, ImageDraw, ImageFont

ROOT = r"C:\FlowDev\githubdevitems\comfyUIItems"
API  = "http://127.0.0.1:8188"
WF   = os.path.join(ROOT, "workflows", "qwen_image_edit_2511_ref.json")
OUT  = os.path.join(ROOT, "storybook", "out", "bakeoff")
INPUT = os.path.join(ROOT, "ComfyUI", "input")
# tells the edit model who the boy is and that the result is a painting, not a retouched photo
LEAD = ("A new children's book illustration, not a photo. The little boy in it is the child shown in image 1 "
        "and image 2: keep his face, eyes, hair and proportions, but draw him in the illustration style described. ")

# v2: a short instruction that names the reference pictures the way the Qwen edit encoder labels them
LEAD_V2 = ("Picture 1 and Picture 2 show the same little boy. Draw exactly this boy, with the same face, "
           "the same short black hair and the same round rosy cheeks, as the character in a new "
           "children's picture book illustration: ")

# style: the refs are pages of the same book; copy their look, not their content or layout
LEAD_STYLE = ("Picture 1 and Picture 2 are pages from a children's picture book, shown only as samples of the art "
              "style. Create a completely different new page for the same book, with a new place, a new layout and "
              "new objects, drawn in the same art style: the same colors, line work, simple shapes and paper "
              "texture. The new page shows: ")
# restyle: keep Picture 1's composition, take Picture 2's look
LEAD_RESTYLE = ("Redraw Picture 1 in exactly the art style of Picture 2, with the same colors, line work, simple "
                "shapes and paper texture as Picture 2. Keep the scene, the composition and the objects of Picture 1. "
                "The page shows: ")
V2 = False
MODE = None   # None | "style" | "restyle"
UNET = None   # --unet=<file> swaps the workflow's Edit model, e.g. the smaller Q3_K_M when RAM is tight

def page_prompt(story, p):
    if MODE == "style":
        return LEAD_STYLE + p.get("prompt", f"{p['scene']} ({story['style']})")
    if MODE == "restyle":
        # the scene alone gave a smooth vector look; naming the book's medium pulls in its texture too
        return LEAD_RESTYLE + f"{p['scene']} Art style: {story['style']}."
    if "prompt" in p:
        body = p["prompt"]
    else:
        body = ", ".join(x for x in ["ohwx boy", story.get("character"), story["style"], p["scene"]] if x)
    return (LEAD_V2 if V2 else LEAD) + body.replace("ohwx boy, ", "", 1)

def submit(prompt, seed, prefix, refs):
    wf = json.load(open(WF, encoding="utf-8"))
    wf["20"]["inputs"]["image"], wf["21"]["inputs"]["image"] = refs
    if UNET:
        wf["1"]["inputs"]["unet_name"] = UNET
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

def compose(slug, n, refs, current):
    first = {"style": "style reference", "restyle": "text-to-image input"}.get(MODE, "reference photo")
    cells = [(first, os.path.join(INPUT, refs[0])),
             ("Flux dev + LoRA", os.path.join(ROOT, "storybook", "out", slug + "_lora", f"page_{n:02d}.png")),
             ("Qwen text-to-image", os.path.join(OUT, f"{slug}_p{n:02d}_lightning8.png")),
             ("Qwen Edit (long prompt)", os.path.join(OUT, f"{slug}_p{n:02d}_edit8.png")),
             ("Qwen Edit v2 (Picture 1/2)", os.path.join(OUT, f"{slug}_p{n:02d}_edit8v2.png"))]
    if MODE == "restyle":
        cells[0] = ("style page", os.path.join(INPUT, refs[1]))
    if UNET and not MODE:
        cells.append((f"Qwen Edit v2 {quant_tag().upper()}", os.path.join(OUT, f"{slug}_p{n:02d}_edit8v2_{quant_tag()}.png")))
    if MODE:
        cells.append((f"Qwen Edit {MODE}", current))
    cells = [(label, f) for label, f in cells if os.path.exists(f)]
    S, H = 640, 44
    sheet = Image.new("RGB", (S * len(cells), S + H), "white")
    draw = ImageDraw.Draw(sheet); font = ImageFont.truetype("arial.ttf", 26)
    for i, (label, f) in enumerate(cells):
        im = Image.open(f).convert("RGB")
        im.thumbnail((S, S), Image.LANCZOS)
        sheet.paste(im, (i * S + (S - im.width) // 2, H + (S - im.height) // 2))
        draw.text((i * S + 12, 8), label, fill="black", font=font)
    dst = os.path.join(OUT, f"cmp_{MODE or 'edit'}_{slug}_p{n:02d}.png"); sheet.save(dst)
    return dst

def main(refs, targets):
    os.makedirs(OUT, exist_ok=True)
    for t in targets:
        path, n = t.rsplit(":", 1); n = int(n)
        story = json.load(open(os.path.join(ROOT, path), encoding="utf-8"))
        p = next(x for x in story["pages"] if x["n"] == n)
        slug = story["slug"]; seed = p.get("seed", story.get("seed_base", 2000) + n)
        tag = {"style": "style8", "restyle": "restyle8"}.get(MODE) or ("edit8v2" if V2 else "edit8")
        mode = tag + (f"_{quant_tag()}" if UNET else "")
        page_refs = list(refs)
        if MODE == "restyle":
            src = os.path.join(OUT, f"{slug}_p{n:02d}_lightning8.png")
            page_refs[0] = f"restyle_{slug}_p{n:02d}.png"
            shutil.copy2(src, os.path.join(INPUT, page_refs[0]))
        t0 = time.time()
        # 和 bakeoff_qwen 里同一个毛病：ComfyUI 偶发读模型文件失败，抛出去就把整批
        # 剩下的全废掉。本地重试三次，三次都不行就跳过这一页，别拖累后面的。
        f = None
        for attempt in range(1, 4):
            try:
                f = submit(page_prompt(story, p), seed, f"{mode}_{slug}_p{n:02d}", page_refs)
                break
            except Exception as e:
                print(f"{slug} p{n:02d} 第 {attempt} 次失败：{str(e)[:120]}", flush=True)
                if attempt < 3:
                    time.sleep(20)
        if f is None:
            print(f"{slug} p{n:02d} 三次都失败，跳过", flush=True)
            continue
        dst = os.path.join(OUT, f"{slug}_p{n:02d}_{mode}.png")
        shutil.copy2(os.path.join(ROOT, "ComfyUI", "output", f[0]), dst)
        print(f"{slug} p{n:02d} {mode} {time.time()-t0:.0f}s  sheet: {compose(slug, n, page_refs, dst)}", flush=True)

def quant_tag():
    # "qwen-image-edit-2511-Q3_K_M.gguf" -> "q3_k_m"
    return UNET.rsplit("-", 1)[-1].split(".")[0].lower()

if __name__ == "__main__":
    args = sys.argv[1:]
    while args and args[0].startswith("--"):
        flag = args.pop(0)
        if flag == "--v2":
            V2 = True
        elif flag in ("--style", "--restyle"):
            MODE = flag[2:]
        elif flag.startswith("--unet="):
            UNET = flag.split("=", 1)[1]
    main(args[0:2], args[2:])
