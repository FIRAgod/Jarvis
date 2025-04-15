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
    "target": {
      "left": {"position":{"x":0.598496,"y":0.215795,"z":0.969917},"orientation":{"x": -0.706945,"y":0.707267,"z":0.000749088,"w":-0.000752005}},
      "right":{"position":{"x":0.598437,"y":-0.242747,"z":0.970099},"orientation":{"x":0.707186,"y":-0.707026,"z":-0.000816345,"w":0.000903315}},
    }
  }'

  # 2
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "target": {
      "left": {"position":{"x":0.448143,"y":0.215858,"z":0.799669},"orientation":{"x": 0.707254,"y":-0.706959,"z":-0.00077078,"w":0.000763329}},
      "right":{"position":{"x":0.448154,"y":-0.243421,"z":0.799829},"orientation":{"x":-0.706976,"y":0.707237,"z":0.000867492,"w":-0.000912744}},
    }
  }'

  # 3
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "target": {
      "left": {"position":{"x":0.598496,"y":0.215795,"z":1.269917},"orientation":{"x": -0.706945,"y":0.707267,"z":0.000749088,"w":-0.000752005}},
      "right":{"position":{"x":0.598437,"y":-0.242747,"z":1.270099},"orientation":{"x":0.707186,"y":-0.707026,"z":-0.000816345,"w":0.000903315}},
    }
  }'

  # 4
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "target": {
      "left": {"position":{"x":0.8005,"y":0.216,"z":1.1775},"orientation":{"x":0.5,"y":-0.5,"z":0.5,"w":-0.5}},
      "right":{"position":{"x":0.8005,"y":-0.244,"z":1.1775},"orientation":{"x":-0.5,"y":0.5,"z":-0.5,"w":0.5}},
    }
  }'

  # 5
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "target": {
      "left": {"position":{"x":0.8005,"y":0.116,"z":1.1775},"orientation":{"x":0.5,"y":-0.5,"z":0.5,"w":-0.5}},
      "right":{"position":{"x":0.8005,"y":-0.344,"z":1.1775},"orientation":{"x":-0.5,"y":0.5,"z":-0.5,"w":0.5}},
    }
  }'

  # 6
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "target": {
      "left": {"position":{"x":0.8005,"y":0.316,"z":1.1775},"orientation":{"x":0.5,"y":-0.5,"z":0.5,"w":-0.5}},
      "right":{"position":{"x":0.8005,"y":-0.144,"z":1.1775},"orientation":{"x":-0.5,"y":0.5,"z":-0.5,"w":0.5}},
    }
  }'

  # 7
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "target": {
      "left": {"position":{"x":0.8005,"y":0.216,"z":1.1775},"orientation":{"x":0.5,"y":-0.5,"z":0.5,"w":-0.5}},
      "right":{"position":{"x":0.8005,"y":-0.244,"z":1.1775},"orientation":{"x":-0.5,"y":0.5,"z":-0.5,"w":0.5}},
    }
  }'

  # 8
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "target": {
      "left": {"position":{"x":0.8005,"y":0.216,"z":1.0775},"orientation":{"x":0.5,"y":-0.5,"z":0.5,"w":-0.5}},
      "right":{"position":{"x":0.8005,"y":-0.244,"z":1.0775},"orientation":{"x":-0.5,"y":0.5,"z":-0.5,"w":0.5}},
    }
  }'

  # 9
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "target": {
      "left": {"position":{"x":0.8005,"y":0.216,"z":1.2775},"orientation":{"x":0.5,"y":-0.5,"z":0.5,"w":-0.5}},
      "right":{"position":{"x":0.8005,"y":-0.244,"z":1.2775},"orientation":{"x":-0.5,"y":0.5,"z":-0.5,"w":0.5}},
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
    -X POST 'http://127.0.0.1:56322/rpc/aimdk.protocol.McMotionService/LinearMove' \
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
