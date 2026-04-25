#!/bin/bash
# vLLM 实时监控脚本
# 显示请求状态、GPU使用、日志摘要

VLLM_API="http://localhost:30000"
CONTAINER_NAME="vllm-qwen3"

clear
echo "========================================"
echo "🔍 vLLM 实时监控"
echo "========================================"
echo "按 Ctrl+C 退出"
echo "========================================"
echo ""

while true; do
    clear
    echo "========================================"
    echo "🔍 vLLM 服务监控"
    echo "========================================"
    echo "📅 时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""

    # 1. 请求状态
    echo "📊 [1/4] 请求状态"
    echo "────────────────────────────────────────"
    metrics=$(curl -s ${VLLM_API}/metrics 2>/dev/null)

    running=$(echo "$metrics" | grep "num_requests_running" | awk '{print $2}')
    waiting=$(echo "$metrics" | grep "num_requests_waiting" | awk '{print $2}')

    echo "  运行中: ${running:-0} 个请求"
    echo "  等待中: ${waiting:-0} 个请求"
    echo ""

    # 2. 缓存状态
    echo "💾 [2/4] 缓存状态"
    echo "────────────────────────────────────────"
    kv_cache=$(echo "$metrics" | grep "kv_cache_usage_perc" | awk '{print $2}')
    echo "  KV缓存使用: ${kv_cache:-0}%"

    # 从日志获取缓存命中率
    cache_rate=$(docker exec ${CONTAINER_NAME} tail -5 /tmp/vllm.log 2>/dev/null | grep -oP "MM cache hit rate: \K[0-9.]+%" | tail -1)
    echo "  MM缓存命中率: ${cache_rate:-N/A}"
    echo ""

    # 3. GPU 状态
    echo "🎮 [3/4] GPU 状态"
    echo "────────────────────────────────────────"
    docker exec ${CONTAINER_NAME} nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total --format=csv,noheader | awk '{
        printf "  GPU %s: %s\n", $1, $2
        printf "    利用率: %s%%\n", $3
        printf "    显存: %s / %s MB\n", $4, $5
        print ""
    }' | head -8
    echo ""

    # 4. 最新日志
    echo "📝 [4/4] 最新日志（最后3行）"
    echo "────────────────────────────────────────"
    docker exec ${CONTAINER_NAME} tail -3 /tmp/vllm.log 2>/dev/null | sed 's/^/  /' || echo "  无法获取日志"
    echo ""

    echo "========================================"
    echo "⏱️  刷新间隔: 5秒 | 按 Ctrl+C 退出"
    echo "========================================"

    sleep 5
done
