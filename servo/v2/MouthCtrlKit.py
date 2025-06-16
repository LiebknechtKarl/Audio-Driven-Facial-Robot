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

LUpperLipVert   = Servo(13, 90,  99,  0, 11.1, 0, 0, 1) #左上唇
RUpperLipVert   = Servo( 6, 90, 180, 81, 11.1, 0, 0, 0) #右上唇
LLowerLipVert   = Servo( 5, 90, 126, 81, 11.1, 0, 0, 0) #左下唇
RLowerLipVert   = Servo(14, 90,  99, 54, 11.1, 0, 0, 1) #右下唇
 
LSmile          = Servo( 0, 90, 180,  0, 11.1, 0, 0, 1) #左微笑上
RSmile          = Servo( 8, 90, 180,  0, 11.1, 0, 0, 0) #右微笑上
LSad            = Servo(12, 90, 180,  0, 11.1, 0, 0, 1) #左微笑下
RSad            = Servo( 7, 90, 180,  0, 11.1, 0, 0, 0) #右微笑下

LJawOpen        = Servo( 2, 90, 135, 90, 11.1, 0, 0, 0) #左下颚提
RJawOpen        = Servo(10, 90,  90, 45, 11.1, 0, 0, 1) #右下颚提
LJawForward     = Servo( 1, 90, 135, 45, 11.1, 0, 0, 0) #左下颚拉
RJawForward     = Servo( 9, 90, 135, 45, 11.1, 0, 0, 1) #右下颚拉

servos = [LUpperLipVert, RUpperLipVert, LLowerLipVert, RLowerLipVert,
          LSmile, RSmile, LSad, RSad,
          LJawOpen, RJawOpen, LJawForward, RJawForward
]

class MouthCtrl(Serial):
    #*args, **kwargs 这种写法代表这个方法接受任意个数的参数
    def __init__(self, arg, *args, **kwargs):
        super().__init__(arg, *args, **kwargs)
        if self.is_open:
            print('Open Success')
        else:
            print('Open Error')

        self.LUpperLipVert = 0.1            # 左* 上嘴唇向下 [0,0.1,1] 上嘴唇向上
        self.RUpperLipVert = 0.1            # 右* 上嘴唇向下 [0,0.1,1] 上嘴唇向上
        self.LLowerLipVert = 0.2            # 左* 下嘴唇向上[0,0.2,1] 下嘴唇向下
        self.RLowerLipVert = 0.2            # 右* 下嘴唇向上[0,0.2,1] 下嘴唇向下

        self.LSmile = 0.5                   # 左* 嘴角前凸 [0,0.5,1] 嘴角上扬
        self.RSmile = 0.5                   # 右* 嘴角前凸 [0,0.5,1] 嘴角上扬
        self.LSad = 0.5                     # 左* 嘴角向后下 [0,0.5,1] 嘴角前凸（暂不使用）
        self.RSad = 0.5                     # 右* 嘴角向后下 [0,0.5,1] 嘴角前凸（暂不使用）

        self.LJawOpen = 0.01                # 左* 下巴正常 [0,0.01,1] 下巴向下
        self.RJawOpen = 0.01                # 右* 下巴正常 [0,0.01,1] 下巴向下
        self.LJawForward = 0.5              # 左* 下巴向前 [0,0.5,1] 下巴向后
        self.RJawForward = 0.5              # 右* 下巴向前 [0,0.5,1] 下巴向后
        
        self.init_msg = self.msgs

    @property
    def msgs(self):
        return [
            self.LUpperLipVert, self.RUpperLipVert, self.LLowerLipVert, self.RLowerLipVert,
            self.LSmile, self.RSmile, self.LSad, self.RSad,
            self.LJawOpen, self.RJawOpen, self.LJawForward, self.RJawForward
        ]

    def setmsg(self, data):
        self.LUpperLipVert      = data[0]
        self.RUpperLipVert      = data[1]
        self.LLowerLipVert      = data[2]
        self.RLowerLipVert      = data[3]
        
        self.LSmile             = data[4]
        self.RSmile             = data[5]
        self.LSad               = data[6]
        self.RSad               = data[7]

        self.LJawOpen           = data[8]
        self.RJawOpen           = data[9]

        self.LJawForward        = data[10]
        self.RJawForward        = data[11]

    def act_init_servo(self):
        self.setmsg(self.init_msg)
        self.send()
        
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

        if self.is_open:
            self.write(frameData)


#直接执行这个.py文件运行下边代码，import到其他脚本中下边代码不会执行
if __name__ == '__main__':
    
    ctrl = MouthCtrl('/dev/ttyACM0')

    ctrl.LUpperLipVert     = 0.1
    ctrl.RUpperLipVert    = 0.1
    ctrl.LLowerLipVert   = 0.2
    ctrl.RLowerLipVert  = 0.2

    ctrl.LSmile    = 0.5
    ctrl.RSmile   = 0.5
    ctrl.LSad  = 0.5
    ctrl.RSad = 0.5

    ctrl.LJawOpen         = 0.01
    ctrl.RJawOpen        = 0.01
    ctrl.LJawForward          = 0.5
    ctrl.RJawForward         = 0.5
    ctrl.send()
    print(ctrl.msgs)

    ctrl.act_init_servo()