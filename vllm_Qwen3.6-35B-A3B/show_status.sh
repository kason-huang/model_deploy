#!/bin/bash
# vLLM 服务状态快速查看

CONTAINER_NAME="vllm-qwen3"
API_BASE="http://localhost:30000"

echo "========================================"
echo "📊 vLLM 服务状态"
echo "========================================"
echo "📅 检查时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 1. 快速状态
echo "🔍 快速状态检查"
echo "────────────────────────────────────────"

# 容器状态
if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "✅ 容器: 运行中"
else
    echo "❌ 容器: 未运行"
    echo ""
    echo "💡 提示: 运行 ./start_vllm.sh 启动服务"
    exit 1
fi

# API 状态
if curl -s "${API_BASE}/v1/models" > /dev/null 2>&1; then
    echo "✅ API: 正常"
else
    echo "⚠️  API: 响应异常"
fi

# GPU 状态
if docker exec ${CONTAINER_NAME} nvidia-smi > /dev/null 2>&1; then
    echo "✅ GPU: 可用"
else
    echo "❌ GPU: 不可用"
fi

echo ""

# 2. 详细信息
echo "📋 详细信息"
echo "────────────────────────────────────────"

# 模型信息
echo "🤖 模型信息:"
curl -s "${API_BASE}/v1/models" 2>/dev/null | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    model = data['data'][0]
    print(f'   名称: {model[\"id\"]}')
    print(f'   最大长度: {model[\"max_model_len\"]} tokens')
    print(f'   路径: {model[\"root\"]}')
except:
    print('   (获取失败)')
" 2>/dev/null

echo ""

# GPU 详情
echo "🎮 GPU 详情:"
docker exec ${CONTAINER_NAME} nvidia-smi --query-gpu=index,name,utilization.gpu,memory.used,memory.total --format=csv,noheader 2>/dev/null | awk '{
    printf "   GPU %s: %s\n", $1, $2
    printf "   利用率: %s%%\n", $3
    printf "   显存: %s / %s MB\n", $4, $5
    print ""
}' | head -8

echo ""

# 3. 最近日志
echo "📝 最近日志 (最后10行)"
echo "────────────────────────────────────────"
docker logs --tail 10 ${CONTAINER_NAME} 2>&1 | sed 's/^/  /'

echo ""
echo "========================================"
echo "💡 相关命令:"
echo "  实时监控: ./monitor_service.sh"
echo "  查看日志: ./logs_vllm.sh"
echo "  停止服务: ./stop_vllm.sh"
echo "========================================"
