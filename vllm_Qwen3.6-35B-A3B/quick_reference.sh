#!/bin/bash
#
# vLLM 快速参考卡片
# 显示所有常用命令和操作
#

cat << 'EOF'
╔═══════════════════════════════════════════════════════════════╗
║                    vLLM Qwen3 快速参考                         ║
╚═══════════════════════════════════════════════════════════════╝

📋 基本操作
────────────────────────────────────────────────────────────────
  启动服务：    ./start_vllm.sh
  停止服务：    ./stop_vllm.sh
  查看日志：    ./logs_vllm.sh
  测试API：     ./test_api.sh 或 ./test_api.py

🐳 Docker 命令
────────────────────────────────────────────────────────────────
  查看容器：    docker ps | grep vllm
  查看日志：    docker logs -f vllm-qwen3
  进入容器：    docker exec -it vllm-qwen3 bash
  重启服务：    docker restart vllm-qwen3
  GPU状态：     docker exec vllm-qwen3 nvidia-smi

📡 API 测试
────────────────────────────────────────────────────────────────
  健康检查：    curl http://localhost:30000/health
  模型列表：    curl http://localhost:30000/v1/models
  简单生成：    curl -X POST http://localhost:30000/v1/chat/completions \
                -H "Content-Type: application/json" \
                -d '{"model":"qwen3.6-35b-a3b","messages":[{"role":"user","content":"你好"}]}'

📊 监控命令
────────────────────────────────────────────────────────────────
  实时日志：    tail -f <(docker logs vllm-qwen3)
  GPU监控：     watch -n 1 'docker exec vllm-qwen3 nvidia-smi'
  API延迟：    time curl -s http://localhost:30000/health

🔧 故障排查
────────────────────────────────────────────────────────────────
  检查容器：    docker ps -a | grep vllm
  最近日志：    docker logs --tail 100 vllm-qwen3
  端口占用：    netstat -tulpn | grep 30000
  磁盘空间：    df -h /home/user/models/

⚙️  配置文件
────────────────────────────────────────────────────────────────
  启动脚本：    /root/start_vllm.sh
  测试脚本：    /root/test_api.sh
  Python客户端：/root/test_api.py
  完整文档：    /root/README_VLLM_DEPLOYMENT.md
  检查清单：    /root/deployment_checklist.md

💡 提示
────────────────────────────────────────────────────────────────
  - 首次启动需要下载依赖，可能需要5-10分钟
  - 模型加载需要时间，请耐心等待健康检查通过
  - 使用 --tensor-parallel-size 调整GPU数量
  - 使用 --gpu-memory-utilization 调整显存使用率

📚 更多帮助
────────────────────────────────────────────────────────────────
  查看完整文档：  cat README_VLLM_DEPLOYMENT.md
  查看部署清单：  cat deployment_checklist.md
  官方文档：     https://docs.vllm.ai/

EOF
