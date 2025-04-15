import subprocess
import time

# 定义一个包含Python文件名的列表
python_files = ['recover_0.py','claw_water_firststep.py','set_hand_command.py','arm_joint5_rotate.py','release_hand.py']

# 遍历列表，依次执行每个Python文件
for file in python_files:
    try:
        # 使用subprocess.run来执行Python文件
        result = subprocess.run(['python3', file], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 打印标准输出
        print(f"Output from {file}:\n{result.stdout.decode()}")
        if(file=='claw_water_firststep.py'):  time.sleep(6)
        else: time.sleep(2)
    except subprocess.CalledProcessError as e:
        # 如果执行出错，打印错误信息
        print(f"An error occurred while executing {file}:\n{e.stderr.decode()}")
