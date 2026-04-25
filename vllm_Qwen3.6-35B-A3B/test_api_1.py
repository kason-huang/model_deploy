#!/usr/bin/env python3
"""
vLLM API 增强测试脚本
支持更多测试场景和详细的输出
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

    def test_health(self):
        """测试1: 健康检查"""
        print("\n" + "="*60)
        print("🧪 测试 1: 健康检查")
        print("="*60)
        try:
            import requests
            response = requests.get(f"{self.client.base_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ 服务健康检查通过")
                return True
            else:
                print(f"❌ 健康检查失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 连接失败: {str(e)}")
            return False

    def test_list_models(self):
        """测试2: 列出模型"""
        print("\n" + "="*60)
        print("🧪 测试 2: 列出可用模型")
        print("="*60)
        try:
            models = self.client.models.list()
            model = models.data[0]
            print(f"✅ 模型名称: {model.id}")
            print(f"   最大长度: {model.max_model_len} tokens")
            print(f"   模型路径: {model.root}")
            return True
        except Exception as e:
            print(f"❌ 获取模型列表失败: {str(e)}")
            return False

    def test_simple_chat(self):
        """测试3: 简单对话"""
        print("\n" + "="*60)
        print("🧪 测试 3: 简单对话")
        print("="*60)
        try:
            start = time.time()
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": "你好，请用一句话介绍你自己。"}],
                temperature=0.7,
                max_tokens=512
            )
            elapsed = time.time() - start

            msg = response.choices[0].message
            content = msg.content or "(推理过程在reasoning字段)"
            reasoning = msg.reasoning or ""

            print(f"🤖 模型回复: {content}")
            if reasoning:
                print(f"🧠 推理过程: {reasoning[:100]}...")
            print(f"⏱️  响应时间: {elapsed:.2f}秒")
            print(f"📊 Token使用: {response.usage.total_tokens} (输入:{response.usage.prompt_tokens}, 输出:{response.usage.completion_tokens})")
            return True
        except Exception as e:
            print(f"❌ 对话失败: {str(e)}")
            return False

    def test_math_reasoning(self):
        """测试4: 数学推理"""
        print("\n" + "="*60)
        print("🧪 测试 4: 数学推理")
        print("="*60)
        try:
            start = time.time()
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": "计算 123 × 456 = ？只给出最终数字答案。"}],
                temperature=0.0,
                max_tokens=512
            )
            elapsed = time.time() - start

            msg = response.choices[0].message
            content = msg.content or "（需要更多tokens）"

            print(f"❓ 问题: 123 × 456 = ？")
            print(f"💡 答案: {content}")
            print(f"⏱️  响应时间: {elapsed:.2f}秒")
            print(f"📊 Token使用: {response.usage.total_tokens}")
            return True
        except Exception as e:
            print(f"❌ 推理失败: {str(e)}")
            return False

    def test_code_generation(self):
        """测试5: 代码生成"""
        print("\n" + "="*60)
        print("🧪 测试 5: 代码生成")
        print("="*60)
        try:
            start = time.time()
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": "用Python写一个冒泡排序函数，只给代码不要解释。"}],
                temperature=0.0,
                max_tokens=300
            )
            elapsed = time.time() - start

            content = response.choices[0].message.content or "（无内容）"

            print(f"📝 生成的代码:")
            print("-" * 40)
            lines = content.split('\n')[:8]
            for line in lines:
                print(f"  {line}")
            if len(content.split('\n')) > 8:
                print("  ...")
            print("-" * 40)
            print(f"⏱️  响应时间: {elapsed:.2f}秒")
            print(f"📊 Token使用: {response.usage.total_tokens}")
            return True
        except Exception as e:
            print(f"❌ 代码生成失败: {str(e)}")
            return False

    def test_streaming(self):
        """测试6: 流式输出"""
        print("\n" + "="*60)
        print("🧪 测试 6: 流式输出")
        print("="*60)
        try:
            print("📤 问题: 讲一个简短的笑话")
            print("💬 回答（逐字显示）:")

            stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": "讲一个50字以内的简短笑话。"}],
                stream=True,
                max_tokens=200
            )

            full_content = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    print(content, end="", flush=True)
                    full_content += content

            print()  # 换行
            print(f"✅ 流式输出完成，共 {len(full_content)} 字符")
            return True
        except Exception as e:
            print(f"\n❌ 流式输出失败: {str(e)}")
            return False

    def test_multi_turn(self):
        """测试7: 多轮对话"""
        print("\n" + "="*60)
        print("🧪 测试 7: 多轮对话")
        print("="*60)
        try:
            messages = [
                {"role": "system", "content": "你是一个有帮助的助手。"},
                {"role": "user", "content": "我的名字是张三"},
                {"role": "assistant", "content": "你好张三！很高兴认识你。"},
                {"role": "user", "content": "你还记得我的名字吗？"}
            ]

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=200
            )

            content = response.choices[0].message.content or "（无内容）"

            print(f"🗣️  多轮对话测试:")
            print(f"  用户: 我的名字是张三")
            print(f"  助手: 你好张三！很高兴认识你。")
            print(f"  用户: 你还记得我的名字吗？")
            print(f"  助手: {content}")
            print(f"✅ 多轮对话正常")
            return True
        except Exception as e:
            print(f"❌ 多轮对话失败: {str(e)}")
            return False

    def run_all_tests(self):
        """运行所有测试"""
        print("\n" + "🚀"*30)
        print("   vLLM API 完整测试套件")
        print("🚀"*30)
        print(f"\n📊 测试配置:")
        print(f"   服务地址: {self.client.base_url}")
        print(f"   模型名称: {self.model_name}")
        print(f"   Python版本: {sys.version.split()[0]}")

        results = []

        # 运行所有测试
        tests = [
            ("健康检查", self.test_health),
            ("列出模型", self.test_list_models),
            ("简单对话", self.test_simple_chat),
            ("数学推理", self.test_math_reasoning),
            ("代码生成", self.test_code_generation),
            ("流式输出", self.test_streaming),
            ("多轮对话", self.test_multi_turn),
        ]

        for name, test_func in tests:
            try:
                result = test_func()
                results.append((name, result))
            except Exception as e:
                print(f"\n❌ 测试 '{name}' 异常: {str(e)}")
                results.append((name, False))

        # 测试总结
        print("\n" + "="*60)
        print("📋 测试总结")
        print("="*60)

        passed = sum(1 for _, result in results if result)
        total = len(results)

        for name, result in results:
            status = "✅ 通过" if result else "❌ 失败"
            print(f"{status}  {name}")

        print(f"\n📊 测试结果: {passed}/{total} 通过")

        if passed == total:
            print("\n🎉 所有测试通过！vLLM 服务运行正常！")
        else:
            print(f"\n⚠️  {total - passed} 个测试失败，请检查服务状态")

        return passed == total


def main():
    client = VLLMClient()
    success = client.run_all_tests()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
