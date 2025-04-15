#!/bin/bash

service="McBaseService"
func="GetWorkMode"

# 
curl -i \
  -H 'content-type:application/json' \
  -X POST "http://127.0.0.1:56322/rpc/aimdk.protocol.$service/$func" \
  -d "{}"

