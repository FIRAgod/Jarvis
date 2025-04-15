#!/usr/bin/env python3

import json
import time
import requests
from datetime import datetime
import numpy as np
import copy

# 初始位置配置
DEFAULT_LEFT_POSITION = [
    -0.10545928031206131,
    1.254409909248352,
    0,
    -0.7177416086196899,
    1.499998688697815,
    -0.0004906999690468513,
    0.002540077572709486
]

DEFAULT_RIGHT_POSITION = [
    -0.10546022653579712,
    -0.854409909248352,
    0,
    1.7177397608757019,
    2.7999996423721313,
    0.2007985953758035265,
    -0.027439736109331043
]

def create_header():
    now = datetime.utcnow()
    return {
        "timestamp": {
            "seconds": int(now.timestamp()),
            "nanos": now.microsecond * 1000,
            "ms_since_epoch": int(now.timestamp() * 1000),
        },
        "control_source": "ControlSource_MANUAL"
    }

def generate_trajectory_points(positions_list):
    points = []
    for positions in positions_list:
        point = {
            "time_since_reference": 0.0,
            "positions": positions,
        }
        points.append(point)
    return points

def print_formatted_positions(left_position, right_position):
    print("\n=== 当前位置的完整JSON格式 ===")
    print("左臂位置:")
    print("[\n    " + ",\n    ".join([f"{x:0.6f}" for x in left_position]) + "\n]")
    print("\n右臂位置:")
    print("[\n    " + ",\n    ".join([f"{x:0.6f}" for x in right_position]) + "\n]")
    
    # 生成完整的JSON结构并打印
    full_json = {
        "header": create_header(),
        "target": {
            "left": {
                "reference_time": 0.0,
                "points": generate_trajectory_points([left_position])
            },
            "right": {
                "reference_time": 0.0,
                "points": generate_trajectory_points([right_position])
            }
        }
    }
    print("\n完整JSON结构:")
    print(json.dumps(full_json, indent=4))
    print("===========================\n")

def send_json_data(json_data, url):
    json_str = json.dumps(json_data, indent=2)
    print("\n发送的JSON数据:")
    print(json_str)
    print("")

    headers = {'content-type': 'application/json'}
    try:
        response = requests.post(url, headers=headers, data=json_str)
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}\n")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"发送请求时出错: {e}")
        return False

def generate_and_send_command(left_position, right_position, url):
    data = {
        "header": create_header(),
        "target": {
            "left": {
                "reference_time": 0.0,
                "points": generate_trajectory_points([left_position])
            },
            "right": {
                "reference_time": 0.0,
                "points": generate_trajectory_points([right_position])
            }
        }
    }
    return send_json_data(data, url)

def validate_input(value_str):
    try:
        value = float(value_str)
        if -0.5 <= value <= 0.5:
            return True, value
        else:
            print("错误：输入值必须在 -0.5 到 0.5 之间")
            return False, None
    except ValueError:
        print("错误：请输入有效的数字")
        return False, None

def print_current_positions(left_position, right_position):
    print("\n当前位置:")
    print("左臂:", [round(x, 4) for x in left_position])
    print("右臂:", [round(x, 4) for x in right_position])

def main():
    url = 'http://127.0.0.1:56322/rpc/aimdk.protocol.McMotionService/TrajectoryMove'
    
    current_left = copy.deepcopy(DEFAULT_LEFT_POSITION)
    current_right = copy.deepcopy(DEFAULT_RIGHT_POSITION)
    
    print("机器人交互控制程序")
    print("使用说明:")
    print("- 输入 'l' 或 'r' 选择左臂或右臂")
    print("- 输入 1-7 选择电机")
    print("- 输入 -0.5 到 0.5 之间的值调整位置")
    print("- 输入 'q' 退出程序")
    print("- 输入 'p' 打印当前位置")
    print("- 输入 'reset' 重置到默认位置")

    # 打印初始位置的JSON
    print_formatted_positions(current_left, current_right)

    while True:
        print_current_positions(current_left, current_right)
        
        arm = input("\n请选择控制臂 (l/r/q/p/reset): ").lower()
        
        if arm == 'q':
            print("程序退出")
            break
        
        elif arm == 'p':
            print_formatted_positions(current_left, current_right)
            continue
            
        elif arm == 'reset':
            current_left = copy.deepcopy(DEFAULT_LEFT_POSITION)
            current_right = copy.deepcopy(DEFAULT_RIGHT_POSITION)
            if generate_and_send_command(current_left, current_right, url):
                print("已重置到默认位置")
                print_formatted_positions(current_left, current_right)
            continue
            
        if arm not in ['l', 'r']:
            print("错误：请输入 'l' 或 'r' 选择控制臂")
            continue
            
        motor = input("请选择电机 (1-7): ")
        if not motor.isdigit() or int(motor) < 1 or int(motor) > 7:
            print("错误：请输入1-7之间的数字")
            continue
            
        value = input("请输入调整值 (-0.5 到 0.5): ")
        valid, delta = validate_input(value)
        if not valid:
            continue
            
        motor_idx = int(motor) - 1
        if arm == 'l':
            current_left[motor_idx] += delta
        else:
            current_right[motor_idx] += delta
            
        if generate_and_send_command(current_left, current_right, url):
            print(f"成功更新{'左' if arm == 'l' else '右'}臂电机 {motor} 位置")
            print_formatted_positions(current_left, current_right)
        else:
            if arm == 'l':
                current_left[motor_idx] -= delta
            else:
                current_right[motor_idx] -= delta
            print("命令发送失败，位置已恢复")

if __name__ == "__main__":
    main() 