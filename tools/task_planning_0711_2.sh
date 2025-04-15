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
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_DEFAULT",
    "target": {
      "type": "SE3",
      "left": {"position":{"x":0.8005,"y":0.21600000000000003,"z":1.1775},"orientation":{"x":0.5,"y":-0.5,"z":0.5,"w":-0.5}},
      "right":{"position":{"x":0.8005,"y":-0.244,"z":1.1775},"orientation":{"x":-0.5,"y":0.5,"z":-0.5,"w":0.5}},
    },
  }'

  # 2
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_GRAB",
    "obj_info":{"name":"grab","pose":{"position":{"x":0.8005,"y":-0.013999999999999985,"z":1.1775},"orientation":{"x":0.5,"y":0.5,"z":0.5,"w":0.5}},"type":"UNKNOWN","parent_frame":""}
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
    "obj_info":{"name":"grab","pose":{"position":{"x":1.0005,"y":-0.013999999999999985,"z":1.1775},"orientation":{"x":0.5,"y":0.5,"z":0.5,"w":0.5}},"type":"UNKNOWN","parent_frame":""}
  }'
# 4
'{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_GRAB",
    "obj_info":{"name":"grab","pose":{"position":{"x":1.0005,"y":-0.013999999999999985,"z":1.1775},"orientation":{"x":0.5,"y":0.5,"z":0.5,"w":0.5}},"type":"UNKNOWN","parent_frame":""}
  }'
# 5
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_CLOSURE",
    "target": {
      "type": "SE3",
      "left": {"position":{"x":0.611721,"y":0.212367,"z":1.02752},"orientation":{"x": 0.703405,"y":0.710737,"z":0.00512373,"w":-0.0069008}},
      "right":{"position":{"x":0.613836,"y":-0.233753,"z":1.01955},"orientation":{"x":-0.705596,"y":0.708462,"z":0.0107509,"w":0.00999545}},
    },
    "obj_info":{"name":"grab","pose":{"position":{"x":0.8005,"y":-0.013999999999999985,"z":1.1775},"orientation":{"x":0.5,"y":0.5,"z":0.5,"w":0.5}},"type":"UNKNOWN","parent_frame":""}
  }'
# 6
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_GRAB",
    "obj_info":{"name":"grab","pose":{"position":{"x":0.8005,"y":-0.013999999999999985,"z":1.1775},"orientation":{"x":0.5,"y":0.5,"z":0.5,"w":0.5}},"type":"UNKNOWN","parent_frame":""}
  }'
  
  # 7
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_CLOSURE",
    "target": {
      "type": "SE3",
      "left": {"position":{"x":0.611721,"y":0.212367,"z":1.02752},"orientation":{"x": 0.703405,"y":0.710737,"z":0.00512373,"w":-0.0069008}},
      "right":{"position":{"x":0.613836,"y":-0.233753,"z":1.01955},"orientation":{"x":-0.705596,"y":0.708462,"z":0.0107509,"w":0.00999545}},
    },
    "obj_info":{"name":"grab","pose":{"position":{"x":0.6005,"y":-0.013999999999999985,"z":0.97},"orientation":{"x":0.7071067811865475,"y":0.7071067811865475,"z":0,"w":0}},"type":"UNKNOWN","parent_frame":""}
  }'


  # 8
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_GRAB",
    "obj_info":{"name":"grab","pose":{"position":{"x":0.6005,"y":-0.013999999999999985,"z":0.97},"orientation":{"x":0.7071067811865475,"y":0.7071067811865475,"z":0,"w":0}},"type":"UNKNOWN","parent_frame":""}
  }'

  # 9
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_CLOSURE",
    "target": {
      "type": "SE3",
      "left": {"position":{"x":0.611721,"y":0.212367,"z":1.02752},"orientation":{"x": 0.703405,"y":0.710737,"z":0.00512373,"w":-0.0069008}},
      "right":{"position":{"x":0.613836,"y":-0.233753,"z":1.01955},"orientation":{"x":-0.705596,"y":0.708462,"z":0.0107509,"w":0.00999545}},
    },
    "obj_info":{"name":"grab","pose":{"position":{"x": 0.4005,"y":-0.013999999999999985,"z":0.97},"orientation":{"x":0.7071067811865475,"y":0.7071067811865475,"z":0,"w":0}},"type":"UNKNOWN","parent_frame":""}
  }'

  # 10
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_GRAB",
    "obj_info":{"name":"grab","pose":{"position":{"x": 0.4005,"y":-0.013999999999999985,"z":0.97},"orientation":{"x":0.7071067811865475,"y":0.7071067811865475,"z":0,"w":0}},"type":"UNKNOWN","parent_frame":""}
  }'

  # 11
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_CLOSURE",
    "target": {
      "type": "SE3",
      "left": {"position":{"x":0.611721,"y":0.212367,"z":1.02752},"orientation":{"x": 0.703405,"y":0.710737,"z":0.00512373,"w":-0.0069008}},
      "right":{"position":{"x":0.613836,"y":-0.233753,"z":1.01955},"orientation":{"x":-0.705596,"y":0.708462,"z":0.0107509,"w":0.00999545}},
    },
    "obj_info":{"name":"grab","pose":{"position":{"x": 0.6005,"y":-0.013999999999999985,"z":0.97},"orientation":{"x":0.7071067811865475,"y":0.7071067811865475,"z":0,"w":0}},"type":"UNKNOWN","parent_frame":""}
  }'
   # 12
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_GRAB",
    "obj_info":{"name":"grab","pose":{"position":{"x":0.6005,"y":-0.013999999999999985,"z":0.97},"orientation":{"x":0.7071067811865475,"y":0.7071067811865475,"z":0,"w":0}},"type":"UNKNOWN","parent_frame":""}
  }'

  # 13
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_CLOSURE",
    "target": {
      "type": "SE3",
      "left": {"position":{"x":0.611721,"y":0.212367,"z":1.02752},"orientation":{"x": 0.703405,"y":0.710737,"z":0.00512373,"w":-0.0069008}},
      "right":{"position":{"x":0.613836,"y":-0.233753,"z":1.01955},"orientation":{"x":-0.705596,"y":0.708462,"z":0.0107509,"w":0.00999545}},
    },
    "obj_info":{"name":"grab","pose":{"position":{"x": 0.4005,"y":-0.013999999999999985,"z":0.97},"orientation":{"x":0.7071067811865475,"y":0.7071067811865475,"z":0,"w":0}},"type":"UNKNOWN","parent_frame":""}
  }'

  # 14
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_CLOSURE",
    "target": {
      "type": "EE",
      "left": {"position":{"x":0.121426,"y":1.1927,"z":2.16747},"orientation":{"x":0.485031,"y":-0.484126,"z":0.515441,"w":0.514479}},
      "right": {"position":{"x":0.121516,"y":-1.1927,"z":2.16746},"orientation":{"x":0.514331,"y":0.515332,"z":-0.484243,"w":0.485186}}
    }
  }'

  # '{
  #   "group": "McPlanningGroup_DUAL_ARM",
  #   "mode": "McPlanningMode_CLOSURE",
  #   "target": {
  #     "type": "SE3",
  #     "left": {"position":{"x":0.611721,"y":0.212367,"z":1.02752},"orientation":{"x": 0.703405,"y":0.710737,"z":0.00512373,"w":-0.0069008}},
  #     "right":{"position":{"x":0.613836,"y":-0.233753,"z":1.01955},"orientation":{"x":-0.705596,"y":0.708462,"z":0.0107509,"w":0.00999545}},
  #   },
  #   "reference": {
  #     "joint_position": [-0.501953, -1.51642, 1.41742, -0.562623, -2.98023, 1.51644, -0.0357748, 0.496604, -1.46366, -1.3173, -0.560841, -3.41377, -1.52633, 0.0383312]
  #   },
  #   "obj_info":{"name":"grab","pose":{"position":{"x": 0.4005,"y":-0.013999999999999985,"z":0.97},"orientation":{"x":0.7071067811865475,"y":0.7071067811865475,"z":0,"w":0}},"type":"UNKNOWN","parent_frame":""}
  # }'
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
