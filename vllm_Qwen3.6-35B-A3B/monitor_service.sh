#!/bin/bash
# vLLM 服务实时监控脚本

CONTAINER_NAME="vllm-qwen3"
API_BASE="http://localhost:30000"

clear
echo "========================================"
echo "🔍 vLLM 服务实时监控"
echo "========================================"
echo "按 Ctrl+C 退出"
echo "========================================"
echo ""

while true; do
    clear
    echo "========================================"
    echo "🔍 vLLM 服务实时监控"
    echo "========================================"
    echo "📅 时间: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""

    # 1. 容器状态
    echo "📦 [1/5] 容器状态"
    echo "────────────────────────────────────────"
    if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        status=$(docker inspect -f '{{.State.Status}}' ${CONTAINER_NAME})
        uptime=$(docker inspect -f '{{.State.StartedAt}}' ${CONTAINER_NAME} | xargs date -d)
        echo "  ✅ 容器状态: 运行中"
        echo "  📅 启动时间: $uptime"
    else
        echo "  ❌ 容器状态: 未运行"
    fi
    echo ""

    # 2. API 状态
    echo "🌐 [2/5] API 服务状态"
    echo "────────────────────────────────────────"
    if curl -s "${API_BASE}/v1/models" > /dev/null 2>&1; then
        echo "  ✅ API 服务: 正常"
        model_info=$(curl -s "${API_BASE}/v1/models" 2>/dev/null | python3 -c "import sys, json; data=json.load(sys.stdin); print(f'{data[\"data\"][0][\"id\"]} ({data[\"data\"][0][\"max_model_len\"]} tokens)')" 2>/dev/null)
        echo "  🤖 模型信息: $model_info"
    else
        echo "  ❌ API 服务: 不可用"
    fi
    echo ""

    # 3. GPU 状态
    echo "🎮 [3/5] GPU 使用情况"
    echo "────────────────────────────────────────"
    if docker exec ${CONTAINER_NAME} nvidia-smi > /dev/null 2>&1; then
        gpu_count=$(docker exec ${CONTAINER_NAME} nvidia-smi --query-gpu=count --format=csv,noheader 2>/dev/null)
        gpu_usage=$(docker exec ${CONTAINER_NAME} nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader 2>/dev/null | head -1)
        echo "  📊 GPU 数量: $gpu_count"
        echo "  💻 GPU 利用率: $gpu_usage"
    else
        echo "  ❌ 无法获取 GPU 信息"
    fi
    echo ""

    # 4. 进程状态
    echo "⚙️  [4/5] 进程状态"
    echo "────────────────────────────────────────"
    process_count=$(docker exec ${CONTAINER_NAME} ps aux | grep -E "(vllm|python)" | grep -v grep | wc -l)
    echo "  🔢 进程数量: $process_count"
    if [ $process_count -gt 0 ]; then
        echo "  📌 主进程:"
        docker exec ${CONTAINER_NAME} ps aux | grep -E "vllm.*api_server" | grep -v grep | awk '{printf "     PID %s, MEM %s, CPU %s%%\n", $2, $6, $4}' | head -1
    fi
    echo ""

    # 5. 最新日志
    echo "📝 [5/5] 最新日志 (最后5行)"
    echo "────────────────────────────────────────"
    docker logs --tail 5 ${CONTAINER_NAME} 2>&1 | sed 's/^/  /'
    echo ""

    echo "========================================"
    echo "⏱️  刷新间隔: 5秒 | 按 Ctrl+C 退出"
    echo "========================================"

    sleep 5
done
