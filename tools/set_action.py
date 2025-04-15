#!/usr/bin/env python3

import argparse
from motion_control_service import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser("set motion control action")
    MotionControlService.add_arguments(parser)
    args = parser.parse_args()

    MotionControlService(args).select_action()
