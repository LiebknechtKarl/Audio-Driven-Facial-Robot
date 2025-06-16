#!/usr/bin/env python3
import time
import os
import sys
MASTER_DIC = os.path.dirname(os.path.dirname(__file__))
sys.path.append(MASTER_DIC)
from model.bs51_servo import manual_model  
from servo.v2.HeadCtrlKit import HeadCtrl 
from servo.v2.MouthCtrlKit import MouthCtrl 
from utils.Blandshape_Msgs import Emotalk_BS
# csv time stampt
class CsvProcess() :
    def __init__(self, csv_path, FrameNumber = 30,  duration =1, publish_complete = print):
        
        self.csv_path = csv_path
        self.FrameNumber = FrameNumber
        self.duration = duration

        self.publish_complete = publish_complete   
        self.total_bs = self.add_timestamp() 

    def add_timestamp(self) :
        total_bs = []
        time_step = 0
        number_list = []

        # 遍历csv&rpy 中的动作，发送数据给舵机以控制
        with open(self.csv_path, 'r') as file:

            # 遍历 csv&rpy参数
            for line in file :
                numbers = line.split(',')                                       # 将一行文本按空格分割成多个数值
                numbers = [float(num) for num in numbers]                       # 将数值转化为浮点数
                number_list.append(numbers)                                     # 将这一行的数值加入到列表中

                blendshape_dict = {}
                if numbers is not None:
                    for shape in Emotalk_BS:
                        blendshape_dict[shape.name] = numbers[shape.value-1]

                total_bs.append([time_step/self.FrameNumber , blendshape_dict])
                time_step+=1
        return total_bs

    def find_nearest_bs(self, input_time):
        # 找到离输入时间最近的时间点对应的字母
        min_diff = float('inf')  # 初始化最小时间差为无穷大
        # nearest_letter = None
        bs = None
        for row in self.total_bs:
            time_diff = abs(input_time - row[0])
            if time_diff < min_diff:
                min_diff = time_diff
                bs = row[1]
        return bs

if __name__ == '__main__':
    from utils.read_config import get_wav_csv_config

    csv_path = MASTER_DIC + '/material/csv/droid.csv'
    wav_path = MASTER_DIC + '/material/voice/droid.wav'

    (duration_s, FrameNumber) = get_wav_csv_config(wav_path, csv_path)

    csv_process = CsvProcess(csv_path,FrameNumber, duration_s)
    processed_bs = csv_process.add_timestamp()
    # print(processed_bs)
    print(csv_process.find_nearest_bs(1.5))

    ####### -------------  一个具体的控制例子
    port_head = '/dev/ttyACM1'
    port_mouth = '/dev/ttyACM0'        
    headCtrl = HeadCtrl(port_head)    # 921600
    mouthCtrl = MouthCtrl(port_mouth) # 921600

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

        # if current_elapsed_time >= processed_bs[-1][0]:
        if current_elapsed_time >= processed_bs[300][0]:

            print("程序结束, 表情初始化")
            headCtrl.act_init_servo()
            mouthCtrl.act_init_servo()

            break
