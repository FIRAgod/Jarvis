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
    "reference": {
      "joint_position": [-0.008218569229830636, -0.898732865902017, 0.013364052627754806, -1.7212509423562699, -3.1416903220549424, -1.049147597238987, 1.5575419090620746, 0.10419200932783146, -0.8550660846603833, -0.16723107479199525, -1.723683004962783, -3.150217579826487, 1.0016340686481107, -1.4358776786689904]
    }
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
    "reference": {
      "joint_position": [-0.501953, -1.51642, 1.41742, -0.562623, -2.98023, 1.51644, -0.0357748, 0.496604, -1.46366, -1.3173, -0.560841, -3.41377, -1.52633, 0.0383312]
    },
    "obj_info":{"name":"grab","pose":{"position":{"x":0.6005,"y":-0.013999999999999985,"z":0.97},"orientation":{"x":0.7071067811865475,"y":0.7071067811865475,"z":0,"w":0}},"type":"UNKNOWN","parent_frame":""}
  }'

  # 4
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_GRAB",
    "obj_info":{"name":"grab","pose":{"position":{"x":0.6005,"y":-0.013999999999999985,"z":0.97},"orientation":{"x":0.7071067811865475,"y":0.7071067811865475,"z":0,"w":0}},"type":"UNKNOWN","parent_frame":""}
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
    "reference": {
      "joint_position": [-0.008218569229830636, -0.898732865902017, 0.013364052627754806, -1.7212509423562699, -3.1416903220549424, -1.049147597238987, 1.5575419090620746, 0.10419200932783146, -0.8550660846603833, -0.16723107479199525, -1.723683004962783, -3.150217579826487, 1.0016340686481107, -1.4358776786689904]
    },
    "obj_info":{"name":"grab","pose":{"position":{"x":0.8005,"y":-0.013999999999999985,"z":1.1775},"orientation":{"x":0.5,"y":0.5,"z":0.5,"w":0.5}},"type":"UNKNOWN","parent_frame":""}
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
