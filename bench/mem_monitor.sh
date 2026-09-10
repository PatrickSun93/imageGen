#!/bin/bash
# 每 5 秒记一次内存压力和 swap 使用，用于确认是否在 swap
# 用法: ./mem_monitor.sh <输出文件> [间隔秒]
OUT="${1:?需要输出文件}"
INT="${2:-5}"
PAGESIZE=$(vm_stat | head -1 | grep -oE '[0-9]+')
echo "时间,内存空闲%,swapins,swapouts,compressed_pages,swap_used_MB,swap_total_MB" > "$OUT"
while true; do
    t=$(date '+%H:%M:%S')
    free=$(memory_pressure 2>/dev/null | grep -i "free percentage" | grep -oE '[0-9]+')
    vs=$(vm_stat)
    si=$(echo "$vs"  | awk -F: '/Swapins/       {gsub(/[ .]/,"",$2); print $2}')
    so=$(echo "$vs"  | awk -F: '/Swapouts/      {gsub(/[ .]/,"",$2); print $2}')
    cp=$(echo "$vs"  | awk -F: '/Pages occupied by compressor/ {gsub(/[ .]/,"",$2); print $2}')
    sw=$(sysctl -n vm.swapusage 2>/dev/null)
    st=$(echo "$sw" | grep -oE 'total = [0-9.]+M' | grep -oE '[0-9.]+')
    su=$(echo "$sw" | grep -oE 'used = [0-9.]+M'  | grep -oE '[0-9.]+')
    echo "$t,${free:-?},${si:-0},${so:-0},${cp:-0},${su:-0},${st:-0}" >> "$OUT"
    sleep "$INT"
done
