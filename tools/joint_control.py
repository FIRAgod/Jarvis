#!/usr/bin/env python3

import sys
import json
import time
import random
import requests
from datetime import datetime

target_action = "PLANNING_MOVE"
# 定义左右臂关节名称和限位
left_arm_joints = [
    {"name": "idx12_left_arm_joint1", "limit": (-6.28, 6.28)},
    {"name": "idx13_left_arm_joint2", "limit": (-1.570, 0.785)},
    {"name": "idx14_left_arm_joint3", "limit": (-6.28, 6.28)},
    {"name": "idx15_left_arm_joint4", "limit": (-2.530, 0.523)},
    {"name": "idx16_left_arm_joint5", "limit": (-6.283, 6.283)},
    {"name": "idx17_left_arm_joint6", "limit": (-1.570, 1.570)},
    {"name": "idx18_left_arm_joint7", "limit": (-6.283, 6.283)}
]

right_arm_joints = [
    {"name": "idx19_right_arm_joint1", "limit": (-6.28, 6.28)},
    {"name": "idx20_right_arm_joint2", "limit": (-1.570, 0.785)},
    {"name": "idx21_right_arm_joint3", "limit": (-6.28, 6.28)},
    {"name": "idx22_right_arm_joint4", "limit": (-2.530, 0.523)},
    {"name": "idx23_right_arm_joint5", "limit": (-6.283, 6.283)},
    {"name": "idx24_right_arm_joint6", "limit": (-1.570, 1.570)},
    {"name": "idx25_right_arm_joint7", "limit": (-6.283, 6.283)}
]

head_joints = [
    {"name": "idx11_head_joint", "limit": (-1.02, 1.02)}
]

waist_lift_joints = [
    {"name": "idx09_lift_joint", "limit": (-0.265, 0.265)}
]

waist_pitch_joints = [
    {"name": "idx10_waist_joint", "limit": (0.053, 1.55)}
]

# 组合双臂关节数据
dual_arm_joints = left_arm_joints + right_arm_joints

# 将所有关节组定义在一起
joint_data = {
    "LEFT_ARM": left_arm_joints,
    "RIGHT_ARM": right_arm_joints,
    "DUAL_ARM": dual_arm_joints,
    "HEAD":  head_joints,
    "WAIST_LIFT":  waist_lift_joints,
    "WAIST_PITCH":  waist_pitch_joints
}


def get_current_action():
    # Step 1: 使用 requests 发起 POST 请求获取 actions 列表
    url = 'http://127.0.0.1:56322/rpc/aimdk.protocol.McActionService/GetAction'
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json={})

    # 解析返回的 JSON 内容，提取 actions 列表
    if response.status_code == 200:
        data = response.json()
        info = data.get('info', [])
        action = info.get('ext_action', [])
        return action
    return ""


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


def set_action(selected_action):
    # Step 3: 使用 requests 发起 POST 请求设置 action
    url = 'http://127.0.0.1:56322/rpc/aimdk.protocol.McActionService/SetAction'
    headers = {'Content-Type': 'application/json'}
    payload = {
        "header": create_header(),
        "command": {
            "action": "McAction_USE_EXT_CMD",
            "ext_action": selected_action
        }
    }
    response = requests.post(url, headers=headers, json=payload)

    return response


def check_and_set_action(selected_action):
    while True:
        current_action = get_current_action()
        if current_action == selected_action:
            break
        set_action(selected_action)
        print("set action: ", selected_action)
        time.sleep(0.5)


# 根据传入的组名称，创建 JointControlRequest 对象，数量与关节名称列表数量相同
def generate_random_joint_cmds(group, mode="ABSOLUTE"):
    if group not in joint_data:
        raise ValueError(f"关节组 {group} 不存在")

    cmds = []
    for joint in joint_data[group]:
        name = joint["name"]
        min_limit, max_limit = joint["limit"]

        if mode == "ABSOLUTE":
            # 生成随机位置在限位范围内
            position = random.uniform(min_limit, max_limit)
        elif mode == "RELATIVE":
            position = random.uniform(-0.2, 0.2)
        else:
            raise ValueError(f"不支持的模式: {mode}")
        cmd = {
            "name": name,
            "mode": mode,
            "angle": position
        }
        cmds.append(cmd)

    return cmds


def create_joint_control(group):
    payload = {
        "header": create_header(),
        "group": group,
        "cmds": generate_random_joint_cmds(group)
    }

    # print(json.dumps(payload, indent=2))
    return payload


# 获取任务状态
def get_task_state(task_id):
    url = 'http://127.0.0.1:56322/rpc/aimdk.protocol.McDataService/GetTaskState'
    headers = {'Content-Type': 'application/json'}
    payload = {
        "task_id": task_id
    }
    response = requests.post(url, headers=headers, json=payload)
    # print(response.text)
    return response


def set_joint_control(group):
    # Step 2: 使用 requests 发起 POST 请求设置 joint control
    url = 'http://127.0.0.1:56322/rpc/aimdk.protocol.McMotionService/JointControl'
    headers = {'Content-Type': 'application/json'}

    payload = create_joint_control(group)
    response = requests.post(url, headers=headers, json=payload)
    # print(response.text)
    return response


def set_joint_control_and_check(group):
    response = set_joint_control(group)
    task_id = response.json().get('task_id')
    while True:
        response = get_task_state(task_id)
        state = response.json().get('state')
        print(f"task_id: {task_id}, state: {state}")
        if state == 'CommonState_SUCCESS' or state == 'CommonState_FAILURE':
            break
        time.sleep(1)


def main():
    check_and_set_action(target_action)

    for data in joint_data:
        # 获取 data的关键字
        # create_joint_control(data)
        # set_joint_control(data)
        set_joint_control_and_check(data)


if __name__ == "__main__":
    main()
