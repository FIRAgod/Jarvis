#!/bin/bash
# send_motion_id.sh

# 定义 IP 地址变量
IP_ADDRESS="127.0.0.1:56444"    #目标机器人的地址和端口，端口不用改，主要是ip地址
# 定义完整的 URL 字符串
URL="http://$IP_ADDRESS/rpc/aimdk.protocol.MotionCommandService/SendMotionCommand"

if [ $# -eq 0 ]; then
    echo "arg error, need file absolute path"
    exit 0
fi

# 获取第一个参数作为 motion_id
# 例如：/agibot/data/var/rc/motion_player/default/跳舞/跳舞
MC_ID="$1"

# 判断参数是否为“停止动作”或“暂停播放器”
if [ "$MC_ID" == "停止动作" ]; then
    # 如果是“停止动作”，则 motion_id 为空，cmd_reset 设为 true
    DATA='{
      "motion_id": "",
      "duration_ms": 10000,
      "cmd_end": true,
      "cmd_pause": false,
      "cmd_reset": true
    }'
elif [ "$MC_ID" == "暂停播放器" ]; then
    # 如果是“暂停播放器”，则 motion_id 保持不变，cmd_pause 设为 true
    DATA='{
      "motion_id": "",
      "duration_ms": 10000,
      "cmd_end": true,
      "cmd_pause": true,
      "cmd_reset": false
    }'
elif [ "$MC_ID" == "下一个动作" ]; then
    # 如果是“下一个动作”，则 播放list中的下一个动作
    DATA='{
      "motion_id": "next_motion",
      "duration_ms": 10000,
      "cmd_end": true,
      "cmd_pause": false,
      "cmd_reset": false
    }'
else
    # 如果不是“停止动作”或“暂停播放器”，保持原有逻辑
    DATA='{
      "motion_id": "'"$MC_ID"'",
      "duration_ms": 10000,
      "cmd_end": true,
      "cmd_pause": false,
      "cmd_reset": false
    }'
fi

# 使用 curl 发送 POST 请求
curl -i \
    -H 'content-type:application/json' \
    -H 'timeout: 60000' \
    -X POST "$URL" \
    -d "$DATA"

# 打印发送的数据
echo "$DATA"
