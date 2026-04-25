#!/bin/bash
# vLLM 性能分析脚本
# 从日志中提取性能统计信息

CONTAINER_NAME="vllm-qwen3"

echo "========================================"
echo "📊 vLLM 性能分析"
echo "========================================"
echo ""

echo "📈 最近10次请求的吞吐量统计"
echo "────────────────────────────────────────"
docker exec ${CONTAINER_NAME} tail -100 /tmp/vllm.log | grep "Avg.*throughput" | tail -10

echo ""
echo "💾 缓存效率统计"
echo "────────────────────────────────────────"
docker exec ${CONTAINER_NAME} tail -100 /tmp/vllm.log | grep "cache hit rate" | tail -10

echo ""
echo "🎮 GPU 内存使用"
echo "────────────────────────────────────────"
docker exec ${CONTAINER_NAME} nvidia-smi --query-gpu=index,memory.used,memory.total --format=csv,noheader | awk '{
    printf "GPU %s: %s / %s MB\n", $1, $3, $4
    usage = ($3 / $4) * 100
    printf "  使用率: %.1f%%\n", usage
}'

echo ""
echo "🌐 API 请求统计"
echo "────────────────────────────────────────"
request_count=$(docker exec ${CONTAINER_NAME} grep "POST /v1/chat/completions" /tmp/vllm.log 2>/dev/null | wc -l)
echo "总处理请求数: $request_count"

echo ""
echo "========================================"
echo "💡 提示:"
echo "  - 实时监控: ./monitor_vllm.sh"
echo "  - 详细指南: cat VLLM_MONITORING_GUIDE.md"
echo "========================================"
