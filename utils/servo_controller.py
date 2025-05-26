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
sys.path.append(MASTER_DIC)
# 准备工作 ：确定人头的型号
os.environ["ROBOT_ID"] = "v2_2"
from model.bs51_servo import manual_model   
from utils.servo.v2.arkitCtrl import ArkitCtrl , HeadCtrl , MouthCtrl
from random_actions_model import FaceBlendShape , eye_action, eye_level , simulate_random_direction_head_movement , simulate_random_head_whole_body , simulate_random_head_dian
from csv_time_model import csv_time



class ControlServo():
    def __init__(self, publish_complete = print):
        self.OldName = ""
        self.FrameNumber = 30

        port_head = '/dev/ttyACM1'
        port_mouth = '/dev/ttyACM0'        
        self.headCtrl = HeadCtrl(port_head)    # 921600
        self.mouthCtrl = MouthCtrl(port_mouth) # 921600
        self.arkit = ArkitCtrl(port_head, port_mouth) # 串口初始化
        self.arkit.startCtrlThread() # 启动线程
        self.publish_complete = publish_complete

        # 舵机控制 -- 单个或多个舵机控制
        self.servo_dict = { "left_blink"          : 0.5,  # 眼皮向上 [0,0.5,1] 眼皮向下
                            "left_eye_erect"      : 0.5,  # 眼球向上 [0,0.5,1] 眼球向下
                            "left_eye_level"      : 0.5,  # 眼球向右 [0,0.5,1] 眼球向左
                            "left_eyebrow_erect"  : 0.0,  #         [0,0.01,1] 眉毛上挑
                            "left_eyebrow_level"  : 0.0,  #         [0,0.01,1] 皱眉（眉毛向眉心运动）
                            "right_blink"         : 0.5,  # 眼皮向上 [0,0.5，1] 眼皮向下
                            "right_eye_erect"     : 0.5,  # 眼球向上 [0,0.5,1] 眼球向下
                            "right_eye_level"     : 0.5,  # 眼球向右 [0,0.5,1] 眼球向左
                            "right_eyebrow_erect" : 0.0,  #         [0,0.01,1] 眉毛上挑
                            "right_eyebrow_level" : 0.0,  #         [0,0.01,1] 皱眉（眉毛向眉心运动）
                            "head_dian"           : 0.5,  # 向上抬头 [0,0.5,1] 向下低头
                            "head_yao"            : 0.5,  # 右转 [0,0.5,1] 左转
                            "head_bai"            : 0.5,  # 右摆 [0,0.5,1] 左摆

                            "mouthUpperUpLeft"    : 0.76, # * 上嘴唇向上 [0,0.76,1] 上嘴唇向前 
                            "mouthUpperUpRight"   : 0.76,
                            "mouthLowerDownLeft"  : 0.2,  # * 下嘴唇向前[0,0.2,1] 下嘴唇向下
                            "mouthLowerDownRight" : 0.2,

                            "mouthCornerUpLeft"   : 0.23, # * 嘴角前凸 [0,0.23,1] 嘴角上扬
                            "mouthCornerUpRight"  : 0.23,
                            "mouthCornerDownLeft" : 0.5,  # * 嘴角向下 [0,0.5,1] 嘴角前凸（暂不使用）
                            "mouthCornerDownRight": 0.5,

                            "jawFrontLeft"        : 0.01, #        [0,0.01,1] 下巴向下
                            "jawFrontRight"       : 0.01,
                            "jawBackLeft"         : 0.5,  # 下巴向后 [0,0.5,1] 下巴向前
                            "jawBackRight"        : 0.5,
                            } # 输入需要控制的舵机名称和系数    

    # 控制舵机
    def send_control_msgs(self, head_list, mouth_list):
        try:
            print(head_list,'===========================')

            # 用数据替换 servo_dict 的值
            self.servo_dict.update(zip(self.servo_dict.keys(), head_list+mouth_list))
            self.arkit.setServo(self.servo_dict)
        except Exception as e:
            print(f"Failed to send control messages: {e}")

    def find_nearest_letter(self,total_bs_rpy, input_time):
        # 找到离输入时间最近的时间点对应的字母
        min_diff = float('inf')  # 初始化最小时间差为无穷大
        # nearest_letter = None
        bs = None
        rpy = None
        for row in total_bs_rpy:
            time_diff = abs(input_time - row[0])
            if time_diff < min_diff:
                min_diff = time_diff
                bs = row[1]
                rpy = row[2]
        return bs,rpy


    def control_based_stamp(self, total_bs_rpy) :
        # 获取当前时间
        start_time = time.time()
        while True:
            current_elapsed_time = time.time() - start_time
            bs, rpy = self.find_nearest_letter(total_bs_rpy , current_elapsed_time)
            head_list, mouth_list = manual_model(bs, rpy)
            self.send_control_msgs(head_list, mouth_list)

            time.sleep(0.005)  # 短暂休眠，避免重复输出

            if current_elapsed_time >= total_bs_rpy[-1][0]:
                print("程序结束")
                break



def test_complete(success):                                                 # 设置的任务执行接口
    print(success) 

class Msg:
    pass  # 初始时没有 data 属性
setattr(Msg, 'data', 'art')                                     # 给类 Msg 添加属性 data        这样设置是为了和 ros2衔接

from random_actions_model import Msg_Parameter


def main():
    msg = Msg()

    msg_para = Msg_Parameter(MASTER_DIC)
    voice_path,csv_path, FrameNumber , duration_s = msg_para.wav_csv_parameter(msg)
    total_bs_rpy = csv_time(csv_path, FrameNumber , duration_s)   

    print(total_bs_rpy)     
    controller = ControlServo()     
    controller.control_based_stamp(total_bs_rpy)              

if __name__ == '__main__':
    main()