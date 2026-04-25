#!/bin/bash

# vLLM 日志查看脚本
# 用途：实时查看 vLLM 服务日志

CONTAINER_NAME="vllm-qwen3"

echo "实时查看 ${CONTAINER_NAME} 日志（Ctrl+C 退出）"
echo "========================================"

docker logs -f "${CONTAINER_NAME}"
