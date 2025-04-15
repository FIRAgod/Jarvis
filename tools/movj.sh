#!/bin/bash

# 参数校验
if [ -z "$1" ]; then
  echo "Usage: $0 <group_number>"
  exit 1
fi

# 参数组定义
declare -a groups=(
  '{"header":{"timestamp":{"seconds":"1716257041","nanos":437390804,"msSinceEpoch":"1716257041437"}},"group":"McPlanningGroup_DUAL_ARM_WAIST_HEAD","angles":[0.0, 0.053, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}'
  '{"header":{"timestamp":{"seconds":"1716257041","nanos":437390804,"msSinceEpoch":"1716257041437"}},"group":"McPlanningGroup_DUAL_ARM_WAIST_HEAD","angles":[0.1, 0.2, 0.006, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}'
  '{"header":{"timestamp":{"seconds":"1716257041","nanos":437390804,"msSinceEpoch":"1716257041437"}},"group":"McPlanningGroup_DUAL_ARM_WAIST_HEAD","angles":[0.006, 0.053, 0.006, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}'

  '{"header":{"timestamp":{"seconds":"1716257041","nanos":437390804,"msSinceEpoch":"1716257041437"}},"group":"McPlanningGroup_DUAL_ARM_WAIST_HEAD","angles":[0.006, 0.053, 0.006, 0.006, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}'

  '{"header":{"timestamp":{"seconds":"1716257041","nanos":437390804,"msSinceEpoch":"1716257041437"}},"group":"McPlanningGroup_DUAL_ARM_WAIST_HEAD","angles":[0.006, 0.053, 0.006, 0.006, 0.006, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}'

  '{"header":{"timestamp":{"seconds":"1716257041","nanos":437390804,"msSinceEpoch":"1716257041437"}},"group":"McPlanningGroup_DUAL_ARM_WAIST_HEAD","angles":[0.006, 0.0581, 0.006, 0.006, 0.006, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}'

  '{"header":{"timestamp":{"seconds":"1716257041","nanos":437390804,"msSinceEpoch":"1716257041437"}},"group":"McPlanningGroup_DUAL_ARM_WAIST_HEAD","angles":[0.006, 0.0581, 0.006, 0.006, 0.006, 0.006, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}'


  # '{"header":{"timestamp":{"seconds":"1716257041","nanos":437390804,"msSinceEpoch":"1716257041437"}},"group":"McPlanningGroup_DUAL_ARM","angles":[-0.008218569229830636, -0.898732865902017, 0.013364052627754806, -1.7212509423562699, -3.1416903220549424, -1.049147597238987, 1.5575419090620746, 0.10419200932783146, -0.8550660846603833, -0.16723107479199525, -1.723683004962783, -3.150217579826487, 1.0016340686481107, -1.4358776786689904]}'
  # '{"header":{"timestamp":{"seconds":"1716257041","nanos":437390804,"msSinceEpoch":"1716257041437"}},"group":"McPlanningGroup_DUAL_ARM_WAIST","angles":[-0.25, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}'
  # '{"header":{"timestamp":{"seconds":"1716257041","nanos":437390804,"msSinceEpoch":"1716257041437"}},"group":"McPlanningGroup_WAIST_LIFT","angles":[0.25]}'
  # '{"header":{"timestamp":{"seconds":"1716257041","nanos":437390804,"msSinceEpoch":"1716257041437"}},"group":"McPlanningGroup_WAIST_PITCH","angles":[1.0]}'
  # '{"header":{"timestamp":{"seconds":"1716257041","nanos":437390804,"msSinceEpoch":"1716257041437"}},"group":"McPlanningGroup_HEAD","angles":[-1.0]}'
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

loop_count = 100
if [[ -n "$2" ]]; then
  loop_count=$2
fi

if [[ "$1" == "all" || "$1" == "ALL" ]]; then
  for ((j = 1; j <= loop_count; j++)); do
    echo "第 $j 次循环"
    for ((i = 1; i <= ${#groups[@]}; i++)); do
      call $i
      sleep 0.1
    done
  done
else
  call $1
fi
