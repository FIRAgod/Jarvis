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
                "reference_time": 5.0,
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
    	[
	-0.10545928031206131,
	1.254409909248352,
	 0,
	 -0.7177416086196899,
	 1.499998688697815,
	 -0.0004906999690468513,
	 0.002540077572709486
	]
        ]
        # [0.24, -1.4, 1.5708, 0.8, 0, 0, 0],
        # [0.44, -1.1, 1.3708, 1.0, 0, 0, 0],
        # [0.64, -0.8, 1.1708, 1.2, 0, 0, 0],
        # [0., 0., 0., 0., 0., 0., 0.]    ]

    right_positions_list = [
        # fixed set point
        # [-0.24, -1.4, -1.5708, 0.8, 0, 0, 0],
        # [-0.44, -1.1, -1.3708, 1.0, 0, 0, 0],
        # [-0.64, -0.8, -1.1708, 1.2, 0, 0, 0],
        # [0., 0., 0., 0., 0., 0., 0.],
        # fixed set point
        # [0.369, -1.347, -1.652, 0.980, 0.305, 0.025, -0.168],
        # [1.459, -1.506, -1.844, 0.172, 0.176, 0.569, 0.027],
        # fixed set poin
 [
    0.90546022653579712,
    -0.9054409909248352,
     0,
      0.79397608757019,
     1.47999996423721313,
     0.0007985953758035265,
     -0.0027439736109331043

]


    ]

    url = 'http://127.0.0.1:56322/rpc/aimdk.protocol.McMotionService/TrajectoryMove'

    json_data = generate_json(
        left_positions_list, right_positions_list, interpolate=False)
    send_json_data(json_data, url)


if __name__ == "__main__":
    main()
