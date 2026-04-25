#!/bin/bash
# 快速API测试脚本

API_BASE="http://localhost:30000"
MODEL_NAME="qwen3.6-35b-a3b"

echo "========================================"
echo "🧪 vLLM API 快速测试"
echo "========================================"
echo ""

# 测试1: 健康检查
echo "[1/4] 健康检查"
if curl -s "${API_BASE}/health" > /dev/null 2>&1; then
    echo "  ✅ 服务正常"
else
    echo "  ❌ 服务异常"
    exit 1
fi
echo ""

# 测试2: 模型信息
echo "[2/4] 模型信息"
curl -s "${API_BASE}/v1/models" | python3 -c "
import sys, json
data = json.load(sys.stdin)
model = data['data'][0]
print(f'  模型名称: {model[\"id\"]}')
print(f'  最大长度: {model[\"max_model_len\"]} tokens')
print(f'  模型路径: {model[\"root\"]}')
"
echo ""

# 测试3: 简单推理
echo "[3/4] 推理测试: 1+1=?"
curl -s -X POST "${API_BASE}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"${MODEL_NAME}\",
    \"messages\": [{\"role\": \"user\", \"content\": \"1+1等于几？只回答数字。\"}],
    \"max_tokens\": 512,
    \"temperature\": 0.0
  }" | python3 -c "
import sys, json
data = json.load(sys.stdin)
msg = data['choices'][0]['message']
content = msg.get('content', '(无)')
print(f'  答案: {content}')
print(f'  使用tokens: {data[\"usage\"][\"total_tokens\"]}')
"
echo ""

# 测试4: 响应时间
echo "[4/4] 性能测试"
start=$(date +%s.%N)
curl -s -X POST "${API_BASE}/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d "{
    \"model\": \"${MODEL_NAME}\",
    \"messages\": [{\"role\": \"user\", \"content\": \"你好\"}],
    \"max_tokens\": 50
  }" > /dev/null
end=$(date +%s.%N)
elapsed=$(echo "$end - $start" | bc)
printf "  响应时间: %.2f 秒\n" $elapsed
echo ""

echo "========================================"
echo "✅ 测试完成！"
echo "========================================"
echo ""
echo "💡 提示:"
echo "  - 运行完整测试: ./test_api.sh"
echo "  - Python测试: ./test_api.py"
echo "  - 查看日志: ./logs_vllm.sh"
echo ""
