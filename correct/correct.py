# import os
# import time
# import subprocess

# def run_bash_script(script_path, change_dir=False, directory=None, command_args=None):
#     try:
#         if change_dir and directory:
#             print(f"切换到目录：{directory}")
#             os.chdir(directory)

#         # 构造命令：如果有参数则追加，否则不传
#         command = ['bash', script_path]
#         if command_args:
#             command += command_args
#         print(f"执行命令：{command}")

#         result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         print(f"执行成功，输出：\n{result.stdout.decode()}")
#     except subprocess.CalledProcessError as e:
#         print(f"执行命令时发生错误：{command}")
#         print("错误信息：\n", e.stderr.decode())

# def run_python_script(script_path, change_dir=False, directory=None, command_args=None):
#     try:
#         if change_dir and directory:
#             print(f"切换到目录：{directory}")
#             os.chdir(directory)

#         # 构造命令：如果有参数则追加，否则不传
#         command = ['python3', script_path]
#         if command_args:
#             command += command_args
#         print(f"执行命令：{command}")

#         result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#         print(f"执行成功，输出：\n{result.stdout.decode()}")
#     except subprocess.CalledProcessError as e:
#         print(f"执行 Python 脚本时发生错误：{command}")
#         print("错误信息：\n", e.stderr.decode())

# def main():
#     # 改进后的脚本映射表：允许参数存在与否
#     scripts_mapping = {
#         1: [
#             # 示例：不带参数的脚本
#             ("/agibot/data/home/agi/Desktop/RC", "send_motion_id.sh", ['暂停播放器']),
#         ],
#         2: [
#             #("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "recover.py", None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "right_hand_step2.py",None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "right_hand_step3.py",None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "sleep.py",['0.5']),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "right_hand_claw.py", None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "right_hand_step4.py",None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "right_hand_step5.py",None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "sleep.py",['0.5']),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "right_hand_release.py",None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "sleep.py",['0.5']),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "right_hand_step6.py",None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "right_hand_step7.py",None),
#             #("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "right_hand_step8.py",None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "recover.py",None),
#         ],
#         3: [
#             #("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "recover.py", None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "left_hand_step2.py",None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "left_hand_step3.py",None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "sleep.py",['0.5']),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "left_hand_claw.py", None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "left_hand_step4.py",None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "left_hand_step5.py",None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "sleep.py",['0.5']),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "left_hand_release.py",None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "sleep.py",['0.5']),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "left_hand_step6.py",None),
#             #("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "left_hand_step7.py",None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "left_hand_step7.py",None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "recover.py",None),
#         ],
#         4: [
#              #("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "recover.py", None),
#              ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "left_hand_step2.py",None),
#              ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "left_hand_step3.py",None),
#              ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "sleep.py",['0.5']),
#              ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "left_hand_claw.py", None),
#              ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "left_hand_step4.py",None),
#              ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "left_hand_step5.py",None),
#              ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "sleep.py",['0.5']),
#              ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "left_hand_release.py",None),
#              ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "sleep.py",['0.5']),
#              ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "left_hand_step6.py",None),
#              #("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "left_hand_step7.py",None),
#              ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "left_hand_step7.py",None),
#              ("/agibot/data/home/agi/jarvis/Motion_Library/left_hand_claw", "recover.py",None),
#         ],
#         5: [
#              ("/agibot/data/home/agi/jarvis/Motion_Library", "a2_SetAction.sh",["STAND_ARM_EXT_JOINT_TRAJ"]),
#              ("/agibot/data/home/agi/jarvis/Motion_Library", "send_motion_id.sh",["暂停播放器"]),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "right_hand_step1.py",None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "right_hand_step2.py",None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "right_hand_step3.py",None),
#             #("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "sleep.py",['0.5']),
#             #("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "right_hand_claw.py", None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "sleep.py",['0.5']),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "2right_hand_claw.py",None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "right_hand_step4.py",None),
#          ],
#           6: [
#             ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "recover.py",None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "right_hand_step1.py",None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "right_hand_step7.py",None),
#             ("/agibot/data/home/agi/jarvis/Motion_Library", "a2_SetAction.sh",["STAND_ARM_EXT_JOINT_SERVO"]),
#             #("/agibot/data/home/agi/jarvis/Motion_Library", "send_motion_id.sh",["暂停播放器"]),
#          ],
#     }

#     while True:
#         print("请输入要执行的脚本编号（1-8），按 'q' 退出：")
#         choice = input()

#         if choice == 'q':
#             print("退出程序。")
#             break

#         try:
#             choice = int(choice)
#             if choice < 1 or choice > 8:
#                 print("无效的编号，请输入 1 到 8 之间的数字。")
#                 continue

#             scripts_to_run = scripts_mapping.get(choice)
#             if scripts_to_run:
#                 for script_info in scripts_to_run:
#                     # 解包时处理可能存在的参数缺失情况
#                     directory, script = script_info[0], script_info[1]
#                     command_args = script_info[2] if len(script_info) > 2 else None

#                     script_path = os.path.join(directory, script)
#                     if not os.path.exists(script_path):
#                         print(f"脚本 {script_path} 不存在，请检查路径。")
#                         continue

#                     print(f"即将执行脚本：{script_path}，参数：{command_args if command_args else '无'}")
#                     if script.endswith('.sh'):
#                         run_bash_script(
#                             script_path,
#                             change_dir=True,
#                             directory=directory,
#                             command_args=command_args
#                         )
#                     elif script.endswith('.py'):
#                         run_python_script(
#                             script_path,
#                             change_dir=True,
#                             directory=directory,
#                             command_args=command_args
#                         )
#                     time.sleep(1)
#             else:
#                 print("未找到对应的脚本组。")

#         except ValueError:
#             print("输入无效，请输入一个有效的数字。")

# if __name__ == "__main__":
#     main()

import os
import time
import subprocess
import argparse  # 新增 argparse 模块

def run_bash_script(script_path, change_dir=False, directory=None, command_args=None):
    try:
        if change_dir and directory:
            print(f"切换到目录：{directory}")
            os.chdir(directory)

        # 构造命令：如果有参数则追加，否则不传
        command = ['bash', script_path]
        if command_args:
            command += command_args
        print(f"执行命令：{command}")

        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"执行成功，输出：\n{result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        print(f"执行命令时发生错误：{command}")
        print("错误信息：\n", e.stderr.decode())

def run_python_script(script_path, change_dir=False, directory=None, command_args=None):
    try:
        if change_dir and directory:
            print(f"切换到目录：{directory}")
            os.chdir(directory)

        # 构造命令：如果有参数则追加，否则不传
        command = ['python3', script_path]
        if command_args:
            command += command_args
        print(f"执行命令：{command}")

        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"执行成功，输出：\n{result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        print(f"执行 Python 脚本时发生错误：{command}")
        print("错误信息：\n", e.stderr.decode())

def main():
    # 初始化参数解析器
    parser = argparse.ArgumentParser(description="执行预定义的脚本组")
    parser.add_argument("group",
                       type=int,
                       choices=range(1, 15),  # 允许1-8的整数
                       help="要执行的脚本组编号 (1-8)")
    args = parser.parse_args()

    scripts_mapping = {
         5: [
             #("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "recover.py", None),
             ("/agibot/data/home/agi/jarvis/Motion_Library", "send_motion_id.sh",["暂停播放器"]),
             ("/agibot/data/home/agi/jarvis/Motion_Library/finger_dance", "final.py",None),
        ],
         2: [
            ("/agibot/data/home/agi/jarvis/Motion_Library", "a2_SetAction.sh",["STAND_ARM_EXT_JOINT_TRAJ"]),
            ("/agibot/data/home/agi/jarvis/Motion_Library", "send_motion_id.sh",["暂停播放器"]),
            ("/agibot/data/home/agi/jarvis/Motion_Library/shake_hand_right", "step1.py", None),
            ("/agibot/data/home/agi/jarvis/Motion_Library/shake_hand_right", "step3.py",None),
         ],
         3: [
            ("/agibot/data/home/agi/jarvis/Motion_Library/shake_hand_right", "hand.py",None),
            ("/agibot/data/home/agi/jarvis/Motion_Library/shake_hand_right", "step4.py",None),
         ],
         4: [
            ("/agibot/data/home/agi/jarvis/Motion_Library/shake_hand_right", "hand_recover.py",None),
            ("/agibot/data/home/agi/jarvis/Motion_Library/right_hand_claw", "sleep.py",['0.5']),
            ("/agibot/data/home/agi/jarvis/Motion_Library/shake_hand_right", "step1.py",None),
            ("/agibot/data/home/agi/jarvis/Motion_Library/shake_hand_right", "step0.py", None),
         ],
    }

    # 获取要执行的脚本组
    choice = args.group
    scripts_to_run = scripts_mapping.get(choice)

    if not scripts_to_run:
        print(f"编号 {choice} 对应的脚本组不存在")
        return

    # 执行选定脚本组
    for script_info in scripts_to_run:
        # 解包时处理可能存在的参数缺失情况
        directory, script = script_info[0], script_info[1]
        command_args = script_info[2] if len(script_info) > 2 else None

        script_path = os.path.join(directory, script)
        if not os.path.exists(script_path):
            print(f"脚本 {script_path} 不存在，请检查路径。")
            continue

        print(f"正在执行：{script_path}，参数：{command_args if command_args else '无'}")
        try:
            if script.endswith('.sh'):
                run_bash_script(
                    script_path,
                    change_dir=True,
                    directory=directory,
                    command_args=command_args
                )
            elif script.endswith('.py'):
                run_python_script(
                    script_path,
                    change_dir=True,
                    directory=directory,
                    command_args=command_args
                )
            time.sleep(1)
        except Exception as e:
            print(f"执行过程中发生错误: {str(e)}")
            break

if __name__ == "__main__":
    main()
