      
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
    "group": "McPlanningGroup_DUAL_ARM_WAIST_WHEEL",
    "mode": "McPlanningMode_DEFAULT",
    "target": {
      "type": "SE3",
      "left": {"position":{"x":1.8005,"y":0.216,"z":1.1775},"orientation":{"x":0.5,"y":-0.5,"z":0.5,"w":-0.5}},
      "right":{"position":{"x":1.8005,"y":-0.244,"z":1.1775},"orientation":{"x":-0.5,"y":0.5,"z":-0.5,"w":0.5}},
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

    
