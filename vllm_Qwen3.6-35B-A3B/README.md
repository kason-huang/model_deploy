# 🚀 Qwen3.6-35B-A3B 模型部署 - 主文档

> **快速开始**: 查看 [START_HERE.md](START_HERE.md) | **文件清单**: 查看 [MANIFEST.md](MANIFEST.md)

---

## ⚡ 快速开始（3步）

### 1️⃣ 启动服务
```bash
./start_vllm.sh
```
等待 8-10 分钟，直到看到 "✓ vLLM 服务启动成功！"

### 2️⃣ 测试验证
```bash
./test_api.sh
```

### 3️⃣ 开始使用
```bash
curl http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3.6-35b-a3b","messages":[{"role":"user","content":"你好"}],"max_tokens":512}'
```

---

## 📋 服务信息

| 项目 | 值 |
|------|-----|
| **API 地址** | http://localhost:30000/v1 |
| **模型名称** | qwen3.6-35b-a3b |
| **模型路径** | /models/Qwen3.6-35B-A3B |
| **GPU 需求** | 8 张 GPU (tensor parallel) |
| **数据类型** | float16 |
| **最大长度** | 32768 tokens |

---

## 🛠️ 常用命令

### 服务管理
```bash
./start_vllm.sh              # 启动服务
./stop_vllm.sh               # 停止服务
docker logs -f vllm-qwen3    # 查看日志
```

### 测试验证
```bash
./test_api.sh                # Bash 测试
python test_api.py           # Python 测试
```

### 监控工具
```bash
./monitor_vllm.sh            # ⭐ 实时监控（推荐）
./show_status.sh             # 快速状态
./analyze_vllm_performance.sh # 性能分析
```

### 快速参考
```bash
./quick_reference.sh         # 所有常用命令
```

---

## 📚 文档导航

### 主目录文档（3个）
| 文件 | 用途 |
|------|------|
| **START_HERE.md** | 🚀 最简洁入门指南 |
| **README.md** | 📖 本文件 - 主文档 |
| **MANIFEST.md** | 📋 项目文件清单 |

### 详细文档（docs/ 目录）
| 文件 | 用途 |
|------|------|
| **docs/vllm_Qwen3.6-35B-A3B.md** | 完整技术文档 ⭐ |
| **docs/README_VLLM_DEPLOYMENT.md** | 部署详细指南 |
| **docs/VLLM_MONITORING_GUIDE.md** | 监控完整指南 |
| **docs/VLLM_LOGS_GUIDE.md** | 日志查看指南 |
| **docs/REASONING_MODEL_GUIDE.md** | 推理模型说明 |
| **docs/deployment_checklist.md** | 部署检查清单 |

---

## ❓ 常见问题

### Q: 服务启动时间过长？
**A**: 正常现象，首次启动需要 8-10 分钟
- 模型加载: ~77秒
- torch.compile: ~48秒
- Triton 编译: ~5分钟

### Q: API 返回内容为空？
**A**: 推理模型特性，需要增加 `max_tokens` 参数
```json
{"max_tokens": 512}
```
详见：`docs/REASONING_MODEL_GUIDE.md`

### Q: 如何监控服务性能？
**A**: 使用监控脚本
```bash
./monitor_vllm.sh              # 实时监控
./analyze_vllm_performance.sh  # 性能分析
```
详见：`docs/VLLM_MONITORING_GUIDE.md`

### Q: 如何查看详细日志？
**A**: 多种方式
```bash
docker logs -f vllm-qwen3                    # 容器日志
docker exec vllm-qwen3 tail -f /tmp/vllm.log # 服务日志
./logs_vllm.sh                               # 脚本查看
```
详见：`docs/VLLM_LOGS_GUIDE.md`

### Q: 服务启动失败？
**A**: 检查清单
1. GPU 是否可用: `nvidia-smi`
2. 模型路径: `ls /home/user/models/Qwen3.6-35B-A3B`
3. 端口占用: `netstat -tulpn | grep 30000`
4. 详细排查: `docs/README_VLLM_DEPLOYMENT.md`

---

## 🎯 部署前检查

- [ ] Docker 已安装
- [ ] 8 张 GPU 可用
- [ ] 模型已下载到 `/home/user/models/Qwen3.6-35B-A3B`
- [ ] 至少 128GB 内存
- [ ] 端口 30000 未被占用

详细清单：`docs/deployment_checklist.md`

---

## 🔧 高级配置

### 性能优化
**高吞吐量**（编辑 `start_vllm.sh`）:
```bash
--gpu-memory-utilization 0.95
--max-model-len 32768
```

**低延迟**:
```bash
--gpu-memory-utilization 0.85
--max-model-len 8192
```

### 生产部署
使用 systemd 管理服务：
```bash
sudo cp vllm-qwen3.service /etc/systemd/system/
sudo systemctl enable vllm-qwen3
sudo systemctl start vllm-qwen3
```

---

## 📊 性能参考

**当前配置性能**：
- **生成吞吐**: 5-20 tokens/s
- **输入吞吐**: 8-113 tokens/s
- **缓存命中**: 70-72%
- **GPU 显存**: 32GB/GPU（满载）

**性能测试**：
```bash
./analyze_vllm_performance.sh  # 查看实际性能
```

---

## 🎓 学习资源

**本地文档**：
- `docs/vllm_Qwen3.6-35B-A3B.md` - 完整技术文档
- `docs/VLLM_MONITORING_GUIDE.md` - 监控与性能
- `docs/VLLM_LOGS_GUIDE.md` - 日志与排查

**官方资源**：
- [vLLM 官方文档](https://docs.vllm.ai/)
- [OpenAI API 文档](https://platform.openai.com/docs/api-reference)
- [Qwen3 模型文档](https://github.com/QwenLM/Qwen3)

---

## 💡 使用建议

### 新手用户
1. 阅读 `START_HERE.md`
2. 运行 `./start_vllm.sh`
3. 运行 `./test_api.sh`

### 运维人员
1. 快速参考: `./quick_reference.sh`
2. 监控工具: `./monitor_vllm.sh`
3. 详细文档: `docs/`

### 开发人员
1. API 使用: `python test_api.py`
2. 推理模型: `docs/REASONING_MODEL_GUIDE.md`
3. 集成示例: `docs/README_VLLM_DEPLOYMENT.md`

---

**版本**: v2.0 | **更新**: 2026-04-25 | **状态**: ✅ 最新

**当前目录**: `/root/workspace/model_deploy/vllm_Qwen3.6-35B-A3B/`

---

**有问题？** 查看 `docs/vllm_Qwen3.6-35B-A3B.md` 获取完整技术文档。
