#!/bin/bash
# DMD2 对比：同一 attention 后端（SDPA，即 start.sh 将采用的配置）下比才公平
ROOT=/Volumes/externalssd/devitems/learning/imageGen
cd "$ROOT" || exit 1
ATT="--use-pytorch-cross-attention"

echo "########## G: Pony V6 + DMD2 LoRA（8 步 / CFG 1 / lcm / sgm_uniform）##########"
./bench/bench.sh "G-V6-DMD2-8步" "$ATT" workflows/pony_v6_dmd2.json 2 1

echo "########## H: Pony V6 25 步基线（同为 SDPA，公平对照）##########"
./bench/bench.sh "H-V6-基线25步-sdpa" "$ATT" workflows/pony_v6_xl.json 2 1

echo "########## 结果 ##########"
column -t -s, "$ROOT/bench/results.csv"
