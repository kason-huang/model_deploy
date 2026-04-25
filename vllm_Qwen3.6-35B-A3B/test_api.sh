#!/bin/bash

# vLLM API 测试脚本
# 用途：测试部署的 vLLM 服务是否正常工作

set -e

API_BASE="http://localhost:30000/v1"
MODEL_NAME="qwen3-vl"

echo "========================================"
echo "vLLM API 测试"
echo "========================================"

# 测试 1: 健康检查
echo -e "\n[测试 1] 健康检查..."
HEALTH_RESPONSE=$(curl -s http://localhost:30000/health)
echo "响应: ${HEALTH_RESPONSE}"

# 测试 2: 列出模型
echo -e "\n[测试 2] 列出可用模型..."
MODELS_RESPONSE=$(curl -s "${API_BASE}/models")
echo "响应: ${MODELS_RESPONSE}"

# 测试 3: 文本生成（简单问答）
echo -e "\n[测试 3] 文本生成测试..."
curl -s "${API_BASE}/chat/completions" \
    -H "Content-Type: application/json" \
    -d "{
        \"model\": \"${MODEL_NAME}\",
        \"messages\": [
            {
                \"role\": \"user\",
                \"content\": \"你好，请用一句话介绍你自己。\"
            }
        ],
        \"temperature\": 0.7,
        \"max_tokens\": 100
    }" | jq -r '.choices[0].message.content' || echo "生成失败"

# 测试 4: 流式输出
echo -e "\n[测试 4] 流式输出测试（前5个token）..."
echo "提示: 输入 '你好'"
curl -s "${API_BASE}/chat/completions" \
    -H "Content-Type: application/json" \
    -d "{
        \"model\": \"${MODEL_NAME}\",
        \"messages\": [
            {
                \"role\": \"user\",
                \"content\": \"你好\"
            }
        ],
        \"stream\": true,
        \"max_tokens\": 50
    }" | head -n 10

# 测试 5: 推理测试
echo -e "\n\n[测试 5] 推理能力测试..."
echo "提示: 计算 123 + 456 = ?"
curl -s "${API_BASE}/chat/completions" \
    -H "Content-Type: application/json" \
    -d "{
        \"model\": \"${MODEL_NAME}\",
        \"messages\": [
            {
                \"role\": \"user\",
                \"content\": \"计算 123 + 456 = ？只给出最终数字答案。\"
            }
        ],
        \"temperature\": 0.0,
        \"max_tokens\": 50
    }" | jq -r '.choices[0].message.content' || echo "推理失败"

echo -e "\n\n========================================"
echo "测试完成"
echo "========================================"
