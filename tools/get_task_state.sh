#!/bin/bash

task_id=$1

service="McDataService"
func="GetTaskState"

# service="McMotionService"
# func="GetTempPlanningResult"

# 
curl -i \
  -H 'content-type:application/json' \
  -X POST "http://127.0.0.1:56322/rpc/aimdk.protocol.$service/$func" \
  -d "{"task_id":"$task_id"}"

