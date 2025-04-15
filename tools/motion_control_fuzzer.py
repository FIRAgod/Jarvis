#!/usr/bin/env python3

import sys
import time
import json
import inspect
import argparse
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Tuple, Optional, Any

# query delay generator
def query_generator(max_query_time, min_interval, initial_interval, decay_factor=0.5):
    start_time = time.time()
    interval = initial_interval
    while True:
        elapsed_time = time.time() - start_time
        time_remaining = max_query_time - elapsed_time

        if time_remaining <= 0:
            break

        actual_interval = min(max(interval, min_interval), time_remaining)
        time.sleep(actual_interval)

        interval *= decay_factor

        yield

class MotionControlFuzzer(ABC):
    @staticmethod
    def add_arguments(parser):
        check_min_value = lambda value, min_val: (
            float(value) if float(value) >= min_val else argparse.ArgumentTypeError(f"Value must be at least {min_val}")
        )
        check_bounded_value = lambda value, min_val, max_val: (
            float(value) if min_val <= float(value) <= max_val else argparse.ArgumentTypeError(f"Value must be between {min_val} and {max_val}")
        )
        check_integral = lambda value: (
            int(value) if int(value) >= 1 else argparse.ArgumentTypeError("Integral value must be greater than or equal to 1")
        )

        # loop_interval: default is 10, min is 3, float
        parser.add_argument(
            "--loop-interval",
            type=lambda x: check_min_value(x, 3),
            default=10.0,
            help="Loop interval (seconds), minimum is 3, default is 10.",
        )

        # query_interval: default is 1, min is 0.1, max is loop_interval, float
        parser.add_argument(
            "--query-interval",
            type=lambda x: check_bounded_value(
                x, 0.1, 10.0
            ),  # 10.0 is loop_interval default
            default=1.5,
            help="Query interval (seconds), must be between 0.1 and loop_interval, default is 1.5.",
        )

        parser.add_argument(
            "--estimated-duration",
            type=lambda x: check_bounded_value(
                x, 1.0, 60.0
            ),
            default=5.0,
            help="Estimated duration (seconds), must be between 1 and 60, default is 3.",
        )

        # max_tasks: default is None, integral number
        parser.add_argument(
            "--max-tasks",
            type=lambda x: int(x) if x is not None else None,
            default=None,
            help="Maximum number of tasks, default is None.",
        )

        # fail_block: default is False, boolean
        parser.add_argument(
            "--fail-block",
            action="store_true",
            help="Block the program if a task fails",
        )

        # running block timeout: default is 30, min is 0, float
        parser.add_argument(
            "--running-timeout",
            type=lambda x: check_min_value(x, 30.0),
            default=30.0,
            help="Block the program if a task fails",
        )

    def __init__(self, args):
        if args.query_interval > args.loop_interval:
            raise ValueError(
                "query_interval must be less than or equal to loop_interval.")

        self.log_messages = []
        self.loop_interval = args.loop_interval
        self.query_interval = args.query_interval
        self.estimated_duration = args.estimated_duration
        self.max_tasks = args.max_tasks
        self.recent_logs = 2
        self.task_status = {
            "SUCCESS": set(),
            "FAILURE": set(),
            "ABORTED": set(),
            "TIMEOUT": set(),
            "INVALID": set(),
            "CREATED": set(),
            "RUNNING": set(),
            "PENDING": set(),
            "NOT_READY": set(),
            "UNKNOWN": set(),
            "IN_MANUAL": set(),
        }
        self.finished_status = set(
            ["SUCCESS", "FAILURE", "ABORTED", "TIMEOUT", "INVALID"]
        )
        self.running_status = set(["CREATED", "RUNNING", "PENDING"])
        self.hidden_status = set(
            ["NOT_READY", "UNKNOWN", "IN_MANUAL", "ABORTED", "INVALID"]
        )
        self.current_id = 0
        self.fail_block = args.fail_block
        self.running_timeout = args.running_timeout

    @abstractmethod
    def submit_task(self) -> Tuple[Any, Optional[str]]:
        pass

    @abstractmethod
    def query_status(self, task_id: Any) -> Optional[str]:
        pass

    def log(self, message):
        self.log_messages.append(
            datetime.now().strftime("%H:%M:%S.%f")[:-3] + " " + message
        )
        self.log_messages = self.log_messages[-self.recent_logs :]

    def display(self):
        # Move cursor to top left without clearing screen
        print("\033[?25l\033[H", end="")

        lines = []

        # Add progress bar to the output
        finished_progress = (
            sum(
                [
                    len(tasks) if state in self.finished_status else 0
                    for state, tasks in self.task_status.items()
                ]
            )
            / self.current_id
        )
        if self.max_tasks is not None:
            progress = self.current_id / self.max_tasks
            lines.append(
                f"Current: {self.current_id} Progress: {progress:.2%} Finished: {finished_progress:.2%}\033[K"
            )
            lines.append("\033[K")
        else:
            lines.append(
                f"Current: {self.current_id} Finished: {finished_progress:.2%}\033[K"
            )
            lines.append("\033[K")

        # Add the state counts table to the output
        names = []
        counts = []
        for state in self.task_status.keys():
            if state in self.hidden_status:
                continue
            names.append(state)
            counts.append(len(self.task_status[state]))

        max_len = max(len(name) for name in names)
        state_line = "+".join([f"{'-' * (max_len + 2)}" for _ in names]) + "\033[K"
        header_line = "| " + " | ".join([f"{name:<{max_len}}" for name in names]) + " |\033[K"
        count_line = (
            "| " + " | ".join([f"{count:^{max_len}}" for count in counts]) + " |\033[K"
        )
        lines.extend(
            [
                f"+{state_line}+\033[K",
                header_line,
                f"+{state_line}+\033[K",
                count_line,
                f"+{state_line}+\033[K",
                "\033[K",
            ]
        )

        # Add the logs to the output
        log_to_show = self.log_messages[-self.recent_logs :]
        if len(log_to_show) > 0:
            log_to_show[0] = "\x1b[0J" + log_to_show[0]

        lines.extend(log_to_show)

        # Print everything at once
        print("\n".join(lines))

    def run(self):
        try:
            task_number = 0
            while self.max_tasks is None or task_number < self.max_tasks:
                task_number += 1
                start_time = time.time()
                self.current_id = task_number
                task_id, task_status = self.submit_task()
                if task_id == 0:
                    elasped_time = time.time() - start_time
                    if self.loop_interval > elasped_time:
                        time.sleep(self.loop_interval - elasped_time)
                    continue

                if task_status is not None:
                    self.update_task_status(task_id, task_status)

                task_completed = False
                for _ in query_generator(self.loop_interval, self.query_interval, self.estimated_duration, 0.75):
                    # # If not blocked
                    # if self.fail_block is not True and time.time() - start_time > self.loop_interval:
                    #     break
                    status = self.query_status(task_id)
                    if status is None:
                        continue
                    self.update_task_status(task_id, status)
                    self.display()

                    if status in self.finished_status:
                        break

                    # Deal with block items
                    if self.running_timeout >= 0.0 and not task_completed and time.time() - start_time > self.running_timeout:
                        ret = input(f"Task {task_id} timed out after {self.running_timeout} seconds, input anything to CONTINUE...\033[?25h")
                    if self.fail_block and task_completed and status != "SUCCESS":
                        ret = input(f"Task {task_id} failed with {status}, input anything to CONTINUE...\033[?25h")

                # Ensure each task starts with the proper interval between submissions
                elasped_time = time.time() - start_time
                if self.loop_interval > elasped_time:
                    try_anothers = int(self.loop_interval - elasped_time) * 10
                    if try_anothers > 0:
                        task_ids = [
                            taskid
                            for key in self.running_status
                            if key in self.task_status
                            for taskid in self.task_status[key]
                        ]
                        for i, task_id in enumerate(task_ids):
                            if i < try_anothers:
                                status = self.query_status(task_id)
                                self.update_task_status(task_id, status)
                                self.display()
                            else:
                                self.log(f"Skipping {len(task_ids) - i} tasks")
                                break

                    elasped_time = time.time() - start_time
                    if self.loop_interval > elasped_time:
                        time.sleep(self.loop_interval - elasped_time)
        except KeyboardInterrupt:
            print("\nGracefully shutting down...")
        except Exception as e:
            self.log(f"Exception: {e}")
        finally:
            sys.stdout.write('\033[?25h')
            sys.stdout.flush()

    def update_task_status(self, task_id, new_status):
        """Update the count of each task state by ensuring each task ID is only counted once per state."""
        # Remove task_id from all other states if present
        for state, tasks in self.task_status.items():
            if task_id in tasks:
                tasks.discard(task_id)

        if state in self.hidden_status:
            self.hidden_status.remove(state)

        # Add task_id to the new state set
        if new_status in self.task_status:
            self.task_status[new_status].add(task_id)
        else:
            self.log(f"Unknown status: {task_id} - {new_status}")

class MotionControlFuzzer_Menu(MotionControlFuzzer):
    def __init__(self, service, args, choice = None):
        super().__init__(args)
        self.service = service
        self.supported_methods = [
            name[4:-8] for name, method in inspect.getmembers(self.service, predicate=inspect.ismethod)
            if name.startswith("gen_") and name.endswith("_request") and hasattr(self.service, name[4:-8])
        ]
        try:
            if isinstance(choice, str):
                choice = self.supported_methods.index(choice)
                self.method = self.supported_methods[choice]
                self.req_method = getattr(self.service, self.method)
                self.gen_method = getattr(self.service, "gen_" + self.method + "_request")
            elif isinstance(choice, int) and 0 <= choice < len(self.supported_methods):
                self.method = self.supported_methods[choice]
                self.req_method = getattr(self.service, self.method)
                self.gen_method = getattr(self.service, "gen_" + self.method + "_request")
            else:
                self.method = None
                self.req_method = None
                self.gen_method = None
        except ValueError:
            self.method = None
            self.req_method = None
            self.gen_method = None
            self.log(f"Invalid choice: {choice}")

    def select_method(self):
        print("Available tasks:")
        for idx, task_name in enumerate(self.supported_methods, 1):
            print(f"{idx}. {task_name}")

        try:
            choice = int(input("Enter the task number to execute: \033[?25h")) - 1
            if isinstance(choice, int) and 0 <= choice < len(self.supported_methods):
                self.method = self.supported_methods[choice]
                self.req_method = getattr(self.service, self.method)
                self.gen_method = getattr(self.service, "gen_" + self.method + "_request")
            else:
                self.method = None
                self.req_method = None
                self.gen_method = None
        except (ValueError, IndexError):
            raise RuntimeError("Invalid choice. Exiting.")

    def submit_task(self):
        if self.method is None:
            self.select_method()

        gen_method = self.gen_method
        req_method = self.req_method

        try:
            task_id = 0
            tasks_status = None
            generated_request = gen_method()
            self.log(json.dumps(generated_request, separators=(',', ':')))
            response = req_method(generated_request)
            if response.status_code == 200:
                task_id = response.json()["task_id"]
                tasks_status = response.json()["state"].replace("CommonState_", "")

            return task_id, tasks_status
        except Exception as e:
            self.log(str(e))
            return 0, None

    def query_status(self, task_id):
        try:
            return self.service.get_task_status(task_id)
        except Exception as e:
            self.log(str(e))
            return None
