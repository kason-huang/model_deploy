# 📦 vLLM Qwen3.6-35B-A3B 项目文件清单

## 🎯 快速导航

**想快速开始？** 🚀 查看 `START_HERE.md`

**需要主文档？** 📖 查看 `README.md`

**想要所有命令？** ⚡ 运行 `./quick_reference.sh`

---

## 📁 项目结构

```
vllm_Qwen3.6-35B-A3B/
│
├── 🎯 入口文档（主目录）
│   ├── START_HERE.md          ⭐ 从这里开始！
│   ├── README.md              📖 主文档
│   └── MANIFEST.md            📋 本文件
│
├── 📚 详细文档（docs/ 目录）
│   ├── vllm_Qwen3.6-35B-A3B.md          # 完整技术文档
│   ├── README_VLLM_DEPLOYMENT.md        # 部署详细指南
│   ├── VLLM_MONITORING_GUIDE.md         # 监控完整指南
│   ├── VLLM_LOGS_GUIDE.md               # 日志查看指南
│   ├── LOGS_AND_MONITORING_COMPLETE.md  # 综合监控指南
│   ├── REASONING_MODEL_GUIDE.md         # 推理模型说明
│   ├── deployment_checklist.md          # 部署检查清单
│   └── QUICKSTART.md                    # 快速开始
│
├── 🚀 部署脚本
│   ├── start_vllm.sh           ⭐ 一键启动
│   ├── stop_vllm.sh            # 停止服务
│   └── vllm-qwen3.service      # systemd 配置
│
├── 🧪 测试脚本
│   ├── test_api.py             ⭐ Python 测试
│   ├── test_api.sh             # Bash 测试
│   ├── quick_test.sh           # 快速测试
│   └── test/
│       └── test_bailian_api.py # 百炼 API 测试
│
├── 📈 监控脚本
│   ├── monitor_vllm.sh         ⭐ 实时监控
│   ├── analyze_vllm_performance.sh  # 性能分析
│   ├── show_status.sh          # 快速状态
│   ├── monitor_service.sh      # 服务监控
│   ├── analyze_logs.sh         # 日志分析
│   ├── logs_vllm.sh            # 日志查看
│   └── quick_reference.sh      # 快速参考
│
└── 📦 其他
    ├── requirements.txt        # Python 依赖
    └── archive/                # 归档旧文件
```

---

## 🎯 配置信息

| 项目 | 值 |
|------|-----|
| **模型名称** | qwen3.6-35b-a3b |
| **API 地址** | http://localhost:30000/v1 |
| **GPU 需求** | 8 张 |
| **启动时间** | 8-10 分钟 |

---

## 📝 文档说明

### 主目录文档（3个）

| 文件 | 用途 | 适合 |
|------|------|------|
| **START_HERE.md** | 🚀 **最简洁入门** | 新手必看 |
| **README.md** | 📖 主文档 | 日常参考 |
| **MANIFEST.md** | 📋 文件清单 | 查找文件 |

### 详细文档（docs/ 目录，8个）

| 文件 | 大小 | 用途 |
|------|------|------|
| **vllm_Qwen3.6-35B-A3B.md** | 17KB | ⭐ 完整技术文档 |
| **README_VLLM_DEPLOYMENT.md** | 3.9KB | 部署详细指南 |
| **VLLM_MONITORING_GUIDE.md** | 11KB | 监控完整指南 |
| **VLLM_LOGS_GUIDE.md** | 9.2KB | 日志查看指南 |
| **LOGS_AND_MONITORING_COMPLETE.md** | 15KB | 综合监控指南 |
| **REASONING_MODEL_GUIDE.md** | 6.7KB | 推理模型说明 |
| **deployment_checklist.md** | 3KB | 部署检查清单 |
| **QUICKSTART.md** | 3.6KB | 快速开始 |

---

## 🔧 脚本文件

### 部署脚本（3个）
- `start_vllm.sh` - ⭐ 一键启动
- `stop_vllm.sh` - 停止服务
- `vllm-qwen3.service` - systemd 配置

### 测试脚本（4个）
- `test_api.py` - ⭐ Python 测试
- `test_api.sh` - Bash 测试
- `quick_test.sh` - 快速测试
- `test/test_bailian_api.py` - 百炼 API

### 监控脚本（7个）
- `monitor_vllm.sh` - ⭐ 实时监控
- `analyze_vllm_performance.sh` - 性能分析
- `show_status.sh` - 快速状态
- `monitor_service.sh` - 服务监控
- `analyze_logs.sh` - 日志分析
- `logs_vllm.sh` - 日志查看
- `quick_reference.sh` - 快速参考

---

## 🚀 快速开始

### 1. 启动服务
```bash
./start_vllm.sh
```

### 2. 测试验证
```bash
./test_api.sh
```

### 3. 监控服务
```bash
./monitor_vllm.sh
```

---

## 📊 文件统计

| 类型 | 数量 | 位置 |
|------|------|------|
| 🎯 入口文档 | 3 | 主目录 |
| 📚 详细文档 | 8 | docs/ |
| 🚀 部署脚本 | 3 | 主目录 |
| 🧪 测试脚本 | 4 | 主目录 + test/ |
| 📈 监控脚本 | 7 | 主目录 |
| **总计** | **25** | - |

---

## 🔍 按需求查找

### 我想...

**快速开始** → `START_HERE.md`
**部署服务** → `./start_vllm.sh`
**测试 API** → `./test_api.sh`
**监控服务** → `./monitor_vllm.sh`
**查看状态** → `./show_status.sh`
**所有命令** → `./quick_reference.sh`

### 遇到问题...

**服务启动失败** → `docs/README_VLLM_DEPLOYMENT.md`
**API 返回空** → `docs/REASONING_MODEL_GUIDE.md`
**性能问题** → `docs/VLLM_MONITORING_GUIDE.md`
**查看日志** → `docs/VLLM_LOGS_GUIDE.md`
**完整排查** → `docs/vllm_Qwen3.6-35B-A3B.md`

---

## 📞 获取帮助

**最快的方式**：
```bash
./quick_reference.sh
```

**查看文档**：
```bash
cat START_HERE.md          # 入门指南
cat README.md              # 主文档
cat docs/vllm_Qwen3.6-35B-A3B.md  # 完整文档
```

---

**版本**: v2.0 | **更新**: 2026-04-25 | **状态**: ✅ 最新