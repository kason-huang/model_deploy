# ⚡ 快速开始指南

## 🎯 30 秒快速部署

```bash
# 进入目录
cd /root/vllm_Qwen3.6-35B-A3B/

# 启动服务
./start_vllm.sh

# 等待 8-10 分钟，然后测试
./test_api.sh
```

## 📖 5 分钟完整部署

### 步骤 1: 环境检查（1分钟）

```bash
# 检查 Docker
docker --version

# 检查 GPU（需要 8 张）
nvidia-smi

# 检查模型文件
ls -la /home/user/models/Qwen3.6-35B-A3B/
```

### 步骤 2: 阅读文档（2分钟）

```bash
# 总览文档
cat README.md

# 或查看完整文档
cat vllm_Qwen3.6-35B-A3B.md
```

### 步骤 3: 启动服务（10秒）

```bash
# 一键启动
./start_vllm.sh
```

### 步骤 4: 等待就绪（8-10分钟）

服务启动需要时间：
- ✅ 容器启动: 10秒
- ✅ 模型加载: 77秒
- ✅ torch.compile: 48秒
- ✅ Triton 编译: 3-5分钟
- ✅ 服务启动: 10秒

**监控日志**:
```bash
./logs_vllm.sh
```

等待看到：
```
INFO:     Started server process [99]
INFO:     Application startup complete.
```

### 步骤 5: 验证服务（1分钟）

```bash
# 健康检查
curl http://localhost:30000/health

# 运行测试
./test_api.sh
```

## 📋 常用命令速查

### 服务管理

```bash
./start_vllm.sh     # 启动服务
./stop_vllm.sh      # 停止服务
./logs_vllm.sh      # 查看日志
```

### Docker 命令

```bash
docker ps | grep vllm                    # 查看容器
docker logs -f vllm-qwen3                # 实时日志
docker exec -it vllm-qwen3 bash          # 进入容器
docker restart vllm-qwen3                # 重启服务
```

### API 测试

```bash
# 健康检查
curl http://localhost:30000/health

# 模型列表
curl http://localhost:30000/v1/models

# 文本生成
curl http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3-vl","messages":[{"role":"user","content":"你好"}],"max_tokens":512}'
```

### Python 客户端

```bash
# 安装依赖
pip3 install -r requirements.txt

# 运行测试
./test_api.py
```

## 🔍 快速参考

### 查看所有命令

```bash
./quick_reference.sh
```

### 查看文件清单

```bash
cat MANIFEST.md
```

### 查看部署文档

```bash
cat vllm_Qwen3.6-35B-A3B.md
```

## ⚠️ 常见问题

### Q: 服务启动需要多久？
A: 首次启动 8-10 分钟，后续启动约 2-3 分钟（使用缓存）

### Q: 如何知道服务已就绪？
A: 看到 `Application startup complete.` 或健康检查通过

### Q: API 返回内容为空？
A: 增加 `max_tokens` 参数到 512 或更大

### Q: 如何查看日志？
A: 运行 `./logs_vllm.sh` 或 `docker logs -f vllm-qwen3`

### Q: 如何停止服务？
A: 运行 `./stop_vllm.sh` 或 `docker stop vllm-qwen3`

## 📊 服务信息

| 项目 | 值 |
|------|-----|
| 服务地址 | http://0.0.0.0:30000 |
| 模型名称 | qwen3-vl |
| 最大长度 | 32768 tokens |
| GPU 数量 | 8 张 |

## 🎓 学习路径

### 新手
1. 阅读 `README.md`
2. 运行 `./start_vllm.sh`
3. 执行 `./test_api.sh`
4. 查看 `vllm_Qwen3.6-35B-A3B.md`

### 进阶
1. 深入 `vllm_Qwen3.6-35B-A3B.md`
2. 参考 `README_VLLM_DEPLOYMENT.md`
3. 调优参数配置
4. 集成到应用

### 专家
1. 研究架构设计
2. 性能优化
3. 生产部署
4. 监控告警

## 📞 获取帮助

### 查看文档
```bash
ls -lh *.md
```

### 查看脚本
```bash
ls -lh *.sh
```

### 查看所有文件
```bash
ls -lh
```

## 🎯 下一步

1. ✅ 环境已就绪
2. ✅ 服务已部署
3. ✅ API 已测试
4. 🚀 **开始集成到您的应用！**

---

**提示**: 将此目录复制到您的项目目录，方便后续使用。

**目录**: `/root/vllm_Qwen3.6-35B-A3B/`
**压缩包**: `/root/vllm_Qwen3.6-35B-A3B.tar.gz`
