#!/bin/bash

# 设置运控的action
# ./a2_SetAction.sh action_name

# 定义 IP 地址变量
IP_ADDRESS="127.0.0.1:59001"
# 定义完整的 URL 字符串
URL="http://$IP_ADDRESS/rpc/aimdk.protocol.RemoteControlService/SetAction"
if [ $# -eq 0 ]; then
    echo "arg error, need action_id, ./a2wPlayerMotion.sh action_id, example: "
    echo ./a2_SetAction.sh PASSIVE_DEFAULT
    exit 0
fi

# 获取当前时间戳
timestamp_seconds=$(date +%s)
timestamp_nanos=$(date +%N)
ms_since_epoch=$((timestamp_seconds * 1000 + timestamp_nanos / 1000000))

# 获取第一个参数
DO_ID=$1
# 构造 JSON 数据字符串
DATA="{\"header\":{"timestamp":{\"seconds\":\"$timestamp_seconds\",\"nanos\":\"$timestamp_nanos\",\"msSinceEpoch\":\"$ms_since_epoch\"}},\"command\":{"action": \"McAction_USE_EXT_CMD\", "ext_action": \"$DO_ID\"}}"

echo $DATA

# 使用 curl 发送 POST 请求
curl -i \
    -H 'content-type:application/json' \
    -H 'timeout: 60000' \
    -X POST "$URL" \
    -d "$DATA"

