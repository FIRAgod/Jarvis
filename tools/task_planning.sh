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
      "left": {"position":{"x":0.6455504298210144,"y":0.24099871516227722,"z":1.0444597125053405}, "orientation":{"x":0.017005208313945547,"y":0.74622726226388925,"z":-0.019005805291182242,"w":0.66520258215792694}},
      "right":{"position":{"x":0.53719568252563477,"y":-0.33073535561561584,"z":1.217516701221466},"orientation":{"x":0.706942388906146,"y":-0.28797655198937122,"z":0.23698070460962384,"w":-0.60095100458748762}},
    },
    "reference": {
      "joint_position": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    }
  }'

  # 2
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_DEFAULT",
    "target": {
      "type": "SE3",
      "left": {"position":{"x":0.602869,"y":0.214161,"z":1.17483},"orientation":{"x":0.496816,"y":0.501868,"z":0.49808,"w":0.503209}},
      "right":{"position":{"x":0.601528,"y":-0.232955,"z":1.17512},"orientation":{"x":-0.497367,"y":0.503137,"z":-0.496875,"w":0.502588}},
    },
    "reference": {
      "joint_position": [-0.008218569229830636, -0.898732865902017, 0.013364052627754806, -1.7212509423562699, -3.1416903220549424, -1.049147597238987, 1.5575419090620746, 0.10419200932783146, -0.8550660846603833, -0.16723107479199525, -1.723683004962783, -3.150217579826487, 1.0016340686481107, -1.4358776786689904]
    }
  }'

  # 3
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_GRAB",
    "obj_info":{"name":"grab","pose":{"position":{"x":0.602093,"y":-0.00939718,"z":1.17589},"orientation":{"x":-0.00038796,"y":0.706711,"z":0.000847439,"w":0.707501}},"type":"UNKNOWN","parent_frame":""}
  }'

  # 4
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_CLOSURE",
    "target": {
      "type": "SE3",
      "left": {"position":{"x":0.603427,"y":0.21234,"z":1.17425},"orientation":{"x":0.499617,"y":0.50109,"z":0.495841,"w":0.503421}},
      "right":{"position":{"x":0.600957,"y":-0.233046,"z":1.17741},"orientation":{"x":-0.496798,"y":0.503183,"z":-0.497264,"w":0.50272}},
    },
    "reference": {
      "joint_position": [-0.6489297668125308, -1.546983293661404, 1.571992440295108, -1.7191082982461126, -3.1194765261684805, -1.070551175038024, -0.00017898503412130647, 0.6546985959169933, -1.450562350248012, -1.525254249225766, -1.7252539741321231, -3.220632234982017, 1.0650928784156273, -0.06706219494959109]
    },
    "obj_info":{"name":"grab","pose":{"position":{"x":0.602193,"y":-0.0103529,"z":1.17583},"orientation":{"x":0.00198302,"y":0.706448,"z":-0.00100059,"w":0.707761}},"type":"UNKNOWN","parent_frame":""}
  }'

  # 5
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_GRAB",
    "obj_info":{"name":"grab","pose":{"position":{"x":0.602636,"y":-0.0103691,"z":1.17049},"orientation":{"x":0.00195546,"y":0.70854,"z":-0.00092043,"w":0.705667}},"type":"UNKNOWN","parent_frame":""}
  }'

  # 6
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_CLOSURE",
    "target": {
      "type": "SE3",
      "left": {"position":{"x":0.461721,"y":0.212367,"z":1.02752},"orientation":{"x": 0.703405,"y":0.710737,"z":0.00512373,"w":-0.0069008}},
      "right":{"position":{"x":0.463836,"y":-0.233753,"z":1.01955},"orientation":{"x":-0.705596,"y":0.708462,"z":0.0107509,"w":0.00999545}},
    },
    "reference": {
      "joint_position": [-0.6489297668125308, -1.546983293661404, 1.571992440295108, -1.7191082982461126, -3.1194765261684805, 0.5, -0.00017898503412130647,0.6546985959169933, -1.450562350248012, -1.525254249225766, -1.7252539741321231, -3.220632234982017, -0.5, -0.06706219494959109]
    },
    "obj_info":{"name":"grab","pose":{"position":{"x":0.462778,"y":-0.010693,"z":1.02353},"orientation":{"x":-0.00154398,"y":0.999934,"z":0.0111849,"w":0.00218042}},"type":"UNKNOWN","parent_frame":""}
  }'

  # 7
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_GRAB",
    "obj_info":{"name":"grab","pose":{"position":{"x":0.462778,"y":-0.010693,"z":1.02353},"orientation":{"x":-0.00154398,"y":0.999934,"z":0.0111849,"w":0.00218042}},"type":"UNKNOWN","parent_frame":""}
  }'

  # 8
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_CLOSURE",
    "target": {
      "type": "SE3",
      "left": {"position":{"x":0.611721,"y":0.212367,"z":1.02752},"orientation":{"x": 0.703405,"y":0.710737,"z":0.00512373,"w":-0.0069008}},
      "right":{"position":{"x":0.613836,"y":-0.233753,"z":1.01955},"orientation":{"x":-0.705596,"y":0.708462,"z":0.0107509,"w":0.00999545}},
    },
    "reference": {
      "joint_position": [-0.523068, -1.46404, 1.15019, -0.560614, -2.70585, 1.5708, -0.148636, 0.50788, -1.42846, -1.17354, -0.557452, -3.5314, -1.55465, 0.0931139]
    },
    "obj_info":{"name":"grab","pose":{"position":{"x":0.612778,"y":-0.010693,"z":1.17353},"orientation":{"x":-0.00154398,"y":0.999934,"z":0.0111849,"w":0.00218042}},"type":"UNKNOWN","parent_frame":""}
  }'
  # 9
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_GRAB",
    "obj_info":{"name":"grab","pose":{"position":{"x":0.612778,"y":-0.010693,"z":1.02353},"orientation":{"x":-0.00154398,"y":0.999934,"z":0.0111849,"w":0.00218042}},"type":"UNKNOWN","parent_frame":""}
  }'

  # 10
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_CLOSURE",
    "target": {
      "type": "SE3",
      "left": {"position":{"x":0.602869,"y":0.214161,"z":1.17483},"orientation":{"x":0.496816,"y":0.501868,"z":0.49808,"w":0.503209}},
      "right":{"position":{"x":0.601528,"y":-0.232955,"z":1.17512},"orientation":{"x":-0.497367,"y":0.503137,"z":-0.496875,"w":0.502588}},
    },
    "reference": {
      "joint_position": [-0.008218569229830636, -0.898732865902017, 0.013364052627754806, -1.7212509423562699, -3.1416903220549424, -1.049147597238987, 1.5575419090620746, 0.10419200932783146, -0.8550660846603833, -0.16723107479199525, -1.723683004962783, -3.150217579826487, 1.0016340686481107, -1.4358776786689904]
    },
    "obj_info":{"name":"grab","pose":{"position":{"x":0.602093,"y":-0.00939718,"z":1.17589},"orientation":{"x":-0.00154398,"y":0.999934,"z":0.0111849,"w":0.00218042}},"type":"UNKNOWN","parent_frame":""}
  }'

  # 11
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_DEFAULT",
    "target": {
      "type": "JOINT",
      "joints": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    "reference": {
      "joint_position": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    }
  }'

  # 12
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_DEFAULT",
    "target": {
      "type": "JOINT",
      "joints": [-0.008218569229830636, -0.898732865902017, 0.013364052627754806, -1.7212509423562699, -3.1416903220549424, -1.049147597238987, 1.5575419090620746, 0.10419200932783146, -0.8550660846603833, -0.16723107479199525, -1.723683004962783, -3.150217579826487, 1.0016340686481107, -1.4358776786689904]
    },
    "reference": {
      "joint_position": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    }
  }'

  # 13
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_CLOSURE",
    "target": {
      "type": "JOINT",
      "joints": [-0.6489297668125308, -1.546983293661404, 1.571992440295108, -1.7191082982461126, -3.1194765261684805, -1.070551175038024, -0.00017898503412130647, 0.6546985959169933, -1.450562350248012, -1.525254249225766, -1.7252539741321231, -3.220632234982017, 1.0650928784156273, -0.06706219494959109]
    },
    "reference": {
      "joint_position": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    }
  }'

  # 14
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_CLOSURE",
    "target": {
      "type": "JOINT",
      "joints": [-0.6489297668125308, -1.546983293661404, 1.571992440295108, -1.7191082982461126, -3.1194765261684805, 0.5, -0.00017898503412130647,0.6546985959169933, -1.450562350248012, -1.525254249225766, -1.7252539741321231, -3.220632234982017, -0.5, -0.06706219494959109]
    },
    "reference": {
      "joint_position": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    }
  }'

  # 15
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_GRAB",
    "obj_info":{"name":"grab","pose":{"position":{"x":0.6005,"y":-0.013999999999999985,"z":1.1775},"orientation":{"x":0.5,"y":0.5,"z":0.5,"w":0.5}},"type":"UNKNOWN","parent_frame":""}
  }'

  # 16
  '{
    "group": "McPlanningGroup_DUAL_ARM",
    "mode": "McPlanningMode_CLOSURE",
    "target": {
      "type": "SE3",
      "left": {"position":{"x":0.6005,"y":0.21600000000000003,"z":1.1775},"orientation":{"x":0.5,"y":0.5,"z":0.5,"w":0.5}},
      "right":{"position":{"x":0.6005,"y":-0.244,"z":1.1775},"orientation":{"x":0.5,"y":0.5,"z":0.5,"w":0.5}},
    },
    "reference": {
      "joint_position": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    "obj_info":{"name":"grab","pose":{"position":{"x":0.5,"y":-0.013999999999999985,"z":1.0775},"orientation":{"x":0.70710678118654746,"y":0.70710678118654746,"z":0.5,"w":0.5}},"type":"UNKNOWN","parent_frame":""}
  }'

  # 17
  '{
    "group": "McPlanningGroup_DUAL_ARM_WAIST",
    "mode": "McPlanningMode_DEFAULT",
    "target": {
      "type": "JOINT",
      "joints": [0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    }
  }'

  # 18
  '{
    "group": "McPlanningGroup_DUAL_ARM_WAIST",
    "mode": "McPlanningMode_DEFAULT",
    "target": {
      "type": "JOINT",
      "joints": [0.1, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    }
  }'

  # 19
  '{
    "group": "McPlanningGroup_HEAD",
    "mode": "McPlanningMode_DEFAULT",
    "target": {
      "type": "JOINT",
      "joints": [0.5]
    }
  }'

  # 20
  '{
    "group": "McPlanningGroup_WAIST_LIFT",
    "mode": "McPlanningMode_DEFAULT",
    "target": {
      "type": "JOINT",
      "joints": [0.2]
    }
  }'
  
  # 21
  '{
    "group": "McPlanningGroup_WAIST_PITCH",
    "mode": "McPlanningMode_DEFAULT",
    "target": {
      "type": "JOINT",
      "joints": [0.3]
    }
  }'

  # 22
  '{
    "group": "McPlanningGroup_DUAL_ARM_WAIST_HEAD",
    "mode": "McPlanningMode_DEFAULT",
    "target": {
      "type": "JOINT",
      "joints": [0.1, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
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
