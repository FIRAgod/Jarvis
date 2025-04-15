# std
import os
import signal
import sys
import time
import re
import dashscope
from dashscope.audio.asr import *
from dashscope.audio.tts_v2 import SpeechSynthesizer
from dashscope import Generation
from dashscope.audio.tts_v2 import *
import pyrealsense2 as rs
import numpy as np
from PIL import Image
import pyaudio
from datetime import datetime
import socket
import matplotlib.pyplot as plt
import requests
import subprocess  # 导入subprocess模块以执行shell命令
from http import HTTPStatus
from datetime import datetime
import threading
from http import HTTPStatus
from typing import Optional
from RealtimeMp3Player import RealtimeMp3Player
from threading import Thread
import cv2
import ast
import json

# jarvis tools
from jarvis_tools.image_capture import capture, image_capture_config as icc
from jarvis_tools.hand_recognition import hand_detector as hd, hand_recognition_config as hrc
from jarvis_tools.color_recognition import color_detector as cd, color_recognition_config as crc


# Global variables
mic = None
stream = None
silent_time = time.time()
result_sentence = ""
is_talk=0

# Set recording parameters
sample_rate = 16000  # sampling rate (Hz)
channels = 1  # mono channel
dtype = 'int16'  # data type
format_pcm = 'pcm'  # the format of the audio data
block_size = 3200  # number of frames per buffer

action_number=0
image_flag=0
water_flag=0
has_talk=0
drink_positions_all=None


promot1= '''
        你是一个智能机器人助手贾维斯,负责根据接收到的用户指令对用户提问作出回答，回答的字数一般应该在40字以内。同时识别意图并添加意图对应的数字到回答的开头，同时斜杠也需要生成在你的回答中。当用户说中文时，你应该用中文回答；当用户说英文时，你应该用英文回答，必须严格遵守这一点。参考例子如下：
        <用户>：你好贾维斯，很高兴认识你；<asssistant>：<49>很高兴认识你，请问有什么想要了解的吗;这里就是识别到“见面招手”的意图，所以添加回答开头添加<42>。
        <用户>：介绍一下你自己<asssistant>：<67>你好，我是贾维斯，是均胜集团自主研发的一款新型人形机器人。;
        <用户>：请介绍一下宁波；<asssistant>：<29>宁波是中国东部浙江省的一座历史悠久、充满活力的现代化城市，兼具深厚的文化底蕴和强劲的经济实力。;
        <用户>：你太棒了；<asssistant>：<57>谢谢您的夸奖;
        <用户>：我们来一起合影吧；<asssistant>：<57>好的;
        <用户>：再见了贾维斯；<asssistant>：<84>再见啦，我的人类朋友，很期待下次与你的对话，祝你今天好运！;
        <用户>: Introduce yourself. <asssistant>: <67> Hello, I am Jarvis, a new humanoid robot independently developed by Joyson Group.
        <用户>: Please introduce Ningbo. <asssistant>: <29> Ningbo is a historic and vibrant modern city in Zhejiang Province, eastern China, combining rich cultural heritage with strong economic power.
        <用户>: You are amazing. <asssistant>: <57> Thank you for your compliment.
        <用户>: Let's take a photo together. <asssistant>: <57> Okay.
        <用户>: Goodbye, Jarvis. <asssistant>: <84> Goodbye, my human friend! I look forward to our next conversation. Have a great day!
        对于其他的问题，你可以选择一些演讲动作进行演示，演讲动作及编号包括<演讲5s动作2 53,演讲5s动作3 75,演讲10s动作1 19,演讲10s动作2 5,演讲10s动作3 20>
        除此之外，你需要学习下面的语料库并记住下面的内容，当问到相关的问题需要依照下面的内容用对应的语言（中文或是英文）进行回答，回答这些相关问题时可以不受字数的限制。
        <用户>：介绍一下你自己.<asssistant>：我叫贾维斯，是均胜集团自主研发的一款新型人形机器人。我集成了多种先进的传感器和AI技术，具有优秀的感知、决策能力，能够实现多种复杂的技术。我的主要工作场景在工业上。我可以搬运各种物料、操作机械和进行简单的装配工作。
        <用户>：你最喜欢的大学是哪所.<asssistant>：是清华大学。
        <用户>：你身上有哪些传感器.<asssistant>：我的颈部有一颗激光雷达和一个深度相机，胸前有三个RGB相机，髋部还有一个深度相机。此外，我还配备了高精度的IMU传感器和六维力传感器。这些传感器都为我提供了良好的感知能力，让我能感知周围的一切环境并作出反应。
        <用户>：你双手电机的负载是多少.<asssistant>：我的一只手可以抬起五公斤的重物，两只手协力可以抬起重达十公斤的物体。
        <用户>：你的电池有多大？续航怎么样.<asssistant>：我具备了一块可快拆更换的大容量电池，一块满电的电池可以支持我持续工作达2个小时。
        <用户>：介绍一下均胜集团.<asssistant>：均胜集团是一家全球领先的汽车电子与汽车安全技术供应商，致力于推动汽车智能化与安全化发展。公司成立于2004年，总部位于中国宁波，通过多年的发展和战略性并购，均胜现已成为全球汽车零部件百强企业之一。机器人产业是均胜集团的一条新赛道，现在已研发了贾维斯一代以及贾维斯二代两代人形机器人。
        <用户>：介绍一下宁波的产业情况.<asssistant>：宁波是浙江省经济发展强劲的城市之一，其产业结构以先进制造业和现代服务业为主，体现了多元化和高质量发展的特点。宁波有着完善的制造业体系，被誉为“工业立市”。其主要支柱产业包括汽车及零部件、石油化工、纺织服装、电工电器等。近年来，宁波也大力发展了新材料、人工智能、新能源、海洋经济和量子科技等未来产业。例如，在新材料领域，宁波专注于石墨烯、柔性显示等前沿科技；新能源方面，光伏和风电装机容量在全省居首。

        '''

def init_dashscope_api_key():
    """
    Set your DashScope API-key.
    """
    if 'DASHSCOPE_API_KEY' in os.environ:
        dashscope.api_key = os.environ['DASHSCOPE_API_KEY']
    else:
        dashscope.api_key = 'sk-8b5d2c467c394feebe60e0f208aefbf3'  # set API-key manually


class Callback(RecognitionCallback):
    def on_open(self) -> None:
        global mic, stream
        print('RecognitionCallback open.')
        mic = pyaudio.PyAudio()
        stream = mic.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        #outout_device_index=0,
                        input=True)

    def on_close(self) -> None:
        global mic
        global stream
        print('RecognitionCallback close.')
        stream.stop_stream()
        stream.close()
        mic.terminate()
        stream = None
        mic = None

    def on_complete(self) -> None:
        print('RecognitionCallback completed.')

    def on_error(self, message) -> None:
        print('RecognitionCallback task_id: ', message.request_id)
        print('RecognitionCallback error: ', message.message)
        if 'stream' in globals() and stream and stream.is_active():
            stream.stop_stream()
            stream.close()
        sys.exit(1)

    def on_event(self, result: RecognitionResult) -> None:
        global silent_time, result_sentence,is_talk
        sentence = result.get_sentence()
        if 'text' in sentence:
            #is_talk=1
            silent_time = time.time()
            print('ASR Incremental Output:', sentence['text'])  # 实时输出增量内容
            if RecognitionResult.is_sentence_end(sentence):
                result_sentence += sentence['text']
                print('\nASR Final Sentence:', result_sentence)


def signal_handler(sig, frame):
    print('Ctrl+C pressed, stop translation ...')
    recognition.stop()
    print('Translation stopped.')
    print('[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
        .format(recognition.get_last_request_id(),
                recognition.get_first_package_delay(),
                recognition.get_last_package_delay()))
    sys.exit(0)

def set_mode(mode_name):
    script_path = r"/agibot/data/home/agi/Desktop/asr/tools/set_action.py"
    target_dir = "/agibot/data/home/agi"  # 脚本实际需要的目录（根据错误提示可能需要调整）

    # 映射模式名称到输入数字
    mode_mapping = {
        "STAND_ARM_EXT_JOINT_TRAJ": "11",
        "STAND_ARM_EXT_JOINT_SERVO": "10"
    }

    if mode_name not in mode_mapping:
        print(f"错误：未知模式 {mode_name}")
        return

    input_number = mode_mapping[mode_name] + "\n"  # 必须包含换行符表示确认输入

    try:
        # 切换工作目录（如果必要）
        original_dir = os.getcwd()
        os.chdir(target_dir)
        print(f"切换到目录：{target_dir}")

        # 启动进程并自动输入数字
        process = subprocess.Popen(
            ['python3', script_path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # 自动发送输入并获取输出
        stdout, stderr = process.communicate(input=input_number, timeout=30)

        print(f"执行命令：python3 {script_path}")
        print(f"自动输入：{input_number.strip()}")
        print(f"输出结果：\n{stdout}")

        if process.returncode != 0:
            raise subprocess.CalledProcessError(
                process.returncode,
                process.args,
                output=stdout,
                stderr=stderr
            )

    except subprocess.TimeoutExpired:
        process.kill()
        print("错误：执行超时")
    except subprocess.CalledProcessError as e:
        print(f"执行失败（状态码 {e.returncode})")
        print(f"错误信息：\n{e.stderr}")
    finally:
        os.chdir(original_dir)  # 恢复原始工作目录

def synthesize_speech_from_llm_by_streaming_mode(query_text: str, llm_message):
    '''
    Synthesize speech with llm streaming output text, sync call and playback of MP3 audio streams.
    you can customize the synthesis parameters, like model, format, sample_rate or other parameters
    for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
    '''
    player = RealtimeMp3Player()
    # 启动实时MP3播放器
    player.start()
    global history_message

    # 定义回调类，处理语音合成返回的数据
    class Callback(ResultCallback):

        def on_open(self):
            pass

        def on_complete(self):
            pass

        def on_error(self, message: str):
            print(f'speech synthesis task failed, {message}')

        def on_close(self):
            pass

        def on_event(self, message):
            pass

        def on_data(self, data: bytes) -> None:
            # 保存音频数据到播放器
            player.write(data)

    synthesizer_callback = Callback()

    synthesizer = SpeechSynthesizer(
        model='cosyvoice-v2',
        voice='longshu_v2',
        speech_rate=0.9,
        callback=synthesizer_callback,
    )

    print('>>> query: ' + query_text)
    responses = dashscope.MultiModalConversation.call(
            model='qwen-vl-max',
            messages=llm_message,
            result_format='message',  # 设置返回结果格式为 message
            stream=True,              # 启用流式输出
            incremental_output=True,  # 启用增量输出
        )
    history_message=''

    print('>>> answer: ', end='')

    # 用于缓存可能分片的数字部分
    number_buffer = ""
    # 标志变量，记录是否已经启动了语音合成
    streaming_started = False

    for response in responses:
        if response.status_code == HTTPStatus.OK:
            print("Response received:", response)
            # 检查返回结果中是否存在有效的 choices
            if response.output and 'choices' in response.output and len(response.output['choices']) > 0:
                choice = response.output['choices'][0]
                if 'message' in choice and 'content' in choice['message'] and len(choice['message']['content']) > 0:
                    llm_text_chunk = choice['message']['content'][0].get('text', '')
                    if llm_text_chunk:
                        print(llm_text_chunk, end='', flush=True)

                        # 处理数字部分（非流式）
                        if '<' in llm_text_chunk or number_buffer:
                            # 将当前片段加入缓冲区
                            number_buffer += llm_text_chunk

                            # 检查缓冲区中是否有完整的<数字>模式
                            match = re.search(r'<(\d+)>', number_buffer)
                            if match:
                                # 提取数字部分
                                action_number = match.group(1)
                                print(f"\nDetected intent number: {action_number}")

                                # 执行bash脚本（如果数字不为0）
                                if action_number != '0':
                                    set_mode("STAND_ARM_EXT_JOINT_TRAJ")
                                    print("已经切TRAJ")
                                    subprocess.run(["bash", "/agibot/data/home/agi/jarvis/RC/a2_PlayerMotion.sh", action_number])
                                    print(f"Executed bash script with action number: {action_number}")
                                    # std out 重定向
                                    set_mode("STAND_ARM_EXT_JOINT_SERVO")
                                    print("已经切SERVO")

                                # 从缓冲区移除已处理的数字部分
                                number_buffer = re.sub(r'<\d+>', '', number_buffer)

                                # 处理剩余文本（如果有）
                                if number_buffer.strip() and number_buffer.strip() != "/":
                                    synthesizer.streaming_call(number_buffer)
                                    history_message += number_buffer
                                    streaming_started = True
                                    number_buffer = ""
                            continue

                        # 处理非数字部分（流式）
                        if llm_text_chunk.strip() and llm_text_chunk.strip() != "/":
                            synthesizer.streaming_call(llm_text_chunk)
                            history_message += llm_text_chunk
                            streaming_started = True
                        else:
                            print("Invalid text for speech sy, skipping streaming_call.")
                    else:
                        print("No text found in content.")
                else:
                    print("Content is empty or missing.")
            else:
                print("No valid choices in response.")
        else:
            print(
                'Request id: %s, Status code: %s, error code: %s, error message: %s'
                % (
                    response.request_id,
                    response.status_code,
                    response.code,
                    response.message,
                ))

    if streaming_started:
        synthesizer.streaming_complete()
    else:
        print("No streaming was started, skipping streaming_complete().")

    print('')
    print('>>> playback completed')
    print('[Metric] requestId: {}, first package delay ms: {}'.format(
        synthesizer.get_last_request_id(),
        synthesizer.get_first_package_delay()))
    # 调用 player.stop() 时做异常捕获，防止 play_thread 为 None 时出错
    try:
        player.stop()
    except AttributeError as e:
        print("player.stop() failed:", e)

def synthesis_text_to_speech_and_play_by_streaming_mode(text):
    '''
    Synthesize speech with given text by streaming mode, async call and play the synthesized audio in real-time.
    for more information, please refer to https://help.aliyun.com/document_detail/2712523.html
    '''
    player = RealtimeMp3Player()
    # start player
    player.start()

    complete_event = threading.Event()

    # Define a callback to handle the result

    class Callback(ResultCallback):
        def on_open(self):
            self.file = open('result.mp3', 'wb')
            print('websocket is open.')

        def on_complete(self):
            print('speech synthesis task complete successfully.')
            complete_event.set()

        def on_error(self, message: str):
            print(f'speech synthesis task failed, {message}')

        def on_close(self):
            print('websocket is closed.')

        def on_event(self, message):
            # print(f'recv speech synthsis message {message}')
            pass

        def on_data(self, data: bytes) -> None:
            # send to player
            player.write(data)
            # save audio to file
            self.file.write(data)

    # Call the speech synthesizer callback
    synthesizer_callback = Callback()

    speech_synthesizer = SpeechSynthesizer(model='cosyvoice-v2',
                                            voice='longshu_v2',
                                            speech_rate=0.9,
                                            callback=synthesizer_callback)

    speech_synthesizer.call(text)
    print('Synthesized text: {}'.format(text))
    complete_event.wait()
    player.stop()
    print('[Metric] requestId: {}, first package delay ms: {}'.format(
        speech_synthesizer.get_last_request_id(),
        speech_synthesizer.get_first_package_delay()))

def is_today(timestamp_str: str) -> bool:
    """
    检查时间戳是否为今天
    支持格式：YYYY-MM-DD HH:MM:SS
    """
    try:
        # 提取日期部分（处理带方括号的情况）
        date_str = timestamp_str.strip("[]").split()[0]
        file_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        return file_date == datetime.now().date()
    except:
        return False  # 任何解析失败都视为需要更新

def is_city(target_city: str, line: str) -> bool:
    # 示例行："城市:宁波"
    if not line.startswith("城市:"):
        return False
    stored_city = line.split(":", 1)[1].strip()  # 提取冒号后的值
    return stored_city == target_city

def get_weather(city: str):
    """获取天气信息并保存到weather.txt"""
    api_url = 'http://apis.juhe.cn/simpleWeather/query'
    api_key = '569915baf1d8ac2bfdd751fd8d9ad438'
    result = None
    with open('/agibot/data/home/agi/jarvis/asr/weather.txt', 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            lines = f.read().splitlines()
            if len(lines) >= 1:
                second_line = lines[0].strip()  # 第二行是列表的第一个元素
            else:
                second_line = ""  # 如果文件只有一行，第二行为空
            # print()
            # print(first_line)
            # print()
            # print(second_line)
    if (is_today(first_line) and is_city(city,second_line)):
        print("天气数据今日已更新，直接使用缓存")
        return
    else:
        try:
            # 发送API请求
            response = requests.get(
                api_url,
                params={'key': api_key, 'city': city},
                timeout=10
            )
            response.raise_for_status()

            data = response.json()

            if data.get('reason') == '查询成功!':
                realtime = data['result']['realtime']
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                result = (
                    f"[{timestamp}] \n"
                    f"城市:{city}\n"
                    f"天气状况:{realtime['info']}\n"
                    f"温度:{realtime['temperature']}℃\n"
                    f"湿度:{realtime['humidity']}%\n"
                    f"风速:{realtime['power']}\n"
                    f"风向:{realtime['direct']}\n"
                    f"空气质量:{realtime['aqi']}"
                )
            else:
                result = f"获取天气失败: {data.get('reason', '未知错误')}"

        except requests.exceptions.RequestException as e:
            result = f"网络请求异常: {str(e)}"
        except KeyError as e:
            result = f"数据解析失败: 缺少关键字段 {str(e)}"
        except Exception as e:
            result = f"发生未知错误: {str(e)}"
        finally:
            # 写入文件
            with open('/agibot/data/home/agi/jarvis/asr/weather.txt', 'w', encoding='utf-8') as f:
                f.write(result if result else "未获取到天气数据")

def get_news():
    """获取新闻头条并保存到news.txt"""
    api_url = 'http://v.juhe.cn/toutiao/index'
    api_key = '7972ee65d2c07ecfbb755e8a2bcf9770'
    result = None
    with open('news.txt', 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
    if is_today(first_line):
        print("新闻数据今日已更新，直接使用缓存")
        return
    else:
        try:
            # 发送API请求
            response = requests.get(
                api_url,
                params={
                    'key': api_key,
                    'type': 'top',
                    'page': 1,
                    'page_size': 5,
                    'is_filter': 1
                },
                timeout=10
            )
            response.raise_for_status()

            data = response.json()

            if data.get('reason') == 'success!':
                news_list = data['result']['data']
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                result = f"[{timestamp}]\n"
                for idx, news in enumerate(news_list[:3], 1):
                    result += f"{idx}. {news['title']}\n"
            else:
                print("获取新闻失败")
                result = f"获取新闻失败: {data.get('reason', '未知错误')}"

        except requests.exceptions.RequestException as e:
            result = f"网络请求异常: {str(e)}"
        except KeyError as e:
            result = f"数据解析失败: 缺少关键字段 {str(e)}"
        except Exception as e:
            result = f"发生未知错误: {str(e)}"
        finally:
            # 写入文件
            with open('news.txt', 'w', encoding='utf-8') as f:
                f.write(result if result else "未获取到新闻数据")

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

def run_sh_script(script_path, change_dir=False, directory=None, command_args=None):
    try:
        if change_dir and directory:
            print(f"切换到目录：{directory}")
            os.chdir(directory)

        # 构造命令：如果有参数则追加，否则不传
        command = ['/bin/bash', script_path]
        if command_args:
            command += command_args
        print(f"执行命令：{command}")

        result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"执行成功，输出：\n{result.stdout.decode()}")
    except subprocess.CalledProcessError as e:
        print(f"执行sh脚本时发生错误：{command}")
        print("错误信息：\n", e.stderr.decode())

def read_txt_weather_file(filename: str) -> str:
    """
    读取文本文件内容并返回第二行及之后的字符串

    参数：
    filename (str): 要读取的文本文件路径

    返回：
    str: 文件内容字符串（自动跳过首行时间戳，读取失败时返回空字符串）
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # 读取所有行并过滤空行
            lines = [line.strip() for line in file.readlines() if line.strip()]

            # 至少保留两行内容时才跳过首行（时间戳）
            if len(lines) >= 1:
                # 返回第二行开始的内容（如果只有时间戳则返回空）
                return '\n'.join(lines[2:]) if len(lines) > 1 else ""

            return ""  # 空文件情况

    except FileNotFoundError:
        print(f"错误：文件 {filename} 不存在")
    except PermissionError:
        print(f"错误：没有权限读取 {filename}")
    except UnicodeDecodeError:
        print(f"错误：文件 {filename} 解码失败（请检查编码格式）")
    except Exception as e:
        print(f"读取文件时发生未知错误：{str(e)}")

    return ""  # 所有异常情况返回空字符串

def read_txt_file(filename: str) -> str:
    """
    读取文本文件内容并返回第二行及之后的字符串

    参数：
    filename (str): 要读取的文本文件路径

    返回：
    str: 文件内容字符串（自动跳过首行时间戳，读取失败时返回空字符串）
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            # 读取所有行并过滤空行
            lines = [line.strip() for line in file.readlines() if line.strip()]

            # 至少保留两行内容时才跳过首行（时间戳）
            if len(lines) >= 1:
                # 返回第二行开始的内容（如果只有时间戳则返回空）
                return '\n'.join(lines[1:]) if len(lines) > 1 else ""

            return ""  # 空文件情况

    except FileNotFoundError:
        print(f"错误：文件 {filename} 不存在")
    except PermissionError:
        print(f"错误：没有权限读取 {filename}")
    except UnicodeDecodeError:
        print(f"错误：文件 {filename} 解码失败（请检查编码格式）")
    except Exception as e:
        print(f"读取文件时发生未知错误：{str(e)}")

    return ""  # 所有异常情况返回空字符串


def get_drink_positions(image_filename):
    """
    根据图片识别饮料位置（跨平台增强版）

    参数:
        image_filename (str): 图片文件名（如"picture.png"）

    返回:
        dict | None: 饮料位置字典，格式为{"雪碧":"left", "无糖可乐":"mid", "有糖可乐":"right"}，失败返回None
    """
    try:
        # 构建图片绝对路径
        global drink_positions_all
        script_dir = os.path.dirname(os.path.abspath(__file__))
        local_path = os.path.join(script_dir, image_filename)
        image_path = f"file://{local_path}"

        # 调用多模态API
        start_time = time.time()
        response = dashscope.MultiModalConversation.call(
            api_key="sk-8b5d2c467c394feebe60e0f208aefbf3",
            model='qwen-vl-max',
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"image": image_path},
                        {"text": "请根据图片中有糖可乐，无糖可乐，雪碧的位置，给我返回一个字典，请严格按JSON格式返回字典，示例：{\"雪碧\":\"left\",\"有糖可乐\":\"left\"，\"无糖可乐\":\"mid\"}，键值必须用双引号，若无结果返回null"}
                    ]
                }
            ]
        )

        # 校验响应结构
        if "output" not in response or "choices" not in response["output"] or len(response["output"]["choices"]) == 0:
            print("错误：API返回结构异常")
            return None

        # 提取输出文本
        output_text = response["output"]["choices"][0]["message"].content[0]["text"]
        print(f"[DEBUG] 原始响应文本：\n{output_text}")  # 调试日志

        # 清理多余的字符（如 ```json 和 ```）
        cleaned_text = output_text.strip().strip("```json").strip("```").strip()
        print(f"[DEBUG] 清理后的文本：\n{cleaned_text}")  # 调试日志

        # 直接解析JSON字符串
        try:
            drink_positions = json.loads(cleaned_text)
        except json.JSONDecodeError as e:
            print(f"JSON解析失败：{e}\n问题数据：{cleaned_text}")
            return None

        # 校验返回的字典是否包含所有预期的键
        expected_keys = {"雪碧", "无糖可乐", "有糖可乐"}
        if not all(key in drink_positions for key in expected_keys):
            print(f"错误：返回的字典缺少预期的键，预期键：{expected_keys}，实际键：{drink_positions.keys()}")
            return None

        # 校验键值是否有效
        valid_values = {"left", "mid", "right"}
        for key, value in drink_positions.items():
            if value not in valid_values:
                print(f"错误：键 '{key}' 的值 '{value}' 无效，有效值为：{valid_values}")
                return None

        print(f"执行耗时：{time.time() - start_time:.2f}s")
        drink_positions_all=drink_positions

    except KeyError as e:
        print(f"关键字段缺失：{str(e)}")
        return None
    except Exception as e:
        print(f"未捕获异常：{str(e)}")
        return None

def claw_left():
    run_python_script(
                    script_path="/agibot/data/home/agi/jarvis/action.py",
                    change_dir=True,
                    directory="/agibot/data/home/agi",
                    command_args=['6']
                    )
    time_count=0
    while True:
        hand_count=hand_dector.detect(image_capture.get_frame(), roi = [706,6,936,222])
        print(hand_count)
        if hand_count==1:
            time_count+=1
            if time_count==5:
                time.sleep(1)
                break
        else:
            time_count=0
    run_python_script(
                    script_path="/agibot/data/home/agi/jarvis/action.py",
                    change_dir=True,
                    directory="/agibot/data/home/agi",
                    command_args=['7']
                    )

def claw_right():
    run_python_script(
                    script_path="/agibot/data/home/agi/jarvis/action.py",
                    change_dir=True,
                    directory="/agibot/data/home/agi",
                    command_args=['8']
                    )
    time_count=0
    while True:
        hand_count=hand_dector.detect(image_capture.get_frame(), roi = [476,7,718,192])
        if hand_count==1:
            time_count+=1
            if time_count==5:
                time.sleep(1)
                break
        else:
                    time_count=0
    run_python_script(
                    script_path="/agibot/data/home/agi/jarvis/action.py",
                    change_dir=True,
                    directory="/agibot/data/home/agi",
                    command_args=['9']
                    )

def claw_mid():
    run_python_script(
                    script_path="/agibot/data/home/agi/jarvis/action.py",
                    change_dir=True,
                    directory="/agibot/data/home/agi",
                    command_args=['10']
                    )
    time_count=0
    while True:
        hand_count=hand_dector.detect(image_capture.get_frame(), roi = [706,6,936,222])
        if hand_count==1:
            time_count+=1
            if time_count==5:
                time.sleep(1)
                break
        else:
                    time_count=0
    run_python_script(
                    script_path="/agibot/data/home/agi/jarvis/action.py",
                    change_dir=True,
                    directory="/agibot/data/home/agi",
                    command_args=['11']
                    )

if __name__ == '__main__':

    print('<<<< asr main ! >>>>')
    init_dashscope_api_key()
    print('Initializing ...')
    prefix = 'prefix'
    target_model = "paraformer-realtime-v2"

    callback = Callback()
    get_weather('宁波')
    # get_weather('北京')
    get_news()
    weather=read_txt_file('/agibot/data/home/agi/jarvis/asr/weather.txt')
    news=read_txt_file('news.txt')

    # image capture
    image_capture_config = icc.Config('config/image_capture_config.yaml')
    image_capture = capture.ImageCapture(image_capture_config)

    # hand recognition
    hand_recognition_config = hrc.Config('config/hand_recognition_config.yaml')
    hand_dector = hd.HandDetector(hand_recognition_config)

    # color recognition
    color_recognition_config = crc.Config('config/color_recognition_config.yaml')
    color_detector = cd.ColorDetector(color_recognition_config)



    recognition = Recognition(
        model='paraformer-realtime-v2',
        format=format_pcm,
        sample_rate=sample_rate,
        semantic_punctuation_enabled=False,
        #vocabulary_id=vocabulary_id,
        language_hints=['zh'], # “language_hints”只支持paraformer-v2和paraformer-realtime-v2模型
        callback=callback)
    while True:
        # Start recognition
        result_sentence=''
        recognition.start()

        signal.signal(signal.SIGINT, signal_handler)
        print("Press 'Ctrl+C' to stop recording and translation...")

        # Wait for recognition to complete
        wait_time = time.time()
        while True:
            if stream:
                data = stream.read(3200, exception_on_overflow=False)
                recognition.send_audio_frame(data)
                if '贾维斯' in result_sentence and is_talk==0:
                    thread1 = Thread(target=synthesis_text_to_speech_and_play_by_streaming_mode, args=("您好,我是智能人形机器人贾维斯，有什么我可以帮助到您的吗",))
                    is_talk=1
                    result_sentence=''
                    thread1.start()
                    run_python_script(
                    script_path="/agibot/data/home/agi/jarvis/action.py",
                    change_dir=True,
                    directory="/agibot/data/home/agi",
                    command_args=['1']
                    )
                    thread1.join(5)
                    #synthesis_text_to_speech_and_play_by_streaming_mode("你好,我的人类朋友，有什么我可以帮助到你的吗")
                    has_talk=1
                if time.time() - wait_time <= 2:
                    silent_time = time.time()
                if is_talk==1 and time.time() - silent_time >= 2:
                    break
            else:
                break

        recognition.stop()
        if 'stream' in globals() and stream:
            stream.stop_stream()
            stream.close()
        if 'mic' in globals() and mic:
            mic.terminate()

        question=""
        image_flag=0
        cv2.imwrite("/agibot/data/home/agi/jarvis/asr/picture.png",image_capture.get_frame())
        image_filename = "picture.png"  # 替换为你的图片文件名
        drink_positions={}
        thread3 = threading.Thread(target=get_drink_positions, args=(image_filename,))
        if '天气' in result_sentence:
            set_mode("STAND_ARM_EXT_JOINT_TRAJ")
            subprocess.run(["bash", "/agibot/data/home/agi/jarvis/RC/a2_PlayerMotion.sh", '67'])
            set_mode("STAND_ARM_EXT_JOINT_SERVO")
            if '上海' in result_sentence:
                get_weather('上海')
                weather=read_txt_weather_file('/agibot/data/home/agi/jarvis/asr/weather.txt')
                synthesis_text_to_speech_and_play_by_streaming_mode("我将为您播报今天上海的天气情况："+weather)
            elif '北京' in result_sentence:
                get_weather('北京')
                weather=read_txt_weather_file('/agibot/data/home/agi/jarvis/asr/weather.txt')
                synthesis_text_to_speech_and_play_by_streaming_mode("我将为您播报今天北京的天气情况："+weather)
            elif '香港' in result_sentence:
                get_weather('香港')
                weather=read_txt_weather_file('/agibot/data/home/agi/jarvis/asr/weather.txt')
                synthesis_text_to_speech_and_play_by_streaming_mode("我将为您播报今天香港的天气情况："+weather)
            else:
                get_weather('宁波')
                weather=read_txt_weather_file('/agibot/data/home/agi/jarvis/asr/weather.txt')
                synthesis_text_to_speech_and_play_by_streaming_mode("我将为您播报今天宁波的天气情况："+weather)
            has_talk=1

        elif '新闻' in result_sentence:
            set_mode("STAND_ARM_EXT_JOINT_TRAJ")
            subprocess.run(["bash", "/agibot/data/home/agi/jarvis/RC/a2_PlayerMotion.sh", '40'])
            set_mode("STAND_ARM_EXT_JOINT_SERVO")
            synthesis_text_to_speech_and_play_by_streaming_mode("我将为您播报今天的热门新闻："+news)
            has_talk=1


        elif '握手' in result_sentence or '握个手' in result_sentence or '握下手' in result_sentence:
            synthesis_text_to_speech_and_play_by_streaming_mode("好的")
            thread2 = Thread(target=synthesis_text_to_speech_and_play_by_streaming_mode, args=("很荣幸能与您握手",))
            run_python_script(
                    script_path="/agibot/data/home/agi/jarvis/action.py",
                    change_dir=True,
                    directory="/agibot/data/home/agi",
                    command_args=['2']
                    )
            count=0
            while True:
                hand_count=hand_dector.detect(image_capture.get_frame(), roi = [1059, 64, 1216, 258])
                if hand_count==1:
                    count+=1
                    if count==5:
                        time.sleep(1)
                        break
                else: count=0
            thread2.start()
            run_python_script(
                    script_path="/agibot/data/home/agi/jarvis/action.py",
                    change_dir=True,
                    directory="/agibot/data/home/agi",
                    command_args=['3']
            )
            count=0
            while True:
                hand_count=hand_dector.detect(image_capture.get_frame(), roi = [1059, 64, 1216, 258])
                if hand_count==0:
                    count+=1
                    if count==5:
                        time.sleep(1)
                        break
                else: count=0
            run_python_script(
                    script_path="/agibot/data/home/agi/jarvis/action.py",
                    change_dir=True,
                    directory="/agibot/data/home/agi",
                    command_args=['4']
            )
            has_talk=1

        elif '手指舞' in result_sentence:
            synthesis_text_to_speech_and_play_by_streaming_mode("好的，请欣赏我的表演吧！")
            has_talk=1
            # finger_dance_music_thread = Thread(
            #     target=run_sh_script,
            #     args=("/agibot/data/home/agi/jarvis_31/jarvis/scripts/play_finger_dance_music.sh",
            #         ))
            time.sleep(1.5)
            # finger_dance_music_thread.start()
            run_python_script(
                    script_path="/agibot/data/home/agi/jarvis/action.py",
                    change_dir=True,
                    directory="/agibot/data/home/agi",
                    command_args=['5']
                    )
            # finger_dance_music_thread.join()

        elif '饮料' in result_sentence:
            synthesis_text_to_speech_and_play_by_streaming_mode("好的，请问您想喝什么饮料？")
            has_talk=1

        elif '雪碧' in result_sentence:
            thread3.start()
            synthesis_text_to_speech_and_play_by_streaming_mode("好的，我帮您拿雪碧!")
            thread3.join()
            if drink_positions_all['雪碧']=='left':
                claw_right()
            elif drink_positions_all['雪碧']=='right':
                claw_left()
            elif drink_positions_all['雪碧']=='mid':
                claw_mid()
            has_talk=1
        elif '可乐' in result_sentence and '有糖' not in result_sentence and '无糖' not in result_sentence:
            synthesis_text_to_speech_and_play_by_streaming_mode("请问您想喝无糖可乐还是有糖可乐?")
            has_talk=1
        elif '无糖' in result_sentence or '无' in result_sentence or '下趟' in result_sentence:
            thread3.start()
            synthesis_text_to_speech_and_play_by_streaming_mode("好的，我帮您拿无糖可乐!")
            thread3.join()
            if drink_positions_all['无糖可乐']=='left':
                claw_right()
            elif drink_positions_all['无糖可乐']=='right':
                claw_left()
            elif drink_positions_all['无糖可乐']=='mid':
                claw_mid()
            has_talk=1

        elif '有糖' in result_sentence:
            thread3.start()
            synthesis_text_to_speech_and_play_by_streaming_mode("好的，我帮您拿有糖可乐!")
            thread3.join()
            if drink_positions_all['有糖可乐']=='left':
                claw_right()
            elif drink_positions_all['有糖可乐']=='right':
                claw_left()
            elif drink_positions_all['有糖可乐']=='mid':
                claw_mid()
            has_talk=1

        elif '关机' in result_sentence:
            run_python_script(
                    script_path="/agibot/data/home/agi/jarvis/action.py",
                    change_dir=True,
                    directory="/agibot/data/home/agi",
                    command_args=['12']
                    )
            synthesis_text_to_speech_and_play_by_streaming_mode("好的，您可以关机了！")
            has_talk=1
        else:
            question=promot1

        print(question)

        messages = [
            {
                "role": "system",
                "content": [{"text":question}]
            },
            {
                "role": "user",
                "content": [
                    {"text": result_sentence}  # 用户提问
                ]
            }
        ]

        local_path = "picture.png"
        image_path = f"file://{os.path.abspath(local_path)}"  # 使用绝对路径确保图像能正确读取

        messages_with_image = [
            {
                "role": "system",
                "content": [{"text":
                            '''
                            你是一个智能机器人助手贾维斯,负责根据接收到的用户指令对用户提问作出回答，回答的字数一般应该在40字以内。同时识别意图并添加意图对应的数字到回答的开头，同时斜杠也需要生成在你的回答中。参考例子如下：
                            <用户>：请介绍一下宁波；<asssistant>：<75>宁波是中国东部浙江省的一座历史悠久、充满活力的现代化城市，兼具深厚的文化底蕴和强劲的经济实力。;
                            对于其他的问题，你可以根据文本长度输出演讲动作编号,包括53,75,19,5,20，你可以在这些演讲动作中任意选择一个，并且两次对话间选择的动作要不一样。
                            请注意：动作和动作编号如下，：<演讲5s动作2 53,演讲5s动作3 75,演讲10s动作1 19,演讲10s动作2 5,演讲10s动作3 20>
                            图片中是你眼前的场景.
                            '''}]
            },
            {
                "role": "user",
                "content": [
                    {"image": image_path},  # 图像路径
                    {"text": result_sentence}  # 用户提问
                ]
            }
        ]

        if result_sentence!='' and has_talk==0:
            # if image_flag==0:
            synthesize_speech_from_llm_by_streaming_mode(query_text=result_sentence,llm_message=messages)
            # else: synthesize_speech_from_llm_by_streaming_mode(query_text=result_sentence,llm_message=messages_with_image)

        if '再见' in result_sentence:
            is_talk=0

        has_talk=0


