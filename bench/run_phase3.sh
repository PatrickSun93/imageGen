#!/bin/bash
# B: 无 MPS 回落  C: Anima Turbo  D: V7 20步 1024 + swap  E: V7 20步 768
ROOT=/Volumes/externalssd/devitems/learning/imageGen
cd "$ROOT" || exit 1
ATT="--use-pytorch-cross-attention"

echo "########## B: 去掉 PYTORCH_ENABLE_MPS_FALLBACK（Anima 1 张）##########"
./bench/bench.sh "B-无MPS回落" "$ATT" workflows/anima_aesthetic.json 1 0
echo "--- B 阶段是否有 MPS 算子报错 ---"
tr '\r' '\n' < bench/log_B-无MPS回落.txt | grep -iE "not implemented|NotImplementedError|aten::|MPS backend|falling back|Error" | head -10 || echo "  无报错"

echo "########## C: Anima Turbo v1.0（10 步 / CFG 1）##########"
./bench/bench.sh "C-Turbo-10步" "$ATT" workflows/anima_turbo.json 2 1

echo "########## D: Pony V7 20 步 @1024（带 swap 专项监控）##########"
nohup ./bench/mem_monitor.sh bench/mem_trace_v7.csv 5 >/dev/null 2>&1 &
MEMPID=$!
./bench/bench.sh "D-V7-20步-1024" "$ATT" workflows/pony_v7_s20.json 2 1
kill $MEMPID 2>/dev/null

echo "########## E: Pony V7 20 步 @768（1 张）##########"
./bench/bench.sh "E-V7-20步-768" "$ATT" workflows/pony_v7_768.json 1 1

echo "########## V7 期间 swap 结论 ##########"
awk -F, 'NR==2{si=$3;so=$4;su=$6}
         END{printf "swapins  %s → %s  增量 %d\n", si,$3,$3-si;
             printf "swapouts %s → %s  增量 %d 页 ≈ %.1f MB\n", so,$4,$4-so,($4-so)*16/1024;
             printf "swap已用 %s → %s MB\n", su,$6}' bench/mem_trace_v7.csv
echo "V7 期间最低内存空闲%: $(awk -F, 'NR>1{print $2}' bench/mem_trace_v7.csv | sort -n | head -1)"

echo "########## 全部结果 ##########"
column -t -s, "$ROOT/bench/results.csv"
