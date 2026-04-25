#!/bin/bash

# vLLM 服务停止脚本
# 用途：优雅地停止 vLLM 容器

set -e

CONTAINER_NAME="vllm-qwen3"

echo "正在停止容器 ${CONTAINER_NAME}..."

if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    docker stop "${CONTAINER_NAME}"
    echo "✓ 容器已停止"
else
    echo "提示：容器 ${CONTAINER_NAME} 未在运行"
fi
