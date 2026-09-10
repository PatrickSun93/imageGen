#!/bin/bash
# v1 / v2 各存档 A/B 对比：同场景同种子，只换 LoRA
# 用法: ./compare_lora.sh
ROOT=/Volumes/externalssd/devitems/learning/imageGen
LT="$ROOT/lora_training"
cd "$ROOT" || exit 1

SEED=777
run() {  # $1=LoRA文件绝对路径  $2=标签  $3=工作流
  cp "$1" ComfyUI/models/loras/_ab_test.safetensors
  /usr/bin/python3 -c "
import json
wf=json.load(open('$3'))
wf['2']['inputs']['lora_name']='_ab_test.safetensors'
wf['10' if '10' in wf else '8']['inputs']['filename_prefix']='ab_$2'
json.dump(wf,open('/tmp/ab.json','w'),ensure_ascii=False)"
  printf "  %-16s " "$2"
  ComfyUI/venv/bin/python workflows/run_workflow.py /tmp/ab.json --seed $SEED 2>&1 | grep -oE "输出: .*" || echo "失败"
}

echo "=== 森林场景，seed $SEED，只换 LoRA ==="
run "$LT/output_v1/son_ohwx_v1.safetensors"                 "v1_1200"  workflows/son_forest_fd.json
for s in 00000400 00000800 00001200; do
  f="$LT/output/son_ohwx_v2-step$s.safetensors"
  [ -f "$f" ] && run "$f" "v2_${s#0000000}" workflows/son_forest_fd.json
done
run "$LT/output/son_ohwx_v2.safetensors"                    "v2_1500"  workflows/son_forest_fd.json

echo
echo "=== 条纹衫污染检查（提示词明确穿别的衣服）==="
/usr/bin/python3 -c "
import json
wf=json.load(open('workflows/son_forest_fd.json'))
wf['2']['inputs']['lora_name']='_ab_test.safetensors'
t=wf['3']['inputs']['text']
wf['3']['inputs']['text']=t.replace('crouching in a lush green forest','wearing a bright red raincoat and yellow rain boots, standing in the rain under a big umbrella, puddles on the street')
wf['10']['inputs']['filename_prefix']='ab_stripecheck'
json.dump(wf,open('/tmp/ab2.json','w'),ensure_ascii=False)"
printf "  红雨衣测试     "
ComfyUI/venv/bin/python workflows/run_workflow.py /tmp/ab2.json --seed 888 2>&1 | grep -oE "输出: .*"
rm -f ComfyUI/models/loras/_ab_test.safetensors
echo
echo "全部输出在 ComfyUI/output/ab_*.png"
