#!/usr/bin/env python3
"""
vLLM API 测试脚本（修复版）
正确处理推理模型的 reasoning 和 content 字段
"""

from openai import OpenAI
import time
import sys


class VLLMClient:
    def __init__(self, base_url="http://localhost:30000/v1", model_name="qwen3-vl"):
        self.client = OpenAI(
            base_url=base_url,
            api_key="dummy"
        )
        self.model_name = model_name

    def get_answer(self, response):
        """从响应中提取答案（处理推理模型）"""
        msg = response.choices[0].message
        content = msg.content
        reasoning = msg.reasoning

        # 优先使用 content，如果为空则尝试从 reasoning 提取
        if content and content.strip():
            return content, reasoning
        elif reasoning:
            # 尝试从 reasoning 中提取最终答案
            # 通常答案在推理过程的最后
            lines = reasoning.strip().split('\n')
            # 查找可能的答案行
            for line in reversed(lines[-5:]):  # 检查最后5行
                line = line.strip()
                if line and not line.startswith(('1.', '2.', '3.', '4.', '5.', '-', '*', '#')):
                    return line, reasoning
            return reasoning[-500:] if len(reasoning) > 500 else reasoning, reasoning
        else:
            return "(无回答)", None

    def test_simple_chat(self):
        """测试1: 简单对话"""
        print("\n" + "="*60)
        print("🧪 测试 1: 简单对话")
        print("="*60)
        print("问题：你好，请介绍一下自己")

        try:
            start = time.time()
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": "你好，请用一句话介绍你自己。"}],
                temperature=0.7,
                max_tokens=512
            )
            elapsed = time.time() - start

            answer, reasoning = self.get_answer(response)

            print(f"回答：{answer}")
            if reasoning and len(reasoning) > 100:
                print(f"🧠 推理过程（前100字符）: {reasoning[:100]}...")
            print(f"⏱️  响应时间: {elapsed:.2f}秒")
            print(f"📊 Token使用: {response.usage.total_tokens}")
            return True
        except Exception as e:
            print(f"❌ 错误: {str(e)}")
            return False

    def test_math_reasoning(self):
        """测试2: 数学推理"""
        print("\n" + "="*60)
        print("🧪 测试 2: 数学推理")
        print("="*60)
        print("问题：1+1等于几？只回答数字。")

        try:
            start = time.time()
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": "1+1等于几？只回答数字。"}],
                temperature=0.0,
                max_tokens=512
            )
            elapsed = time.time() - start

            answer, reasoning = self.get_answer(response)

            print(f"答案：{answer}")
            print(f"⏱️  响应时间: {elapsed:.2f}秒")
            print(f"📊 Token使用: {response.usage.total_tokens}")
            return True
        except Exception as e:
            print(f"❌ 错误: {str(e)}")
            return False

    def test_code_generation(self):
        """测试3: 代码生成"""
        print("\n" + "="*60)
        print("🧪 测试 3: 代码生成")
        print("="*60)
        print("问题：用Python写一个冒泡排序")

        try:
            start = time.time()
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": "用Python写一个冒泡排序函数，只给代码不要解释。"}],
                temperature=0.0,
                max_tokens=300
            )
            elapsed = time.time() - start

            answer, reasoning = self.get_answer(response)

            print(f"代码：\n{answer}")
            print(f"⏱️  响应时间: {elapsed:.2f}秒")
            print(f"📊 Token使用: {response.usage.total_tokens}")
            return True
        except Exception as e:
            print(f"❌ 错误: {str(e)}")
            return False

    def test_with_more_tokens(self):
        """测试4: 增加token数量"""
        print("\n" + "="*60)
        print("🧪 测试 4: 增加Token数量")
        print("="*60)
        print("问题：计算 123 × 456")
        print("配置：max_tokens=1024")

        try:
            start = time.time()
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": "计算 123 × 456 = ？只给出最终数字答案。"}],
                temperature=0.0,
                max_tokens=1024  # 增加token数量
            )
            elapsed = time.time() - start

            msg = response.choices[0].message
            content = msg.content
            reasoning = msg.reasoning

            print(f"Content 字段: {content if content else '(空)'}")
            if reasoning:
                print(f"🧠 推理过程（最后200字符）: {reasoning[-200:]}")
            print(f"⏱️  响应时间: {elapsed:.2f}秒")
            print(f"📊 Token使用: {response.usage.total_tokens}")
            print(f"📊 完成状态: {response.choices[0].finish_reason}")
            return True
        except Exception as e:
            print(f"❌ 错误: {str(e)}")
            return False


def main():
    print("=" * 60)
    print("vLLM Qwen3 客户端测试（修复版）")
    print("=" * 60)
    print(f"模型: qwen3-vl (推理模型)")
    print(f"提示: 回答可能在 content 或 reasoning 字段中")
    print("=" * 60)

    client = VLLMClient()

    # 运行测试
    results = []
    results.append(("简单对话", client.test_simple_chat()))
    #results.append(("数学推理", client.test_math_reasoning()))
    #results.append(("代码生成", client.test_code_generation()))
    #results.append(("增加Token", client.test_with_more_tokens()))

    # 总结
    print("\n" + "="*60)
    print("📋 测试总结")
    print("="*60)
    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status}  {name}")

    passed = sum(1 for _, r in results if r)
    print(f"\n结果: {passed}/{len(results)} 通过")

    if passed == len(results):
        print("🎉 所有测试通过！")
    else:
        print("⚠️  部分测试失败")


if __name__ == "__main__":
    main()
