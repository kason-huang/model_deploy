# vLLM Qwen3.6-35B-A3B 模型部署文档

## 📋 目录
- [环境信息](#环境信息)
- [部署准备](#部署准备)
- [部署流程](#部署流程)
- [遇到的问题与解决方案](#遇到的问题与解决方案)
- [验证与测试](#验证与测试)
- [运维管理](#运维管理)

---

## 环境信息

### 硬件配置
- **GPU**: 8 张 NVIDIA GPU（V100，计算能力 7.0）
- **CPU**: 未指定
- **内存**: 建议至少 128GB
- **磁盘**: 模型文件约 70GB+

### 软件环境
- **操作系统**: Linux 5.15.0-76-generic
- **Docker 版本**: 29.1.5
- **Docker 镜像**: vllm/vllm-openai:latest
- **vLLM 版本**: 0.19.1
- **Python**: 3.12（容器内）

### 模型信息
- **模型名称**: Qwen3.6-35B-A3B
- **模型架构**: Qwen3_5MoeForConditionalGeneration
- **模型大小**: 35B 参数（MoE 架构）
- **模型路径**: /home/user/models/Qwen3.6-35B-A3B
- **服务名称**: qwen3.6-35b-a3b

---

## 部署准备

### 1. 环境检查

在开始部署前，需要确认以下环境：

```bash
# 检查 Docker 是否安装
docker --version

# 检查 GPU 可用性
nvidia-smi

# 检查 GPU 数量（需要至少 8 张）
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader | wc -l

# 检查模型文件是否存在
ls -la /home/user/models/Qwen3.6-35B-A3B/

# 检查磁盘空间
df -h /home/user/models/
```

### 2. 创建部署脚本

创建以下脚本文件用于自动化部署：

#### start_vllm.sh（启动脚本）
```bash
#!/bin/bash
set -e

CONTAINER_NAME="vllm-qwen3"
IMAGE="vllm/vllm-openai:latest"
PORT=30000
HOST_PATH="/home/user/models"

# 启动容器（覆盖默认入口点）
docker run -itd --rm --name "${CONTAINER_NAME}" \
    --gpus all \
    --net=host \
    --shm-size 32g \
    -v "${HOST_PATH}:/models" \
    --entrypoint "" \
    "${IMAGE}" sleep infinity

# 启动 vLLM 服务
docker exec -d "${CONTAINER_NAME}" bash -c 'export VLLM_USE_FLASH_ATTN=0 && cd / && python3 -m vllm.entrypoints.openai.api_server --model /models/Qwen3.6-35B-A3B --served-model-name qwen3.6-35b-a3b --tensor-parallel-size 8 --port 30000 --host 0.0.0.0 --dtype float16 --trust-remote-code --gpu-memory-utilization 0.9 --max-model-len 32768 --reasoning-parser qwen3'
```

#### 其他辅助脚本
- `stop_vllm.sh`: 停止服务
- `logs_vllm.sh`: 查看日志
- `test_api.sh`: Bash API 测试
- `test_api.py`: Python 客户端示例

---

## 部署流程

### 步骤 1: 环境验证

```bash
$ docker --version
Docker version 29.1.5, build 0e6fee6

$ nvidia-smi --query-gpu=name,memory.total --format=csv,noheader | wc -l
8

$ ls -la /home/user/models/
drwxr-xr-x 3 root root 4096 Apr 25 11:11 Qwen3.6-35B-A3B
```

✅ 环境检查通过

### 步骤 2: 启动容器

```bash
docker run -itd --rm --name vllm-qwen3 \
    --gpus all \
    --net=host \
    --shm-size 32g \
    -v /home/user/models:/models \
    --entrypoint "" \
    vllm/vllm-openai:latest sleep infinity
```

**参数说明**:
- `--gpus all`: 使用所有可用 GPU
- `--net=host`: 使用宿主机网络（避免端口映射问题）
- `--shm-size 32g`: 设置共享内存 32GB
- `-v /home/user/models:/models`: 挂载模型目录
- `--entrypoint ""`: 覆盖默认入口点（重要！）
- `sleep infinity`: 保持容器运行

### 步骤 3: 启动 vLLM 服务

```bash
docker exec -d vllm-qwen3 bash -c \
  'export VLLM_USE_FLASH_ATTN=0 && cd / && \
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
    --reasoning-parser qwen3'
```

**参数说明**:
- `--model`: 模型路径（容器内路径）
- `--served-model-name`: API 调用时使用的模型名称
- `--tensor-parallel-size 8`: 使用 8 张 GPU 进行张量并行
- `--port 30000`: API 服务端口
- `--dtype float16`: 使用半精度（FP16）
- `--trust-remote-code`: 信任远程代码（Qwen 模型需要）
- `--gpu-memory-utilization 0.9`: GPU 显存利用率
- `--max-model-len 32768`: 最大序列长度
- `--reasoning-parser qwen3`: 使用 Qwen3 推理解析器

### 步骤 4: 等待服务启动

服务启动需要经历以下阶段：

#### 4.1 模型加载（约 1-2 分钟）
```
Loading safetensors checkpoint shards: 100% Completed | 26/26
Loading weights took 77.06 seconds
Model loading took 8.36 GiB memory and 77.514684 seconds
```

#### 4.2 torch.compile 编译（约 1 分钟）
```
Dynamo bytecode transform time: 8.63 s
Compiling a graph for compile range (1, 2048) takes 36.81 s
torch.compile took 48.00 s in total
```

#### 4.3 Triton 内核编译（约 3-5 分钟）
```
# 会看到多个 PTXAS 进程运行
/usr/local/lib/python3.12/dist-packages/triton/backends/nvidia/bin/ptxas
```

#### 4.4 服务启动
```
INFO:     Started server process [99]
INFO:     Application startup complete.
```

**总启动时间**: 约 8-10 分钟

### 步骤 5: 验证服务

```bash
# 健康检查
curl http://localhost:30000/health

# 列出模型
curl http://localhost:30000/v1/models

# 测试生成
curl http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3.6-35b-a3b","messages":[{"role":"user","content":"你好"}],"max_tokens":512}'
```

---

## 遇到的问题与解决方案

### 问题 1: 脚本语法错误

**现象**:
```bash
/root/start_vllm.sh: line 17: Qwen3: command not found
```

**原因**:
脚本第 13 行变量定义错误：
```bash
PORT=30000"  # 多了一个引号
```

**解决方案**:
修正变量定义：
```bash
PORT=30000
```

**教训**: 编写脚本后要进行语法检查，特别是变量定义和引号匹配。

---

### 问题 2: 模型路径解析错误

**现象**:
```
model   bash
OSError: Can't load the configuration of 'bash'
```

**原因**:
模型路径 `/models/Qwen3.6-35B-A3B` 包含特殊字符（点 `.` 和连字符 `-`），在使用 `docker exec -d` 的双引号中，变量展开导致路径被错误解析。

**错误代码**:
```bash
docker exec -d "${CONTAINER_NAME}" bash -c "
    --model ${MODEL_PATH}  # 路径被解析为 bash
"
```

**解决方案**:
使用单引号，直接硬编码路径：
```bash
docker exec -d "${CONTAINER_NAME}" bash -c '
    --model /models/Qwen3.6-35B-A3B
'
```

或者使用转义：
```bash
--model \"/models/Qwen3.6-35B-A3B\"
```

**教训**:
- 复杂路径建议使用单引号或直接硬编码
- 使用 `docker exec` 时要注意 shell 变量展开

---

### 问题 3: 容器默认命令冲突

**现象**:
容器内同时运行两个进程：
```
root         1  /usr/bin/python3 /usr/local/bin/vllm serve bash
root         156  python3 -m vllm.entrypoints.openai.api_server --model /models/Qwen3.6-35B-A3B ...
```

**原因**:
`vllm/vllm-openai:latest` 镜像的默认入口点是自动启动 vLLM 服务，导致容器内同时运行两个实例。

**解决方案**:
覆盖默认入口点：
```bash
docker run -itd --rm --name vllm-qwen3 \
    --entrypoint "" \
    vllm/vllm-openai:latest sleep infinity
```

**教训**:
- 使用 `docker inspect <image>` 查看镜像默认配置
- 使用 `--entrypoint ""` 可以覆盖默认入口点
- 使用 `sleep infinity` 保持容器运行

---

### 问题 4: FlashAttention 不兼容

**现象**:
```
ERROR: Cannot use FA version 2 is not supported due to FA2 is only supported on devices with compute capability >= 8
```

**原因**:
V100 GPU 的计算能力为 7.0，不支持 FlashAttention 2（需要计算能力 >= 8.0）。

**解决方案**:
禁用 FlashAttention：
```bash
export VLLM_USE_FLASH_ATTN=0
```

**注意事项**:
- 虽然设置了环境变量，但日志仍显示 FA 错误
- 这是正常的警告，vLLM 会自动降级到其他注意力机制
- 最终使用的是 TRITON_ATTN 后端

**验证**:
```
INFO: Using TRITON_ATTN attention backend
```

**教训**:
- V100 等旧 GPU 需要禁用 FlashAttention
- 检查 GPU 计算能力：`nvidia-smi --query-gpu=compute_cap --format=csv`

---

### 问题 5: PTXAS 编译耗时

**现象**:
服务启动长时间卡在编译阶段：
```
INFO: No available shared memory broadcast block found in 60 seconds.
```

同时看到多个 PTXAS 进程：
```bash
/usr/local/lib/python3.12/dist-packages/triton/backends/nvidia/bin/ptxas
```

**原因**:
Triton 需要为 V100（sm_70）编译 PTX 内核，这是一个计算密集型过程，每张 GPU 都需要编译。

**正常编译时间**:
- 首次启动：3-5 分钟
- 后续启动：使用缓存，约 1-2 分钟

**解决方案**:
这是正常现象，只需等待。可以：
1. 监控 PTXAS 进程：`docker exec vllm-qwen3 ps aux | grep ptxas`
2. 查看日志：`docker logs -f vllm-qwen3`
3. 等待出现：`INFO: Application startup complete.`

**优化建议**:
- 缓存目录：`/root/.cache/vllm/torch_compile_cache/`
- 可以持久化缓存目录以加速后续启动

**教训**:
- 首次启动需要预留 8-10 分钟
- 编译过程是 CPU 密集型，监控 CPU 使用率
- 不要在编译阶段强制终止容器

---

### 问题 6: API 返回内容为空

**现象**:
调用 API 后返回：
```json
{
  "choices": [{
    "message": {
      "content": null,
      "reasoning": "Here's a thinking process:..."
    }
  }],
  "finish_reason": "length"
}
```

**原因**:
1. Qwen3 是推理模型，需要更多 tokens 完成思考过程
2. 默认 `max_tokens=100` 不足以完成推理
3. 推理内容存储在 `reasoning` 字段而非 `content`

**解决方案**:
增加 `max_tokens` 参数：
```bash
curl http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.6-35b-a3b",
    "messages": [{"role": "user", "content": "你好"}],
    "max_tokens": 512
  }'
```

**建议设置**:
- 简单问答：512 tokens
- 复杂推理：1024-2048 tokens
- 长文本生成：4096+ tokens

**API 响应结构**:
```json
{
  "choices": [{
    "message": {
      "content": "实际回答内容",
      "reasoning": "推理过程（可选）"
    }
  }]
}
```

**教训**:
- 推理模型需要预留足够 tokens
- 注意检查 `finish_reason` 字段
- 区分 `content` 和 `reasoning` 字段

---

## 验证与测试

### 1. 健康检查

```bash
$ curl -s http://localhost:30000/health
OK
```

### 2. 模型列表

```bash
$ curl -s http://localhost:30000/v1/models | python3 -m json.tool

{
    "object": "list",
    "data": [
        {
            "id": "qwen3.6-35b-a3b",
            "object": "model",
            "created": 1777088791,
            "owned_by": "vllm",
            "root": "/models/Qwen3.6-35B-A3B",
            "max_model_len": 32768
        }
    ]
}
```

### 3. 文本生成测试

```bash
curl -s http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.6-35b-a3b",
    "messages": [{"role": "user", "content": "1+1等于几？只回答数字。"}],
    "temperature": 0.0,
    "max_tokens": 512
  }'
```

**结果**:
```json
{
  "choices": [{
    "message": {
      "content": "\n\n2",
      "reasoning": "Here's a thinking process:\n\n1. **Analyze User Input:**\n   - Question: \"1+1等于几？\"\n   - Constraint: \"只回答数字。\"\n   ..."
    }
  }],
  "finish_reason": "stop"
}
```

### 4. 性能测试

```bash
# 测试响应时间
time curl -s http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3.6-35b-a3b","messages":[{"role":"user","content":"你好"}],"max_tokens":512}'

# 并发测试
for i in {1..5}; do
  curl -s http://localhost:30000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{"model":"qwen3.6-35b-a3b","messages":[{"role":"user","content":"测试'$i'"}],"max_tokens":100}' &
done
wait
```

---

## 运维管理

### 常用命令

#### 查看服务状态
```bash
# 容器状态
docker ps | grep vllm

# 服务健康
curl http://localhost:30000/health

# GPU 使用
docker exec vllm-qwen3 nvidia-smi
```

#### 日志管理
```bash
# 实时日志
docker logs -f vllm-qwen3

# 最近 100 行
docker logs --tail 100 vllm-qwen3

# 持续监控
watch -n 1 'docker logs --tail 20 vllm-qwen3'
```

#### 服务控制
```bash
# 停止服务
docker stop vllm-qwen3

# 重启服务
docker restart vllm-qwen3

# 进入容器
docker exec -it vllm-qwen3 bash

# 查看进程
docker exec vllm-qwen3 ps aux | grep python
```

### 性能监控

#### GPU 监控
```bash
# 实时监控 GPU
watch -n 1 'docker exec vllm-qwen3 nvidia-smi'

# 查看显存使用
docker exec vllm-qwen3 nvidia-smi --query-gpu=memory.used,memory.total --format=csv
```

#### API 性能
```bash
# 响应时间测试
time curl -s http://localhost:30000/health

# 吞吐量测试
for i in {1..10}; do
  time curl -s http://localhost:30000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{"model":"qwen3.6-35b-a3b","messages":[{"role":"user","content":"测试"}],"max_tokens":50}'
done
```

### 故障排查

#### 服务无法启动
```bash
# 查看详细日志
docker logs --tail 200 vllm-qwen3

# 检查端口占用
netstat -tulpn | grep 30000

# 检查 GPU
nvidia-smi
docker exec vllm-qwen3 nvidia-smi

# 检查模型文件
ls -la /home/user/models/Qwen3.6-35B-A3B/
```

#### API 调用失败
```bash
# 检查服务是否就绪
curl -v http://localhost:30000/health

# 检查模型列表
curl http://localhost:30000/v1/models

# 查看 API 日志
docker logs vllm-qwen3 | grep -i error
```

#### 性能问题
```bash
# 检查 GPU 利用率
docker exec vllm-qwen3 nvidia-smi

# 调整参数
# --gpu-memory-utilization 0.85  # 降低显存使用
# --max-model-len 16384          # 减少序列长度
```

### 配置优化

#### 高吞吐量场景
```bash
--gpu-memory-utilization 0.95
--max-model-len 32768
--dtype float16
--tensor-parallel-size 8
```

#### 低延迟场景
```bash
--gpu-memory-utilization 0.85
--max-model-len 8192
--dtype float16
--tensor-parallel-size 8
```

#### 调试模式
```bash
--gpu-memory-utilization 0.7
--max-model-len 4096
VLLM_USE_FLASH_ATTN=0
```

### 生产部署建议

#### 1. 持久化配置
```bash
# 使用 Docker Compose
cat > docker-compose.yml <<EOF
version: '3'
services:
  vllm:
    image: vllm/vllm-openai:latest
    container_name: vllm-qwen3
    entrypoint: [""]
    command: ["sleep", "infinity"]
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
    volumes:
      - /home/user/models:/models
      - vllm-cache:/root/.cache/vllm
    network_mode: host
    shm_size: 32g
    restart: unless-stopped

volumes:
  vllm-cache:
EOF
```

#### 2. 日志管理
```bash
# 持久化日志
docker run -v /var/log/vllm:/logs \
  --log-driver json-file \
  --log-opt max-size=10m \
  --log-opt max-file=3 \
  vllm-qwen3
```

#### 3. 监控告警
```bash
# 使用 Prometheus + Grafana
# 暴露指标端点
curl http://localhost:30000/metrics
```

#### 4. 负载均衡
```bash
# 启动多实例（不同端口）
for port in 30000 30001 30002; do
  docker run -d --name vllm-qwen3-$port \
    --gpus all \
    -p $port:30000 \
    ...
done

# 使用 Nginx 负载均衡
upstream vllm_backend {
    server localhost:30000;
    server localhost:30001;
    server localhost:30002;
}
```

---

## 总结

### 部署时间线

| 阶段 | 耗时 | 说明 |
|------|------|------|
| 环境准备 | 5 分钟 | 检查环境、创建脚本 |
| 容器启动 | 10 秒 | Docker 容器启动 |
| 模型加载 | 77 秒 | 加载 26 个 checkpoint shards |
| torch.compile | 48 秒 | 编译模型图 |
| Triton 编译 | 3-5 分钟 | PTXAS 编译（首次） |
| 服务启动 | 10 秒 | 启动 API 服务器 |
| **总计** | **8-10 分钟** | 首次启动 |

### 关键经验

1. **环境准备很重要**
   - 确认 GPU 数量和计算能力
   - 验证模型文件完整性
   - 检查磁盘空间

2. **脚本需要仔细测试**
   - 语法检查
   - 变量引号处理
   - 容器入口点覆盖

3. **耐心等待编译**
   - 首次启动需要 8-10 分钟
   - PTXAS 编译是正常现象
   - 不要强制终止进程

4. **API 参数调优**
   - 推理模型需要更多 tokens
   - 区分 content 和 reasoning 字段
   - 注意 finish_reason 状态

5. **运维监控**
   - 使用日志和监控工具
   - 定期检查 GPU 使用率
   - 准备故障排查手册

### 相关资源

- **vLLM 官方文档**: https://docs.vllm.ai/
- **OpenAI API 兼容性**: https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html
- **Qwen3 模型**: https://github.com/QwenLM/Qwen3
- **Triton 文档**: https://triton-lang.org/

### 附录：完整脚本

所有脚本文件已保存在 `/root/` 目录：
- `start_vllm.sh` - 启动脚本
- `stop_vllm.sh` - 停止脚本
- `logs_vllm.sh` - 日志查看
- `test_api.sh` - Bash 测试脚本
- `test_api.py` - Python 客户端
- `README_VLLM_DEPLOYMENT.md` - 完整文档
- `deployment_checklist.md` - 部署清单
- `quick_reference.sh` - 快速参考

---

**文档版本**: v1.0
**最后更新**: 2026-04-25
**部署状态**: ✅ 成功
**服务地址**: http://0.0.0.0:30000
