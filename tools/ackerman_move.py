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
            "ms_since_epoch": int(now.timestamp() * 1000)
        }
    }
    return header


def create_ackerman_motion_channel(header, turn_pos, move_vel):
    return {
        "header": header,
        "turn_pos": turn_pos,
        "move_vel": move_vel
    }


def send_ackerman_data(url, ackerman_data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=ackerman_data)
    return response


def main():
    url = 'http://127.0.0.1:56322/channel/%2Fmc%2Fmotor_ackermann_joystick/pb%3Aaimdk.protocol.MotorAckermannJoystickChannel'
    # 定义初始速度
    turn_pos = 0.1
    move_vel = 0.4

    try:
        while True:
            header = create_header()
            ackerman_motion_channel = create_ackerman_motion_channel(
                header, turn_pos, move_vel)

            response = send_ackerman_data(url, ackerman_motion_channel)

            print(
                f"Sent data: {json.dumps(ackerman_motion_channel, indent=2)}")
            print(f"Response: {response.status_code} - {response.text}\n")

            # 每隔50ms发送一次
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("Stopped by user")


if __name__ == "__main__":
    main()
