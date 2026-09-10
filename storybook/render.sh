#!/bin/bash
# 逐页出图。全书固定同一套身份词/画风词/LoRA 强度，保证翻页时人物一致。
ROOT=/Volumes/externalssd/devitems/learning/imageGen
cd "$ROOT" || exit 1
BOOK="${1:-storybook/story_rafflesia.json}"
OUT="${2:-storybook/pages}"
mkdir -p "$OUT"

/usr/bin/python3 - "$BOOK" "$OUT" <<'PY'
import json, sys, subprocess, os, time
book, outdir = sys.argv[1], sys.argv[2]
d = json.load(open(book))

# 角色设定表：全书固定，杜绝每页换衣服
CHAR  = d.get("character", "")
IDENT = "ohwx boy, solo, 1boy, asian toddler, 3 years old" + (", " + CHAR if CHAR else "")
# 尺度参照：全书固定，杜绝同一物体忽大忽小
SCALE = d.get("scale", "")
STYLE = d.get("style", "children's picture book illustration, storybook art, soft watercolor painting, "
                        "gentle rounded lineart, warm pastel colors, flat shading, soft diffused light")
NEG_EXTRA = d.get("neg_extra", "")
NEG   = ("photo, photorealistic, realistic, 3d render, cgi, detailed skin texture, "
         "worst quality, low quality, blurry, jpeg artifacts, deformed, bad anatomy, "
         "extra fingers, mutated hands, adult, teenager, 2boys, multiple people, text, watermark")
NEG = NEG + (", " + NEG_EXTRA if NEG_EXTRA else "")

base = json.load(open(d.get("workflow","workflows/son_forest_fd.json")))
for p in d["pages"]:
    wf = json.loads(json.dumps(base))
    wf["2"]["inputs"]["strength_model"] = 1.0    # 画风优先
    wf["2"]["inputs"]["strength_clip"]  = 1.0
    wf["3"]["inputs"]["text"] = f"{IDENT}, {STYLE}, {p['scene']}" + (", " + SCALE if SCALE else "")
    wf["4"]["inputs"]["text"] = NEG
    wf["6"]["inputs"]["seed"] = 2000 + p["n"]
    wf["9"]["inputs"]["seed"] = 2000 + p["n"]
    wf["10"]["inputs"]["filename_prefix"] = f"{d.get('slug','book')}/p{p['n']:02d}"
    if "11" in wf: del wf["11"]
    tmp = f"/tmp/page{p['n']}.json"
    json.dump(wf, open(tmp, "w"), ensure_ascii=False)
    t0 = time.time()
    r = subprocess.run(["ComfyUI/venv/bin/python", "workflows/run_workflow.py", tmp],
                       capture_output=True, text=True)
    out = [l for l in r.stdout.splitlines() if l.startswith("完成")]
    print(f"  第 {p['n']:2d} 页  {time.time()-t0:5.1f}s  {out[0] if out else '失败'}", flush=True)
PY
echo "全部页面完成，图在 ComfyUI/output/book/"
