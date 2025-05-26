import numpy as np
import os
import sys
MASTER_DIC = os.path.dirname(os.path.dirname(__file__))
sys.path.append(MASTER_DIC)
# 准备工作 ：确定人头的型号
os.environ["ROBOT_ID"] = "v2_2"
from random_actions_model import FaceBlendShape , eye_action, eye_level , simulate_random_direction_head_movement , simulate_random_head_whole_body , simulate_random_head_dian

def csv_time(csv_path, FrameNumber = 60, duration =1) :

    number_list = []
    # 通过csv文件信息计算 语音时间
    with open(csv_path, 'r') as file:
        line_count = sum(1 for line in file)
    duration = line_count/60 + 1   # 时间

    # 迭代时间，确保根据时间生成的动作数量不小于 csv 行数
    while True :
        if len(simulate_random_direction_head_movement(duration)) < line_count :
            duration = duration * 1.1
        else :
            break

    # rpy是专门设计的随机动作，独立于csv的预设动作
    # rpy     [点头(此处置0)，      摇头（随机摇头），      摆头（此处置0）     ，  眨眼     ，眼睛平动       ]
    rpy = [np.append(simulate_random_direction_head_movement(duration)[:line_count-1], 0.5)*0,
        np.append(simulate_random_direction_head_movement(duration)[:line_count-1], 0),
        np.append(simulate_random_direction_head_movement(duration)[:line_count-1], 0)*0,
        np.append(eye_action(duration)[:line_count-1], 0.47),
        np.append(eye_level(duration)[:line_count-1], 0.)
        ]  
            
    rpy = np.vstack(rpy).T
    total_bs_rpy = []
    time_step = 0

    # 遍历csv&rpy 中的动作，发送数据给舵机以控制
    with open(csv_path, 'r') as file:

        # 遍历 csv&rpy参数
        for (line,rpy_) in zip(file, rpy) :
            numbers = line.split(',')                                       # 将一行文本按空格分割成多个数值
            numbers = [float(num) for num in numbers]                       # 将数值转化为浮点数
            number_list.append(numbers)                                     # 将这一行的数值加入到列表中

            blendshape_dict = {}
            if numbers is not None:
                for shape in FaceBlendShape:
                    blendshape_dict[shape.name] = numbers[shape.value-1]

            # 使用 rpy 中专门设计的参数替换 原本的动作
            blendshape_dict["EyeBlinkLeft"] = rpy_[3]
            blendshape_dict["EyeBlinkRight"] = rpy_[3]
            blendshape_dict["EyeLookOutLeft"] =  rpy_[4]

            total_bs_rpy.append([time_step/FrameNumber , blendshape_dict, rpy_[:-1]])
            time_step+=1

    return total_bs_rpy

def main():

    csv_path, FrameNumber , duration_s = '/home/fu/Desktop/ubuntu_data/nlp/demo_51_qiangnao_voice/dda/material/csv/art.csv', 29.947054930509598, 12.088 
    total_bs_rpy = csv_time(csv_path, FrameNumber , duration_s)   
    print(total_bs_rpy)     

if __name__ == '__main__':
    main()






