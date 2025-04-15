import subprocess
import time

python_files = ['step1.py','step2.py','step3.py','hand.py','step4.py','step5,py','step3.py','step4.py','step5,py','step3.py','step4.py','step5,py','step1.py','recover_hand.py','recover_arm.py']

# 遍历列表，依次执行每个Python文件
for file in python_files:
    try:
        # 使用subprocess.run来执行Python文件
        result = subprocess.run(['python3', file], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 打印标准输出
        time.sleep(0.4)
        print(f"Output from {file}:\n{result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        # 如果执行出错，打印错误信息
        print(f"An error occurred while executing {file}:\n{e.stderr.decode()}")