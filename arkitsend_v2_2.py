# 准备工作 ：确定人头的型号
import os , sys
os.environ["ROBOT_ID"] = "v2_2"

# 函数初始化
# sys.path.append("/media/ubuntu/1T1/ubuntu_data/nlp/demo_47_audio_control/ulaa_head_250211/src/ulaa_head/ulaa_head/utils/servo")

# from v2.arkitCtrl import ArkitCtrl
from utils.servo.v2.arkitCtrl import ArkitCtrl

port_head = '/dev/ttyACM1' # 头部串口
port_mouth = '/dev/ttyACM0' # 嘴巴串口
arkit = ArkitCtrl(port_head, port_mouth) # 串口初始化
arkit.startCtrlThread() # 启动线程
# print(arkit.init_head_dict,arkit.init_mouth_dict) # 读取舵机默认的初始值
# servo_init =  {**arkit.init_head_dict, **arkit.init_mouth_dict}
# arkit.setServo(servo_init) # 输入舵机的名称和归一化后的系数进行人头控制

# 示例
# 舵机控制 -- 单个或多个舵机控制
servo_dict = {  "left_blink"          : 0.5,  # 眼皮向上 [0,0.5,1] 眼皮向下
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


print(servo_dict)
arkit.setServo(servo_dict)

# blendshape系数控制 -- 单个或多个blendshape控制
# 舵机系数转换
# from bs2servo import get_bs_dict, BStoServos, get_servo_head_dict, get_servo_mouth_dict
# data_in = [] # blendshape系数数组
# bs_dict = get_bs_dict(data_in) # 转为blendshape系数字典
# ROBOT_ID = os.getenv("ROBOT_ID", "v2_1") # 读取机器人型号的环境变量
# data_in_num = 52 # blendshape系数数组数量52 或者 61
# mode_name = "emotalk" # 模型的名称 可以不输入
# servo_head, servo_mouth = BStoServos(bs_dict, data_in_num, ROBOT_ID,mode_name)  # blendshape转为舵机系数
# servo_mouth_dict = get_servo_mouth_dict(servo_mouth)
# arkit.setServo(servo_mouth_dict)