#!/bin/bash
# vLLM 日志分析工具

CONTAINER_NAME="vllm-qwen3"

show_menu() {
    clear
    echo "========================================"
    echo "📊 vLLM 日志分析工具"
    echo "========================================"
    echo ""
    echo "1. 实时日志 (tail -f)"
    echo "2. 最近日志 (最后50行)"
    echo "3. 错误日志"
    echo "4. 启动日志"
    echo "5. 性能日志"
    echo "6. 统计信息"
    echo "7. 返回主菜单"
    echo ""
    echo -n "请选择 (1-7): "
}

realtime_logs() {
    echo ""
    echo "📝 实时日志 (按 Ctrl+C 退出)"
    echo "========================================"
    docker logs -f ${CONTAINER_NAME} 2>&1
}

recent_logs() {
    echo ""
    echo "📝 最近日志 (最后50行)"
    echo "========================================"
    docker logs --tail 50 ${CONTAINER_NAME} 2>&1
    echo ""
    read -p "按 Enter 继续..."
}

error_logs() {
    echo ""
    echo "❌ 错误日志"
    echo "========================================"
    docker logs ${CONTAINER_NAME} 2>&1 | grep -i "error\|exception\|failed" | tail -20
    echo ""
    read -p "按 Enter 继续..."
}

startup_logs() {
    echo ""
    echo "🚀 启动日志"
    echo "========================================"
    docker logs ${CONTAINER_NAME} 2>&1 | head -50
    echo ""
    read -p "按 Enter 继续..."
}

performance_logs() {
    echo ""
    echo "⚡ 性能日志"
    echo "========================================"
    docker logs ${CONTAINER_NAME} 2>&1 | grep -E "took|seconds|INFO.*completed" | tail -20
    echo ""
    read -p "按 Enter 继续..."
}

show_stats() {
    echo ""
    echo "📊 日志统计"
    echo "========================================"
    total_lines=$(docker logs ${CONTAINER_NAME} 2>&1 | wc -l)
    error_count=$(docker logs ${CONTAINER_NAME} 2>&1 | grep -ci "error")
    warning_count=$(docker logs ${CONTAINER_NAME} 2>&1 | grep -ci "warning")

    echo "总日志行数: $total_lines"
    echo "错误数量: $error_count"
    echo "警告数量: $warning_count"
    echo ""

    echo "最近错误 (最后5个):"
    docker logs ${CONTAINER_NAME} 2>&1 | grep -i "error" | tail -5
    echo ""
    read -p "按 Enter 继续..."
}

# 主循环
while true; do
    show_menu
    read choice

    case $choice in
        1) realtime_logs ;;
        2) recent_logs ;;
        3) error_logs ;;
        4) startup_logs ;;
        5) performance_logs ;;
        6) show_stats ;;
        7) echo "退出..."; break ;;
        *) echo "无效选择，请重试"; sleep 1 ;;
    esac
done
