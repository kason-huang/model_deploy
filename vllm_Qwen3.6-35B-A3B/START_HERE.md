# 🎯 从这里开始

**欢迎！** 这是最简洁的入门指南。

---

## 🚀 只需3步

### 第1步：启动服务
```bash
./start_vllm.sh
```
⏱️ 等待 8-10 分钟，直到看到 "✓ vLLM 服务启动成功！"

### 第2步：验证服务
```bash
./test_api.sh
```
✅ 看到测试通过即可

### 第3步：开始使用
```bash
curl http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen3.6-35b-a3b","messages":[{"role":"user","content":"你好"}],"max_tokens":512}'
```

---

## 💡 关键信息

- **API 地址**: http://localhost:30000/v1
- **模型名称**: `qwen3.6-35b-a3b`
- **启动时间**: 8-10 分钟（首次）
- **GPU 需求**: 8 张

---

## 🛠️ 常用命令

```bash
# 启动/停止
./start_vllm.sh
./stop_vllm.sh

# 测试
./test_api.sh

# 监控
./monitor_vllm.sh      # 实时监控 ⭐
./show_status.sh       # 快速状态

# 日志
docker logs -f vllm-qwen3
```

---

## 📚 更多文档？

- **快速参考**: `./quick_reference.sh`
- **完整文档**: `README.md`
- **文件清单**: `MANIFEST.md`
- **一步步部署**：`vllm_Qwen3.6-35B-A3B/vllm_Qwen3.6-35B-A3B.md`

---

**有问题？** 查看 `README.md` 获取更多信息。

**就这么简单！** 🎉
