#!/bin/bash
# ComfyUI 启动脚本 —— 手动启动用：cd $ROOT && nohup ./start.sh >/dev/null 2>&1 &
# 保留了开机自启时需要的健壮性：等待外置盘挂载后再启动（外置盘可能比登录晚挂上）。
# 日志重定向、cd、等待挂载全部在本脚本内部完成，脚本可以直接双击/命令行跑。

ROOT=/Volumes/externalssd/devitems/learning/imageGen
COMFY="$ROOT/ComfyUI"
LOGDIR="$ROOT/logs"
PORT=8188            # 8502 已被别的服务占用，不要改成 8502

# ---- 1. 等待外置盘挂载（开机时外置盘可能比登录晚，最多等 60 秒）----
# 日志目录还不存在时先往 /tmp 写，挂载成功后再切到 $ROOT/logs
BOOTLOG=/tmp/comfyui-boot.log
for i in $(seq 1 60); do
    [ -d "$COMFY" ] && break
    echo "$(date '+%F %T') 等待 /Volumes/externalssd 挂载… ${i}/60" >> "$BOOTLOG"
    sleep 1
done

if [ ! -d "$COMFY" ]; then
    echo "$(date '+%F %T') 超时 60 秒，$COMFY 仍不存在，放弃启动" >> "$BOOTLOG"
    exit 1
fi

# ---- 2. 日志 ----
mkdir -p "$LOGDIR"
exec >> "$LOGDIR/comfyui.log" 2>> "$LOGDIR/comfyui.err"
echo "===== $(date '+%F %T') 启动 ComfyUI (port $PORT) ====="

# ---- 3. 环境 ----
cd "$COMFY" || exit 1
# MPS 尚未实现的算子回落到 CPU，而不是直接报错
export PYTORCH_ENABLE_MPS_FALLBACK=1

# ---- 4. 启动 ----
# --use-pytorch-cross-attention: ComfyUI 只对 nvidia/xpu/部分 AMD 自动开 SDPA，MPS 不在
#   自动列表里（comfy/model_management.py），默认会退回慢的 sub-quadratic。实测：
#   Pony V6 快 22% (5.06→3.96 s/it)，Anima 快 5.8% (12.30→11.59)。
#   注意 Pony V7 是例外，它用 sub-quadratic 反而快 9.6%——认真跑 V7 时去掉这个参数。
#   详见 bench/FINDINGS.md
exec "$COMFY/venv/bin/python" main.py --listen 0.0.0.0 --port "$PORT" \
     --use-pytorch-cross-attention
