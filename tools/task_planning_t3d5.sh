#!/bin/bash

# 参数校验
if [ -z "$1" ]; then
  echo "Usage: $0 <group_number>"
  exit 1
fi

# 参数组定义
declare -a groups=(
  # 1
  '{
    "group":"McPlanningGroup_DUAL_ARM",
    "target": {
      "type": "SE3",
      "left": {'position': {'x': 1.1, 'y': 0.2, 'z': 1.13}, 'orientation': {'x': -0.5, 'y': 0.5, 'z': -0.5, 'w': 0.5}},
      "right":{'position': {'x': 1.1, 'y': -0.2, 'z': 1.13}, 'orientation': {'x': -0.5, 'y': 0.5, 'z': -0.5, 'w': 0.5}},
    },
    "reference" :{
      "joint_position": [-0.705114, 0.766697, -0.206043, -1.71393, -0.204488, 0.903486, -0.60327, 0.707658, 0.676087, 0.130518, -1.78968, 0.10254, -1.13168, 0.710919] 
    }
  }'

  # 2
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_GRAB",
    "obj_info":{"name":"grab","pose":{'position': {'x': 1.1, 'y': 0.2, 'z': 1.13}, 'orientation': {'x': -0.5, 'y': 0.5, 'z': -0.5, 'w': 0.5}},"type":"UNKNOWN","parent_frame":""}
  }'

  # 3
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_CLOSURE",
    "target": {
      "type": "SE3",
      "left": {"position":{"x":0.611721,"y":0.212367,"z":1.02752},"orientation":{"x": 0.703405,"y":0.710737,"z":0.00512373,"w":-0.0069008}},
      "right":{"position":{"x":0.613836,"y":-0.233753,"z":1.01955},"orientation":{"x":-0.705596,"y":0.708462,"z":0.0107509,"w":0.00999545}},
    },
    "reference": {
      "joint_position": [0.78905, 0.470547, -0.704431, -0.577, -1.77087, 1.83251, -0.253787, -0.939039, 0.496086, 0.785611, -0.438611, 1.7734, -1.83251, 0.137814]
    },
    "obj_info":{
      "name":"grab",
      "pose":{
        "position":{'x': 0.84, 'y': 0.2, 'z': 0.9}, 
        "orientation": {'x': -0.707099437713623, 'y': 0.7067989110946655, 'z': -0.01782071590423584, 'w': -0.011316240765154362}
      },
      "type":"UNKNOWN",
      "parent_frame":""
    }
  }'

  # 4
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_GRAB",
    "obj_info":{"name":"grab","pose":{"position":{'x': 0.84, 'y': 0.2, 'z': 0.9}, "orientation": {'x': -0.707099437713623, 'y': 0.7067989110946655, 'z': -0.01782071590423584, 'w': -0.011316240765154362}},"type":"UNKNOWN","parent_frame":""}
  }'

  # 5
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_CLOSURE",
    "target": {
      "type": "SE3",
      "left": {'position': {'x': 1.1, 'y': 0.2, 'z': 1.13}, 'orientation': {'x': -0.5, 'y': 0.5, 'z': -0.5, 'w': 0.5}},
      "right":{'position': {'x': 1.1, 'y': -0.2, 'z': 1.13}, 'orientation': {'x': -0.5, 'y': 0.5, 'z': -0.5, 'w': 0.5}},
    },
    "reference" :{
      "joint_position": [-0.705114, 0.766697, -0.206043, -1.71393, -0.204488, 0.903486, -0.60327, 0.707658, 0.676087, 0.130518, -1.78968, 0.10254, -1.13168, 0.710919] 
    },
    "obj_info":{
      "name":"grab",
      "pose":{
        'position': {'x': 1.1, 'y': 0.2, 'z': 1.13}, 
        'orientation': {'x': -0.5, 'y': 0.5, 'z': -0.5, 'w': 0.5}
      },
      "type":"UNKNOWN",
      "parent_frame":""
    }
  }'

  # 2.2
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_GRAB",
    "obj_info":{"name":"grab","pose":{'position': {'x': 1.1, 'y': 0.2, 'z': 1.13}, 'orientation': {'x': -0.5, 'y': 0.5, 'z': -0.5, 'w': 0.5}},"type":"UNKNOWN","parent_frame":""}
  }'

  # 2.3
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_CLOSURE",
    "target": {
      "type": "SE3",
      "left": {"position":{"x":0.611721,"y":0.212367,"z":1.02752},"orientation":{"x": 0.703405,"y":0.710737,"z":0.00512373,"w":-0.0069008}},
      "right":{"position":{"x":0.613836,"y":-0.233753,"z":1.01955},"orientation":{"x":-0.705596,"y":0.708462,"z":0.0107509,"w":0.00999545}},
    },
    "reference": {
      "joint_position": [0.78905, 0.470547, -0.704431, -0.577, -1.77087, 1.83251, -0.253787, -0.939039, 0.496086, 0.785611, -0.438611, 1.7734, -1.83251, 0.137814]
    },
    "obj_info":{"name":"grab","pose":{"position":{'x': 0.84, 'y': 0.2, 'z': 0.9}, "orientation": {'x': -0.707099437713623, 'y': 0.7067989110946655, 'z': -0.01782071590423584, 'w': -0.011316240765154362}},"type":"UNKNOWN","parent_frame":""}
  }'

  # 2.4
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_GRAB",
    "obj_info":{"name":"grab","pose":{"position":{'x': 0.84, 'y': 0.2, 'z': 0.9}, "orientation": {'x': -0.707099437713623, 'y': 0.7067989110946655, 'z': -0.01782071590423584, 'w': -0.011316240765154362}},"type":"UNKNOWN","parent_frame":""}
  }'

  # 2.5
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_CLOSURE",
    "target": {
      "type": "SE3",
      "left": {'position': {'x': 1.1, 'y': 0.2, 'z': 1.13}, 'orientation': {'x': -0.5, 'y': 0.5, 'z': -0.5, 'w': 0.5}},
      "right":{'position': {'x': 1.1, 'y': -0.2, 'z': 1.13}, 'orientation': {'x': -0.5, 'y': 0.5, 'z': -0.5, 'w': 0.5}},
    },
    "reference" :{
      "joint_position": [-0.705114, 0.766697, -0.206043, -1.71393, -0.204488, 0.903486, -0.60327, 0.707658, 0.676087, 0.130518, -1.78968, 0.10254, -1.13168, 0.710919] 
    },
    "obj_info":{
      "name":"grab",
      "pose":{
        'position': {'x': 1.1, 'y': 0.2, 'z': 1.13}, 
        'orientation': {'x': -0.5, 'y': 0.5, 'z': -0.5, 'w': 0.5}
      },
      "type":"UNKNOWN",
      "parent_frame":""
    }
  }'

)

function call() {
  # 获取对应的参数组
  group_number=$1
  if [[ $group_number -lt 1 || $group_number -gt ${#groups[@]} ]]; then
    echo "Invalid group number. Please provide a number between 1 and ${#groups[@]}"
    exit 1
  fi

  # 选择对应的JSON数据
  data=${groups[$((group_number - 1))]}

  # 执行curl请求
  curl -i \
    -H 'content-type:application/json' \
    -X POST 'http://127.0.0.1:56322/rpc/aimdk.protocol.McMotionService/PlanningMove' \
    -d "$data"
  echo -e "\n"
}

if [[ "$1" == "all" || "$1" == "ALL" ]]; then
  for ((i = 1; i <= ${#groups[@]}; i++)); do
    call $i
    sleep 0.1
  done
else
  call $1
fi
