# vLLM 监控指南 - 服务状态与性能指标

## 📋 目录
- [快速开始](#快速开始)
- [监控端点](#监控端点)
- [关键指标](#关键指标)
- [监控工具](#监控工具)
- [Prometheus集成](#prometheus集成)
- [性能分析](#性能分析)

---

## 🚀 快速开始

### 3个核心监控命令

```bash
# 1. Prometheus格式指标（推荐）
curl -s http://localhost:30000/metrics | grep vllm:

# 2. 查看日志中的性能统计
docker exec vllm-qwen3 tail -50 /tmp/vllm.log | grep throughput

# 3. 查看GPU状态
docker exec vllm-qwen3 nvidia-smi
```

---

## 📡 监控端点

### 端点列表

| 端点 | 格式 | 说明 |
|------|------|------|
| **`/metrics`** | Prometheus | 标准监控指标 |
| **`/health`** | 文本 | 健康检查 |
| **`/v1/models`** | JSON | 模型信息 |

### 1. Prometheus 指标端点 ⭐

**URL**: `http://localhost:30000/metrics`

**获取所有指标**:
```bash
curl -s http://localhost:30000/metrics
```

**只查看vLLM指标**:
```bash
curl -s http://localhost:30000/metrics | grep vllm:
```

**实时监控脚本**:
```bash
watch -n 1 'curl -s http://localhost:30000/metrics | grep vllm:num_requests'
```

---

### 2. 健康检查端点

**URL**: `http://localhost:30000/health`

```bash
curl http://localhost:30000/health
# 返回: OK (或无内容)
```

---

## 📊 关键指标详解

### 1️⃣ 请求指标

#### 正在处理的请求
```
vllm:num_requests_running{engine="0",model_name="qwen3-vl"}
```
- **含义**: 当前正在执行的请求数
- **正常值**: 0-10
- **告警**: > 20 (可能过载)

#### 等待中的请求
```
vllm:num_requests_waiting{engine="0",model_name="qwen3-vl"}
```
- **含义**: 排队等待的请求数
- **正常值**: 0-5
- **告警**: > 10 (需要扩容)

#### 总请求数
```
vllm:num_requests_success{engine="0",model_name="qwen3-vl"}       # 成功
vllm:num_requests_failed{engine="0",model_name="qwen3-vl"}        # 失败
```

---

### 2️⃣ 性能指标

#### Token处理速度
```
vllm:request_prompt_tokens_sum        # 输入tokens总数
vllm:request_generation_tokens_sum     # 输出tokens总数
```

**计算吞吐量**:
```bash
# 查看当前累计的tokens
curl -s http://localhost:30000/metrics | grep "tokens_sum"

# 计算每秒tokens (需要两次采样)
sleep 10
curl -s http://localhost:30000/metrics | grep "tokens_sum"
```

#### Token分布直方图
```
vllm:request_prompt_tokens_bucket{le="100"}      # ≤100 tokens
vllm:request_prompt_tokens_bucket{le="1000"}     # ≤1000 tokens
vllm:request_prompt_tokens_bucket{le="10000"}    # ≤10000 tokens
```
- **用途**: 了解请求规模分布
- **优化**: 根据分布优化资源配置

---

### 3️⃣ 缓存指标

#### KV缓存使用率
```
vllm:kv_cache_usage_perc{engine="0",model_name="qwen3-vl"}
```
- **含义**: KV缓存使用百分比
- **正常值**: 0-80%
- **告警**: > 90% (需要增加缓存或减少batch)

#### 缓存命中率
```
日志中显示:
- GPU KV cache usage: 0.1-0.2%
- Prefix cache hit rate: 0.0%
- MM cache hit rate: 50-70%
```

---

### 4️⃣ 延迟指标

#### TTFT (Time To First Token)
```
日志中的: Avg prompt throughput
```
- **含义**: 首token延迟
- **计算**: prompt_tokens / prompt_time
- **正常值**: 10-50 tokens/s

#### TPOT (Time Per Output Token)
```
日志中的: Avg generation throughput
```
- **含义**: 每个输出token的时间
- **计算**: generation_tokens / generation_time
- **正常值**: 5-20 tokens/s

---

### 5️⃣ GPU利用率

#### FLOPS利用率
```
vllm:estimated_flops_per_gpu_total
```
- **含义**: GPU浮点运算利用率
- **计算**: 实际FLOPS / 理论最大FLOPS
- **正常值**: 30-70%

#### 显存使用
```
vllm:estimated_read_bytes_per_gpu_total    # 读取
vllm:estimated_write_bytes_per_gpu_total   # 写入
```

---

## 🛠️ 监控工具

### 工具1: 实时监控脚本

```bash
#!/bin/bash
# vllm_monitor.sh

echo "=== vLLM 实时监控 ==="
while true; do
    clear
    echo "时间: $(date '+%H:%M:%S')"
    echo ""
    
    # 请求状态
    echo "📊 请求状态:"
    curl -s http://localhost:30000/metrics | grep "num_requests" | grep -v "#"
    echo ""
    
    # GPU状态
    echo "🎮 GPU状态:"
    docker exec vllm-qwen3 nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.free --format=csv,noheader
    echo ""
    
    # 最近日志
    echo "📝 最近日志:"
    docker exec vllm-qwen3 tail -3 /tmp/vllm.log
    echo ""
    
    sleep 5
done
```

---

### 工具2: 性能统计脚本

```bash
#!/bin/bash
# vllm_stats.sh

echo "=== vLLM 性能统计 ==="
echo ""

# 从日志中提取统计信息
docker exec vllm-qwen3 tail -100 /tmp/vllm.log | grep "throughput" | tail -5

echo ""
echo "=== 缓存命中率 ==="
docker exec vllm-qwen3 tail -100 /tmp/vllm.log | grep "cache hit rate" | tail -5
```

---

### 工具3: 完整监控仪表板

```python
#!/usr/bin/env python3
"""
vLLM 监控仪表板
显示实时监控指标
"""

import requests
import time
from datetime import datetime

VLLM_API = "http://localhost:30000"

def get_metrics():
    """获取Prometheus指标"""
    response = requests.get(f"{VLLM_API}/metrics")
    metrics = {}
    
    for line in response.text.split('\n'):
        if line.startswith('vllm:num_'):
            parts = line.split(' ')
            metric_name = parts[0].split('{')[0]
            metric_value = float(parts[1])
            metrics[metric_name] = metric_value
    
    return metrics

def monitor():
    """实时监控"""
    print("🚀 vLLM 实时监控")
    print("=" * 50)
    
    while True:
        metrics = get_metrics()
        timestamp = datetime.now().strftime('%H:%M:%S')
        
        print(f"\n[{timestamp}] 当前状态:")
        print(f"  运行中请求: {metrics.get('vllm:num_requests_running', 0):.0f}")
        print(f"  等待中请求: {metrics.get('vllm:num_requests_waiting', 0):.0f}")
        print(f"  KV缓存使用: {metrics.get('vllm:kv_cache_usage_perc', 0):.1f}%")
        
        time.sleep(5)

if __name__ == '__main__':
    monitor()
```

---

## 📈 Prometheus 集成

### 1. Prometheus 配置

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

### 2. Grafana 仪表板

#### vLLM 核心指标查询

**请求队列**:
```promql
rate(vllm:num_requests_waiting[5m])
```

**Token吞吐量**:
```promql
rate(vllm:request_generation_tokens_sum[1m])
```

**缓存使用率**:
```promql
vllm:kv_cache_usage_perc
```

**引擎状态**:
```promql
vllm:engine_sleep_state{sleep_state="awake"}
```

---

## 🔍 性能分析

### 分析吞吐量

```bash
# 方法1: 从日志分析
docker exec vllm-qwen3 tail -200 /tmp/vllm.log | grep "throughput" | tail -20

# 方法2: 从metrics计算
# 采样1
TOKENS1=$(curl -s http://localhost:30000/metrics | grep "generation_tokens_sum" | awk '{print $2}')
sleep 10
# 采样2
TOKENS2=$(curl -s http://localhost:30000/metrics | grep "generation_tokens_sum" | awk '{print $2}')
# 计算
RATE=$(echo "($TOKENS2 - $TOKENS1) / 10" | bc)
echo "生成吞吐量: $RATE tokens/s"
```

### 分析请求分布

```bash
# 查看请求大小分布
curl -s http://localhost:30000/metrics | grep "prompt_tokens_bucket"
```

**示例输出**:
```
le="100": 23      # 23个请求 ≤100 tokens
le="1000": 37     # 37个请求 ≤1000 tokens
le="10000": 44    # 44个请求 ≤10000 tokens
```

---

## 📋 常用监控场景

### 场景1: 服务健康检查

```bash
# 检查服务状态
curl http://localhost:30000/health && echo "✓ 服务正常" || echo "✗ 服务异常"

# 检查请求队列
curl -s http://localhost:30000/metrics | grep "num_requests"
```

### 场景2: 性能问题排查

```bash
# 检查GPU利用率
docker exec vllm-qwen3 nvidia-smi

# 检查请求队列
curl -s http://localhost:30000/metrics | grep "num_requests_waiting"

# 检查吞吐量
docker exec vllm-qwen3 tail -50 /tmp/vllm.log | grep throughput
```

### 场景3: 容量规划

```bash
# 查看历史最大并发
curl -s http://localhost:30000/metrics | grep "num_requests_running" | awk '{print $2}' | sort -rn | head -1

# 查看平均请求大小
curl -s http://localhost:30000/metrics | grep "prompt_tokens_sum" | awk '{sum+=$2} END {print "平均:", sum/NR}'
```

---

## 🎯 监控最佳实践

### 1. 设置告警阈值

| 指标 | 告警阈值 | 处理建议 |
|------|----------|----------|
| **等待请求数** | > 10 | 考虑扩容或增加GPU |
| **KV缓存使用率** | > 90% | 增加GPU或优化请求 |
| **GPU利用率** | < 30% | 检查是否有瓶颈 |
| **请求失败率** | > 5% | 检查日志排查错误 |

### 2. 定期巡检

```bash
# 每天检查一次
curl -s http://localhost:30000/metrics > /var/log/vllm_metrics_$(date +%Y%m%d).log
```

### 3. 性能优化

**低缓存命中率** (<50%):
- 增加 `gpu_memory_utilization`
- 优化请求batch size
- 启用前缀缓存

**低GPU利用率** (<30%):
- 增加 `max_model_len`
- 增加并发请求
- 检查是否有其他瓶颈

**高延迟** (>50 tokens/s):
- 检查网络延迟
- 优化模型配置
- 检查GPU温度

---

## 💡 快速参考

### 核心指标查询

```bash
# 当前状态
curl -s http://localhost:30000/metrics | grep "num_requests"

# 吞吐量趋势
docker exec vllm-qwen3 tail -100 /tmp/vllm.log | grep throughput

# GPU状态
docker exec vllm-qwen3 nvidia-smi

# 缓存效率
docker exec vllm-qwen3 tail -50 /tmp/vllm.log | grep "cache"
```

### 实时监控命令

```bash
# 方法1: 使用watch
watch -n 1 'curl -s http://localhost:30000/metrics | grep num_requests'

# 方法2: 使用脚本
docker exec -it vllm-qwen3 tail -f /tmp/vllm.log

# 方法3: 使用提供的监控脚本
./monitor_service.sh  # 如果已创建
```

---

## 🎓 总结

### vLLM 提供的监控能力

✅ **Prometheus指标端点**: `/metrics`
✅ **丰富的性能指标**: 请求、缓存、吞吐量
✅ **实时统计**: 在日志中显示
✅ **GPU监控**: 集成 nvidia-smi
✅ **健康检查**: `/health` 端点

### 推荐监控方案

1. **Prometheus + Grafana**: 专业监控
2. **自定义脚本**: 轻量级监控
3. **日志分析**: 深入分析

### 下一步

1. 集成Prometheus采集指标
2. 配置Grafana仪表板
3. 设置告警规则
4. 定期分析性能数据

---

**vLLM监控功能完整，推荐使用 `/metrics` 端点获取标准Prometheus指标！** 🎉
