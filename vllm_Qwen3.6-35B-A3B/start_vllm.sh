#!/bin/bash

# vLLM Qwen3 模型部署脚本
# 用途：端到端启动 vLLM 服务

set -e

# 配置变量
CONTAINER_NAME="vllm-qwen3"
IMAGE="vllm/vllm-openai:latest"
MODEL_PATH="/models/Qwen3.6-35B-A3B"
SERVED_MODEL_NAME="qwen3.6-35b-a3b"
PORT=30000
HOST_PATH="/home/user/models"

echo "========================================"
echo "vLLM Qwen3 模型部署脚本"
echo "========================================"

# 检查是否存在同名容器
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "检测到已存在的容器 ${CONTAINER_NAME}，正在删除..."
    docker stop "${CONTAINER_NAME}" 2>/dev/null || true
    docker rm "${CONTAINER_NAME}" 2>/dev/null || true
fi

# 检查模型路径是否存在
if [ ! -d "${HOST_PATH}" ]; then
    echo "错误：模型路径 ${HOST_PATH} 不存在！"
    echo "请确保已下载模型到该目录"
    exit 1
fi

echo "步骤 1: 启动容器..."
docker run -itd --rm --name "${CONTAINER_NAME}" \
    --gpus all \
    --net=host \
    --shm-size 32g \
    -v "${HOST_PATH}:/models" \
    "${IMAGE}" bash

echo "步骤 2: 等待容器就绪..."
sleep 3

# 检查容器是否运行
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "错误：容器启动失败！"
    exit 1
fi

echo "步骤 3: 启动 vLLM 服务..."
docker exec -d "${CONTAINER_NAME}" bash -c '
    export VLLM_USE_FLASH_ATTN=0
    python3 -m vllm.entrypoints.openai.api_server \
        --model /models/Qwen3.6-35B-A3B \
        --served-model-name qwen3.6-35b-a3b \
        --tensor-parallel-size 8 \
        --port 30000 \
        --host 0.0.0.0 \
        --dtype float16 \
        --trust-remote-code \
        --gpu-memory-utilization 0.9 \
        --max-model-len 32768 \
        --reasoning-parser qwen3
'

echo "步骤 4: 等待服务启动（这可能需要几分钟）..."
echo "提示：您可以使用 'docker logs -f ${CONTAINER_NAME}' 查看详细日志"

# 等待服务响应
MAX_WAIT=300  # 最多等待5分钟
WAIT_TIME=0
while [ $WAIT_TIME -lt $MAX_WAIT ]; do
    if curl -s http://localhost:${PORT}/health > /dev/null 2>&1; then
        echo ""
        echo "========================================"
        echo "✓ vLLM 服务启动成功！"
        echo "========================================"
        echo "服务地址: http://0.0.0.0:${PORT}"
        echo "模型名称: ${SERVED_MODEL_NAME}"
        echo ""
        echo "常用命令："
        echo "  查看日志: docker logs -f ${CONTAINER_NAME}"
        echo "  进入容器: docker exec -it ${CONTAINER_NAME} bash"
        echo "  停止服务: docker stop ${CONTAINER_NAME}"
        echo "  测试API: ./test_api.sh"
        echo "========================================"
        exit 0
    fi
    echo -n "."
    sleep 2
    WAIT_TIME=$((WAIT_TIME + 2))
done

echo ""
echo "警告：服务未在预期时间内启动"
echo "请检查日志：docker logs ${CONTAINER_NAME}"
exit 1
