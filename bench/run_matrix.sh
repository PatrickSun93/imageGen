#!/bin/bash
# 按用户要求的矩阵依次测试，每次只改一项
ROOT=/Volumes/externalssd/devitems/learning/imageGen
cd "$ROOT" || exit 1
WF=workflows/anima_aesthetic.json

echo "########## 阶段 A: Anima 参数矩阵（每组 2 张，取第 2 张）##########"
./bench/bench.sh "A1-基线"          ""                              "$WF" 2 1
./bench/bench.sh "A2-pytorch-attn"  "--use-pytorch-cross-attention" "$WF" 2 1
./bench/bench.sh "A3-force-fp16"    "--force-fp16"                  "$WF" 2 1
./bench/bench.sh "A4-bf16-unet"     "--bf16-unet"                   "$WF" 2 1
./bench/bench.sh "A5-fp16-vae"      "--fp16-vae"                    "$WF" 2 1

echo "########## 阶段 B: 去掉 PYTORCH_ENABLE_MPS_FALLBACK（1 张，看是否报错）##########"
./bench/bench.sh "B-无MPS回落"      ""                              "$WF" 1 0

echo "########## 全部完成 ##########"
column -t -s, "$ROOT/bench/results.csv"
