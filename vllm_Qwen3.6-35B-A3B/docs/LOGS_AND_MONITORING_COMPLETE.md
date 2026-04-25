# vLLM 日志与监控完整指南

## 📋 目录
- [日志查看方法](#日志查看方法)
- [监控服务](#监控服务)
- [性能分析](#性能分析)
- [实战演示](#实战演示)
- [最佳实践](#最佳实践)

---

## 📝 日志查看方法

### 🚀 快速开始（3个最常用命令）

```bash
# 1. 进入容器查看（最灵活）
docker exec -it vllm-qwen3 bash
tail -f /tmp/vllm.log

# 2. 从外部直接查看（最方便）
docker exec vllm-qwen3 tail -50 /tmp/vllm.log

# 3. Docker日志（可能为空）
docker logs --tail 50 vllm-qwen3
```

---

### 📂 日志文件位置

#### 容器内日志
```
/tmp/vllm.log           # vLLM 主日志文件 ⭐
/tmp/*.log              # 其他临时日志
/root/.cache/vllm/     # 缓存和编译日志
```

#### 容器外查看
```bash
# 查看日志文件大小
docker exec vllm-qwen3 ls -lh /tmp/vllm.log

# 查看文件大小
docker exec vllm-qwen3 du -sh /tmp/vllm.log
```

---

### 🔍 方法1: 进入容器查看

#### 步骤

```bash
# 1. 进入容器
docker exec -it vllm-qwen3 bash

# 2. 查看日志文件
ls -la /tmp/
tail -f /tmp/vllm.log

# 3. 查看进程信息
ps aux | grep vllm

# 4. 查看GPU状态
nvidia-smi

# 5. 退出容器
exit
```

#### 容器内常用命令

```bash
# 实时跟踪日志
tail -f /tmp/vllm.log

# 查看最近50行
tail -50 /tmp/vllm.log

# 查看最近100行
tail -100 /tmp/vllm.log

# 搜索错误日志
grep -i error /tmp/vllm.log | tail -20

# 搜索性能日志
grep "throughput" /tmp/vllm.log | tail -10
```

---

### 🔍 方法2: 从容器外查看

#### 基础命令

```bash
# 查看最近50行
docker exec vllm-qwen3 tail -50 /tmp/vllm.log

# 实时跟踪
docker exec -it vllm-qwen3 tail -f /tmp/vllm.log

# 搜索错误
docker exec vllm-qwen3 grep -i error /tmp/vllm.log

# 搜索性能信息
docker exec vllm-qwen3 grep throughput /tmp/vllm.log
```

#### 高级过滤

```bash
# 查找包含特定关键字的日志
docker exec vllm-qwen3 grep "POST /v1/chat/completions" /tmp/vllm.log

# 查找最近的错误
docker exec vllm-qwen3 grep -i error /tmp/vllm.log | tail -10

# 统计错误数量
docker exec vllm-qwen3 grep -ci error /tmp/vllm.log

# 查看最近10分钟的日志
docker exec vllm-qwen3 tail -500 /tmp/vllm.log | grep "INFO" | tail -20
```

---

### 🔍 方法3: Docker日志

```bash
# 查看Docker日志
docker logs vllm-qwen3

# 实时跟踪Docker日志
docker logs -f vllm-qwen3

# 查看最近100行
docker logs --tail 100 vllm-qwen3

# 查看带时间戳的日志
docker logs -t vllm-qwen3 | tail -20

# 查看最近1分钟的日志
docker logs --since 1m vllm-qwen3
```

**注意**: vLLM 服务日志重定向到 `/tmp/vllm.log`，Docker日志可能为空。

---

## 📊 监控服务

### 🎯 vLLM 内置监控能力

vLLM 提供了 **Prometheus 格式**的标准监控指标端点。

#### 监控端点

| 端点 | URL | 格式 | 说明 |
|------|-----|------|------|
| **指标端点** | `http://localhost:30000/metrics` | Prometheus | 标准监控指标 ⭐ |
| **健康检查** | `http://localhost:30000/health` | 文本 | 服务健康状态 |
| **模型信息** | `http://localhost:30000/v1/models` | JSON | 模型列表 |

---

### 📈 关键监控指标

#### 1️⃣ 请求状态指标

```bash
# 查看请求状态
curl -s http://localhost:30000/metrics | grep "num_requests"
```

**输出示例**:
```
vllm:num_requests_running{engine="0",model_name="qwen3.6-35b-a3b"} 0.0
vllm:num_requests_waiting{engine="0",model_name="qwen3.6-35b-a3b"} 0.0
```

**指标说明**:
- `num_requests_running`: 当前正在执行的请求数
- `num_requests_waiting`: 排队等待的请求数
- **正常值**: running: 0-5, waiting: 0-10
- **告警值**: running > 10, waiting > 20

---

#### 2️⃣ Token吞吐指标

```bash
# 查看Token统计
curl -s http://localhost:30000/metrics | grep "tokens_sum"
```

**输出示例**:
```
vllm:request_prompt_tokens_sum{engine="0",model_name="qwen3.6-35b-a3b"} 4027.0
vllm:request_generation_tokens_sum{engine="0",model_name="qwen3.6-35b-a3b"} 8234.0
```

**吞吐量计算**:
```bash
# 方法1: 从日志中查看（实时）
docker exec vllm-qwen3 tail -10 /tmp/vllm.log | grep throughput

# 方法2: 从metrics计算
# 采样1
TOKENS1=$(curl -s http://localhost:30000/metrics | grep "generation_tokens_sum" | awk '{print $2}')
sleep 60
# 采样2
TOKENS2=$(curl -s http://localhost:30000/metrics | grep "generation_tokens_sum" | awk '{print $2}')
# 计算
RATE=$(echo "($TOKENS2 - $TOKENS1) / 60" | bc -l)
echo "生成吞吐量: $RATE tokens/s"
```

---

#### 3️⃣ 缓存效率指标

**从日志中查看缓存命中率**:
```bash
docker exec vllm-qwen3 tail -20 /tmp/vllm.log | grep "cache hit rate"
```

**输出示例**:
```
GPU KV cache usage: 0.1%
Prefix cache hit rate: 0.0%
MM cache hit rate: 70.0%
```

**缓存类型说明**:
- **GPU KV cache**: KV缓存使用率（越低越好，说明有空闲容量）
- **Prefix cache**: 前缀缓存命中率（越高越好，重复prompt加速）
- **MM cache**: 多模态缓存命中率（越高越好，图像缓存）

---

#### 4️⃣ GPU利用指标

**查看GPU状态**:
```bash
docker exec vllm-qwen3 nvidia-smi
```

**从metrics查看GPU FLOPS**:
```bash
curl -s http://localhost:30000/metrics | grep "flops_per_gpu"
```

---

## 🧪 实战演示

### 演示1: 查看当前服务状态

```bash
# 检查容器状态
docker ps | grep vllm-qwen3

# 查看请求指标
curl -s http://localhost:30000/metrics | grep "num_requests"

# 查看GPU使用
docker exec vllm-qwen3 nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader
```

**实际输出**:
```
✓ 容器运行中
✓ 当前无请求（空闲）
✓ GPU显存: 每个GPU 32GB / 32768MB
```

---

### 演示2: 性能分析

**运行性能分析脚本**:
```bash
cd /root/vllm_Qwen3.6-35B-A3B/
./analyze_vllm_performance.sh
```

**输出示例**:
```
📈 最近10次请求的吞吐量统计
────────────────────────────────────────
Avg generation throughput: 20.5 tokens/s
Avg prompt throughput: 32.4 tokens/s

💾 缓存效率统计
────────────────────────────────────────
MM cache hit rate: 70.0%
```

---

### 演示3: 实时监控

**运行实时监控脚本**:
```bash
cd /root/vllm_Qwen3.6-35B-A3B/
./monitor_vllm.sh
```

**监控仪表板显示**:
```
========================================
🔍 vLLM 服务监控
========================================
📅 时间: 2026-04-25 15:20:30

📊 [1/4] 请求状态
  运行中: 0 个请求
  等待中: 0 个请求

💾 [2/4] 缓存状态
  KV缓存使用: 0.0%
  MM缓存命中率: 72%

🎮 [3/4] GPU 状态
  GPU 0: Tesla V100S-PCIE-32GB
    利用率: 0%
    显存: 32002 / 32768 MB

📝 [4/4] 最新日志
  (最新3行日志...)
```

---

## 📊 性能分析

### 日志中的性能指标

vLLM 日志每完成一个请求后都会输出性能统计：

```
INFO [loggers.py:259] Engine 000: Avg prompt throughput: 32.4 tokens/s, 
                          Avg generation throughput: 15.5 tokens/s, 
                          Running: 1 reqs, 
                          Waiting: 0 reqs, 
                          GPU KV cache usage: 0.1%, 
                          Prefix cache hit rate: 0.0%, 
                          MM cache hit rate: 50.0%
```

#### 指标解释

| 指标 | 说明 | 正常范围 |
|------|------|----------|
| **Avg prompt throughput** | 输入处理速度 | 10-50 tokens/s |
| **Avg generation throughput** | 输出生成速度 | 5-20 tokens/s |
| **Running** | 正在处理的请求数 | 0-5 |
| **Waiting** | 排队等待的请求数 | 0-10 |
| **GPU KV cache usage** | KV缓存使用率 | 0-30% |
| **Prefix cache hit rate** | 前缀缓存命中率 | 0-100% |
| **MM cache hit rate** | 多模态缓存命中率 | 40-80% |

---

### 性能优化建议

#### 低缓存命中率 (<50%)

**原因**: 
- 请求多样性高，缓存不命中

**解决**:
- 增加批量请求
- 使用相似的prompt
- 启用prefix caching

#### 低吞吐量 (<10 tokens/s)

**原因**:
- GPU利用率低
- 请求间隔长

**解决**:
- 增加并发请求
- 检查GPU是否空闲
- 优化模型配置

#### 高等待请求数 (>10)

**原因**:
- 服务负载过高
- GPU资源不足

**解决**:
- 增加GPU数量
- 减少max_model_len
- 增加tensor_parallel_size

---

## 🛠️ 监控工具

### 工具1: 实时监控脚本 ⭐

**文件**: `monitor_vllm.sh`

**功能**:
- ✅ 实时显示请求状态
- ✅ GPU使用情况
- ✅ 最新日志摘要
- ✅ 自动刷新（5秒间隔）

**使用**:
```bash
cd /root/vllm_Qwen3.6-35B-A3B/
./monitor_vllm.sh
```

---

### 工具2: 性能分析脚本

**文件**: `analyze_vllm_performance.sh`

**功能**:
- ✅ 吞吐量统计
- ✅ 缓存效率分析
- ✅ GPU内存使用
- ✅ 请求总数统计

**使用**:
```bash
cd /root/vllm_Qwen3.6-35B-A3B/
./analyze_vllm_performance.sh
```

---

### 工具3: Prometheus采集

**配置Prometheus采集**:

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'vllm'
    static_configs:
      - targets: ['localhost:30000']
    metrics_path: '/metrics'
```

**启动Prometheus**:
```bash
prometheus --config.file=prometheus.yml
```

**访问Prometheus UI**: http://localhost:9090

---

## 🎯 实际监控数据

### 当前服务状态

**请求统计**:
- 总处理请求: 44个
- 当前运行: 0个
- 当前等待: 0个
- 状态: ✅ 空闲

**性能指标**:
- 生成吞吐: 5-20 tokens/s
- 输入吞吐: 8-113 tokens/s
- 缓存命中率: 70-72%

**资源使用**:
- GPU显存: 32GB/GPU (已满载)
- KV缓存: 0-0.2% (低使用率)
- GPU利用率: 0% (空闲时)

---

### 告警阈值建议

| 指标 | 正常值 | 警告值 | 处理建议 |
|------|--------|--------|----------|
| **等待请求** | 0-5 | >10 | 考虑扩容 |
| **运行请求** | 0-5 | >10 | 服务过载 |
| **缓存命中率** | >50% | <30% | 优化请求 |
| **GPU显存** | 20-32GB | <10GB | 检查配置 |
| **吞吐量** | >10 tokens/s | <5 tokens/s | 性能优化 |

---

## 💡 最佳实践

### 日常监控流程

#### 每天检查（建议）

```bash
# 1. 快速状态检查
curl -s http://localhost:30000/health

# 2. 运行性能分析
cd /root/vllm_Qwen3.6-35B-A3B/
./analyze_vllm_performance.sh

# 3. 查看GPU状态
docker exec vllm-qwen3 nvidia-smi
```

#### 问题排查

```bash
# 1. 查看最近错误
docker exec vllm-qwen3 grep -i error /tmp/vllm.log | tail -20

# 2. 查看性能指标
docker exec vllm-qwen3 tail -100 /tmp/vllm.log | grep throughput

# 3. 检查GPU
docker exec vllm-qwen3 nvidia-smi

# 4. 实时监控
docker exec -it vllm-qwen3 tail -f /tmp/vllm.log
```

---

### 监控脚本使用

#### 1. 实时监控

```bash
cd /root/vllm_Qwen3.6-35B-A3B/
./monitor_vllm.sh
```

**刷新间隔**: 5秒

**显示内容**:
- 📊 请求状态（运行/等待）
- 💾 缓存状态
- 🎮 GPU使用率
- 📝 最新日志

#### 2. 性能分析

```bash
cd /root/vllm_Qwen3.6-35B-A3B/
./analyze_vllm_performance.sh
```

**显示内容**:
- 📈 最近10次请求吞吐量
- 💾 缓存效率统计
- 🎮 GPU内存使用
- 🌐 总请求数统计

---

## 📚 相关文档

### 已创建的文档

| 文件 | 大小 | 说明 |
|------|------|------|
| **VLLM_LOGS_GUIDE.md** | 12KB | 日志查看完整指南 |
| **VLLM_MONITORING_GUIDE.md** | 15KB | 监控服务完整指南 |
| **monitor_vllm.sh** | 2.7KB | 实时监控脚本 ⭐ |
| **analyze_vllm_performance.sh** | 2.1KB | 性能分析脚本 |

### 文档内容

**VLLM_LOGS_GUIDE.md**:
- 3种日志查看方法详解
- 进入容器查看
- 容器外直接查看
- Docker日志查看
- 高级过滤技巧
- 导出日志

**VLLM_MONITORING_GUIDE.md**:
- Prometheus指标端点
- 关键指标详解
- 监控工具使用
- Prometheus集成
- 性能分析方法

---

## 🎓 总结

### vLLM 监控核心要点

#### 1. 日志位置
- **主日志**: `/tmp/vllm.log` (容器内)
- **查看方式**: `docker exec vllm-qwen3 tail -f /tmp/vllm.log`

#### 2. 监控端点
- **指标端点**: `http://localhost:30000/metrics` (Prometheus格式)
- **健康检查**: `http://localhost:30000/health`

#### 3. 关键指标
- **请求状态**: num_requests_running, num_requests_waiting
- **吞吐量**: prompt_tokens/s, generation_tokens/s
- **缓存效率**: KV cache usage, cache hit rate
- **GPU利用**: FLOPS utilization, memory usage

#### 4. 工具脚本
- **实时监控**: `./monitor_vllm.sh` ⭐
- **性能分析**: `./analyze_vllm_performance.sh`

---

### 快速参考卡

```bash
# === 日志查看 ===
docker exec -it vllm-qwen3 bash
tail -f /tmp/vllm.log

# === 监控指标 ===
curl -s http://localhost:30000/metrics | grep vllm:

# === 性能分析 ===
cd /root/vllm_Qwen3.6-35B-A3B/
./analyze_vllm_performance.sh

# === 实时监控 ===
./monitor_vllm.sh

# === GPU状态 ===
docker exec vllm-qwen3 nvidia-smi
```

---

**vLLM 的日志和监控功能非常完善，推荐使用 `monitor_vllm.sh` 进行实时监控！** 🎉

## 🔧 故障排查

### 问题1: 日志为空

**现象**:
```bash
docker exec vllm-qwen3 tail -50 /tmp/vllm.log
# 无输出
```

**解决**:
```bash
# 检查服务是否运行
curl http://localhost:30000/health

# 检查进程
docker exec vllm-qwen3 ps aux | grep vllm

# 查看Docker日志
docker logs --tail 50 vllm-qwen3
```

---

### 问题2: metrics端点无响应

**现象**:
```bash
curl -s http://localhost:30000/metrics
# 无响应
```

**解决**:
```bash
# 1. 检查服务是否启动
curl http://localhost:30000/v1/models

# 2. 检查端口占用
netstat -tulpn | grep 30000

# 3. 查看容器状态
docker ps | grep vllm-qwen3
```

---

### 问题3: GPU利用率低

**现象**:
```
GPU利用率: 0%
显存使用: 32GB (满载)
```

**分析**:
- 正常现象！vLLM按需使用GPU
- 显存预加载以供快速响应
- 有请求时GPU才会工作

**验证**:
```bash
# 发送测试请求
curl -X POST http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3.6-35b-a3b","messages":[{"role":"user","content":"测试"}],"max_tokens":50}'

# 实时监控GPU
watch -n 1 'docker exec vllm-qwen3 nvidia-smi'
```

---

## 📞 获取帮助

### 查看文档

```bash
cd /root/vllm_Qwen3.6-35B-A3B/

# 查看日志指南
cat VLLM_LOGS_GUIDE.md

# 查看监控指南
cat VLLM_MONITORING_GUIDE.md

# 查看快速参考
./quick_reference.sh
```

### 运行脚本

```bash
# 实时监控
./monitor_vllm.sh

# 性能分析
./analyze_vllm_performance.sh

# 服务状态
./show_status.sh
```

---

**文档版本**: v1.0  
**最后更新**: 2026-04-25  
**vLLM版本**: 0.19.1  
**监控状态**: ✅ 正常运行

---

## 🎯 总结

vLLM 提供了**完整的监控能力**：

1. ✅ **标准Prometheus指标** - `/metrics` 端点
2. ✅ **详细的性能日志** - `/tmp/vllm.log`
3. ✅ **GPU监控集成** - nvidia-smi
4. ✅ **实时统计** - 每个请求的性能数据

**推荐监控方案**:
- 日常: `./analyze_vllm_performance.sh`
- 实时: `./monitor_vllm.sh`
- 深度: Prometheus + Grafana

**所有监控工具已就绪，随时可以使用！** 🎉
