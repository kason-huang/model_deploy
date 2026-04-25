# vLLM 部署检查清单

## ✅ 部署前检查

- [ ] Docker 已安装并运行正常
  ```bash
  docker --version
  sudo systemctl status docker
  ```

- [ ] NVIDIA Container Toolkit 已安装
  ```bash
  docker run --rm --gpus all nvidia/cuda:11.8.0-base-ubuntu22.04 nvidia-smi
  ```

- [ ] 至少 8 张 GPU 可用
  ```bash
  nvidia-smi
  ```

- [ ] 模型文件已下载
  ```bash
  ls -la /home/user/models/Qwen3.6-35B-A3B/
  ```

- [ ] 磁盘空间充足（模型约 70GB）
  ```bash
  df -h /home/user/models/
  ```

- [ ] Python 环境已安装（用于测试脚本）
  ```bash
  python3 --version
  ```

## 🚀 部署步骤

### 步骤 1：安装依赖（如需测试）
```bash
pip3 install -r requirements.txt
```

### 步骤 2：启动服务
```bash
./start_vllm.sh
```

### 步骤 3：验证服务
```bash
# 方法 1：运行测试脚本
./test_api.sh

# 方法 2：运行 Python 测试
./test_api.py

# 方法 3：手动测试
curl http://localhost:30000/health
```

## 📊 部署后验证

- [ ] 容器运行正常
  ```bash
  docker ps | grep vllm-qwen3
  ```

- [ ] 服务健康检查通过
  ```bash
  curl http://localhost:30000/health
  ```

- [ ] 可以看到模型列表
  ```bash
  curl http://localhost:30000/v1/models
  ```

- [ ] GPU 显存已占用
  ```bash
  docker exec vllm-qwen3 nvidia-smi
  ```

- [ ] API 可以正常生成文本
  ```bash
  ./test_api.py
  ```

## 🔧 常见问题处理

### 问题 1：端口被占用
```bash
# 查看端口占用
sudo netstat -tulpn | grep 30000

# 修改端口（编辑 start_vllm.sh）
PORT=30001  # 改为其他端口
```

### 问题 2：显存不足
```bash
# 编辑 start_vllm.sh，调整参数
--gpu-memory-utilization 0.85  # 降低显存利用率
--max-model-len 16384          # 减少最大长度
--tensor-parallel-size 4       # 减少并行 GPU 数量
```

### 问题 3：容器启动失败
```bash
# 查看详细错误
docker logs vllm-qwen3

# 检查模型路径
ls -la /home/user/models/Qwen3.6-35B-A3B/

# 检查 GPU 状态
nvidia-smi
```

## 📈 性能优化建议

### 吞吐量优先
- 增大 `--gpu-memory-utilization` 到 0.95
- 使用 `--max-model-len 32768`
- 增加 `--tensor-parallel-size`

### 延迟优先
- 降低 `--gpu-memory-utilization` 到 0.85
- 减少 `--max-model-len` 到 8192
- 使用更小的 batch size

### 调试模式
- 设置 `VLLM_USE_FLASH_ATTN=0`
- 降低 `--gpu-memory-utilization` 到 0.7
- 减少 `--max-model-len` 到 4096

## 🎯 下一步

部署成功后，您可以：

1. **集成到应用**：使用 Python 或 HTTP 客户端调用 API
2. **性能测试**：使用压测工具评估吞吐量和延迟
3. **生产部署**：配置 systemd 服务、日志轮转、监控告警
4. **多实例部署**：在不同端口启动多个实例进行负载均衡

## 📞 获取帮助

如遇问题，请检查：
1. `./logs_vllm.sh` - 查看详细日志
2. `docker logs vllm-qwen3` - 查看容器日志
3. `nvidia-smi` - 检查 GPU 状态
4. `README_VLLM_DEPLOYMENT.md` - 查看完整文档
