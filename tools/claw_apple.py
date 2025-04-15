import os

def run_script(script_name):
    try:
        os.system(f'python3 {script_name}')
    except Exception as e:
        print(f"Error running script {script_name}: {e}")

while True:
    print("请输入数字 (1, 2, 3) 来运行相应的脚本，按 'q' 退出程序：")
    user_input = input()

    if user_input == '1':
        run_script('claw_apple1.py')
    elif user_input == '2':
        run_script('claw_apple2.py')
    elif user_input == '3':
        run_script('claw_apple3.py')
    elif user_input.lower() == 'q':
        print("退出程序...")
        break
    else:
        print("无效输入，请重新输入。")

