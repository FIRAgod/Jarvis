#!/usr/bin/env python3

import json
import requests
import time
from datetime import datetime


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


def create_locomotion_velocity(forward, lateral, angular):
    return {
        "forward_velocity": forward,
        "lateral_velocity": lateral,
        "angular_velocity": angular
    }


def create_mclocomotion_velocity_channel(header, data):
    return {
        "header": header,
        "data": data
    }


def send_velocity_data(url, velocity_data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=velocity_data)
    return response


def main():
    url = 'http://127.0.0.1:56322/channel/%2Fmotion%2Fcontrol%2Flocomotion_velocity/pb%3Aaimdk.protocol.McLocomotionVelocityChannel'

    # 定义初始速度
    forward_velocity = 0.0
    lateral_velocity = 0.0
    angular_velocity = -0.2

    try:
        while True:
            header = create_header()
            velocity = create_locomotion_velocity(
                forward_velocity, lateral_velocity, angular_velocity)
            mclocomotion_velocity_channel = create_mclocomotion_velocity_channel(
                header, velocity)

            response = send_velocity_data(url, mclocomotion_velocity_channel)

            print(
                f"Sent data: {json.dumps(mclocomotion_velocity_channel, indent=2)}")
            print(f"Response: {response.status_code} - {response.text}\n")

            # 每隔50ms发送一次
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("Stopped by user")


if __name__ == "__main__":
    main()
