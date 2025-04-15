#!/usr/bin/env python3

import json
import time
import requests
from datetime import datetime
import numpy as np


def generate_trajectory_points(positions_list):
    points = []
    for i, positions in enumerate(positions_list):
        point = {
            "time_since_reference": 0.0,
            "positions": positions,
        }
        points.append(point)
    return points


def interpolate_trajectory_points(start_position, end_position):
    points = []
    start_position = np.array(start_position)
    end_position = np.array(end_position)
    num = 2000
    for i in range(num):
        position = start_position + \
            (end_position - start_position) * i / (num - 1)
        point = {
            "time_since_reference": 0.0,
            "positions": position.tolist(),
        }
        points.append(point)
    return points


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


def generate_json(left_positions_list, right_positions_list, interpolate=False):
    if interpolate:
        left_trajectory_points = interpolate_trajectory_points(
            left_positions_list[0], left_positions_list[1])
        right_trajectory_points = interpolate_trajectory_points(
            right_positions_list[0], right_positions_list[1])
    else:
        left_trajectory_points = generate_trajectory_points(
            left_positions_list)
        right_trajectory_points = generate_trajectory_points(
            right_positions_list)
    data = {
        "header": create_header(),
        "target": {
            "left": {
                "reference_time": 0.0,
                "points": left_trajectory_points
            },
            "right": {
                "reference_time": 0.0,
                "points": right_trajectory_points
            }
        }
    }
    return data


def send_json_data(json_data, url):
    json_str = json.dumps(json_data, indent=2)
    print("Sending JSON data:")
    print(json_str)
    print("")

    headers = {'content-type': 'application/json'}
    response = requests.post(url, headers=headers, data=json_str)

    print(f"Response: {response.status_code}")
    print(response.text)
    print("")


def main():
    left_positions_list = [
      # [-0.1055, 1.2544, 0, -0.7177, 1.5, -0.0004, 0.0025]  # 左臂零位
      # [-0.1055, 0.7544, 0, -0.7177, 1.5, -0.0004, 0.0025]  # step1
      [1.2055, 0.8544, 0.3, -1.9177, 2.3, -0.0004, 0.0025]  # step2

    ]

    # 1 - 上下；正为上 2 - 左右；正为外 3 - 转前臂；正为逆时针 4 - 前臂上下；正为上
    # 5 - 转手腕；正为逆时针 6 - 手掌上下；正为下 7 - 手掌左右；正为左

    right_positions_list = [
      # [-0.1056, -1.2544, 0, 0.7177, 1.5, 0.0093, -0.0027]  # 右臂零位
      # [-0.1056, -1.2544, 0, 0.7177, 1.5, 0.0093, -0.0027]  # step1
      [-0.1056, -1.2544, 0, 0.7177, 1.5, 0.0093, -0.0027]  # step2

    ]

    url = 'http://127.0.0.1:56322/rpc/aimdk.protocol.McMotionService/TrajectoryMove'

    json_data = generate_json(
        left_positions_list, right_positions_list, interpolate=False)
    send_json_data(json_data, url)


if __name__ == "__main__":
    main()
