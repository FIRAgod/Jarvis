import argparse
import time

# 设置命令行参数解析器
def parse_args():
    parser = argparse.ArgumentParser(description="休眠指定的秒数")
    parser.add_argument("seconds", type=float, help="要休眠的时间（单位：秒）")
    return parser.parse_args()

def main():
    # 解析命令行参数
    args = parse_args()
    
    # 获取休眠的秒数
    seconds = args.seconds
    
    # 输出提示信息
    print(f"程序将休眠 {seconds} 秒...")
    
    # 使用 time.sleep() 让程序暂停
    time.sleep(seconds)
    
    # 休眠结束后，输出提示信息
    print(f"{seconds} 秒已过，程序继续执行。")

if __name__ == "__main__":
    main()

