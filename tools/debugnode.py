#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from interactive_markers.interactive_marker_server import InteractiveMarkerServer
from interactive_markers.menu_handler import *
from visualization_msgs.msg import InteractiveMarker, InteractiveMarkerControl, InteractiveMarkerFeedback, Marker
import copy
import time
import json
import requests
import argparse
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Tuple, Optional, Any

host = "127.0.0.1"


def transPose(pose, pose0):
  pose.position.x = pose0[0]
  pose.position.y = pose0[1]
  pose.position.z = pose0[2]
  pose.orientation.w = pose0[3]
  pose.orientation.x = pose0[4]
  pose.orientation.y = pose0[5]
  pose.orientation.z = pose0[6]

class SimpleInteractiveMarker(Node):
  def __init__(self):
    super().__init__('simple_interactive_marker')
    self._server = InteractiveMarkerServer(self, 'simple_marker')

    temp_marker = InteractiveMarker()
    self._left_pose = temp_marker.pose
    left_pose0 = [-0.564582, 0.558626, 0.880146,  -0.277229, 0.831177, 0.392099, -0.280262]  # x, y, z, w, x, y, z
    transPose(self._left_pose, left_pose0)
    self._create_marker(left_pose0, "left",  self._int_left_feedback)

    self._right_pose = temp_marker.pose
    right_pose0 = [-0.391609, -0.1921, 1.40247,  -0.0627926, -0.0150623, 0.395557, 0.916168]
    transPose(self._right_pose, right_pose0)
    self._create_marker(right_pose0, "right",  self._int_right_feedback)

  def _create_marker(self, pose0, name: str = "left",  intcallback=None):
    # 创建一个交互标记
    int_marker = InteractiveMarker()
    int_marker.header.frame_id = "base_link"
    int_marker.name = name
    int_marker.description = "Marker:" + name
    int_marker.pose.position.x = pose0[0]
    int_marker.pose.position.y = pose0[1]
    int_marker.pose.position.z = pose0[2]
    int_marker.pose.orientation.w = pose0[3]
    int_marker.pose.orientation.x = pose0[4]
    int_marker.pose.orientation.y = pose0[5]
    int_marker.pose.orientation.z = pose0[6]
    int_marker.scale = 0.2

    # control
    box_marker = Marker()
    box_marker.type = Marker.CUBE
    box_marker.scale.x = 0.15
    box_marker.scale.y = 0.15
    box_marker.scale.z = 0.15
    box_marker.color.r = 0.0
    box_marker.color.g = 0.5
    box_marker.color.b = 0.5
    box_marker.color.a = 1.0
    box_control = InteractiveMarkerControl()
    box_control.always_visible = True
    box_control.markers.append(box_marker)
    box_control.interaction_mode = InteractiveMarkerControl.MOVE_ROTATE_3D
    int_marker.controls.append(box_control)

    control = InteractiveMarkerControl()
    control.orientation.w = 1.0
    control.orientation.x = 1.0
    control.orientation.y = 0.0
    control.orientation.z = 0.0
    control.name = "rotate_x"
    control.interaction_mode = InteractiveMarkerControl.ROTATE_AXIS
    int_marker.controls.append(copy.deepcopy(control))
    control.name = "move_x"
    control.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
    int_marker.controls.append(copy.deepcopy(control))

    control.orientation.w = 1.0
    control.orientation.x = 0.0
    control.orientation.y = 1.0
    control.orientation.z = 0.0
    control.name = "rotate_y"
    control.interaction_mode = InteractiveMarkerControl.ROTATE_AXIS
    int_marker.controls.append(copy.deepcopy(control))
    control.name = "move_y"
    control.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
    int_marker.controls.append(copy.deepcopy(control))

    control.orientation.w = 1.0
    control.orientation.x = 0.0
    control.orientation.y = 0.0
    control.orientation.z = 1.0
    control.name = "rotate_z"
    control.interaction_mode = InteractiveMarkerControl.ROTATE_AXIS
    int_marker.controls.append(copy.deepcopy(control))
    control.name = "move_z"
    control.interaction_mode = InteractiveMarkerControl.MOVE_AXIS
    int_marker.controls.append(copy.deepcopy(control))

    # menu
    self._server.insert(int_marker)
    self._server.setCallback(int_marker.name, intcallback)

    menu_handler = MenuHandler()
    menu_handler.insert("pubSE3", callback=self._menu_feedback)
    menu_handler.apply(self._server, int_marker.name)
    self._server.applyChanges()

  def _int_left_feedback(self, feedback: InteractiveMarkerFeedback):
    self._left_pose = feedback.pose

  def _int_right_feedback(self, feedback: InteractiveMarkerFeedback):
    self._right_pose = feedback.pose

  def _menu_feedback(self, feedback: InteractiveMarkerFeedback):
    # 打印SE3变换
    print("menu_feedback")

    print( f"left Pose: {self.getPose(self._left_pose)}")
    print( f"right Pose: {self.getPose(self._right_pose)}")
    
    try:
      url = f"http://{host}:56322/rpc/aimdk.protocol.McMotionService/PlanningMove"
      headers = {"Content-Type": "application/json"}

      payload = {}
      payload["header"] = self.create_header()
      payload["group"] = "McPlanningGroup_DUAL_ARM_WAIST"
      payload["target"] = {
        "type": "SE3",
        "left": self.getPose(self._left_pose),
        "right": self.getPose(self._right_pose),
      }
      
      response = requests.post(url, headers=headers, json=payload)
      # self.log(response.text)

      if response.status_code == 200:
        task_id = response.json()["task_id"]
        task_status = response.json()["state"].replace(
            "CommonState_", "")
      return task_id, task_status
    except Exception as e:
      self.log(e)
      return 0, None
    
    
  def create_header(self):
    now = datetime.now()
    header = {
        "timestamp": {
            "seconds": int(now.timestamp()),
            "nanos": now.microsecond * 1000,
            "ms_since_epoch": int(now.timestamp() * 1000),
        },
        "control_source": "ControlSource_SAFE",
    }
    return header
  
  def getPose(self, pose):
    return {"position":{"x":pose.position.x,"y":pose.position.y,"z":pose.position.z},"orientation":{"x":pose.orientation.x,"y":pose.orientation.y,"z":pose.orientation.z,"w":pose.orientation.w}}


def main(args=None):
  rclpy.init(args=args)
  node = SimpleInteractiveMarker()
  try:
    rclpy.spin(node)
  except KeyboardInterrupt:
    pass
  rclpy.shutdown()


if __name__ == '__main__':
  main()
