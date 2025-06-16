</br>


</br>.
</br>├── __init__.py
</br>├── model
</br>│   └── bs51_servo.py
</br>├── readme.md
</br>└── utils
</br>    ├── servo
</br>    │   └── v2
</br>    │       ├── HeadCtrlKit.py
</br>    │       └── MouthCtrlKit.py
</br>    └── servo_controller.py



## model/bs51_servo.py
作用：将 blendshape 系数 (bs_dict) 和 头部姿态角 (rpy_angles) 映射为用于控制机器人面部舵机（或虚拟面部）的 舵机控制参数（head 和 mouth）。

map_range(x, from_min, from_max, to_min, to_max)  
    通用线性映射函数，将数值 x 从原始区间 [from_min, from_max] 映射到目标区间 [to_min, to_max]。
    如 map_range(rpy_angles[0], -45, 45, 0, 1) 表示 rpy_angles[0] ∈ [-45, 45]）转为舵机/参数控制区间（如 ∈ [0, 1]）。

manual_model(bs_dict, rpy_angles) 
    输入：
        bs_dict: blendshape 系数字典，键为blandshape键名，值为 0～1 浮点数。
        rpy_angles: 三元组 [roll, pitch, yaw]，表示头部姿态角（单位通常为度），用于控制头部方向。
    输出：
        分别控制 head 和 mouth 的舵机 参数

## utils/servo/v2/HeadCtrlKit.py
作用:控制表情机器人头部的舵机动作，通过串口通信将舵机角度指令发送给舵机控制板。

Servo 类 —— 舵机配置数据结构
    用于表示单个舵机的参数，包括：
        id：舵机编号。
        jdStart：初始角度（未使用）。
        jdMax / jdMin：舵机允许的最大 / 最小角度。
        fScale：发送给串口的缩放因子，将角度映射为PWM信号。
        fOffSet：偏移量（通常为 0）。
        pos：当前舵机位置。
        dir：方向标志位（是否取反控制）。

HeadCtrl 类 —— 表情舵机控制器
作用：
    继承 serial.Serial，实现串口通信；
    储存头部13个表情参数；
    将归一化控制信号（0～1）转换为舵机角度并发送控制帧。

## utils/servo/v2/MouthCtrlKit.py
作用:驱动表情机器人的 嘴部表情舵机，通过串口向舵机控制板发送控制指令。  

Servo 类 -- 略，与utils/servo/v2/HeadCtrlKit.py 类似

MouthCtrl 类（主控制类）
    继承 serial.Serial，实现串口通信；
    储存嘴部12个表情参数；
    将归一化控制信号（0～1）转换为舵机角度并发送控制帧。







