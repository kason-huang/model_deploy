# 🔍 vLLM 服务监控指南

## 📋 目录
- [快速命令](#快速命令)
- [监控脚本](#监控脚本)
- [手动命令](#手动命令)
- [日志分析](#日志分析)
- [性能监控](#性能监控)

---

## 🚀 快速命令

### 最常用（3个命令）

```bash
# 1. 快速查看状态
./show_status.sh

# 2. 实时监控
./monitor_service.sh

# 3. 查看日志
./logs_vllm.sh
```

---

## 🛠️ 监控脚本

### 1. show_status.sh ⭐ 推荐
**用途**: 快速查看服务状态

```bash
cd /root/vllm_Qwen3.6-35B-A3B/
./show_status.sh
```

**显示内容**:
- ✅ 容器状态
- ✅ API 状态
- ✅ GPU 状态
- 🤖 模型信息
- 🎮 GPU 详情
- 📝 最近日志

---

### 2. monitor_service.sh
**用途**: 实时监控（每5秒刷新）

```bash
./monitor_service.sh
```

**显示内容**:
- 📦 容器状态和运行时间
- 🌐 API 服务状态
- 🎮 GPU 使用情况
- ⚙️ 进程状态
- 📝 最新日志

**特点**: 自动刷新，按 Ctrl+C 退出

---

### 3. analyze_logs.sh
**用途**: 交互式日志分析

```bash
./analyze_logs.sh
```

**菜单选项**:
1. 实时日志 (tail -f)
2. 最近日志 (最后50行)
3. 错误日志
4. 启动日志
5. 性能日志
6. 统计信息

---

### 4. logs_vllm.sh
**用途**: 简单的日志查看

```bash
./logs_vllm.sh
```

**功能**: 实时显示所有日志

---

## 🔧 手动命令

### 容器管理

```bash
# 查看容器状态
docker ps | grep vllm

# 查看容器详细信息
docker inspect vllm-qwen3

# 查看容器资源使用
docker stats vllm-qwen3
```

### 日志查看

```bash
# 实时日志
docker logs -f vllm-qwen3

# 最近日志
docker logs --tail 100 vllm-qwen3

# 最近1小时的日志
docker logs --since 1h vllm-qwen3

# 带时间戳的日志
docker logs -t vllm-qwen3
```

### 进程监控

```bash
# 查看容器内进程
docker exec vllm-qwen3 ps aux

# 查看 Python 进程
docker exec vllm-qwen3 ps aux | grep python

# 查看进程树
docker exec vllm-qwen3 pstree -p
```

### GPU 监控

```bash
# GPU 状态
docker exec vllm-qwen3 nvidia-smi

# 实时监控
watch -n 1 'docker exec vllm-qwen3 nvidia-smi'

# GPU 使用率
docker exec vllm-qwen3 nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader

# 显存使用
docker exec vllm-qwen3 nvidia-smi --query-gpu=memory.used,memory.total --format=csv,noheader
```

### API 健康检查

```bash
# 健康检查
curl http://localhost:30000/health

# 模型列表
curl http://localhost:30000/v1/models

# 快速测试
curl -X POST http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3.6-35b-a3b","messages":[{"role":"user","content":"你好"}],"max_tokens":50}'
```

---

## 📊 日志分析

### 查找关键信息

```bash
# 查找错误
docker logs vllm-qwen3 2>&1 | grep -i error

# 查找警告
docker logs vllm-qwen3 2>&1 | grep -i warning

# 查找启动信息
docker logs vllm-qwen3 2>&1 | grep -i "startup\|started\|ready"

# 查找性能信息
docker logs vllm-qwen3 2>&1 | grep -i "took\|seconds\|completed"
```

### 日志统计

```bash
# 统计日志行数
docker logs vllm-qwen3 2>&1 | wc -l

# 统计错误数量
docker logs vllm-qwen3 2>&1 | grep -ci error

# 统计警告数量
docker logs vllm-qwen3 2>&1 | grep -ci warning

# 查看最近20个错误
docker logs vllm-qwen3 2>&1 | grep -i error | tail -20
```

---

## ⚡ 性能监控

### 响应时间测试

```bash
# 单次测试
time curl -s http://localhost:30000/health

# 多次测试
for i in {1..10}; do
  echo "测试 #$i:"
  time curl -s http://localhost:30000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{"model":"qwen3.6-35b-a3b","messages":[{"role":"user","content":"测试"}],"max_tokens":50}' > /dev/null
done
```

### 资源监控

```bash
# 实时监控 GPU 和进程
watch -n 1 '
echo "=== GPU 使用 ===" && \
docker exec vllm-qwen3 nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv,noheader && \
echo "" && \
echo "=== 进程状态 ===" && \
docker exec vllm-qwen3 ps aux | grep python | head -2'
```

### 性能指标收集

```bash
# 持续监控并记录
while true; do
  echo "$(date '+%Y-%m-%d %H:%M:%S')" >> vllm_metrics.log
  docker exec vllm-qwen3 nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader >> vllm_metrics.log
  curl -s http://localhost:30000/health && echo " OK" >> vllm_metrics.log || echo " FAIL" >> vllm_metrics.log
  echo "" >> vllm_metrics.log
  sleep 60
done
```

---

## 🎯 使用场景

### 场景1: 日常巡检（每天一次）
```bash
./show_status.sh
```

### 场景2: 问题排查
```bash
# 1. 查看状态
./show_status.sh

# 2. 分析日志
./analyze_logs.sh

# 3. 查看错误
docker logs vllm-qwen3 2>&1 | grep -i error | tail -20
```

### 场景3: 性能监控
```bash
# 实时监控
./monitor_service.sh

# 或使用 watch
watch -n 1 './show_status.sh'
```

### 场景4: 启动过程监控
```bash
# 启动服务
./start_vllm.sh

# 另一个终端监控
docker logs -f vllm-qwen3
```

---

## 📱 监控工具对比

| 工具 | 刷新频率 | 交互性 | 适用场景 |
|------|----------|--------|----------|
| show_status.sh | 手动 | 低 | 快速查看状态 |
| monitor_service.sh | 5秒 | 低 | 持续监控 |
| analyze_logs.sh | 手动 | 高 | 日志分析 |
| logs_vllm.sh | 实时 | 低 | 简单日志查看 |
| docker logs -f | 实时 | 低 | 原生日志 |

---

## 💡 最佳实践

### 1. 定期检查
```bash
# 设置定时任务（每小时检查）
crontab -e
# 添加: 0 * * * * /root/vllm_Qwen3.6-35B-A3B/show_status.sh >> /var/log/vllm_status.log 2>&1
```

### 2. 告警设置
```bash
# 创建告警脚本
cat > check_vllm.sh << 'EOF'
#!/bin/bash
if ! curl -s http://localhost:30000/health > /dev/null; then
    echo "vLLM 服务异常！" | mail -s "告警" admin@example.com
fi
EOF

# 定期检查
*/5 * * * * /root/check_vllm.sh
```

### 3. 日志轮转
```bash
# 配置日志轮转
cat > /etc/logrotate.d/vllm << 'EOF'
/var/log/vllm/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
}
EOF
```

---

## 🔗 相关文档

- **部署文档**: vllm_Qwen3.6-35B-A3B.md
- **快速开始**: QUICKSTART.md
- **API测试**: test_api_1.py

---

## 📞 获取帮助

```bash
# 查看所有监控脚本
ls -lh *.sh

# 查看脚本帮助
./show_status.sh --help 2>/dev/null || echo "运行脚本即可"

# 查看文档
cat MONITORING_GUIDE.md
```

---

**提示**: 推荐使用 `./show_status.sh` 进行日常检查，使用 `./monitor_service.sh` 进行持续监控。
