# vLLM Qwen3.6-35B-A3B 部署完整文档

## 📁 目录结构

```
vllm_Qwen3.6-35B-A3B/
├── README.md                          # 本文件 - 总览文档
├── vllm_Qwen3.6-35B-A3B.md            # 完整部署文档（核心文档）
├── README_VLLM_DEPLOYMENT.md          # 部署指南
├── deployment_checklist.md            # 部署检查清单
├── quick_reference.sh                 # 快速参考卡片
│
├── start_vllm.sh                      # 一键启动脚本 ⭐
├── stop_vllm.sh                       # 停止服务脚本
├── logs_vllm.sh                       # 日志查看脚本
│
├── test_api.sh                        # Bash API 测试脚本
├── test_api.py                        # Python 客户端示例
├── requirements.txt                   # Python 依赖
│
└── vllm-qwen3.service                 # systemd 服务配置
```

## 🚀 快速开始

### 1. 首次部署（5步）

```bash
# 步骤 1: 阅读部署文档
cat vllm_Qwen3.6-35B-A3B.md

# 步骤 2: 检查环境
cat deployment_checklist.md

# 步骤 3: 安装测试依赖（可选）
pip3 install -r requirements.txt

# 步骤 4: 启动服务
./start_vllm.sh

# 步骤 5: 验证服务（等待8-10分钟后）
./test_api.sh
```

### 2. 日常使用

```bash
# 启动服务
./start_vllm.sh

# 查看日志
./logs_vllm.sh

# 测试 API
./test_api.sh

# 停止服务
./stop_vllm.sh
```

## 📚 文档说明

### 核心文档

| 文件 | 大小 | 用途 |
|------|------|------|
| **vllm_Qwen3.6-35B-A3B.md** | 17KB | ⭐ **完整部署文档**，包含环境、流程、问题解决 |
| **README_VLLM_DEPLOYMENT.md** | 3.9KB | 部署指南，参数说明，API使用示例 |
| **deployment_checklist.md** | 3.0KB | 部署检查清单，故障排查 |

**推荐阅读顺序**:
1. `README.md` (本文件) - 快速了解
2. `vllm_Qwen3.6-35B-A3B.md` - 深入学习
3. `deployment_checklist.md` - 部署前检查
4. `README_VLLM_DEPLOYMENT.md` - 详细参考

## 🛠️ 脚本说明

### 部署脚本

#### start_vllm.sh ⭐
**用途**: 一键启动 vLLM 服务

**功能**:
- 自动检查并清理旧容器
- 验证模型路径
- 启动 Docker 容器
- 启动 vLLM 服务
- 健康检查等待服务就绪

**使用**:
```bash
./start_vllm.sh
```

**预计时间**: 8-10 分钟（首次启动）

#### stop_vllm.sh
**用途**: 停止 vLLM 服务

**使用**:
```bash
./stop_vllm.sh
```

#### logs_vllm.sh
**用途**: 实时查看服务日志

**使用**:
```bash
./logs_vllm.sh
# 按 Ctrl+C 退出
```

### 测试脚本

#### test_api.sh
**用途**: Bash 版本的 API 测试脚本

**测试内容**:
- 健康检查
- 模型列表
- 文本生成
- 流式输出
- 推理能力

**使用**:
```bash
./test_api.sh
```

#### test_api.py
**用途**: Python 版本的客户端示例和测试

**功能**:
- 简单问答
- 数学推理
- 代码生成
- 流式输出
- 多轮对话

**使用**:
```bash
# 安装依赖
pip3 install -r requirements.txt

# 运行测试
./test_api.py
```

### 辅助脚本

#### quick_reference.sh
**用途**: 显示所有常用命令的快速参考

**使用**:
```bash
./quick_reference.sh
```

## 🎯 部署流程概览

### 前置条件

- ✅ Docker 已安装 (v29.1.5+)
- ✅ 8 张 GPU 可用
- ✅ 模型已下载到 `/home/user/models/Qwen3.6-35B-A3B`
- ✅ 至少 128GB 系统内存

### 部署步骤

1. **环境检查** (2分钟)
   ```bash
   docker --version
   nvidia-smi
   ls -la /home/user/models/
   ```

2. **启动容器** (10秒)
   ```bash
   ./start_vllm.sh
   ```

3. **等待服务** (8-10分钟)
   - 模型加载: 77秒
   - torch.compile: 48秒
   - Triton编译: 3-5分钟
   - 服务启动: 10秒

4. **验证服务** (1分钟)
   ```bash
   curl http://localhost:30000/health
   ./test_api.sh
   ```

## 📊 服务信息

| 项目 | 值 |
|------|-----|
| 服务地址 | http://0.0.0.0:30000 |
| 模型名称 | qwen3-vl |
| 模型路径 | /models/Qwen3.6-35B-A3B |
| 最大长度 | 32768 tokens |
| GPU 配置 | 8 张 GPU (tensor parallel) |
| 数据类型 | float16 |

## 🔧 常用命令

### 服务管理

```bash
# 启动
./start_vllm.sh

# 停止
./stop_vllm.sh

# 重启
docker restart vllm-qwen3

# 查看状态
docker ps | grep vllm
```

### 日志查看

```bash
# 实时日志
./logs_vllm.sh

# 最近日志
docker logs --tail 100 vllm-qwen3

# 持续监控
watch -n 1 'docker logs --tail 20 vlll-qwen3'
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

### GPU 监控

```bash
# GPU 使用
docker exec vllm-qwen3 nvidia-smi

# 实时监控
watch -n 1 'docker exec vllm-qwen3 nvidia-smi'
```

## ⚠️ 常见问题

### 1. 服务启动时间过长
**正常现象**: 首次启动需要 8-10 分钟
- 模型加载: ~77秒
- torch.compile: ~48秒
- Triton 编译: ~3-5分钟

### 2. API 返回内容为空
**原因**: max_tokens 太小
**解决**: 设置 `max_tokens=512` 或更大

### 3. FlashAttention 错误
**原因**: V100 GPU 不支持
**解决**: 已自动禁用，使用 TRITON 后端

### 4. 端口被占用
**检查**: `netstat -tulpn | grep 30000`
**修改**: 编辑 `start_vllm.sh` 中的 `PORT` 变量

## 📈 性能优化

### 高吞吐量
```bash
--gpu-memory-utilization 0.95
--max-model-len 32768
```

### 低延迟
```bash
--gpu-memory-utilization 0.85
--max-model-len 8192
```

### 调试模式
```bash
--gpu-memory-utilization 0.7
--max-model-len 4096
VLLM_USE_FLASH_ATTN=0
```

## 🔍 故障排查

### 服务无法启动

```bash
# 查看详细错误
docker logs vllm-qwen3

# 检查 GPU
nvidia-smi

# 检查端口
netstat -tulpn | grep 30000

# 检查模型路径
ls -la /home/user/models/Qwen3.6-35B-A3B/
```

### API 调用失败

```bash
# 检查服务健康
curl -v http://localhost:30000/health

# 查看模型列表
curl http://localhost:30000/v1/models

# 查看 API 日志
docker logs vllm-qwen3 | grep -i error
```

### 性能问题

```bash
# 检查 GPU 利用率
docker exec vllm-qwen3 nvidia-smi

# 调整参数
# 编辑 start_vllm.sh，修改:
# --gpu-memory-utilization 0.85
# --max-model-len 16384
```

## 🎓 学习资源

### 官方文档
- [vLLM 官方文档](https://docs.vllm.ai/)
- [OpenAI API 兼容性](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html)
- [Qwen3 模型文档](https://github.com/QwenLM/Qwen3)

### 本地文档
- `vllm_Qwen3.6-35B-A3B.md` - 完整部署文档 ⭐
- `README_VLLM_DEPLOYMENT.md` - 详细指南
- `deployment_checklist.md` - 检查清单

### 快速参考
```bash
./quick_reference.sh  # 显示所有常用命令
```

## 📝 生产部署建议

### 1. 使用 systemd 管理

```bash
# 复制服务文件
sudo cp vllm-qwen3.service /etc/systemd/system/

# 启用服务
sudo systemctl enable vllm-qwen3
sudo systemctl start vllm-qwen3

# 查看状态
sudo systemctl status vllm-qwen3
```

### 2. 日志轮转

```bash
# 配置 logrotate
cat > /etc/logrotate.d/vllm <<EOF
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

### 3. 监控告警

- GPU 使用率监控
- API 响应时间监控
- 服务健康检查
- 日志错误告警

### 4. 负载均衡

启动多实例，使用 Nginx 或 HAProxy 进行负载均衡。

## 📞 获取帮助

### 查看帮助
```bash
# 快速参考
./quick_reference.sh

# 完整文档
cat vllm_Qwen3.6-35B-A3B.md

# 部署指南
cat README_VLLM_DEPLOYMENT.md

# 检查清单
cat deployment_checklist.md
```

### 查看日志
```bash
# 实时日志
./logs_vllm.sh

# 容器日志
docker logs -f vllm-qwen3
```

## ✅ 部署检查清单

部署前请确认：

- [ ] Docker 已安装并运行
- [ ] 8 张 GPU 可用
- [ ] 模型文件存在
- [ ] 至少 128GB 内存
- [ ] 磁盘空间充足
- [ ] 网络端口可用

部署后请验证：

- [ ] 容器运行正常
- [ ] 服务健康检查通过
- [ ] 可以看到模型列表
- [ ] GPU 显存已占用
- [ ] API 可以正常生成文本

## 📊 版本信息

| 组件 | 版本 |
|------|------|
| 文档版本 | v1.0 |
| 最后更新 | 2026-04-25 |
| vLLM 版本 | 0.19.1 |
| Docker 版本 | 29.1.5 |
| 部署状态 | ✅ 成功 |

## 🎯 下一步

1. **阅读核心文档**: `vllm_Qwen3.6-35B-A3B.md`
2. **检查环境**: `deployment_checklist.md`
3. **启动服务**: `./start_vllm.sh`
4. **测试验证**: `./test_api.sh`
5. **集成应用**: 参考 API 使用示例

---

**提示**: 建议将此目录复制到您的项目目录或文档库中，方便后续查阅和使用。

**目录路径**: `/root/vllm_Qwen3.6-35B-A3B/`
