import subprocess
import time

python_files = ['hand0.py','hand6_1.py','hand6_2.py','hand6_3.py','hand6_4.py','hand6_5.py','hand6_6.py','hand6_7.py','hand6_8.py','hand6_9.py','hand0.py','hand6_10.py','hand0.py','hand6_10.py','hand0.py']

# 遍历列表，依次执行每个Python文件
for file in python_files:
    try:
        # 使用subprocess.run来执行Python文件
        result = subprocess.run(['python3', file], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(0.3)
        print(f"Output from {file}:\n{result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        # 如果执行出错，打印错误信息
        print(f"An error occurred while executing {file}:\n{e.stderr.decode()}")