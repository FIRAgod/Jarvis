#!/usr/bin/env python3

import json
import requests
from datetime import datetime

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

def service_call():
    url = 'http://127.0.0.1:56322/rpc/aimdk.protocol.McMotionService/GoHomePose'
    headers = {'Content-Type': 'application/json'}
    payload = {
        "header": create_header(),
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    return response

def main():
    response = service_call()
    print(response.text)

if __name__ == "__main__":
    main()
