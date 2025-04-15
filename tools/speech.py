import pyaudio
import wave
import os
from datetime import datetime
from modelscope import (
    snapshot_download, AutoModelForCausalLM, AutoTokenizer
)
import torch

# 初始化模型（保持原有的模型加载代码）
model_id = 'qwen/Qwen-Audio-Chat'
revision = 'master'
model_dir = snapshot_download(model_id, revision=revision)
torch.manual_seed(1234)

tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
if not hasattr(tokenizer, 'model_dir'):
    tokenizer.model_dir = model_dir
model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", trust_remote_code=True).eval()
response, history = model.chat(tokenizer, '介绍一下你自己.- 我叫贾维斯，是均胜集团自主研发的一款新型人形机器人。我集成了多种先进的传感器和AI技术，具有优秀的感知、决策能力，能够实现多种复杂的技术。我的主要工作场景在工业上。我可以搬运各种物料、操作机械和进行简单的装配工作。你最喜欢的大学是哪所? 是清华大学。你身上有哪些传感器?我的颈部有一颗激光雷达和一个深度相机，胸前有三个RGB相机，髋部还有一个深度相机。此外，我还配备了高精度的IMU传感器和六维力传感器。这些传感器都为我提供了良好的感知能力，让我能感知周围的一切环境并作出反应。你双手电机的负载是多少?我的一只手可以抬起五公斤的重物，两只手协力可以抬起重达十公斤的物体。你的电池有多大？续航怎么样？我具备了一块可快拆更换的大容量电池，一块满电的电池可以支持我持续工作达2个小时。今天的天气怎么样?很抱歉，我暂时不具备联网查询当天天气的能力，但是我的开发者告诉我在不久的将来我就会具备这个能力。今天是几号?很抱歉，我暂时不具备联网的能力，所以我不知道今天是几号。请介绍一下均胜集团。均胜集团是一家全球领先的汽车电子与汽车安全技术供应商，致力于推动汽车智能化与安全化发展。公司成立于2004年，总部位于中国宁波，通过多年的发展和战略性并购，均胜现已成为全球汽车零部件百强企业之一。机器人产业是均胜集团的一条新赛道，现在已研发了贾维斯一代以及贾维斯二代两代人形机器人。介绍一下宁波的产业情况。宁波是浙江省经济发展强劲的城市之一，其产业结构以先进制造业和现代服务业为主，体现了多元化和高质量发展的特点。宁波有着完善的制造业体系，被誉为“工业立市”。其主要支柱产业包括汽车及零部件、石油化工、纺织服装、电工电器等。近年来，宁波也大力发展了新材料、人工智能、新能源、海洋经济和量子科技等未来产业。例如，在新材料领域，宁波专注于石墨烯、柔性显示等前沿科技；新能源方面，光伏和风电装机容量在全省居首。', history=history)
def record_audio(duration=5):
    """使用PyAudio录制音频"""
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000

    p = pyaudio.PyAudio()

    # 确保存在assets/audio目录
    os.makedirs("assets/audio", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"recording_{timestamp}.wav"
    filepath = os.path.join("assets/audio", filename)

    print(f"开始录音 {duration} 秒...")
    
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    for i in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("录音完成!")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # 保存录音文件
    wf = wave.open(filepath, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filepath

def process_audio(audio_path, history=None):
    """处理音频文件并获取模型回答"""
    query = tokenizer.from_list_format([
        {'audio': audio_path},
        {'text': '请回答这个问题了，注意不要分点作答。'},
    ])
    response, new_history = model.chat(tokenizer, query=query, history=history)
    return response, new_history

def main():
    print("欢迎使用语音识别系统!")
    print("按Enter开始录音（默认5秒），按q退出")
    
    
    while True:
        user_input = input("\n> ")
        if user_input.lower() == 'q':
            print("退出程序...")
            break
            
        try:
            # 录制音频
            audio_file = record_audio()
            
            # 处理音频并获取回答，同时更新历史记录
            response, history = process_audio(audio_file, history)
            print("\n模型回答:", response)
            
        except Exception as e:
            print(f"发生错误: {str(e)}")

if __name__ == "__main__":
    main()