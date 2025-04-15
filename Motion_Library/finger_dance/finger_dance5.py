import subprocess
import time

python_files = ['hand1.py','hand5_1.py','hand5_2.py','hand5_3.py','hand5_2.py','hand5_3.py','hand5_2.py','hand5_3.py','hand5_2.py','hand5_3.py','hand5_2.py','hand5_3.py','hand0.py']

# 遍历列表，依次执行每个Python文件
for file in python_files:
    try:
        # 使用subprocess.run来执行Python文件
        result = subprocess.run(['python3', file], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(0.2)
        print(f"Output from {file}:\n{result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        # 如果执行出错，打印错误信息
        print(f"An error occurred while executing {file}:\n{e.stderr.decode()}")