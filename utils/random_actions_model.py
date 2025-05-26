import numpy as np
import time
import matplotlib.pyplot as plt
from enum import Enum


class FaceBlendShape(Enum):

    # 眉毛5个自由度
    BrowDownLeft = 1
    BrowDownRight = 2
    BrowInnerUp = 3
    BrowOuterUpLeft = 4
    BrowOuterUpRight = 5

    # 脸颊 3个自由度
    CheekPuff = 6
    CheekSquintLeft = 7
    CheekSquintRight = 8

    # 眼睛 14个自由度
    EyeBlinkLeft = 9
    EyeBlinkRight = 10
    EyeLookDownLeft = 11
    EyeLookDownRight = 12
    EyeLookInLeft = 13
    EyeLookInRight = 14
    EyeLookOutLeft = 15
    EyeLookOutRight = 16
    EyeLookUpLeft = 17
    EyeLookUpRight = 18
    EyeSquintLeft = 19
    EyeSquintRight = 20
    EyeWideLeft = 21
    EyeWideRight = 22

    # 下颚 4个自由度
    JawForward = 23
    JawLeft = 24
    JawOpen = 25
    JawRight = 26

    # 嘴部 23个自由度
    MouthClose = 27
    MouthDimpleLeft = 28
    MouthDimpleRight = 29
    MouthFrownLeft = 30
    MouthFrownRight = 31
    MouthFunnel = 32
    MouthLeft = 33
    MouthLowerDownLeft = 34
    MouthLowerDownRight = 35
    MouthPressLeft = 36
    MouthPressRight = 37
    MouthPucker = 38
    MouthRight = 39
    MouthRollLower = 40
    MouthRollUpper = 41
    MouthShrugLower = 42
    MouthShrugUpper = 43
    MouthSmileLeft = 44
    MouthSmileRight = 45
    MouthStretchLeft = 46
    MouthStretchRight = 47
    MouthUpperUpLeft = 48
    MouthUpperUpRight = 49

    # 鼻子 2个自由度
    NoseSneerLeft = 50
    NoseSneerRight = 51


"""
模拟人随机眨眼，闭眼为1，正常睁眼为0.5，每2-3秒眨眼一次，生成的数值在[0.5, 1]区间。

参数:
- duration: 模拟的总时长（秒）。
- fps: 每秒帧数，默认值为60。
- min_interval: 最小眨眼间隔时间（秒）。
- max_interval: 最大眨眼间隔时间（秒）。
- min_blink: 最小眨眼值，表示睁眼的程度，默认值为0.5。
- max_blink: 最大眨眼值，表示闭眼的程度，默认值为1。

返回:
- blinks: 一个数组，包含每帧的眨眼程度。
"""
def eye_action(duration, fps=60, min_interval=1.5, max_interval=2, min_blink=0.47, max_blink=1):

    total_frames = int(duration * fps)     # 总帧数
    time = np.linspace(0, duration, total_frames)

    # 初始化眨眼数组，全为正常睁眼值
    blinks = np.full(total_frames, min_blink)

    # 生成随机眨眼时间点
    current_time = 0

    # 使用while循环，在总时长内生成随机眨眼时间点。
    while current_time < duration:

        # 每次循环生成一个随机的眨眼间隔时间，间隔范围在min_interval和max_interval之间。
        interval = np.random.uniform(min_interval, max_interval)

        blink_time = current_time + interval 
        if blink_time < duration:

            # 眨眼过程中心 frame
            blink_frame = int(blink_time * fps)

            # 设置眨眼开始和结束frame   （防止出现 不在 0-总frame  之间的frame）
            start_frame = max(0, blink_frame - int(fps * 0.1))  # 眨眼开始前0.1秒
            end_frame = min(total_frames, blink_frame + int(fps * 0.1))  # 眨眼结束后0.1秒

            # start_frame = max(0, blink_frame - int(fps * 0.2))  # 眨眼开始前0.1秒
            # end_frame = min(total_frames, blink_frame + int(fps * 0.2))  # 眨眼结束后0.1秒

            # 模拟眨眼过程
            # 眨眼的睁眼过程 插值
            blinks[start_frame:blink_frame] = np.linspace(min_blink, max_blink, blink_frame - start_frame)
            # 眨眼的闭眼过程 插值
            blinks[blink_frame:end_frame] = np.linspace(max_blink, min_blink, end_frame - blink_frame)
        current_time += interval

    return blinks


# 对应眼睛平动
"""
模拟人 眼睛随机平动

参数:
- duration: 模拟的总时长（秒）。
- fps: 每秒帧数，默认值为60。
"""
def eye_level(duration, fps=60):   
    total_frames = int(duration * fps)                          # 总帧数
    time = np.linspace(0, duration, total_frames)               # 时间帧
    base_wave = 0.5* np.sin(4 * np.pi  * time * 0.5)            # 反复眨眼
    for i in range(len(base_wave)):
        # if i/fps <= 6 or i/fps >=8 :
        # if i/fps <= 7.5 or i/fps >=8.5 :
        if i/fps <= 6 or i/fps >=7 :                            # 6-7s 之间不动   专门为一个场景设计的
            base_wave[i] = 0
    return base_wave

"""
模拟正常人不自觉的头部左右随机方向动作，且摇头幅度随机，并确保一半以上时间头部复位。

参数:
- duration: 模拟的总时长（秒）。
- fps: 每秒帧数，默认值为60。
- max_angle: 最大摇动角度（度），默认值为5度。
- frequency: 基础摇动的频率（Hz），默认值为0.1 Hz（每10秒一个完整周期）。

返回:
- angles: 一个数组，包含每帧的头部摇动角度。
"""
# def simulate_random_direction_head_movement(duration, fps=60, max_angle=15, frequency=0.4):
def simulate_random_direction_head_movement(duration, fps=60, max_angle=10, frequency=0.15):

    max_angle_ = max_angle

    total_frames = int(duration * fps)
    time = np.linspace(0, duration, total_frames)

    # 生成正弦波
    # base_wave = np.sin(2 * np.pi * frequency * time)
    base_wave = np.sin(4 * np.pi * frequency * time)

    # 随机方向和随机幅度：每个周期随机选择方向和幅度
    num_cycles = int(duration * frequency)
    directions = np.random.choice([-1, 1], size=num_cycles)
    amplitudes = np.random.uniform(0.5, 1.0, size=num_cycles) * max_angle

    # 应用随机方向和幅度
    cycle_length = int(fps / frequency)
    for i in range(num_cycles):
        start = i * cycle_length
        mid = min(start + cycle_length // 2, total_frames)
        end = min(start + cycle_length, total_frames)

        # 前半段摇头
        base_wave[start:mid] *= directions[i] * amplitudes[i]

        # 后半段逐渐复位
        base_wave[mid:end] = np.linspace(base_wave[mid], 0, end - mid)

    # noise = np.random.normal(0, 0.2, total_frames)
    noise = np.random.normal(0, 0.01, total_frames)   # 基础的摇头噪声

    angles = base_wave + noise
    angles = np.clip(angles, -max_angle, max_angle)  # 限制角度范围在 [-max_angle, max_angle]

    # 确保初始位置和结束位置为0
    angles[0] = 0
    angles[-1] = 0

    angles = angles/max_angle * max_angle_

    return angles


"""
# 逻辑和内容与  simulate_random_direction_head_movement 相同， 但是本函数专门对应 展示 全身动作 时的头部动作
模拟正常人不自觉的头部左右随机方向动作，且摇头幅度随机，并确保一半以上时间头部复位。

参数:
- duration: 模拟的总时长（秒）。
- fps: 每秒帧数，默认值为25。
- max_angle: 最大摇动角度（度），默认值为5度。
- frequency: 基础摇动的频率（Hz），默认值为0.1 Hz（每10秒一个完整周期）。

返回:
- angles: 一个数组，包含每帧的头部摇动角度。
"""
# def simulate_random_head_whole_body(duration, fps=60, max_angle=15, frequency=0.4):
def simulate_random_head_whole_body(duration, fps=60, max_angle=10, frequency=0.2):

    max_angle_ = max_angle

    total_frames = int(duration * fps)
    time = np.linspace(0, duration, total_frames)

    # 生成正弦波
    # base_wave = np.sin(2 * np.pi * frequency * time)
    base_wave = np.sin(4 * np.pi * frequency * time)

    # 随机方向和随机幅度：每个周期随机选择方向和幅度
    num_cycles = int(duration * frequency)
    directions = np.random.choice([-1, 1], size=num_cycles)
    amplitudes = np.random.uniform(0.5, 1.0, size=num_cycles) * max_angle

    # 应用随机方向和幅度
    cycle_length = int(fps / frequency)
    for i in range(num_cycles):
        start = i * cycle_length
        mid = min(start + cycle_length // 2, total_frames)
        end = min(start + cycle_length, total_frames)

        # 前半段摇头
        base_wave[start:mid] *= directions[i] * amplitudes[i]

        # 后半段逐渐复位
        base_wave[mid:end] = np.linspace(base_wave[mid], 0, end - mid)

    # noise = np.random.normal(0, 0.2, total_frames)
    noise = np.random.normal(0, 0.01, total_frames)

    angles = base_wave + noise
    angles = np.clip(angles, -max_angle, max_angle)  # 限制角度范围在 [-max_angle, max_angle]

    # 确保初始位置和结束位置为0
    angles[0] = 0
    angles[-1] = 0

    angles = angles/max_angle * max_angle_
    return angles

# 模拟点头动作，指定  6.5-7.5s 时刻之间完成一个点头周期
def simulate_random_head_dian(duration, fps=60, max_angle=15):
    total_frames = int(duration * fps)
    time = np.linspace(0, duration, total_frames)
    base_wave = 0.5* np.sin(4 * np.pi  * time * 0.5)
    for i in range(len(base_wave)):
        # if i/fps <= 7.5 or i/fps >=8.5 :
        if i/fps <= 6.5 or i/fps >=7.5 :     # 其余时刻动作归0

            base_wave[i] = 0
    base_wave = base_wave * 45
    return base_wave

# def msg_parameter(msg):

import os
from pydub import AudioSegment
import pandas as pd

class Msg_Parameter():
    def __init__(self,master_dic ):
        self.OldName = ''

        self.wav_csv_dic = master_dic + '/material'

        self.voice_dic = self.wav_csv_dic + '/voice'
        self.csv_dic = self.wav_csv_dic + '/csv'
        self.FrameNumber = 30

    def wav_csv_parameter(self,msg) :
        if self.OldName == msg.data  and self.flag == False:
            self.OldName = msg.data
            return
        self.OldName = msg.data
        name_voice = msg.data
        name_csv = msg.data

        # 根据受到的相对路径 输出 csv&wav 绝对路径
        if not name_csv.endswith('.csv'):
            name_csv = f"{name_csv}.csv"
        if not name_voice.endswith('.wav'):
            name_voice = f"{name_voice}.wav"

        voice_path = self.voice_dic +name_voice
        csv_path = self.csv_dic+name_csv

        # csv&wav 绝对路径    寻址
        if not os.path.exists(voice_path):
            print('语音文件不存在: ',voice_path)
            # 发送播放失败消息
            self.publish_complete("0")
            return

        # csv&wav 绝对路径    寻址
        if not os.path.exists(csv_path):
            print('csv文件不存在: ',csv_path)
            # 发送播放失败消息
            self.publish_complete("0")
            return
        


        try:
            audio = AudioSegment.from_wav(voice_path)
            # self.get_logger().info(f"音频文件加载成功: {voice_path}")
            print(f"音频文件加载成功: {voice_path}")
        except Exception as e:
            # self.get_logger().info(f"加载音频文件时出错: {e}")
            print(f"加载音频文件时出错: {e}")


        ## 计算输出  wav&csv文件相关信息
        duration_ms = len(audio)                            # 获取音频文件的播放时长（以毫秒为单位）
        duration_s = duration_ms / 1000.0                   # 将时长转换为秒
        df = pd.read_csv(csv_path)                          # 读取 CSV 文件
        row_count = df.shape[0]                             # 获取行数
        self.FrameNumber = row_count/duration_s             # 计算 每秒对应多少行

        return voice_path,csv_path, self.FrameNumber , duration_s
    
class Msg:
    pass  # 初始时没有 data 属性
# setattr(Msg, 'data', 'russian_welcome')                                     # 给类 Msg 添加属性 data        这样设置是为了和 ros2衔接
setattr(Msg, 'data', 'art')   

def main():
    msg = Msg()

    msg_para = Msg_Parameter('/home/fu/Desktop/ubuntu_data/nlp/demo_51_qiangnao_voice/dda/')


    print(msg_para.wav_csv_parameter(msg))





    duration = 10
    t_fps = np.linspace(0, duration, int(duration * 60))
    action = simulate_random_head_dian(duration)

    # 绘制图形
    plt.plot(t_fps, action)
    plt.show()

if __name__ == '__main__':
    main()









