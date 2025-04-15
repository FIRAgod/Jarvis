#!/bin/bash

# 参数校验
if [ -z "$1" ]; then
  echo "Usage: $0 <group_number>"
  exit 1
fi

# 参数组定义
declare -a groups=(
  '{"header":{"timestamp":{"seconds":"1716257041","nanos":437390804,"msSinceEpoch":"1716257041437"}},"group":"McPlanningGroup_DUAL_ARM_WAIST_HEAD", "angles":[0, 0.053, 0, 1.57, -1.57, -3.14, -2.094, 0, -1.047, 0, -1.57, -1.57, 3.14, -2.094, 0, 1.047, 0]}'
  
  '{"header":{"timestamp":{"seconds":"1716257041","nanos":437390804,"msSinceEpoch":"1716257041437"}},"group":"McPlanningGroup_DUAL_ARM","angles":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}'

  '{"header":{"timestamp":{"seconds":"1716257041","nanos":437390804,"msSinceEpoch":"1716257041437"}},"group":"McPlanningGroup_DUAL_ARM","angles":[0, 1.57, 0, -1.57, 0, 0, 0, 0, 1.57, 0, -1.57, 0, 0, 0]}'

  '{"header":{"timestamp":{"seconds":"1716257041","nanos":437390804,"msSinceEpoch":"1716257041437"}},"group":"McPlanningGroup_DUAL_ARM","angles":[-1.57, 1.57, -1.57, -1.57, 1.57, -1.57, 1.57,   1.57, 1.57, 1.57, -1.57, -1.57, 1.57, 1.57]}'

  '{"header":{"timestamp":{"seconds":"1716257041","nanos":437390804,"msSinceEpoch":"1716257041437"}},"group":"McPlanningGroup_DUAL_ARM","angles":[0, 1.57, 0, -1.57, 0, 0, 0, 0, 1.57, 0, -1.57, 0, 0, 0]}'

  '{"header":{"timestamp":{"seconds":"1716257041","nanos":437390804,"msSinceEpoch":"1716257041437"}},"group":"McPlanningGroup_DUAL_ARM","angles":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}'
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
    -X POST 'http://127.0.0.1:56322/rpc/aimdk.protocol.McMotionService/JointMove' \
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
