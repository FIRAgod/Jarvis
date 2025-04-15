#!/usr/bin/env python3

import json
import requests
from datetime import datetime

# 生成请求头部


def create_header():
    now = datetime.utcnow()
    header = {
        "timestamp": {
            "seconds": int(now.timestamp()),
            "nanos": now.microsecond * 1000,
            "ms_since_epoch": int(now.timestamp() * 1000),
        },
        "control_source": "ControlSource_SAFE"
    }
    return header

# 创建手部控制命令数据（支持单手或双手）


def create_hand_data(left_hand=None, right_hand=None):
    hand_data = {"data": {}}

    if left_hand:
        hand_data["data"]["left"] = left_hand

    if right_hand:
        hand_data["data"]["right"] = right_hand

    return hand_data

# 左手或右手的手指数据，支持传入手指位置的数组


def create_finger_data(finger_positions, finger_torques=None):
    # 默认的扭矩为0
    if finger_torques is None:
        finger_torques = [0] * 6  # 默认每个手指有6个位置/扭矩

    return {
        "agi_hand": {
            "finger": {
                "pos": {
                    "thumb_pos_0": finger_positions[0],
                    "thumb_pos_1": finger_positions[1],
                    "index_pos": finger_positions[2],
                    "middle_pos": finger_positions[3],
                    "ring_pos": finger_positions[4],
                    "pinky_pos": finger_positions[5]
                },
                "toq": {
                    "thumb_toq_0": finger_torques[0],
                    "thumb_toq_1": finger_torques[1],
                    "index_toq": finger_torques[2],
                    "middle_toq": finger_torques[3],
                    "ring_toq": finger_torques[4],
                    "pinky_toq": finger_torques[5]
                }
            }
        }
    }

# 发送服务请求


def service_call(left_hand=None, right_hand=None):
    url = 'http://127.0.0.1:56322/rpc/aimdk.protocol.McMotionService/SetHandCommand'
    headers = {
        'Content-Type': 'application/json',
        'timeout': '60000'
    }

    payload = {
        "header": create_header(),
        **create_hand_data(left_hand=left_hand, right_hand=right_hand)
    }

    response = requests.post(url, headers=headers, json=payload)

    return response

# 主程序入口


def main():
    # 设置左手和右手的手指位置: 0 - 2000
    left_finger_positions =  [100, 100, 100, 100, 100, 100]
    right_finger_positions = [600, 1400, 500, 2000, 2000, 2000] #step7_9
  # right_finger_positions = [100, 100, 100, 2000, 2000, 2000] #step7_8
  # right_finger_positions = [1400, 1000, 900, 900, 2000, 2000] #step7_7
  # right_finger_positions = [100, 100, 2000, 2000, 2000, 100] #step7_6
  # right_finger_positions = [100, 100, 100, 100, 100, 100] #step7_5
  # right_finger_positions = [300, 1600, 100, 100, 100, 100] #step7_4
  # right_finger_positions = [800, 1200, 1000, 100, 100, 100] #step7_3
  # right_finger_positions = [300, 1600, 100, 100, 1800, 1800] #step7_2
  # right_finger_positions = [500, 1000, 100, 2000, 2000, 2000] #step7_1

    # 如果需要，可以传入手指扭矩（默认值为0）
    left_finger_torques = [100, 100, 100, 100, 100, 100]
    right_finger_torques = [100, 100, 100, 100, 100, 100]

    # 创建左手和右手的数据
    left_hand = create_finger_data(left_finger_positions, left_finger_torques)
    right_hand = create_finger_data(
        right_finger_positions, right_finger_torques)

    # 调用服务，传入左右手数据
    response = service_call(left_hand=left_hand, right_hand=right_hand)
    print(response.text)


if __name__ == "__main__":
    main()
