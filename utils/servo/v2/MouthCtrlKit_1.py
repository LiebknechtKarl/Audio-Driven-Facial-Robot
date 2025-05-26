from serial import *
import time

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

mouthUpperUpLeft     = Servo(13, 90,  99,  0, 11.1, 0, 0, 1) #左上唇
mouthUpperUpRight    = Servo( 6, 90, 180, 81, 11.1, 0, 0, 0) #右上唇
mouthLowerDownLeft   = Servo( 5, 90, 126, 81, 11.1, 0, 0, 0) #左下唇
mouthLowerDownRight  = Servo(14, 90,  99, 54, 11.1, 0, 0, 1) #右下唇
 
mouthCornerUpLeft    = Servo( 0, 90, 180,  0, 11.1, 0, 0, 1) #左微笑上
mouthCornerUpRight   = Servo( 8, 90, 180,  0, 11.1, 0, 0, 0) #右微笑上
mouthCornerDownLeft  = Servo(12, 90, 180,  0, 11.1, 0, 0, 1) #左微笑下
mouthCornerDownRight = Servo( 7, 90, 180,  0, 11.1, 0, 0, 0) #右微笑下

jawFrontLeft         = Servo( 2, 90, 135, 90, 11.1, 0, 0, 0) #左下颚提
jawFrontRight        = Servo(10, 90,  90, 45, 11.1, 0, 0, 1) #右下颚提
jawBackLeft          = Servo( 1, 90, 135, 45, 11.1, 0, 0, 0) #左下颚拉
jawBackRight         = Servo( 9, 90, 135, 45, 11.1, 0, 0, 1) #右下颚拉

servos = [mouthUpperUpLeft, mouthUpperUpRight, mouthLowerDownLeft, mouthLowerDownRight,
          mouthCornerUpLeft, mouthCornerUpRight, mouthCornerDownLeft, mouthCornerDownRight,
          jawFrontLeft, jawFrontRight, jawBackLeft, jawBackRight
]

class MouthCtrl(Serial):
    #*args, **kwargs 这种写法代表这个方法接受任意个数的参数
    def __init__(self, arg, *args, **kwargs):
        super().__init__(arg, *args, **kwargs)
        if self.is_open:
            print('Open Success')
        else:
            print('Open Error')

        self.mouthUpperUpLeft     = 0.1
        self.mouthUpperUpRight    = 0.1
        self.mouthLowerDownLeft   = 0.2
        self.mouthLowerDownRight  = 0.2

        self.mouthCornerUpLeft    = 0.5
        self.mouthCornerUpRight   = 0.5
        self.mouthCornerDownLeft  = 0.5
        self.mouthCornerDownRight = 0.5

        self.jawFrontLeft         = 0.01
        self.jawFrontRight        = 0.01
        self.jawBackLeft          = 0.5
        self.jawBackRight         = 0.5
        
        self.initValue = self.msgs

    @property
    def msgs(self):
        return [
            self.mouthUpperUpLeft, self.mouthUpperUpRight, self.mouthLowerDownLeft, self.mouthLowerDownRight,
            self.mouthCornerUpLeft, self.mouthCornerUpRight, self.mouthCornerDownLeft, self.mouthCornerDownRight,
            self.jawFrontLeft, self.jawFrontRight, self.jawBackLeft, self.jawBackRight
        ]

    # 定义索引到属性的映射
    _index_to_attr = [
        'mouthUpperUpLeft', 'mouthUpperUpRight', 'mouthLowerDownLeft', 'mouthLowerDownRight',
        'mouthCornerUpLeft', 'mouthCornerUpRight', 'mouthCornerDownLeft', 'mouthCornerDownRight',
        'jawFrontLeft', 'jawFrontRight', 'jawBackLeft', 'jawBackRight'
    ]

    # 通过索引修改属性值
    def __setitem__(self, index, value):
        if index < 0 or index >= len(self._index_to_attr):
            raise IndexError("Index out of range")
        setattr(self, self._index_to_attr[index], value)
        
    def send(self):
        # print(self.msgs)
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


        # for i in range(len(frameData)):
        #     # print("{0:0.2x} ".format(frameData[i]), end='')
        #     # print(frameData[i])
        if self.is_open:
            self.write(frameData)
            # print('send to servo ok')


#直接执行这个.py文件运行下边代码，import到其他脚本中下边代码不会执行
if __name__ == '__main__':
    
    ctrl = MouthCtrl('/dev/ttyACM0')

    ctrl.mouthUpperUpLeft     = 0.1
    ctrl.mouthUpperUpRight    = 0.1
    ctrl.mouthLowerDownLeft   = 0.2
    ctrl.mouthLowerDownRight  = 0.2

    ctrl.mouthCornerUpLeft    = 0.5
    ctrl.mouthCornerUpRight   = 0.5
    ctrl.mouthCornerDownLeft  = 0.5
    ctrl.mouthCornerDownRight = 0.5

    ctrl.jawFrontLeft         = 0.01
    ctrl.jawFrontRight        = 0.01
    ctrl.jawBackLeft          = 0.5
    ctrl.jawBackRight         = 0.5
    print(ctrl.msgs)
    ctrl.send()
    print(ctrl.msgs)