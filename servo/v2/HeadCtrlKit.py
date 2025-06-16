from serial import *

# TODO: 从xml文件直接读取配置
class Servo:
    def __init__(self, id, jdStart, jdMax, jdMin, fScale, fOffSet, pos, dir):
        self.id = id
        self.jdStart = jdStart
        self.jdMax = jdMax
        self.jdMin = jdMin
        self.fScale = fScale
        self.fOffSet = fOffSet
        self.pos = pos
        self.dir = dir

left_blink          = Servo(14, 90, 135, 54, 11.1, 0, 0, 1) # 左眨眼
left_eye_erect      = Servo( 0, 90, 117, 63, 11.1, 0, 0, 0) # 左眼竖
left_eye_level      = Servo( 1, 90, 113, 68, 11.1, 0, 0, 0) # 左眼平
left_eyebrow_erect  = Servo(12, 90,  90, 45, 11.1, 0, 0, 1) # 左挑眉
left_eyebrow_level  = Servo(13, 90, 162, 90, 11.1, 0, 0, 0) # 左皱眉

right_blink         = Servo( 5, 90, 126, 45, 11.1, 0, 0, 0) # 右眨眼
right_eye_erect     = Servo( 8, 90, 117, 63, 11.1, 0, 0, 1) # 右眼竖
right_eye_level     = Servo( 9, 90, 113, 68, 11.1, 0, 0, 0) # 右眼平
right_eyebrow_erect = Servo( 7, 90, 135, 90, 11.1, 0, 0, 0) # 右挑眉
right_eyebrow_level = Servo( 6, 90,  90, 27, 11.1, 0, 0, 1) # 右皱眉

head_dian           = Servo(10, 90, 126, 50, 11.1, 0, 0, 1) # 点头
head_yao            = Servo(11, 90, 180,  0, 11.1, 0, 0, 0) # 摇头
head_bai            = Servo( 2, 90, 180,  0, 11.1, 0, 0, 0) # 摆头

servos = [left_blink, left_eye_erect, left_eye_level, left_eyebrow_erect, left_eyebrow_level,
          right_blink, right_eye_erect, right_eye_level, right_eyebrow_erect, right_eyebrow_level,
          head_dian, head_yao, head_bai]

class HeadCtrl(Serial):
    #*args, **kwargs 这种写法代表这个方法接受任意个数的参数
    def __init__(self, arg, *args, **kwargs):
        super().__init__(arg, *args, **kwargs)
        if self.is_open:
            print('Open Success')
        else:
            print('Open Error')

        self.left_blink          = 0.44         # 左眨眼  上 [0.01 - 0.44 - 0.99] 下
        self.left_eye_erect      = 0.5          # 眼球 上 [0.01 - 0.5 - 0.99] 眼下
        self.left_eye_level      = 0.5          # 眼球 右 [0.01 - 0.5 - 0.99] 眼左
        self.left_eyebrow_erect  = 0.0          # 左眉竖 正常 [0.01 -- 0.99] 上(挑)
        self.left_eyebrow_level  = 0.0          # 左眉   正常 [0.01 - 0.5 - 0.99] 右(皱)

        self.right_blink         = 0.44         # 右眨眼  上 [0.01 - 0.44 - 0.99] 下
        self.right_eye_erect     = 0.5          # 眼球 上 [0.01 - 0.5 - 0.99] 眼下
        self.right_eye_level     = 0.5          # 眼球 右 [0.01 - 0.5 - 0.99] 眼左
        self.right_eyebrow_erect = 0.0          # 右眉竖   正常 [0.01 -- 0.99] 上(挑)
        self.right_eyebrow_level = 0.0          # 右眉   正常 [0.01 -- 0.99] 左(皱)

        self.head_dian           = 0.47         # 抬头 [0.01 - 0.47 - 0.99]  低头
        self.head_yao            = 0.5          # 右摇 [0.01 - 0.5 - 0.99] 左摇
        self.head_bai            = 0.5          # 右摆 [0.01 - 0.5 - 0.99] 左摆

        self.init_msg = self.msgs

    @property
    def msgs(self):
        return [
            self.left_blink, self.left_eye_erect, self.left_eye_level, self.left_eyebrow_erect, self.left_eyebrow_level,
            self.right_blink, self.right_eye_erect, self.right_eye_level, self.right_eyebrow_erect, self.right_eyebrow_level,
            self.head_dian, self.head_yao, self.head_bai
        ]

    def setmsg(self, data):
        self.left_blink          = data[0]
        self.left_eye_erect      = data[1]
        self.left_eye_level      = data[2]
        self.left_eyebrow_erect  = data[3]
        self.left_eyebrow_level  = data[4]

        self.right_blink         = data[5]
        self.right_eye_erect     = data[6]
        self.right_eye_level     = data[7]
        self.right_eyebrow_erect = data[8]
        self.right_eyebrow_level = data[9]

        self.head_dian           = data[10]
        self.head_yao            = data[11]
        self.head_bai            = data[12]
    
    def act_init_servo(self):
        self.setmsg(self.init_msg)
        self.send()

    def send(self):
        
        head = 0xaa
        num=0x00
        end=0x2f

        frameData = [head, num]

        servo_num = 0
        #msg[[95,1],[50,1],[],[],[]....]
        for node, servo in zip(self.msgs, servos):
            # print("node和servo的值为：",node,servo.pos)
            msg = (1 - servo.dir) * node + servo.dir * (1 - node)
            node = servo.jdMin+msg*(servo.jdMax-servo.jdMin)
            if node and node != servo.pos: # 目标位置改变
                # print(self.msgs)
                if node != 0: # msg 没有值
                    # 限幅
                    if node > servo.jdMax:
                        node = servo.jdMax
                    if node < servo.jdMin:
                        node = servo.jdMin
                    servo.pos = node
                    node = int((node + servo.fOffSet) * servo.fScale)
                    pos_l = node & 0xFF
                    pos_h = (node >> 8) & 0x07
                    pos_h = pos_h | (servo.id<<3)
                    # print(servo.id)
                    # print(pos_h,pos_l)
                    frameData.extend([pos_h, pos_l])
                    servo_num += 1
        if servo_num == 0:
            return
        # print("servo_num的值为：",servo_num)
        num=servo_num
        frameData[1] = num
        frameData.extend([end])

        if self.is_open:
            self.write(frameData)
            # print('send to servo ok')
        

#直接执行这个.py文件运行下边代码，import到其他脚本中下边代码不会执行
if __name__ == '__main__':

    ctrl = HeadCtrl('/dev/ttyACM1')

    ctrl.left_blink          = 0.5
    ctrl.left_eye_erect      = 0.5
    ctrl.left_eye_level      = 0.5
    ctrl.left_eyebrow_erect  = 0.0
    ctrl.left_eyebrow_level  = 0.0

    ctrl.right_blink         = 0.5
    ctrl.right_eye_erect     = 0.5
    ctrl.right_eye_level     = 0.5
    ctrl.right_eyebrow_erect = 0.0
    ctrl.right_eyebrow_level = 0.0

    ctrl.head_dian           = 0.47
    ctrl.head_yao            = 0.5
    ctrl.head_bai            = 0.6


    # ctrl.left_blink = 0.76  # 左眨眼  上 [0.01 - 0.56 - 0.99] 下
    # ctrl.left_eye_erect = 0.56  # 眼上 [0.01 - 0.56 - 0.99] 眼下
    # ctrl.left_eye_level = 0.5  # 眼右 [0.01 - 0.5 - 0.99] 眼左
    # ctrl.left_eyebrow_erect = 1  # 左眉竖  上(挑) [0.01 - 0.5 - 0.99] 下
    # ctrl.left_eyebrow_level = 0  # 左眉平   右(皱) [0.01 - 0.5 - 0.99] 左

    # ctrl.right_blink = 0.24  # 右眨眼  下 [0.01 - 0.44 - 0.99] 上
    # ctrl.right_eye_erect = 0.5  # 眼上 [0.01 - 0.5 - 0.99] 眼下
    # ctrl.right_eye_level = 0.5  # 眼右 [0.01 - 0.5 - 0.99] 眼左
    # ctrl.right_eyebrow_erect = 0  # 右眉竖  下 [0.01 - 0.5 - 0.99]  上(挑)
    # ctrl.right_eyebrow_level = 1  # 右眉平   右 [0.01 - 0.5 - 0.99] 左(皱)

    # ctrl.head_dian = 0.47  # 低头 [0.01 - 0.47 - 0.99] 抬头
    # ctrl.head_yao = 0.5  # 右摇 [0.01 - 0.5 - 0.99] 左摇
    # ctrl.head_bai = 0.5  # 右摆 [0.01 - 0.5 - 0.99] 左摆




    ctrl.send()
    print(ctrl.msgs)

    ctrl.act_init_servo()



