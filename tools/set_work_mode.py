#!/usr/bin/env python3

import json
import requests
from enum import Enum
from datetime import datetime

# 定义 McWorkModeType 枚举
class McWorkModeType(Enum):
    AUTO = 0
    MANUAL = 1
    SAFE = 2
    DISABLED = 3

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


# 列出所有控制模式
def list_work_modes():
    print("Available work mode:")
    for mode in McWorkModeType:
        print(f"{mode.value}: {mode.name}")

# 获取用户选择的步态类型
def get_user_selection():
    while True:
        try:
            user_input = int(input("Please enter the index of the mode type you want to set: "))
            if user_input in [work.value for work in McWorkModeType]:
                return McWorkModeType(user_input)
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

# 设置步态类型
def set_work(work_type):
    # 构造 McWorkModeTypeRequest
    url = 'http://127.0.0.1:56322/rpc/aimdk.protocol.McBaseService/SetWorkMode'
    headers = {'Content-Type': 'application/json'}
    payload = {
        "header": create_header(),
        "mode": work_type.value
    }
    
    print(payload)
    response = requests.post(url, headers=headers, json=payload)
    
    return response

def main():
    list_work_modes()
    selected_work = get_user_selection()
    print(f"You selected: {selected_work.name}")

    response = set_work(selected_work)
    print(f"Response: {response.status_code}")
    print(response.text)

if __name__ == "__main__":
    main()
