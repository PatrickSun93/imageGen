#!/bin/bash
# 用给定的 ComfyUI 启动参数重启服务，跑同一个工作流 N 张，报告每张的 s/it 和耗时。
# 用法: ./bench.sh "<标签>" "<额外启动参数>" "<工作流json>" [张数] [MPS_FALLBACK=1|0]
set -u
ROOT=/Volumes/externalssd/devitems/learning/imageGen
COMFY="$ROOT/ComfyUI"
LABEL="$1"; EXTRA="$2"; WF="$3"; N="${4:-2}"; FB="${5:-1}"
# 下面会 cd 到 ComfyUI 目录，工作流必须先转成绝对路径
case "$WF" in /*) ;; *) WF="$ROOT/$WF" ;; esac
[ -f "$WF" ] || { echo "找不到工作流: $WF" >&2; exit 1; }
RESULT="$ROOT/bench/results.csv"
[ -f "$RESULT" ] || echo "标签,工作流,额外参数,MPS_FALLBACK,第几张,耗时秒,s_per_it,attention" > "$RESULT"

# --- 停掉旧服务 ---
PID=$(lsof -t -nP -iTCP:8188 -sTCP:LISTEN 2>/dev/null)
[ -n "$PID" ] && { kill $PID; while lsof -nP -iTCP:8188 -sTCP:LISTEN >/dev/null 2>&1; do sleep 1; done; }

# --- 用本次参数启动，日志单独存 ---
LOG="$ROOT/bench/log_${LABEL// /_}.txt"
: > "$LOG"
cd "$COMFY" || exit 1
if [ "$FB" = "1" ]; then export PYTORCH_ENABLE_MPS_FALLBACK=1; else unset PYTORCH_ENABLE_MPS_FALLBACK; fi
nohup "$COMFY/venv/bin/python" main.py --listen 0.0.0.0 --port 8188 $EXTRA >> "$LOG" 2>&1 &
for i in $(seq 1 180); do
    if [ "$(curl -s -o /dev/null -w '%{http_code}' --max-time 3 http://127.0.0.1:8188/system_stats)" = "200" ]; then
        # 还要确认节点注册完毕，否则 /prompt 会 400
        curl -s --max-time 10 http://127.0.0.1:8188/object_info/KSampler | grep -q KSampler && break
    fi
    sleep 2
done
ATT=$(grep -oE "Using (pytorch|sub quadratic optimization for|split|quad) [a-z ]*attention" "$LOG" | head -1)

# --- 跑 N 张 ---
for i in $(seq 1 "$N"); do
    MARK=$(wc -l < "$LOG" | tr -d " ")
    OUT=$("$COMFY/venv/bin/python" "$ROOT/workflows/run_workflow.py" "$WF" --seed $((100 + i)) 2>&1)
    echo "--- run_workflow 输出 (第 $i 张) ---" >> "$LOG"; echo "$OUT" >> "$LOG"
    SEC=$(echo "$OUT" | sed -n "s/^ELAPSED=//p")
    SPI=$(tail -n +$MARK "$LOG" | tr '\r' '\n' | grep -oE "[0-9]+/[0-9]+ \[[0-9:]+<00:00, +[0-9.]+s/it\]" | tail -1 | grep -oE "[0-9.]+s/it" | grep -oE "[0-9.]+")
    [ -z "$SPI" ] && SPI=$(tail -n +$MARK "$LOG" | tr '\r' '\n' | grep -oE "[0-9.]+it/s\]" | tail -1 | grep -oE "[0-9.]+" | awk '{print 1/$1}')
    echo "$LABEL,$(basename $WF),$EXTRA,$FB,$i,${SEC:-失败},${SPI:-?},$ATT" >> "$RESULT"
    echo "[$LABEL] 第 $i 张: ${SEC:-失败} 秒, ${SPI:-?} s/it"
done
echo "attention: $ATT"
