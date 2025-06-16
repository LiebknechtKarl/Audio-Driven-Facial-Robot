#!/usr/bin/env python3
import subprocess
import os
MASTER_DIC = os.path.dirname(os.path.dirname(__file__))
from playsound import playsound

# 播放音频后发布消息
def play_wav(voice_path):
    print('语音路径', voice_path)
    try:
        # 定义要执行的命令      执行命令
        # command = ['aplay', '-D', 'plughw:1,0', voice_path]
        command = ['aplay', voice_path]
        subprocess.run(command, check=True)

        # playsound(voice_path)                                   # 使用playsound播放语音文件        
    except Exception as e:
        print('播放语音文件失败')

if __name__ == '__main__':
    voice_path = MASTER_DIC +'/material/voice/droid.wav'
    play_wav(voice_path)                                        # 播放语音    
