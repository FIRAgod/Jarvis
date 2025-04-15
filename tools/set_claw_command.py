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


def create_claw_data(pos, clamp_method, force=100, vel=100):
    # clamp_method: 0：idle  1：夹持   2：释放
    return {
        "agi_claw_cmd": {
            "pos": pos,
            "force": force,
            "clamp_method": clamp_method,
            "vel": vel
        }
    }


def service_call(left_hand=None, right_hand=None):
    # 发送服务请求
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
    left_data = [50, 1, 100, 100]  # 左边夹爪的数据
    right_data = [50, 1, 100, 100]  # 右边夹爪的数据

    # 创建左手和右手的数据
    left_hand = create_claw_data(
        left_data[0], left_data[1], left_data[2], left_data[3])
    right_hand = create_claw_data(
        right_data[0], right_data[1], right_data[2], right_data[3])
    # 调用服务，传入左右手数据
    response = service_call(left_hand=left_hand, right_hand=right_hand)
    print(response.text)


if __name__ == "__main__":
    main()
