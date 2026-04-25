# vLLM 模型运行日志查看指南

## 📋 目录
- [快速查看方法](#快速查看方法)
- [进入容器查看](#进入容器查看)
- [容器外查看日志](#容器外查看日志)
- [日志文件位置](#日志文件位置)
- [实时监控](#实时监控)
- [日志分析](#日志分析)

---

## 🚀 快速查看方法

### 最常用的3个命令

```bash
# 1. 实时日志（最常用）
docker logs -f vllm-qwen3

# 2. 最近100行日志
docker logs --tail 100 vllm-qwen3

# 3. 进入容器
docker exec -it vllm-qwen3 bash
```

---

## 🐳 进入容器查看

### 方法1: 进入容器交互式Shell

```bash
# 进入容器
docker exec -it vllm-qwen3 bash

# 进入后，容器内命令：
# 1. 查看进程
ps aux | grep vllm

# 2. 查看实时日志（如果日志在文件中）
tail -f /tmp/vllm.log

# 3. 查看容器内所有日志文件
ls -la /tmp/

# 4. 退出容器
exit
```

### 方法2: 在容器内执行命令（不进入）

```bash
# 查看容器内进程
docker exec vllm-qwen3 ps aux | grep vllm

# 查看容器内日志文件
docker exec vllm-qwen3 ls -la /tmp/

# 查看容器内日志内容
docker exec vllm-qwen3 tail -50 /tmp/vllm.log

# 查看容器内环境变量
docker exec vllm-qwen3 env | grep VLLM
```

### 方法3: 持续监控容器内日志

```bash
# 实时查看容器内日志文件
docker exec -it vllm-qwen3 tail -f /tmp/vllm.log
```

---

## 📂 容器外查看日志

### 基础命令

```bash
# 查看所有日志
docker logs vllm-qwen3

# 实时跟踪日志（推荐）
docker logs -f vllm-qwen3

# 查看最近100行
docker logs --tail 100 vllm-qwen3

# 查看最近500行并分页
docker logs --tail 500 vllm-qwen3 | less

# 显示时间戳
docker logs -t vllm-qwen3
```

### 高级过滤

```bash
# 查找错误日志
docker logs vllm-qwen3 2>&1 | grep -i error

# 查找警告日志
docker logs vllm-qwen3 2>&1 | grep -i warning

# 查找包含特定关键字的日志
docker logs vllm-qwen3 2>&1 | grep -i "model\|loading\|ready"

# 只显示最近10行错误
docker logs vllm-qwen3 2>&1 | grep -i error | tail -10

# 统计错误数量
docker logs vllm-qwen3 2>&1 | grep -ci error
```

### 时间范围过滤

```bash
# 查看最近1分钟的日志
docker logs --since 1m vllm-qwen3

# 查看最近1小时的日志
docker logs --since 1h vllm-qwen3

# 查看指定时间之后的日志
docker logs --since 2026-04-25T14:00:00 vllm-qwen3

# 查看最近100行带时间戳
docker logs --tail 100 -t vllm-qwen3
```

---

## 📁 日志文件位置

### 容器内日志文件

```bash
# 进入容器
docker exec -it vllm-qwen3 bash

# 查看可能的日志文件位置
ls -la /tmp/
ls -la /root/.cache/vllm/
ls -la /var/log/

# 常见位置：
# /tmp/vllm.log          # vLLM 主日志
# /tmp/vllm_*.log        # 临时日志
# /root/.cache/vllm/     # 缓存和日志目录
```

### 容器外日志位置

```bash
# Docker 容器日志（默认）
# 位置：/var/lib/docker/containers/<container-id>/<container-id>-json.log

# 查看容器ID
docker inspect vllm-qwen3 | grep Id | awk '{print $2}'

# 查看容器日志文件
docker inspect vllm-qwen3 | grep LogPath | awk '{print $2}' | cut -d'"' -f4
```

---

## 🔍 实时监控

### 方法1: 使用 watch 命令

```bash
# 每秒刷新日志（最后20行）
watch -n 1 'docker logs --tail 20 vllm-qwen3'

# 每秒刷新GPU使用
watch -n 1 'docker exec vllm-qwen3 nvidia-smi'

# 每秒刷新进程状态
watch -n 1 'docker exec vllm-qwen3 ps aux | grep python'
```

### 方法2: 使用 tail -f

```bash
# 实时查看Docker日志
docker logs -f vllm-qwen3

# 实时查看并过滤
docker logs -f vllm-qwen3 | grep -v "DEBUG"

# 实时查看并高亮关键字
docker logs -f vllm-qwen3 | grep --color=auto -E "ERROR|WARNING|model"
```

### 方法3: 使用 less 实时查看

```bash
# 实时跟踪日志（按 Shift+F 进入实时模式）
docker logs vllm-qwen3 | less

# 在 less 中：
# - Shift+F: 进入实时模式（类似 tail -f）
# - Ctrl+C: 停止实时模式
# - q: 退出
```

---

## 📊 日志分析

### 分析启动过程

```bash
# 查看完整启动日志
docker logs vllm-qwen3 2>&1 | head -100

# 提取关键启动信息
docker logs vllm-qwen3 2>&1 | grep -E "model|loading|ready|started" | head -20

# 查看模型加载时间
docker logs vllm-qwen3 2>&1 | grep -E "Loading|took" | head -10
```

### 分析性能

```bash
# 查看推理时间
docker logs vllm-qwen3 2>&1 | grep -E "seconds|time|latency" | tail -20

# 查看Token使用
docker logs vllm-qwen3 2>&1 | grep -E "tokens|prompt|completion" | tail -20

# 查看GPU使用情况
docker logs vllm-qwen3 2>&1 | grep -E "GPU|cuda|device" | tail -10
```

### 错误分析

```bash
# 查看所有错误
docker logs vllm-qwen3 2>&1 | grep -i error

# 查看最近20个错误及其上下文
docker logs vllm-qwen3 2>&1 | grep -i -B 5 -A 5 error | tail -30

# 统计错误类型
docker logs vllm-qwen3 2>&1 | grep -i error | awk '{print $0}' | sort | uniq -c | sort -rn
```

---

## 🎯 常用场景

### 场景1: 模型加载中...

**问题**: 想知道模型加载进度

**解决**:
```bash
# 实时查看加载进度
docker logs -f vllm-qwen3 | grep -E "Loading|loaded|shard"

# 或查看最近日志
docker logs --tail 50 vllm-qwen3 | grep -E "Loading|checkpoint|shard"
```

**期望输出**:
```
Loading safetensors checkpoint shards: 50% Completed | 13/26
```

---

### 场景2: 服务卡住不动

**问题**: 请求没有响应，想知道发生了什么

**解决**:
```bash
# 1. 检查容器状态
docker ps | grep vllm-qwen3

# 2. 查看最新日志
docker logs --tail 50 vllm-qwen3

# 3. 检查GPU是否在用
docker exec vllm-qwen3 nvidia-smi

# 4. 检查进程状态
docker exec vllm-qwen3 ps aux | grep python
```

---

### 场景3: 推理速度慢

**问题**: 响应时间太长

**解决**:
```bash
# 查看推理时间统计
docker logs vllm-qwen3 2>&1 | grep -E "seconds|time|TTFT|TPOT" | tail -20

# 查看GPU利用率
docker exec vllm-qwen3 nvidia-smi

# 查看是否有编译缓存
docker exec vllm-qwen3 ls -la /root/.cache/vllm/torch_compile_cache/
```

---

### 场景4: 查看API请求

**问题**: 想知道收到的请求和返回

**解决**:
```bash
# 查看最近的处理请求
docker logs --tail 100 vllm-qwen3 | grep -E "request|response|completion"

# 进入容器查看更详细的日志
docker exec -it vllm-qwen3 bash
tail -f /tmp/vllm.log
```

---

## 🔧 高级技巧

### 1. 日志过滤和分析工具

```bash
# 使用 jq 分析JSON格式日志
docker logs vllm-qwen3 2>&1 | jq -r '.log' | tail -20

# 使用 awk 提取时间戳和消息
docker logs -t vllm-qwen3 2>&1 | awk '{print $1, $2, $NF}' | tail -20

# 统计日志级别
docker logs vllm-qwen3 2>&1 | grep -oE "INFO|WARNING|ERROR" | sort | uniq -c
```

### 2. 导出日志

```bash
# 导出到文件
docker logs vllm-qwen3 > /tmp/vllm_full.log 2>&1

# 导出最近1000行
docker logs --tail 1000 vllm-qwen3 > /tmp/vllm_recent.log 2>&1

# 导出最近1小时的日志
docker logs --since 1h vllm-qwen3 > /tmp/vllm_last_hour.log 2>&1
```

### 3. 监控脚本

```bash
# 创建监控脚本
cat > monitor_vllm.sh << 'EOF'
#!/bin/bash
while true; do
    clear
    echo "=== vLLM 监控 $(date +%H:%M:%S) ==="
    echo ""
    echo "容器状态:"
    docker ps | grep vllm-qwen3
    echo ""
    echo "GPU 使用:"
    docker exec vllm-qwen3 nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader
    echo ""
    echo "最近日志（最后5行）:"
    docker logs --tail 5 vllm-qwen3
    echo ""
    sleep 5
done
EOF

chmod +x monitor_vllm.sh
./monitor_vllm.sh
```

---

## 💡 最佳实践

### 日常巡检

```bash
# 每天检查一次
# 1. 容器状态
docker ps | grep vllm-qwen3

# 2. 最近的错误
docker logs vllm-qwen3 2>&1 | grep -i error | tail -10

# 3. GPU状态
docker exec vllm-qwen3 nvidia-smi
```

### 问题排查

```bash
# 完整诊断流程
# 1. 容器是否运行
docker ps -a | grep vllm-qwen3

# 2. 查看完整日志
docker logs --tail 200 vllm-qwen3 > /tmp/debug.log

# 3. 进入容器检查
docker exec -it vllm-qwen3 bash
#   - ps aux | grep python
#   - nvidia-smi
#   - ls -la /tmp/
```

### 性能优化

```bash
# 监控关键指标
# 1. 响应时间
docker logs vllm-qwen3 2>&1 | grep -E "time|seconds|latency" | tail -20

# 2. Token使用
docker logs vllm-qwen3 2>&1 | grep -E "tokens|usage" | tail -20

# 3. GPU利用率
watch -n 1 'docker exec vllm-qwen3 nvidia-smi'
```

---

## 📞 快速参考卡

```bash
# === 最常用命令 ===
docker logs -f vllm-qwen3                    # 实时日志
docker logs --tail 100 vllm-qwen3            # 最近100行
docker exec -it vllm-qwen3 bash               # 进入容器

# === 容器内操作 ===
docker exec vllm-qwen3 ps aux                # 查看进程
docker exec vllm-qwen3 nvidia-smi            # 查看GPU
docker exec vllm-qwen3 tail -f /tmp/vllm.log # 容器内日志

# === 日志过滤 ===
docker logs vllm-qwen3 2>&1 | grep error     # 查找错误
docker logs vllm-qwen3 2>&1 | grep model     # 查找模型相关
docker logs vllm-qwen3 2>&1 | grep loading    # 查找加载进度

# === 导出日志 ===
docker logs vllm-qwen3 > debug.log          # 完整日志
docker logs --since 1h vllm-qwen3 > last_hour.log  # 最近1小时
```

---

**提示**: 推荐使用 `docker logs -f vllm-qwen3` 实时监控日志，这是最直接有效的方法！
