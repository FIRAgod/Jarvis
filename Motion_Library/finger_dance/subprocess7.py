import subprocess
import sys

# 启动第一个 Python 文件
subprocess.Popen(["python3", "complete_step7.py"])

# 启动第二个 Python 文件
subprocess.Popen(["python3", "finger_dance7.py"])

# # 等待两个文件执行完毕
# process1.wait()
# process2.wait()

# # 继续执行其他代码（如果需要）
# print("两个文件已启动")

sys.exit()