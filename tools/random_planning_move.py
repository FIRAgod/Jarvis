#!/usr/bin/env python3

import argparse
from motion_control_fuzzer import *
from motion_control_service import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Random planning move fuzzer")

    MotionControlFuzzer.add_arguments(parser)
    MotionControlService.add_arguments(parser)

    args = parser.parse_args()

    try:
        service = MotionControlService(args)
        service.ensure_action("PLANNING_MOVE")
    except Exception as e:
        print("\nGracefully shutting down...")
        exit(0)

    fuzzer = MotionControlFuzzer_Menu(
        service = service,
        choice="planning_move",
        args=args
    )
    fuzzer.run()
