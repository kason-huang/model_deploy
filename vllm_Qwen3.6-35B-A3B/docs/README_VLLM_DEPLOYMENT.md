# vLLM Qwen3 模型部署指南

## 📋 前置要求

1. **Docker 已安装**：确保 Docker 和 nvidia-docker 已正确安装
2. **GPU 资源**：至少 8 张 GPU（tensor-parallel-size=8）
3. **模型文件**：模型已下载到 `/home/user/models/Qwen3.6-35B-A3B`
4. **内存**：系统内存充足（建议 128GB+）

## 🚀 快速开始

### 1. 一键启动服务

```bash
./start_vllm.sh
```

该脚本会自动：
- ✅ 检查并清理旧容器
- ✅ 验证模型路径
- ✅ 启动 Docker 容器
- ✅ 启动 vLLM 服务
- ✅ 等待服务就绪

### 2. 测试 API 服务

```bash
./test_api.sh
```

测试内容包括：
- 健康检查
- 模型列表
- 文本生成
- 流式输出
- 推理能力

### 3. 查看服务日志

```bash
./logs_vllm.sh
```

### 4. 停止服务

```bash
./stop_vllm.sh
```

## 🔧 配置说明

### 容器配置

| 参数 | 值 | 说明 |
|------|-----|------|
| 容器名称 | vllm-qwen3 | 可修改 |
| GPU | all | 使用所有可用 GPU |
| 网络模式 | host | 直接使用宿主机网络 |
| 共享内存 | 32GB | 用于模型加载 |

### 模型配置

| 参数 | 值 | 说明 |
|------|-----|------|
| 模型路径 | /models/Qwen3.6-35B-A3B | 容器内路径 |
| 服务名称 | qwen3.6-35b-a3b | API 调用使用的名称 |
| 端口 | 30000 | API 服务端口 |
| Tensor 并行 | 8 | 分布在 8 张 GPU |
| 数据类型 | float16 | 半精度 |
| GPU 利用率 | 0.9 | 显存利用率 |
| 最大长度 | 32768 | 最大序列长度 |
| FlashAttention | 禁用 | V100 兼容性 |

## 📡 API 使用示例

### Python 客户端

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:30000/v1",
    api_key="dummy"  # vLLM 不需要真实密钥
)

response = client.chat.completions.create(
    model="qwen3.6-35b-a3b",
    messages=[
        {"role": "user", "content": "你好！"}
    ],
    temperature=0.7,
    max_tokens=100
)

print(response.choices[0].message.content)
```

### cURL 示例

```bash
curl http://localhost:30000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "qwen3.6-35b-a3b",
        "messages": [{"role": "user", "content": "你好！"}],
        "temperature": 0.7,
        "max_tokens": 100
    }'
```

## 🛠️ 常用 Docker 命令

```bash
# 查看容器状态
docker ps

# 查看容器日志
docker logs -f vllm-qwen3

# 进入容器
docker exec -it vllm-qwen3 bash

# 在容器内执行命令
docker exec vllm-qwen3 nvidia-smi

# 重启服务
docker restart vllm-qwen3

# 强制停止
docker kill vllm-qwen3
```

## 📊 监控指标

### GPU 使用率

```bash
docker exec vllm-qwen3 nvidia-smi
```

### API 性能测试

```bash
# 简单压测
for i in {1..10}; do
    time curl -s http://localhost:30000/health
done
```

## ⚠️ 故障排查

### 问题 1：容器启动失败

```bash
# 检查 Docker 服务
sudo systemctl status docker

# 检查 GPU 可用性
nvidia-smi

# 检查模型路径
ls -la /home/user/models/
```

### 问题 2：服务未响应

```bash
# 查看详细日志
docker logs --tail 100 vllm-qwen3

# 检查端口占用
netstat -tulpn | grep 30000

# 检查 GPU 显存
docker exec vllm-qwen3 nvidia-smi
```

### 问题 3：OOM（显存不足）

修改 `start_vllm.sh` 中的参数：
- 降低 `--gpu-memory-utilization`（如 0.85）
- 减少 `--max-model-len`（如 16384）
- 减少 `--tensor-parallel-size`（如 4）

## 📝 参数调优建议

### 高吞吐量场景

```bash
--gpu-memory-utilization 0.95
--max-model-len 32768
--dtype float16
```

### 低延迟场景

```bash
--gpu-memory-utilization 0.85
--max-model-len 8192
--dtype float16
```

### 调试模式

```bash
--gpu-memory-utilization 0.7
--max-model-len 4096
VLLM_USE_FLASH_ATTN=0
```

## 📚 参考文档

- [vLLM 官方文档](https://docs.vllm.ai/)
- [OpenAI API 兼容性](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html)
- [Qwen3 模型文档](https://github.com/QwenLM/Qwen3)
