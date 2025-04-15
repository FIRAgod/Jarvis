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
    print(json.dumps(json_data, indent=2, ensure_ascii=False))


def main():
    options = [
        {"service": "McActionService", "func": "GetAction"},
        {"service": "McActionService", "func": "GetAvailableCommands"},
        {"service": "McActionService", "func": "GetAvailableActions"},
        {"service": "McBaseService", "func": "GetWorkState"},
        {"service": "McBaseService", "func": "GetWorkMode"},
        {"service": "McBaseService", "func": "GetState"},
        {"service": "McBaseService", "func": "GetJakaState"},
        {"service": "McDataService", "func": "GetJointAngle"},
        {"service": "McDataService", "func": "GetJointState"},
        {"service": "McDataService", "func": "GetNeckState"},
        {"service": "McDataService", "func": "GetHandState"}
    ]

    print("Please choose a function by entering the corresponding number:")
    for i, option in enumerate(options):
        print(f"{i + 1}. {option['func']}")

    choice = int(input("Enter the number of your choice: ")) - 1

    if 0 <= choice < len(options):
        selected_option = options[choice]
        service = selected_option["service"]
        func = selected_option["func"]

        response_json = send_request(service, func)
        pretty_print_json(response_json)
    else:
        print("Invalid choice. Please run the script again and select a valid number.")


if __name__ == "__main__":
    main()
