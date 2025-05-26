from utils.audio_player import PlayWav
from utils.servo_controller import ControlServo 
from utils.random_actions_model import Msg_Parameter
from utils.csv_time_model import csv_time
import os
import sys
MASTER_DIC = os.path.dirname(os.path.dirname(__file__))
# import thread
import threading



def test_complete(success):                                                 # 设置的任务执行接口
    print(success) 

class Msg:
    pass  # 初始时没有 data 属性
# setattr(Msg, 'data', 'russian_welcome')                                     # 给类 Msg 添加属性 data        这样设置是为了和 ros2衔接
setattr(Msg, 'data', 'art')                                     # 给类 Msg 添加属性 data        这样设置是为了和 ros2衔接
# setattr(Msg, 'data', 'liu')                                     # 给类 Msg 添加属性 data        这样设置是为了和 ros2衔接
# setattr(Msg, 'data', 'liu1')                                     # 给类 Msg 添加属性 data        这样设置是为了和 ros2衔接

from concurrent.futures import ThreadPoolExecutor

def wav_servo_thread(msg) :

    msg_para = Msg_Parameter(MASTER_DIC)
    voice_path,csv_path, FrameNumber , duration_s = msg_para.wav_csv_parameter(msg)

    total_bs_rpy = csv_time(csv_path, FrameNumber , duration_s)  

    Function_play = PlayWav(test_complete)
    # Function_play.play_voice(voice_path)                               # 播放语音

    Function_control = ControlServo(test_complete)     
    # controller.read_time_stamp_bs(total_bs_rpy)     

    thread_pool  = ThreadPoolExecutor(max_workers=2)

    thread_pool.submit(Function_play.play_voice , voice_path)           # wav
    thread_pool.submit(Function_control.control_based_stamp, total_bs_rpy)     # csv




if __name__ == '__main__':
    msg = Msg()



    wav_servo_thread(msg)