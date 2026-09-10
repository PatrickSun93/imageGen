#!/bin/bash
# 阶段 C/D：Anima Turbo 对比 + Pony V7 20 步（带独立 swap 监控）
ROOT=/Volumes/externalssd/devitems/learning/imageGen
cd "$ROOT" || exit 1

echo "########## 阶段 C: Anima Turbo v1.0（10 步 / CFG 1）##########"
./bench/bench.sh "C-Turbo-10步" "--use-pytorch-cross-attention" workflows/anima_turbo.json 2 1

echo "########## 阶段 D: Pony V7 20 步 + swap 专项监控 ##########"
# 单独记一份 V7 期间的内存轨迹，便于和 Anima 期间对比
nohup ./bench/mem_monitor.sh bench/mem_trace_v7.csv 5 >/dev/null 2>&1 &
MEMPID=$!
echo "V7 内存监控 PID $MEMPID"
./bench/bench.sh "D-V7-20步" "--use-pytorch-cross-attention" workflows/pony_v7_s20.json 2 1
kill $MEMPID 2>/dev/null

echo "########## V7 期间 swap 结论 ##########"
awk -F, 'NR==2{si=$3; so=$4; su=$6}
         END{printf "swapins  起 %s 终 %s 增量 %d\n", si, $3, $3-si;
             printf "swapouts 起 %s 终 %s 增量 %d 页 ≈ %.1f MB\n", so, $4, $4-so, ($4-so)*16/1024;
             printf "swap 已用 起 %s MB 终 %s MB\n", su, $6}' bench/mem_trace_v7.csv
echo "最低内存空闲%: $(awk -F, 'NR>1{print $2}' bench/mem_trace_v7.csv | sort -n | head -1)"

echo "########## 全部结果 ##########"
column -t -s, "$ROOT/bench/results.csv"
