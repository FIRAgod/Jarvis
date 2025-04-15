#!/usr/bin/env python3

import requests
import json


def send_request(service, func):
    url = f"http://127.0.0.1:56322/rpc/aimdk.protocol.{service}/{func}"
    headers = {
        'Content-Type': 'application/json'
    }
    data = {}

    response = requests.post(url, headers=headers, json=data)
    return response.json()


def pretty_print_json(json_data):
    print("Response:")
    print(json.dumps(json_data, indent=2, ensure_ascii=False))


def main():
    service = "McActionService"
    func = "GetAvailableCommands"

    response_json = send_request(service, func)
    pretty_print_json(response_json)


if __name__ == "__main__":
    main()
