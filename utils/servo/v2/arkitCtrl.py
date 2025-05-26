
import socket
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
print(os.path.dirname(__file__))
from PyLiveLinkFace.pylivelinkface import PyLiveLinkFace, FaceBlendShape
from v2.HeadCtrlKit import HeadCtrl
import os 
ROBOT_ID = os.getenv("ROBOT_ID", "v2_1")
print("ROBOT_ID---",ROBOT_ID)
# if ROBOT_ID == "v2_1":
#     from v2.MouthCtrlKit_1 import MouthCtrl
# elif ROBOT_ID == "v2_2":
#     from v2.MouthCtrlKit_2 import MouthCtrl

sys.path.append(os.path.dirname(__file__))
if ROBOT_ID == "v2_1":
    from MouthCtrlKit_1 import MouthCtrl
elif ROBOT_ID == "v2_2":
    from MouthCtrlKit_2 import MouthCtrl
import time
import threading

class ArkitCtrl:
    def __init__(self, port_head, port_mouth):
        self.port_head = port_head
        self.port_mouth = port_mouth
        self.headCtrl = HeadCtrl(self.port_head) #921600
        self.mouthCtrl = MouthCtrl(self.port_mouth) #921600
        self.thread = threading.Thread(target=self.CtrlThread)
        
        self.bs = [0]*61
        self.initValue = [0] * 25  # 初始值

        self.init_head_dict = dict(zip(HeadCtrl._index_to_attr, self.headCtrl.msgs))
        self.init_mouth_dict = dict(zip(MouthCtrl._index_to_attr, self.mouthCtrl.msgs))


    def startCtrlThread(self):
        # self.thread.daemon = True
        self.thread.start()

    def setBs(self, bs, flag):
        if flag:
            self.bs[0:52] = bs[0:52]
        else:
            self.bs= bs
        self.Arkit2Servo()

    def setBs52(self, bs):
        self.bs[0:52] = bs
        self.Arkit2Servo()

    def setBs61(self, bs):
        self.bs = bs
        self.Arkit2Servo()

    def getBs(self):
        return self.bs

    def setBsHead(self, bs):
        self.bs[FaceBlendShape.HeadYaw.value] = bs[0]
        self.bs[FaceBlendShape.HeadPitch.value] = bs[1]
        self.bs[FaceBlendShape.HeadRoll.value] = bs[2]
        self.Arkit2Servo()

    def Arkit2Servo(self):
        self.headCtrl.left_blink         =  self.bs[FaceBlendShape.EyeBlinkLeft.value]   \
                                            - self.bs[FaceBlendShape.LeftEyeYaw.value]*0.7  \
                                            + self.initValue[0]
        self.headCtrl.left_eye_erect     = -self.bs[FaceBlendShape.EyeLookUpLeft.value]  \
                                            + self.bs[FaceBlendShape.EyeLookDownLeft.value] \
                                            + self.initValue[1]
        self.headCtrl.left_eye_level     = -self.bs[FaceBlendShape.EyeLookInLeft.value]  \
                                            + self.bs[FaceBlendShape.EyeLookOutLeft.value]  \
                                            + self.initValue[2]
        self.headCtrl.left_eyebrow_erect = self.bs[FaceBlendShape.BrowOuterUpLeft.value]*2\
                                            + self.initValue[3]
        self.headCtrl.left_eyebrow_level = self.bs[FaceBlendShape.BrowDownLeft.value]*2\
                                            + self.initValue[4]

        self.headCtrl.right_blink         = self.bs[FaceBlendShape.EyeBlinkRight.value]    \
                                            - self.bs[FaceBlendShape.RightEyeYaw.value]*0.7  \
                                            + self.initValue[5]
        self.headCtrl.right_eye_erect     = - self.bs[FaceBlendShape.EyeLookUpRight.value] \
                                            + self.bs[FaceBlendShape.EyeLookDownRight.value] \
                                            + self.initValue[6]
        self.headCtrl.right_eye_level     = self.bs[FaceBlendShape.EyeLookInRight.value]   \
                                            - self.bs[FaceBlendShape.EyeLookOutRight.value]  \
                                            + self.initValue[7]
        self.headCtrl.right_eyebrow_erect = self.bs[FaceBlendShape.BrowOuterUpRight.value]*2\
                                            + self.initValue[8]
        self.headCtrl.right_eyebrow_level = self.bs[FaceBlendShape.BrowDownRight.value]*2\
                                            + self.initValue[9]

        self.headCtrl.head_dian = - self.bs[FaceBlendShape.HeadPitch.value]\
                                    + self.initValue[10]
        self.headCtrl.head_yao  = self.bs[FaceBlendShape.HeadYaw.value]   \
                                + self.initValue[11]
        self.headCtrl.head_bai  = self.bs[FaceBlendShape.HeadRoll.value]  \
                                + self.initValue[12]

        self.mouthCtrl.mouthUpperUpLeft     = self.bs[FaceBlendShape.MouthUpperUpLeft.value] \
                                            - self.bs[FaceBlendShape.MouthPucker.value] \
                                            + self.initValue[13]
        self.mouthCtrl.mouthUpperUpRight    = self.bs[FaceBlendShape.MouthUpperUpRight.value] \
                                            - self.bs[FaceBlendShape.MouthPucker.value] \
                                            + self.initValue[14]
        self.mouthCtrl.mouthLowerDownLeft   = 0.5* self.bs[FaceBlendShape.MouthLowerDownLeft.value] \
                                            + 1.5* self.bs[FaceBlendShape.MouthStretchLeft.value]   \
                                            - self.bs[FaceBlendShape.MouthPucker.value]  \
                                            + self.initValue[15]
        self.mouthCtrl.mouthLowerDownRight  = 0.5* self.bs[FaceBlendShape.MouthLowerDownRight.value] \
                                            + 1.5* self.bs[FaceBlendShape.MouthStretchRight.value]   \
                                            - self.bs[FaceBlendShape.MouthPucker.value]  \
                                            + self.initValue[16]

        self.mouthCtrl.mouthCornerUpLeft    = 0.5* self.bs[FaceBlendShape.MouthSmileLeft.value] \
                                            + 0.5* self.bs[FaceBlendShape.MouthLeft.value] \
                                            - self.bs[FaceBlendShape.MouthRight.value] \
                                            + self.initValue[17]
        self.mouthCtrl.mouthCornerUpRight   = 0.5* self.bs[FaceBlendShape.MouthSmileRight.value] \
                                            + 0.5* self.bs[FaceBlendShape.MouthRight.value] \
                                            - self.bs[FaceBlendShape.MouthLeft.value] \
                                            + self.initValue[18]
        self.mouthCtrl.mouthCornerDownLeft  = 4*self.bs[FaceBlendShape.MouthStretchLeft.value]\
                                            - self.bs[FaceBlendShape.MouthPucker.value]\
                                            + self.initValue[19]
        self.mouthCtrl.mouthCornerDownRight = 4*self.bs[FaceBlendShape.MouthStretchRight.value]\
                                            - self.bs[FaceBlendShape.MouthPucker.value]\
                                            + self.initValue[20]

        self.mouthCtrl.jawFrontLeft         = self.bs[FaceBlendShape.JawOpen.value] + self.initValue[21]
        self.mouthCtrl.jawFrontRight        = self.bs[FaceBlendShape.JawOpen.value] + self.initValue[22]
        self.mouthCtrl.jawBackLeft          = self.bs[FaceBlendShape.JawForward.value]   \
                                            + 1.5*self.bs[FaceBlendShape.JawLeft.value]  \
                                            - 1.5*self.bs[FaceBlendShape.JawRight.value] \
                                            + self.initValue[23]
        self.mouthCtrl.jawBackRight         = self.bs[FaceBlendShape.JawForward.value]   \
                                            + 1.5*self.bs[FaceBlendShape.JawRight.value]  \
                                            - 1.5*self.bs[FaceBlendShape.JawLeft.value] \
                                            + self.initValue[24]    
    def setServo(self, servo):
        """
        根据传入的字典，动态设置对应的头部和嘴部控制器的属性值。

        :param attribute_dict: 一个字典，键是属性名，值是要设置的浮动数值。
        """
        for attribute_name, value in servo.items():
            # 设置头部控制器的属性
            if hasattr(self.headCtrl, attribute_name):
                setattr(self.headCtrl, attribute_name, value)
            # 设置嘴部控制器的属性
            elif hasattr(self.mouthCtrl, attribute_name):
                setattr(self.mouthCtrl, attribute_name, value)
            else:
                print(f"警告: 属性 '{attribute_name}' 未找到。")

    def setHead(self, head):
        self.headCtrl.head_yao = head[0]
        self.headCtrl.head_dian = head[1]
        self.headCtrl.head_bai = head[2]

    def CtrlThread(self):
        while True:
            try:
                # self.headCtrl = HeadCtrl(self.port_head) #921600
                # self.mouthCtrl = MouthCtrl(self.port_mouth) #921600
                self.headCtrl.send()
                self.mouthCtrl.send()
                initheadmsgs = self.headCtrl.initValue
                initmouthmsgs = self.mouthCtrl.initValue
                self.initValue = initheadmsgs +initmouthmsgs
                # print(len(self.initValue))
                print(self.initValue)
                break
            except:
                print("error")
                time.sleep(1)
        while True: 
            try:
                self.headCtrl.send()
                self.mouthCtrl.send()
                time.sleep(0.01)
            except:
                print("error write")
                self.headCtrl.close()
                self.mouthCtrl.close()
                while True:
                    try:
                        self.headCtrl = HeadCtrl(port)
                        self.headCtrl.send()
                        self.mouthCtrl = MouthCtrl(port_mouth) #921600
                        self.mouthCtrl.send()
                        break
                    except:
                        print("error open")
                        time.sleep(0.5)
            pass

if __name__ == '__main__':
    UDP_PORT = 8000
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # port = 'COM10'
    # port_mouth = 'COM9'
    port = '/dev/ttyACM1'
    port_mouth = '/dev/ttyACM0'

    arkit = ArkitCtrl(port, port_mouth)
    arkit.startCtrlThread()
    while True:
        try: 
            # open a UDP socket on all available interfaces with the given port
            s.bind(("", UDP_PORT)) 
            while True: 
                data, addr = s.recvfrom(1024) 

                success, live_link_face = PyLiveLinkFace.decode(data)
                if success:
                    bs = [0]*61
                    for shape in FaceBlendShape:
                        print(f"名称: {shape.name}, 值: {shape.value}")
                        bs[shape.value] = live_link_face.get_blendshape(FaceBlendShape[shape.name])
                    arkit.setBs(bs, 0)
        except KeyboardInterrupt:
            pass
            
        finally: 
            s.close()
