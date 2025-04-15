#!/usr/bin/env python3

import json
import requests
from enum import Enum
from datetime import datetime

# 定义 McGaitType 枚举
class McGaitType(Enum):
    DEFAULT = 0
    STAND = 1
    WALK = 2

def create_header():
    now = datetime.utcnow()
    header = {
        "timestamp": {
            "seconds": int(now.timestamp()),
            "nanos": now.microsecond * 1000,
            "ms_since_epoch": int(now.timestamp() * 1000),
        },
        "control_source": "ControlSource_MANUAL"
    }
    return header


# 列出步态类型
def list_gait_types():
    print("Available gait types:")
    for gait in McGaitType:
        print(f"{gait.value}: {gait.name}")

# 获取用户选择的步态类型
def get_user_selection():
    while True:
        try:
            user_input = int(input("Please enter the index of the gait type you want to set: "))
            if user_input in [gait.value for gait in McGaitType]:
                return McGaitType(user_input)
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# 设置步态类型
def set_gait(gait_type):
    # 构造 McGaitTypeRequest
    url = 'http://127.0.0.1:56322/rpc/aimdk.protocol.McActionService/SetActionGait'
    headers = {'Content-Type': 'application/json'}
    payload = {
        "header": create_header(),
        "gait": gait_type.value
    }
    
    response = requests.post(url, headers=headers, json=payload)
    return response

def main():
    list_gait_types()
    selected_gait = get_user_selection()
    print(f"You selected: {selected_gait.name}")

    response = set_gait(selected_gait)
    print(f"Response: {response.status_code}")
    print(response.text)

if __name__ == "__main__":
    main()
