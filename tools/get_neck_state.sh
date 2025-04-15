#!/bin/bash

service="McDataService"
func="GetNeckState"

#
curl -i \
  -H 'content-type:application/json' \
  -X POST "http://127.0.0.1:56322/rpc/aimdk.protocol.$service/$func" \
  -d "{}"

curl -i \
-H 'content-type:application/json' \
-H 'timeout: 60000' \
-X POST 'http://127.0.0.1:56421/rpc/aimdk.protocol.HalHandService/SetHandCommand' \
-d '{"data":{"left":{"agi_hand":{"finger":{"pos":{"thumb_pos_0":0, "thumb_pos_1":0,"index_pos":0,"middle_pos":0,"ring_pos":0,"pinky_pos":0},"toq":{"thumb_toq_0":0, "thumb_toq_1":0,"index_toq":0,"middle_toq":0,"ring_toq":0,"pinky_toq":0}}}}, "right":{"agi_hand":{"finger":{"pos":{"thumb_pos_0":0, "thumb_pos_1":0,"index_pos":0,"middle_pos":0,"ring_pos":0,"pinky_pos":0},"toq":{"thumb_toq_0":0, "thumb_toq_1":0,"index_toq":0,"middle_toq":0,"ring_toq":0,"pinky_toq":0}}}}}}'
