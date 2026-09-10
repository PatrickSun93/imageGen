#!/bin/bash
# 图层法出图：场景（无人物）→ 贴人物 → 低 denoise 融合
ROOT=/Volumes/externalssd/devitems/learning/imageGen
cd "$ROOT" || exit 1
BOOK="${1:-storybook/story_ants.json}"

"$ROOT/ComfyUI/venv/bin/python" - "$BOOK" <<'PY'
import json, sys, subprocess, time, shutil, glob, os
sys.path.insert(0, "/Volumes/externalssd/devitems/learning/imageGen/storybook")
from compose import place

d = json.load(open(sys.argv[1]))
STYLE, CHAR = d["style"], d["character"]
NEG_SCENE = ("people, person, child, boy, girl, human, figure, "
             "photo, 3d render, watercolor, blurry, " + d["neg_extra"])

sc = json.load(open("workflows/son_forest_fd.json"))
del sc["2"]; del sc["9"]
sc["3"]["inputs"]["clip"]=["1",1]; sc["4"]["inputs"]["clip"]=["1",1]
sc["6"]["inputs"]["model"]=["1",0]; sc["10"]["inputs"]["images"]=["7",0]
if "11" in sc: del sc["11"]

hm = json.load(open("workflows/anima_img2img.json"))
hm["1"]={"class_type":"CheckpointLoaderSimple","inputs":{"ckpt_name":"sd_xl_base_1.0.safetensors"}}
hm["2"]={"class_type":"LoraLoader","inputs":{"model":["1",0],"clip":["1",1],
    "lora_name":"son_ohwx_v2.safetensors","strength_model":0.8,"strength_clip":0.8}}
hm["3"]={"class_type":"VAELoader","inputs":{"vae_name":"pixel_space"}}
hm["5"]["inputs"].update({"width":1024,"height":1024})
hm["6"]["inputs"]["vae"]=["1",2]; hm["10"]["inputs"]["vae"]=["1",2]
hm["7"]["inputs"]["clip"]=["2",1]; hm["8"]["inputs"]["clip"]=["2",1]
hm["9"]["inputs"].update({"model":["2",0],"steps":20,"cfg":6.0,
    "sampler_name":"dpmpp_2m","scheduler":"karras","denoise":0.32})

def run(wf, tag):
    json.dump(wf, open(f"/tmp/{tag}.json","w"), ensure_ascii=False)
    r = subprocess.run(["ComfyUI/venv/bin/python","workflows/run_workflow.py",f"/tmp/{tag}.json"],
                       capture_output=True, text=True)
    return [l for l in r.stdout.splitlines() if l.startswith("完成")]

for p in d["pages"]:
    n = p["n"]; t0 = time.time()
    # 1. 场景
    w = json.loads(json.dumps(sc))
    w["3"]["inputs"]["text"] = f"{STYLE}, {p['scene']}"
    w["4"]["inputs"]["text"] = NEG_SCENE
    w["6"]["inputs"]["seed"] = 9000 + n
    w["10"]["inputs"]["filename_prefix"] = f"lay_scene/p{n:02d}"
    if not run(w, f"ls{n}"): print(f"  第 {n} 页 场景失败"); continue
    scene = sorted(glob.glob(f"ComfyUI/output/lay_scene/p{n:02d}_*.png"))[-1]
    # 2. 贴人物
    place(scene, p["pose"], p["px"], p["py"], p["ph"], "/tmp/comp.png")
    shutil.copy("/tmp/comp.png", "ComfyUI/input/comp.png")
    # 3. 融合
    w = json.loads(json.dumps(hm))
    w["4"]["inputs"]["image"] = "comp.png"
    w["7"]["inputs"]["text"] = f"ohwx boy, {CHAR}, {STYLE}"
    w["8"]["inputs"]["text"] = "photo, 3d render, blurry, deformed, " + d["neg_extra"]
    w["9"]["inputs"]["seed"] = 9000 + n
    w["11"]["inputs"]["filename_prefix"] = f"lay_final/p{n:02d}"
    ok = run(w, f"lh{n}")
    print(f"  第 {n:2d} 页  {time.time()-t0:5.0f}s  {p['pose']:6s}  {'✅' if ok else '❌融合失败'}", flush=True)
PY
echo "全部完成 → ComfyUI/output/lay_final/"
