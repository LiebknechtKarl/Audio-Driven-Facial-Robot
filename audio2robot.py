#!/usr/bin/env python3
import time
import os,sys
import threading
MASTER_DIC = os.path.dirname(__file__)
sys.path.append(MASTER_DIC)
from utils.read_config import get_wav_csv_config
from utils.play_wav import play_wav
from utils.csv_process import CsvProcess
from servo.v2.HeadCtrlKit import HeadCtrl 
from servo.v2.MouthCtrlKit import MouthCtrl 
from model.bs51_servo import manual_model

def csv_servo(csv_path,duration_s, FrameNumber):

    csv_process = CsvProcess(csv_path,FrameNumber, duration_s)
    processed_bs = csv_process.add_timestamp()

    start_time = time.time()
    while True :
        current_elapsed_time = time.time() - start_time
        bs_now = csv_process.find_nearest_bs(current_elapsed_time)
        head_list, mouth_list = manual_model(bs_now, [0,0,0])

        headCtrl.setmsg(head_list)
        mouthCtrl.setmsg(mouth_list)
        headCtrl.send()
        mouthCtrl.send()

        time.sleep(0.05)

        if current_elapsed_time >= processed_bs[-1][0]:
            print("程序结束, 表情初始化")
            headCtrl.act_init_servo()
            mouthCtrl.act_init_servo()
            break

if __name__ == '__main__':

    port_head = '/dev/ttyACM1'
    port_mouth = '/dev/ttyACM0'        
    headCtrl = HeadCtrl(port_head)    # 921600
    mouthCtrl = MouthCtrl(port_mouth) # 921600

    csv_path = MASTER_DIC + '/material/csv/art.csv'
    wav_path = MASTER_DIC + '/material/voice/art.wav'

    (duration_s, FrameNumber) = get_wav_csv_config(wav_path, csv_path)
    print(duration_s, FrameNumber)

    thread_wav = threading.Thread(target = play_wav, args =(wav_path,))         # 语音线程
    thread_csv = threading.Thread(target = csv_servo, args =(csv_path,duration_s, FrameNumber,))                         # csv 线程

    thread_csv.start()
    thread_wav.start()

    # 等待线程执行结束
    thread_wav.join()
    thread_csv.join()