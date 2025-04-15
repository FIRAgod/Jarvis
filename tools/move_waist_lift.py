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

def create_mcmove_waist_channel(header, data):
    return {
        "header": header,
        # "waist_lift_value": data
        # "waist_sideways_value": data
        # "waist_pitch_value": data
        "waist_twist_value": data
    }


def send_pose_data(url, pose_data):
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, json=pose_data)
    return response


def main():
    # url = 'http://127.0.0.1:56322/channel/%2Fmotion%2Fcontrol%2Fmove_waist_lift/pb%3Aaimdk.protocol.McMoveWaistLiftChannel'
    # url = 'http://127.0.0.1:56322/channel/%2Fmotion%2Fcontrol%2Fmove_waist_sideways/pb%3Aaimdk.protocol.McMoveWaistSidewaysChannel'
    # url = 'http://127.0.0.1:56322/channel/%2Fmotion%2Fcontrol%2Fmove_waist_pitch/pb%3Aaimdk.protocol.McMoveWaistPitchChannel'
    url = 'http://127.0.0.1:56322/channel/%2Fmotion%2Fcontrol%2Fmove_waist_twist/pb%3Aaimdk.protocol.McMoveWaistTwistChannel'



    waist_lift_value = [-0.1, 0.0]
    waist_sideways_value = [0.5, 0.0]
    waist_pitch_value = [0.1, 0.0]
    waist_twist_value = [0.5, 0.0]

    # # 定义腰部数据, 共6组数据
    # x = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    # y = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    # z = [-0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    # # 定义腰部姿态数据
    # roll = [0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0]      # 左右
    # pitch = [0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0]     # 前后
    # yaw = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0]       # 旋转

    count = 2

    try:
        for i in range(count):
            count = 0
            while count < 100:
                header = create_header()

                mcmove_waist_channel = create_mcmove_waist_channel(
                    header, waist_twist_value[i])
            
                response = send_pose_data(url, mcmove_waist_channel)

                print(
                    f"Sent data: {json.dumps(mcmove_waist_channel, indent=2)}")
                print(f"Response: {response.status_code} - {response.text}\n")

                # 每隔50ms发送一次
                time.sleep(0.05)
                count = count + 1

    except KeyboardInterrupt:
        print("Stopped by user")


if __name__ == "__main__":
    main()