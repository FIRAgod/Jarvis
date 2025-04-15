#!/bin/bash

# 播放某个动作
# ./a2_PlayerMotion.sh motion_id

# 定义 IP 地址变量
IP_ADDRESS="127.0.0.1:59001"
# 定义完整的 URL 字符串
URL="http://$IP_ADDRESS/rpc/aimdk.protocol.RcMotionPlayerService/PlayerMotion"
if [ $# -eq 0 ]; then
    echo "arg error, need motion_id, ./a2_PlayerMotion.sh motion_id, example: "
    echo ./a2_PlayerMotion.sh 1
    exit 0
fi

# 获取当前时间戳
timestamp_seconds=$(date +%s)
timestamp_nanos=$(date +%N)
ms_since_epoch=$((timestamp_seconds * 1000 + timestamp_nanos / 1000000))

# 获取第一个参数
MODE_ID=$1
# 构造 JSON 数据字符串
DATA="{\"header\":{"timestamp":{\"seconds\":\"$timestamp_seconds\",\"nanos\":\"$timestamp_nanos\",\"msSinceEpoch\":\"$ms_since_epoch\"}},\"motion_id\":\"$MODE_ID\"}"

echo $DATA

# 使用 curl 发送 POST 请求
curl -i \
    -H 'content-type:application/json' \
    -H 'timeout: 60000' \
    -X POST "$URL" \
    -d "$DATA"

