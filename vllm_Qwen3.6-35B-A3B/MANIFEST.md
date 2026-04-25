# 📦 文件清单

## 📁 目录：/root/vllm_Qwen3.6-35B-A3B/

**生成时间**: 2026-04-25
**文件数量**: 12 个
**总大小**: 约 42KB

---

## 📚 文档类（5个文件）

### 1. README.md (8.6KB)
- **类型**: 总览文档
- **用途**: 快速了解整个目录结构和使用方法
- **适合**: 首次使用者
- **关键词**: 快速开始、目录结构、常用命令

### 2. vllm_Qwen3.6-35B-A3B.md (17KB) ⭐
- **类型**: 完整部署文档
- **用途**: 核心文档，包含完整的部署流程和问题解决
- **适合**: 深入学习和问题排查
- **关键词**: 环境信息、部署流程、问题解决、验证测试

### 3. README_VLLM_DEPLOYMENT.md (3.9KB)
- **类型**: 部署指南
- **用途**: 详细的部署说明和 API 使用示例
- **适合**: 部署参考和 API 集成
- **关键词**: 参数说明、API 示例、性能优化

### 4. deployment_checklist.md (3.0KB)
- **类型**: 检查清单
- **用途**: 部署前后的检查清单和故障排查
- **适合**: 部署验证
- **关键词**: 检查清单、故障排查、性能优化

### 5. vllm-qwen3.service (285B)
- **类型**: systemd 服务配置
- **用途**: 系统服务配置文件
- **适合**: 生产环境部署
- **关键词**: systemd、服务管理

---

## 🛠️ 脚本类（5个文件）

### 6. start_vllm.sh (2.9KB) ⭐
- **类型**: 部署脚本（可执行）
- **用途**: 一键启动 vLLM 服务
- **使用**: `./start_vllm.sh`
- **功能**:
  - 自动检查并清理旧容器
  - 验证模型路径
  - 启动 Docker 容器
  - 启动 vLLM 服务
  - 健康检查

### 7. stop_vllm.sh (370B)
- **类型**: 运维脚本（可执行）
- **用途**: 停止 vLLM 服务
- **使用**: `./stop_vllm.sh`

### 8. logs_vllm.sh (259B)
- **类型**: 运维脚本（可执行）
- **用途**: 实时查看服务日志
- **使用**: `./logs_vllm.sh`

### 9. test_api.sh (2.2KB)
- **类型**: 测试脚本（可执行）
- **用途**: Bash 版本的 API 测试
- **使用**: `./test_api.sh`
- **功能**:
  - 健康检查
  - 模型列表
  - 文本生成
  - 流式输出
  - 推理测试

### 10. quick_reference.sh (3.9KB)
- **类型**: 辅助脚本（可执行）
- **用途**: 显示所有常用命令的快速参考
- **使用**: `./quick_reference.sh`

---

## 💻 代码类（2个文件）

### 11. test_api.py (3.6KB)
- **类型**: Python 示例（可执行）
- **用途**: Python 客户端示例和测试
- **使用**: `./test_api.py`
- **依赖**: `requirements.txt`
- **功能**:
  - 简单问答
  - 数学推理
  - 代码生成
  - 流式输出
  - 多轮对话

### 12. requirements.txt (14B)
- **类型**: 依赖配置
- **用途**: Python 依赖列表
- **使用**: `pip3 install -r requirements.txt`
- **内容**: openai>=1.0.0

---

## 🎯 使用建议

### 🚀 首次部署者
1. 先阅读 `README.md` - 了解全貌
2. 再读 `vllm_Qwen3.6-35B-A3B.md` - 深入学习
3. 检查 `deployment_checklist.md` - 验证环境
4. 运行 `./start_vllm.sh` - 启动服务
5. 执行 `./test_api.sh` - 验证部署

### 🔧 运维人员
1. 快速参考: `./quick_reference.sh`
2. 服务管理: `start_vllm.sh` / `stop_vllm.sh` / `logs_vllm.sh`
3. 问题排查: `vllm_Qwen3.6-35B-A3B.md` 第6节
4. API 测试: `./test_api.sh`

### 👨‍💻 开发人员
1. API 使用: `README_VLLM_DEPLOYMENT.md`
2. Python 示例: `test_api.py`
3. 参数说明: `vllm_Qwen3.6-35B-A3B.md` 第2节
4. 性能优化: `README_VLLM_DEPLOYMENT.md` 参数调优

### 📊 架构师
1. 完整文档: `vllm_Qwen3.6-35B-A3B.md`
2. 部署架构: 同上 第2节
3. 生产部署: 同上 第6节
4. 服务配置: `vllm-qwen3.service`

---

## 📊 文件统计

| 类型 | 数量 | 总大小 |
|------|------|---------|
| 📚 文档类 | 5 | 约 33KB |
| 🛠️ 脚本类 | 5 | 约 9KB |
| 💻 代码类 | 2 | 约 3.6KB |
| **总计** | **12** | **约 42KB** |

---

## 🔍 快速查找

### 按用途查找

**我想...**
- 🚀 部署服务 → `start_vllm.sh`
- 📖 学习文档 → `vllm_Qwen3.6-35B-A3B.md`
- 🧪 测试 API → `test_api.sh` 或 `test_api.py`
- 🔍 排查问题 → `vllm_Qwen3.6-35B-A3B.md` 第6节
- 📝 查看日志 → `logs_vllm.sh`
- 🛑 停止服务 → `stop_vllm.sh`
- 💡 快速参考 → `quick_reference.sh`

### 按问题查找

**遇到...**
- 端口被占用 → `README_VLLM_DEPLOYMENT.md` 故障排查
- API 返回空 → `vllm_Qwen3.6-35B-A3B.md` 问题6
- 服务启动慢 → `vllm_Qwen3.6-35B-A3B.md` 问题5
- FlashAttention 错误 → 同上 问题4
- 部署失败 → `deployment_checklist.md` 故障排查

---

## 📞 获取帮助

1. **快速参考**: 运行 `./quick_reference.sh`
2. **完整文档**: 阅读 `vllm_Qwen3.6-35B-A3B.md`
3. **部署清单**: 查看 `deployment_checklist.md`
4. **API 文档**: 参考 `README_VLLM_DEPLOYMENT.md`

---

**清单生成时间**: 2026-04-25
**目录路径**: `/root/vllm_Qwen3.6-35B-A3B/`
**维护状态**: ✅ 最新
