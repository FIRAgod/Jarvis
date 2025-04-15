#!/usr/bin/env python3

import sys
import time
import json
import argparse
import requests
from datetime import datetime
from requests.exceptions import ConnectionError, Timeout, RequestException
from functools import wraps

# 关节名称和限位
# TODO: load from configurations
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
dual_arm_joints = left_arm_joints + right_arm_joints

joint_data = {
    "LEFT_ARM": left_arm_joints,
    "RIGHT_ARM": right_arm_joints,
    "DUAL_ARM": dual_arm_joints,
    "HEAD":  head_joints,
    "WAIST_LIFT":  waist_lift_joints,
    "WAIST_PITCH":  waist_pitch_joints
}

def retry_on_failure(retries=3, delay=2, backoff=1.5):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            last_exception = None
            while attempts < retries:
                try:
                    result = func(*args, **kwargs)
                    sys.stdout.write("\033[K")
                    sys.stdout.flush()
                    return result
                except (ConnectionError, Timeout) as e:
                    last_exception = e
                    sys.stdout.write(f"\rAttempt {attempts + 1}: {str(e)}. Retrying in {current_delay:.1f} seconds...")
                    sys.stdout.flush()
                except RequestException as e:
                    last_exception = e
                    sys.stdout.write(f"\rAttempt {attempts + 1}: Request error: {e}. Stopping retries.\n")
                    sys.stdout.flush()
                    break
                time.sleep(current_delay)
                current_delay *= backoff
                attempts += 1

            sys.stdout.write("\r\033[K")
            sys.stdout.flush()
            if last_exception is not None:
                raise last_exception
            return None
        return wrapper
    return decorator

class MotionControlService:
    @staticmethod
    def add_arguments(parser):
        parser.add_argument(
            "--host",
            type=str,
            default="127.0.0.1",
            help="Host address, default is 127.0.0.1.",
        )

    def __init__(self, args = None):
        self.host = args.host if isinstance(args, argparse.Namespace) else "127.0.0.1"

    def _gen_header(self):
        now = datetime.utcnow()
        header = {
            "timestamp": {
                "seconds": int(now.timestamp()),
                "nanos": now.microsecond * 1000,
                "ms_since_epoch": int(now.timestamp() * 1000),
            },
            "control_source": "ControlSource_SAFE",
        }
        return header

    @retry_on_failure(retries=3, delay=1, backoff=1.5)
    def set_action(self, action):
        url = f"http://{self.host}:56322/rpc/aimdk.protocol.McActionService/SetAction"
        headers = {"Content-Type": "application/json"}
        payload = {
            "header": self._gen_header(),
            "command": {"action": "McAction_USE_EXT_CMD", "ext_action": action},
        }
        return requests.post(url, headers=headers, json=payload)

    @retry_on_failure(retries=3, delay=1, backoff=1.5)
    def get_current_action(self):
        url = f"http://{self.host}:56322/rpc/aimdk.protocol.McActionService/GetAction"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json={})
        response.raise_for_status()

        return response.json().get('info', {}).get('ext_action', '')

    @retry_on_failure(retries=3, delay=1, backoff=1.5)
    def get_available_actions(self):
        url = f"http://{self.host}:56322/rpc/aimdk.protocol.McActionService/GetAvailableActions"
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, json={})
        response.raise_for_status()

        return response.json().get('actions', [])

    def select_action(self, actions = None):
        try:
            if actions is None:
                actions = self.get_available_actions()

            if len(actions) == 0:
                print("No actions available.")
                exit(0)
            elif len(actions) == 1:
                return actions[0]
            else:
                print("Please select an action:")
                for index, action in enumerate(actions, 1):
                    print(f" {index}: {action}")
                choice = input("Enter the number corresponding to the desired action: ")
                if choice.isdigit() and int(choice) >= 0 and int(choice) < len(actions):
                    return self.set_action(actions[int(choice) - 1])
                elif isinstance(choice, str) and choice == "q":
                    exit(0)
                else:
                    print("Invalid choice.")
                    exit(1)
        except Exception as e:
            print(f"Error: {e}")
            exit(1)

    def ensure_action(self, action: str, retries = 3, retry_interval = 5):
        is_target_action = False
        sys.stdout.write("\033[s");
        sys.stdout.flush();
        try:
            for i in range(3):
                if self.get_current_action() == action:
                    is_target_action = True
                    break
                else:
                    self.set_action(action)
                    time.sleep(1 if i == 1 else retry_interval)

            if not is_target_action:
                print("Failed to set action.")
                exit(0)
        except Exception as e:
            print(f"\033[uError: {e}\033[K")
            time.sleep(retry_interval)

        return is_target_action

    @retry_on_failure(retries=3, delay=1, backoff=1.5)
    def joint_move(self, joint_move_request):
        url = f"http://{self.host}:56322/rpc/aimdk.protocol.McMotionService/JointMove"
        headers = {"Content-Type": "application/json"}
        return requests.post(url, headers=headers, json=joint_move_request)

    @retry_on_failure(retries=3, delay=1, backoff=1.5)
    def planning_move(self, planning_move_request):
        url = f"http://{self.host}:56322/rpc/aimdk.protocol.McMotionService/PlanningMove"
        headers = {"Content-Type": "application/json"}
        return requests.post(url, headers=headers, json=planning_move_request)

    @retry_on_failure(retries=3, delay=1, backoff=1.5)
    def joint_control(self, joint_control_request):
        url = f"http://{self.host}:56322/rpc/aimdk.protocol.McMotionService/JointControl"
        headers = {"Content-Type": "application/json"}
        return requests.post(url, headers=headers, json=joint_control_request)

    @retry_on_failure(retries=3, delay=1, backoff=1.5)
    def get_task_status(self, task_id):
        url = f"http://{self.host}:56322/rpc/aimdk.protocol.McDataService/GetTaskState"
        headers = {"Content-Type": "application/json"}
        payload = {"task_id": task_id}
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        return response.json()["state"].replace("CommonState_", "")

    # For testing
    def gen_planning_move_request(self):
        url = f"http://{self.host}:56322/rpc/aimdk.protocol.McTestService/GetPlanningMoveTarget"
        headers = {"Content-Type": "application/json"}
        payload = {
            "header": self._gen_header(),
        }
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()

        return response.json()["planning_move_request"]

    def gen_joint_control_request(self, group = None):
        if group is None:
            group = random.choice(list(joint_data.keys()))
        def generate_random_joint_cmds(group, mode="ABSOLUTE"):
            if group not in joint_data:
                raise ValueError(f"关节组 {group} 不存在")

            cmds = []
            for joint in joint_data[group]:
                name = joint["name"]
                min_limit, max_limit = joint["limit"]

                if mode == "ABSOLUTE":
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

        return {
            "header": self._gen_header(),
            "group": group,
            "cmds": generate_random_joint_cmds(group)
        }
