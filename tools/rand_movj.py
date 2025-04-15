#!/usr/bin/env python3

import sys
import random
import time
import json
import requests
from datetime import datetime

# Define joint position limits
joint_position_limits = [
    (-0.265, 0.265),               # waist lift
    (0.053, 1.55),                 # waist yaw
    # (-1.02, 1.02),                 # head
    (-6.28, 6.28),          # Left arm joint 1
    (-1.570, 0.785),        # Left arm joint 2
    (-6.28, 6.28),          # Left arm joint 3
    (-2.530, 0.523),        # Left arm joint 4
    (-6.283, 6.283),        # Left arm joint 5
    (-1.570, 1.570),        # Left arm joint 6
    (-6.283, 6.283),        # Left arm joint 7
    (-6.28, 6.28),          # Right arm joint 1
    (-1.570, 0.785),        # Right arm joint 2
    (-6.28, 6.28),          # Right arm joint 3
    (-2.530, 0.523),        # Right arm joint 4
    (-6.283, 6.283),        # Right arm joint 5
    (-1.570, 1.570),        # Right arm joint 6
    (-6.283, 6.283)         # Right arm joint 7
]


def generate_random_number(min_val, max_val):
    return random.uniform(min_val, max_val)


def generate_random_joint_data():
    angles = []
    for limits in joint_position_limits:
        min_val, max_val = limits
        angle = generate_random_number(min_val, max_val)
        angles.append(angle)
    return angles


# Parameter validation
if len(sys.argv) != 2 or not sys.argv[1].isdigit():
    print("Usage: python script.py <number_of_sets>")
    sys.exit(1)

number_of_sets = int(sys.argv[1])

# Generate specified number of joint data sets and send requests
for i in range(1, number_of_sets + 1):
    angles = generate_random_joint_data()
    timestamp = int(time.time() * 1000)  # current timestamp in milliseconds

    json_data = {
        "header": {
            "timestamp": {
                "seconds": str(int(timestamp / 1000)),
                "nanos": 0,
                "msSinceEpoch": str(timestamp),
            },
            "control_source": "ControlSource_MANUAL"
        },
        "group": "McPlanningGroup_DUAL_ARM_WAIST",
        "angles": angles
    }

    json_str = json.dumps(json_data)
    print(f"Sending JSON data for set {i}:")
    print(json_str)
    print("")

    # Example of sending data via HTTP POST request
    url = 'http://127.0.0.1:56322/rpc/aimdk.protocol.McMotionService/JointMove'
    headers = {'content-type': 'application/json'}
    response = requests.post(url, headers=headers, data=json_str)

    print(f"Response: {response.status_code}")
    print(response.text)
    print("")

    time.sleep(0.1)  # wait for 0.1 seconds between requests
