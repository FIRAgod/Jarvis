#!/usr/bin/env python3

import json
import time
import requests
from datetime import datetime


def create_request_header(control_source="ControlSource_SAFE"):
    now = datetime.utcnow()
    header = {
        "timestamp": {
            "seconds": int(now.timestamp()),
            "nanos": now.microsecond * 1000,
            "ms_since_epoch": int(now.timestamp() * 1000),
        },
        "control_source": control_source
    }
    return header


def create_pt_wiggle_param(range=0, period=0.3):
    return {
        "range": range,
        "period": period
    }


def create_pt_slide_common_param(contact_axis=None, search_axis=None, contact_force=0.0, start_density=1.0, time_factor=2, random_factor=0, start_search_immediately=True):
    return {
        "contact_axis": contact_axis or [0, 0, 1],
        "search_axis": search_axis or [1, 0, 0],
        "contact_force": contact_force,
        "start_density": start_density,
        "time_factor": time_factor,
        "random_factor": random_factor,
        "start_search_immediately": start_search_immediately
    }


def create_pt_trigger_condition_param(name="insertDis", data=0.1, state=1.0):
    return {
        "name": name,
        "data": data,
        "state": state
    }


def create_pt_trigger_condition(condition_type="PtTriggerConditionType_GREATER", condition_param=None):
    return {
        "type": condition_type,
        "param": condition_param or create_pt_trigger_condition_param(name="insertDis", data=0.03, state=0.0)
    }


def create_pt_trigger_config(condition_type="PtTriggerConditionType_GREATER", conditions=None):
    return {
        "type": condition_type,
        "conditions": conditions or [create_pt_trigger_condition()]
    }


def create_external_force_ctrl_param(
        external_force_axis=None,
        external_goal_wrench=None,
        external_kp=None,
        external_kv=None,
        external_ki=None,
        external_max_integral=None):

    return {
        "external_force_axis": external_force_axis or [1, 1, 0, 0, 0, 1],
        "external_goal_wrench": external_goal_wrench or [0, 0, 0, 0, 0, 0],
        "external_kp": external_kp or [0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
        "external_kv": external_kv or [50.0, 50.0, 20.0, 50.0, 50.0, 10.0],
        "external_ki": external_ki or [0.001, 0.001, 0.001, 0.001, 0.001, 0.001],
        "external_max_integral": external_max_integral or [0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
    }


def create_internal_force_ctrl_param(
        internal_force_axis=None,
        internal_goal_wrench=None,
        internal_kp=None,
        internal_kv=None,
        internal_ki=None,
        internal_max_integral=None):

    return {
        "internal_force_axis": internal_force_axis or [0, 0, 0, 0, 0, 0],
        "internal_goal_wrench": internal_goal_wrench or [0, 0, 0, 0, 0, 0],
        "internal_kp": internal_kp or [0.01, 0.01, 0.01, 0.01, 0.01, 0.01],
        "internal_kv": internal_kv or [50.0, 50.0, 20.0, 50.0, 50.0, 50.0],
        "internal_ki": internal_ki or [0.001, 0.001, 0.001, 0.001, 0.001, 0.001],
        "internal_max_integral": internal_max_integral or [0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
    }


def create_assembly_ctrl_task(external_admittance=None, internal_admittance=None):
    return {
        "external_admittance": external_admittance or create_external_force_ctrl_param(),
        "internal_admittance": internal_admittance or [create_internal_force_ctrl_param(), create_internal_force_ctrl_param()]
    }


def create_pt_slide_spiral_param(
        search_radius=0.0,
        wiggle=None,
        common=None,
        pt_slide_trigger=None,
        pt_control_param=None):

    return {
        "@type": "type.googleapis.com/aimdk.protocol.PtSlideSpiralParam",
        "search_radius": search_radius,
        "wiggle": wiggle or create_pt_wiggle_param(),
        "common": common or create_pt_slide_common_param(),
        "pt_slide_trigger": pt_slide_trigger or create_pt_trigger_config(),
        "pt_control_param": pt_control_param or create_external_force_ctrl_param()
    }


def create_pt_slide_zigzag_param(
        length=10.0,
        height=5.0,
        wiggle=None,
        common=None,
        pt_slide_trigger=None,
        pt_control_param=None):

    return {
        "@type": "type.googleapis.com/aimdk.protocol.PtSlideZigzagParam",
        "length": length,
        "height": height,
        "wiggle": wiggle or create_pt_wiggle_param(),
        "common": common or create_pt_slide_common_param(),
        "pt_slide_trigger": pt_slide_trigger or create_pt_trigger_config(),
        "pt_control_param": pt_control_param or create_external_force_ctrl_param()
    }


def create_pt_dual_slide_spiral_param(
        search_radius=0.0,
        wiggle=None,
        common=None,
        pt_dual_slide_trigger=None,
        pt_control_param=None):

    return {
        "@type": "type.googleapis.com/aimdk.protocol.PtDualSlideSpiralParam",
        "search_radius": search_radius,
        "wiggle": wiggle or create_pt_wiggle_param(),
        "common": common or create_pt_slide_common_param(),
        "pt_dual_slide_trigger": pt_dual_slide_trigger or create_pt_trigger_config(),
        "pt_control_param": pt_control_param or create_assembly_ctrl_task()
    }


def create_pt_dual_slide_zigzag_param(
        length=15.0,
        height=7.5,
        wiggle=None,
        common=None,
        pt_dual_slide_trigger=None,
        pt_control_param=None):

    return {
        "@type": "type.googleapis.com/aimdk.protocol.PtDualSlideZigzagParam",
        "length": length,
        "height": height,
        "wiggle": wiggle or create_pt_wiggle_param(),
        "common": common or create_pt_slide_common_param(),
        "pt_dual_slide_trigger": pt_dual_slide_trigger or create_pt_trigger_config(),
        "pt_control_param": pt_control_param or create_assembly_ctrl_task()
    }


def create_pt_contact_param(
        refer_coordinate="tcp",
        freespace_vel=1.0,
        contact_dir=None,
        max_contact_force=10.0,
        pt_contact_trigger=None):

    return {
        "@type": "type.googleapis.com/aimdk.protocol.PtContactParam",
        "refer_coordinate": refer_coordinate,
        "freespace_vel": freespace_vel,
        "contact_dir": contact_dir or [0.1, 0.2, 0.3],
        "max_contact_force": max_contact_force,
        "pt_contact_trigger": pt_contact_trigger or create_pt_trigger_config()
    }


def create_pt_sleeve_param(
        insert_dir=None,
        alignment_dir=None,
        max_contact_force=20.0,
        insert_vel=0.005,
        deadband_scale=0.1,
        pt_sleeve_trigger=None,
        pt_control_param=None):

    return {
        "@type": "type.googleapis.com/aimdk.protocol.PtSleeveParam",
        "insert_dir": insert_dir or [0, 0, 1],
        "alignment_dir": alignment_dir or [0, 0, 0, 0, 0, 0],
        "max_contact_force": max_contact_force,
        "insert_vel": insert_vel,
        "deadband_scale": deadband_scale,
        "pt_sleeve_trigger": pt_sleeve_trigger or create_pt_trigger_config(),
        "pt_control_param": pt_control_param or create_external_force_ctrl_param()
    }


def create_pt_dual_sleeve_param(
        insert_dir=None,
        alignment_dir=None,
        max_contact_force=25.0,
        insert_vel=0.005,
        deadband_scale=0.15,
        pt_dual_sleeve_trigger=None,
        pt_control_param=None):

    return {
        "@type": "type.googleapis.com/aimdk.protocol.PtDualSleeveParam",
        "insert_dir": insert_dir or [0, 0, 1],
        "alignment_dir": alignment_dir or [0, 0, 0, 0, 0, 0],
        "max_contact_force": max_contact_force,
        "insert_vel": insert_vel,
        "deadband_scale": deadband_scale,
        "pt_dual_sleeve_trigger": pt_dual_sleeve_trigger or create_pt_trigger_config(),
        "pt_control_param": pt_control_param or create_assembly_ctrl_task()
    }


def create_primitive_action(
        type="",
        p=None):
    if p is not None:
        return {
            "type": type,
            "param": p
        }

    param = None
    if type == "PrimitiveType_SLIDE_SPIRAL":
        param = create_pt_slide_spiral_param()
    elif type == "PrimitiveType_SLIDE_ZIGZAG":
        param = create_pt_slide_zigzag_param()
    elif type == "PrimitiveType_SLEEVE":
        param = create_pt_sleeve_param()
    elif type == "PrimitiveType_CONTACT":
        param = create_pt_contact_param()
    elif type == "PrimitiveType_SLIDE_SPIRAL_DUAL":
        param = create_pt_dual_slide_spiral_param()
    elif type == "PrimitiveType_SLIDE_ZIGZAG_DUAL":
        param = create_pt_dual_slide_zigzag_param()
    elif type == "PrimitiveType_SLEEVE_DUAL":
        param = create_pt_dual_sleeve_param()
    elif type == "PrimitiveType_CONTACT_DUAL":
        param = create_pt_dual_contact_param()

    return {
        "type": type,
        "param": param
    }


def create_force_primitive(type=None, actions=None):
    if type is None:
        type = "PrimitiveType_SLIDE_SPIRAL"
    if actions is None:
        actions = [create_primitive_action(type=type)]
    return {
        "actions": actions
    }


def create_force_primitive_request(side="right", type="PrimitiveType_SLEEVE"):
    header = create_request_header()
    force_primitive = create_force_primitive(type=type)
    return {
        "header": header,
        side: force_primitive
    }


def create_dual_force_primitive_request(type="PrimitiveType_SLIDE_SPIRAL_DUAL"):
    return create_force_primitive_request(side="dual", type=type)


def create_left_force_primitive_request(type="PrimitiveType_SLIDE_ZIGZAG"):
    return create_force_primitive_request(side="left", type=type)


def create_right_force_primitive_request(type="PrimitiveType_SLEEVE"):
    return create_force_primitive_request(side="right", type=type)


def set_force_call(side="dual"):
    url = 'http://127.0.0.1:56322/rpc/aimdk.protocol.McForceService/SetForceControlPrimitive'
    headers = {'Content-Type': 'application/json'}
    payload = create_force_primitive_request(side=side)

    # print(json.dumps(payload, indent=2))
    response = requests.post(url, headers=headers, json=payload)
    print(response.text)
    return response

    # 提取响应数据的task_id，并查询状态
    # {"header":{"code":"0","msg":"","timestamp":{"seconds":"1725264591","nanos":527650264,"ms_since_epoch":"0"}},"task_id":"88414522588555","state":"CommonState_PENDING"}


def set_force_call_and_check(side="dual"):
    response = set_force_call(side=side)
    # 提取响应数据的task_id，并查询状态
    # {"header":{"code":"0","msg":"","timestamp":{"seconds":"1725264591","nanos":527650264,"ms_since_epoch":"0"}},"task_id":"88414522588555","state":"CommonState_PENDING"}
    task_id = response.json()["task_id"]

    url = 'http://127.0.0.1:56322/rpc/aimdk.protocol.McDataService/GetTaskState'
    headers = {'Content-Type': 'application/json'}
    payload = {"task_id": task_id}

    while True:
        response = requests.post(url, headers=headers, json=payload)
        state = response.json()["state"]
        print(f"task_id: {task_id}, state: {state}")
        # 如果任务完成，跳出循环
        if state in ["CommonState_SUCCESS", "CommonState_FAILURE"]:
            break
        time.sleep(1)


def main():
    # set_force_call_and_check("dual")
    # set_force_call_and_check("left")
    # set_force_call("dual")
    set_force_call("left")
    set_force_call("right")


if __name__ == "__main__":
    main()
