import subprocess
import time

python_files = ['hand7_1_copy.py','hand7_2_copy.py','hand7_3_copy.py','hand7_4_copy.py','hand7_5_copy.py','hand7_6_copy.py','hand7_7_copy.py','hand7_8_copy.py','hand7_9_copy.py','hand7_10_copy.py']

# 遍历列表，依次执行每个Python文件
for file in python_files:
    try:
        # 使用subprocess.run来执行Python文件
        result = subprocess.run(['python3', file], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # 打印标准输出
        time.sleep(0.6)
        print(f"Output from {file}:\n{result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        # 如果执行出错，打印错误信息
        print(f"An error occurred while executing {file}:\n{e.stderr.decode()}")