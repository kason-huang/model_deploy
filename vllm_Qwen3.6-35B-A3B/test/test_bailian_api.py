#!/usr/bin/env python3
"""
阿里云百炼API场景分类测试脚本

测试使用阿里云百炼多模态模型进行场景分类

功能：
- 测试API连接和认证
- 测试单张图像分类
- 支持批量测试
- 显示详细的API响应
"""

import os
import sys
import base64
import requests
import json
from pathlib import Path
from typing import Dict, Any


class BailianSceneClassifier:
    """阿里云百炼场景分类器"""

    def __init__(self, api_key: str = None):
        """
        初始化分类器

        Args:
            api_key: 阿里云百炼API密钥
        """
        self.api_key = api_key or os.getenv('DASHSCOPE_API_KEY')

        if not self.api_key:
            raise ValueError("❌ API密钥未设置！请设置环境变量 DASHSCOPE_API_KEY")

        print(f"✓ API密钥已加载: {self.api_key[:10]}...")

        # 12类场景分类体系
        self.category_descriptions = {
            "Industrial office": "industrial office tables and chairs, conference rooms, conference TVs",
            "Industrial kitchen": "industrial refrigerator, sink, coffee maker",
            "Industrial dining room": "industrial setting with dining tables",
            "Home office": "desk or desk chairs in a home setting",
            "Home kitchen": "refrigerator, kitchen sink, kitchen tabletop in a home setting",
            "Home dining room": "dining table, dining chairs, in a home setting",
            "Bedroom": "room with a bed",
            "Bathroom": "Showers, baths, toilets, bathroom sinks",
            "Living room": "places with couches, armchairs, coffee tables, tvs in a home setting",
            "Hallway / closet": "areas between rooms, situations where the robot is interacting with a door or objects in a closet",
            "Other": "any other location that does not fit into those categories",
            "Unknown": "a scene that's too hard to classify because the image is dark or too close up"
        }

        # API配置
        #self.api_url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
        #self.model = "qwen3.6-35b-a3b"
        # self.model = "qwen-vl-max"
        # self.api_url = "http://192.168.0.59:30000/v1"
        self.api_url = "http://localhost:30000/v1"  # 使用本地vLLM服务
        self.model="qwen3-vl"
        

    def encode_image_to_base64(self, image_path: str) -> str:
        """
        将图像编码为base64

        Args:
            image_path: 图像文件路径

        Returns:
            base64编码的字符串
        """
        print(f"  编码图像: {Path(image_path).name}")

        try:
            with open(image_path, 'rb') as f:
                image_data = f.read()

            # 检查文件大小
            size_mb = len(image_data) / (1024 * 1024)
            print(f"  文件大小: {size_mb:.2f} MB")

            # 编码为base64
            encoded = base64.b64encode(image_data).decode('utf-8')
            print(f"  ✓ 编码成功，长度: {len(encoded)} 字符")

            return encoded

        except FileNotFoundError:
            print(f"  ❌ 错误: 文件不存在 {image_path}")
            raise
        except Exception as e:
            print(f"  ❌ 编码失败: {e}")
            raise

    def build_prompt(self) -> str:
        """
        构建场景分类的prompt

        Returns:
            prompt字符串
        """
        category_list = "\n".join([
            f"{i}. {name}: {desc}"
            for i, (name, desc) in enumerate(self.category_descriptions.items(), 1)
        ])

        prompt = f"""Please classify the image into one of the following scene categories.
Respond with just the category name (do not include the category number).

{category_list}

Analyze the image and determine which scene category best describes the environment shown."""

        return prompt

    def classify_scene(self, image_path: str, show_details: bool = True) -> Dict[str, Any]:
        """
        分类场景

        Args:
            image_path: 图像文件路径
            show_details: 是否显示详细信息

        Returns:
            包含分类结果的字典
        """
        result = {
            'image_path': str(image_path),
            'success': False,
            'scene_category': None,
            'error': None,
            'api_response': None
        }

        try:
            if show_details:
                print(f"\n{'='*60}")
                print(f"开始分类: {Path(image_path).name}")
                print(f"{'='*60}")

            # 1. 编码图像
            image_base64 = self.encode_image_to_base64(image_path)

            # 2. 构建prompt
            prompt = self.build_prompt()

            if show_details:
                print(f"\n使用模型: {self.model}")
                print(f"API端点: {self.api_url}")

            # 3. 构建请求
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 1024  # 增加token限制，确保推理模型能完成推理过程
            }

            if show_details:
                print(f"\n发送请求...")
                print(f"Headers: {json.dumps({k: v[:20] + '...' if k == 'Authorization' else v for k, v in headers.items()}, indent=2)}")

            # 4. 发送请求
            # 使用完整的聊天端点URL
            chat_url = f"{self.api_url}/chat/completions"

            if show_details:
                print(f"发送请求到: {chat_url}")
                print(f"提示: 图像处理可能需要1-2分钟，请耐心等待...")

            response = requests.post(
                chat_url,
                json=payload,
                headers=headers,
                timeout=120  # 增加超时到120秒（图像处理需要更长时间）
            )

            # 5. 解析响应
            if show_details:
                print(f"\nHTTP状态码: {response.status_code}")

            response.raise_for_status()
            response_data = response.json()

            if show_details:
                print(f"\nAPI响应:")
                print(json.dumps(response_data, indent=2, ensure_ascii=False))

            # 6. 提取分类结果
            msg = response_data['choices'][0]['message']
            content = msg.get('content')
            reasoning = msg.get('reasoning')
            finish_reason = response_data['choices'][0].get('finish_reason', 'unknown')

            # 显示推理信息
            if show_details and finish_reason == 'length':
                print(f"\n⚠️  注意: 达到token限制，推理过程可能被截断")

            if show_details and reasoning:
                print(f"\n🧠 推理过程（前200字符）:")
                print(f"  {reasoning[:200]}...")

            # 优先使用 content，如果为空则尝试从 reasoning 提取
            scene_category = None
            if content and content.strip():
                scene_category = content.strip()
            elif reasoning:
                # 从推理过程中提取可能的分类结果
                # 通常答案在推理过程的最后
                lines = reasoning.strip().split('\n')
                # 查找可能是类别的行
                for line in reversed(lines[-10:]):  # 检查最后10行
                    line = line.strip()
                    # 检查是否匹配某个类别
                    for category in self.category_descriptions.keys():
                        if category.lower() in line.lower():
                            scene_category = category
                            break
                    if scene_category:
                        break
                # 如果没找到，使用reasoning的最后部分
                if not scene_category:
                    scene_category = "Unknown (推理未完成)"
            else:
                scene_category = "Unknown"

            # 验证类别
            valid_categories = list(self.category_descriptions.keys())
            if scene_category not in valid_categories:
                if show_details:
                    print(f"\n⚠️ 警告: API返回了无效类别: '{scene_category}'")
                    print(f"有效类别: {valid_categories}")
                    print(f"归类为: 'Unknown'")
                scene_category = "Unknown"

            result['success'] = True
            result['scene_category'] = scene_category
            result['api_response'] = response_data

            if show_details:
                print(f"\n{'='*60}")
                print(f"✓ 分类成功!")
                print(f"场景类别: {scene_category}")
                print(f"{'='*60}")

        except requests.exceptions.Timeout:
            error_msg = "请求超时（30秒）"
            result['error'] = error_msg
            if show_details:
                print(f"\n❌ {error_msg}")

        except requests.exceptions.RequestException as e:
            error_msg = f"网络请求失败: {e}"
            result['error'] = error_msg
            if show_details:
                print(f"\n❌ {error_msg}")

        except Exception as e:
            error_msg = f"未知错误: {e}"
            result['error'] = error_msg
            if show_details:
                print(f"\n❌ {error_msg}")

        return result

    def test_connection(self) -> bool:
        """
        测试API连接

        Returns:
            连接是否成功
        """
        print("\n" + "="*60)
        print("测试API连接")
        print("="*60)

        try:
            # 发送一个简单的测试请求
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            # 使用一个最小的测试payload
            payload = {
                "model": self.model,
                "messages": [
                    {
                        "role": "user",
                        "content": "Hello, this is a test."
                    }
                ]
            }

            print("发送测试请求...")
            # 使用完整的聊天端点URL
            chat_url = f"{self.api_url}/chat/completions"
            response = requests.post(
                chat_url,
                json=payload,
                headers=headers,
                timeout=10
            )

            print(f"HTTP状态码: {response.status_code}")

            if response.status_code == 200:
                print("✓ API连接成功!")
                return True
            else:
                print(f"❌ API返回错误: {response.status_code}")
                print(f"响应: {response.text[:200]}")
                return False

        except Exception as e:
            print(f"❌ 连接失败: {e}")
            return False


def test_single_image(classifier: BailianSceneClassifier, image_path: str):
    """
    测试单张图像分类

    Args:
        classifier: 分类器对象
        image_path: 图像路径
    """
    result = classifier.classify_scene(image_path, show_details=True)

    # 输出结果摘要
    print(f"\n📊 分类结果摘要:")
    print(f"  图像: {Path(image_path).name}")
    print(f"  状态: {'✓ 成功' if result['success'] else '✗ 失败'}")
    print(f"  场景: {result['scene_category']}")
    if result['error']:
        print(f"  错误: {result['error']}")


def test_batch_images(classifier: BailianSceneClassifier, image_paths: list):
    """
    批量测试图像分类

    Args:
        classifier: 分类器对象
        image_paths: 图像路径列表
    """
    print(f"\n批量测试 {len(image_paths)} 张图像")
    print("="*60)

    results = []
    success_count = 0

    for i, image_path in enumerate(image_paths, 1):
        print(f"\n[{i}/{len(image_paths)}] {Path(image_path).name}")

        result = classifier.classify_scene(image_path, show_details=False)
        results.append(result)

        if result['success']:
            success_count += 1
            print(f"  ✓ 场景: {result['scene_category']}")
        else:
            print(f"  ✗ 失败: {result['error']}")

    # 输出统计
    print(f"\n{'='*60}")
    print(f"批量测试完成")
    print(f"{'='*60}")
    print(f"总计: {len(image_paths)} 张")
    print(f"成功: {success_count} 张")
    print(f"失败: {len(image_paths) - success_count} 张")
    print(f"成功率: {success_count/len(image_paths)*100:.1f}%")

    # 场景分布统计
    if success_count > 0:
        print(f"\n场景分布:")
        from collections import Counter
        scenes = [r['scene_category'] for r in results if r['success']]
        scene_counts = Counter(scenes)

        for scene, count in scene_counts.most_common():
            print(f"  {scene:30s}: {count:2d}")

    return results


def main():
    """主函数"""
    print("阿里云百炼API场景分类测试")
    print("="*60)

    # 检查API密钥
    if 'DASHSCOPE_API_KEY' not in os.environ:
        print("❌ 错误: 未设置环境变量 DASHSCOPE_API_KEY")
        print("\n请先设置API密钥:")
        print("  export DASHSCOPE_API_KEY='your-api-key-here'")
        print("\n获取API密钥:")
        print("  1. 访问: https://bailian.console.aliyun.com/")
        print("  2. 开通多模态服务")
        print("  3. 创建API密钥")
        sys.exit(1)

    try:
        # 创建分类器
        classifier = BailianSceneClassifier()

        # 测试连接（可选，跳过以避免超时）
        print("\n⚠️  跳过连接测试（直接进行图像分类）")
        # if not classifier.test_connection():
        #     print("\n❌ API连接测试失败，请检查:")
        #     print("  1. API密钥是否正确")
        #     print("  2. 网络连接是否正常")
        #     print("  3. 阿里云百炼服务是否可用")
        #     sys.exit(1)

        # 测试图像
        #test_image = "videoframe_7788666.png"
        test_image = "videoframe_21033.png"

        if not Path(test_image).exists():
            print(f"\n❌ 测试图像不存在: {test_image}")
            print(f"   请确保测试图像存在")
            sys.exit(1)

        print(f"\n使用测试图像: {test_image}")
        print(f"图像存在: {Path(test_image).exists()}")

        # 单张图像测试
        test_single_image(classifier, test_image)

        # 如果有其他测试图像，也可以批量测试
        # test_images = [test_image]
        # test_batch_images(classifier, test_images)

        print(f"\n{'='*60}")
        print("测试完成!")
        print(f"{'='*60}")

    except ValueError as e:
        print(f"\n{e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"\n\n用户中断测试")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 测试过程出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
