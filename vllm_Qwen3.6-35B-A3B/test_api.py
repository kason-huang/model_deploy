#!/usr/bin/env python3
"""
vLLM API Python 客户端示例
支持文本生成、流式输出、多轮对话等功能
"""

from openai import OpenAI
import sys


class VLLMClient:
    def __init__(self, base_url="http://localhost:30000/v1", model_name="qwen3-vl"):
        self.client = OpenAI(
            base_url=base_url,
            api_key="dummy"  # vLLM 不需要真实密钥
        )
        self.model_name = model_name

    def generate(self, prompt, temperature=0.7, max_tokens=512, stream=False):
        """文本生成"""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream
            )

            if stream:
                print("回复：", end="", flush=True)
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        print(chunk.choices[0].delta.content, end="", flush=True)
                print()  # 换行
            else:
                return response.choices[0].message.content

        except Exception as e:
            return f"错误: {str(e)}"

    def chat(self, messages, temperature=0.7, max_tokens=512):
        """多轮对话"""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"错误: {str(e)}"

    def list_models(self):
        """列出可用模型"""
        try:
            models = self.client.models.list()
            return [model.id for model in models.data]
        except Exception as e:
            return f"错误: {str(e)}"


def main():
    # 初始化客户端
    client = VLLMClient()

    print("=" * 50)
    print("vLLM Qwen3 客户端测试")
    print("=" * 50)

    # 测试 1：简单问答
    print("\n[测试 1] 简单问答")
    print("问题：你好，请介绍一下自己")
    response = client.generate("你好，请用一句话介绍你自己。")
    print(f"回答：{response}")

    # 测试 2：数学计算
    print("\n[测试 2] 数学推理")
    print("问题：123 + 456 = ？")
    response = client.generate("计算 123 + 456 = ？只给出最终数字答案。", temperature=0.0)
    print(f"回答：{response}")

    # 测试 3：代码生成
    print("\n[测试 3] 代码生成")
    print("问题：用 Python 写一个快速排序")
    response = client.generate("用 Python 写一个快速排序算法，只给出代码。", max_tokens=300)
    print(f"回答：\n{response}")

    # 测试 4：流式输出
    print("\n[测试 4] 流式输出")
    print("问题：讲一个简短的故事")
    client.generate("讲一个100字以内的简短故事。", stream=True)

    # 测试 5：多轮对话
    print("\n[测试 5] 多轮对话")
    messages = [
        {"role": "system", "content": "你是一个有帮助的助手。"},
        {"role": "user", "content": "我的名字是张三"},
        {"role": "assistant", "content": "你好张三！很高兴认识你。"},
        {"role": "user", "content": "你还记得我的名字吗？"}
    ]
    response = client.chat(messages)
    print(f"回答：{response}")

    print("\n" + "=" * 50)
    print("测试完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
