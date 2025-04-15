import os
import re
import json
import time
import dashscope

def get_drink_positions(image_filename):
    """
    根据图片识别饮料位置（跨平台增强版）

    参数:
        image_filename (str): 图片文件名（如"1.png"）

    返回:
        dict | None: 饮料位置字典，格式为{"雪碧":"left", "无糖可乐":"mid", "有糖可乐":"right"}，失败返回None
    """
    try:
        # 构建图片绝对路径
        script_dir = os.path.dirname(os.path.abspath(__file__))
        local_path = os.path.join(script_dir, image_filename)
        image_path = f"file://{local_path}"

        # 调用多模态API
        start_time = time.time()
        response = dashscope.MultiModalConversation.call(
            api_key="sk-8b5d2c467c394feebe60e0f208aefbf3",
            model='qwen-vl-max',
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"image": image_path},
                        {"text": "请根据图片中有糖可乐，无糖可乐，雪碧的位置，给我返回一个字典，请严格按JSON格式返回字典，示例：{\"雪碧\":\"left\",\"有糖可乐\":\"left\"，\"无糖可乐\":\"mid\"}，键值必须用双引号，若无结果返回null"}
                    ]
                }
            ]
        )

        # 校验响应结构
        if "output" not in response or "choices" not in response["output"] or len(response["output"]["choices"]) == 0:
            print("错误：API返回结构异常")
            return None

        # 提取输出文本
        output_text = response["output"]["choices"][0]["message"].content[0]["text"]
        print(f"[DEBUG] 原始响应文本：\n{output_text}")  # 调试日志

        # 清理多余的字符（如 ```json 和 ```）
        cleaned_text = output_text.strip().strip("```json").strip("```").strip()
        print(f"[DEBUG] 清理后的文本：\n{cleaned_text}")  # 调试日志

        # 直接解析JSON字符串
        try:
            drink_positions = json.loads(cleaned_text)
        except json.JSONDecodeError as e:
            print(f"JSON解析失败：{e}\n问题数据：{cleaned_text}")
            return None

        # 校验返回的字典是否包含所有预期的键
        expected_keys = {"雪碧", "无糖可乐", "有糖可乐"}
        if not all(key in drink_positions for key in expected_keys):
            print(f"错误：返回的字典缺少预期的键，预期键：{expected_keys}，实际键：{drink_positions.keys()}")
            return None

        # 校验键值是否有效
        valid_values = {"left", "mid", "right"}
        for key, value in drink_positions.items():
            if value not in valid_values:
                print(f"错误：键 '{key}' 的值 '{value}' 无效，有效值为：{valid_values}")
                return None

        print(f"执行耗时：{time.time() - start_time:.2f}s")
        return drink_positions

    except KeyError as e:
        print(f"关键字段缺失：{str(e)}")
        return None
    except Exception as e:
        print(f"未捕获异常：{str(e)}")
        return None

# 示例调用
if __name__ == "__main__":
    image_file = "1.png"   # 替换实际文件名
    positions = get_drink_positions(image_file)

    if positions:
        print("\n饮料定位结果：")
        for drink, pos in positions.items():
            print(f"- {drink}: {pos}")
    else:
        print("未检测到饮料位置")