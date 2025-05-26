#!/usr/bin/env python3

import numpy as np
import time
from enum import Enum
from concurrent.futures import ThreadPoolExecutor
from pydub import AudioSegment
import pandas as pd
from playsound import playsound

import os
import sys
MASTER_DIC = os.path.dirname(os.path.dirname(__file__))
# 准备工作 ：确定人头的型号
os.environ["ROBOT_ID"] = "v2_2"

sys.path.append(MASTER_DIC + "/utils")
from random_actions_model import Msg_Parameter

class PlayWav():
    def __init__(self, publish_complete):
        # 创建线程池，最大线程数为2
        self.publish_complete = publish_complete
        self.OldName = ""

    # 播放音频后发布消息
    def play_voice(self, voice_path):
        print('语音路径', voice_path)
        try:
            self.flag = False
            playsound(voice_path)                           # 使用playsound播放语音文件
            self.flag = True
            self.publish_complete("1")                      # 播放完成后发送成功消息

        except Exception as e:
            print('播放语音文件失败')
            self.publish_complete("0")                      # 发送播放失败消息

def test_complete(success):                                 # 设置的任务执行接口
    print(success) 

class Msg:
    pass                                                    # 初始时没有 data 属性
setattr(Msg, 'data', 'art')                                 # 给类 Msg 添加属性 data        这样设置是为了和 ros2衔接

def main():
    voice_path = MASTER_DIC +'/material/voice/home_school.wav'
    Function_play = PlayWav(test_complete)
    Function_play.play_voice(voice_path)                    # 播放语音

if __name__ == '__main__':
    main()