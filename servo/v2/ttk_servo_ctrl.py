import tkinter as tk
from tkinter import ttk
from HeadCtrlKit import HeadCtrl
from MouthCtrlKit import MouthCtrl
import tkinter as tk
from tkinter import ttk

class ServoControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("25舵机控制界面")
        
        # 初始化控制器
        self.mouth_ctrl = MouthCtrl('/dev/ttyACM0')
        self.head_ctrl = HeadCtrl('/dev/ttyACM1')
        
        # 主框架
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建嘴部和头部控制区域
        self.create_mouth_controls()
        self.create_head_controls()
        
        # 添加控制按钮区域
        self.create_control_buttons()
        
        # 添加状态栏
        self.status_var = tk.StringVar()
        self.status_bar = ttk.Label(root, textvariable=self.status_var, relief=tk.SUNKEN)
        self.status_bar.pack(fill=tk.X)
        self.status_var.set("就绪")
    
    def create_mouth_controls(self):
        # 嘴部舵机控制框架
        mouth_frame = ttk.LabelFrame(self.main_frame, text="嘴部控制 (12舵机)")
        mouth_frame.pack(fill=tk.X, padx=5, pady=5)
        
        mouth_servos = [
            ("LUpperLipVert", "LUpperLipVert", 0.1),
            ("RUpperLipVert", "RUpperLipVert", 0.1),
            ("LLowerLipVert", "LLowerLipVert", 0.2),
            ("RLowerLipVert", "RLowerLipVert", 0.2),
            ("LSmile", "LSmile", 0.5),
            ("RSmile", "RSmile", 0.5),
            ("LSad", "LSad", 0.5),
            ("RSad", "RSad", 0.5),
            ("LJawOpen", "LJawOpen", 0.01),
            ("RJawOpen", "RJawOpen", 0.01),
            ("LJawForward", "LJawForward", 0.5),
            ("RJawForward", "RJawForward", 0.5)
        ]        
        self.mouth_vars = {}
        
        for i, (attr, label, default) in enumerate(mouth_servos):
            row = i % 6  # 分为两列
            col = i // 6
            
            frame = ttk.Frame(mouth_frame)
            # frame.grid(row=row, column=col, padx=5, pady=2, sticky="ew")
            frame.grid(row=row, column=col, padx=10, pady=4, sticky="ew")
            
            lbl = ttk.Label(frame, text=label, width=20)
            # lbl = ttk.Label(frame, text=label, width=30)

            lbl.pack(side=tk.LEFT)
            
            current_val = getattr(self.mouth_ctrl, attr)
            
            # 数值输入框
            var = tk.DoubleVar(value=current_val)
            self.mouth_vars[attr] = var
            
            entry = ttk.Entry(frame, textvariable=var, width=6)
            entry.pack(side=tk.LEFT)
            
            # 滑块 - 实时控制
            scale = ttk.Scale(frame, from_=0, to=1, variable=var, 
                             command=lambda v, a=attr: self.on_mouth_scale_change(v, a, True))
            scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # 应用按钮
            btn = ttk.Button(frame, text="应用", width=4,
                            command=lambda a=attr: self.apply_mouth_value(a))
            btn.pack(side=tk.LEFT)
    
    def create_head_controls(self):
        # 头部舵机控制框架
        head_frame = ttk.LabelFrame(self.main_frame, text="头部控制 (13舵机)")
        # head_frame.pack(fill=tk.X, padx=5, pady=5)
        head_frame.pack(fill=tk.X, padx=5, pady=5)
        
        
        head_servos = [
            ("left_blink", "left_blink", 0.5),
            ("left_eye_erect", "left_eye_erect", 0.5),
            ("left_eye_level", "left_eye_level", 0.5),
            ("left_eyebrow_erect", "left_eyebrow_erect", 0.0),
            ("left_eyebrow_level", "left_eyebrow_level", 0.0),
            ("right_blink", "right_blink", 0.5),
            ("right_eye_erect", "right_eye_erect", 0.5),
            ("right_eye_level", "right_eye_level", 0.5),
            ("right_eyebrow_erect", "right_eyebrow_erect", 0.0),
            ("right_eyebrow_level", "right_eyebrow_level", 0.0),
            ("head_dian", "head_dian", 0.47),
            ("head_yao", "head_yao", 0.5),
            ("head_bai", "head_bai", 0.6)
        ]
        
        self.head_vars = {}
        
        for i, (attr, label, default) in enumerate(head_servos):
            row = i % 7  # 分为两列
            col = i // 7
            
            frame = ttk.Frame(head_frame)
            # frame.grid(row=row, column=col, padx=5, pady=2, sticky="ew")
            frame.grid(row=row, column=col, padx=10, pady=4, sticky="ew")
            
            # lbl = ttk.Label(frame, text=label, width=15)
            lbl = ttk.Label(frame, text=label, width=20)
            lbl.pack(side=tk.LEFT)
            
            current_val = getattr(self.head_ctrl, attr)
            
            # 数值输入框
            var = tk.DoubleVar(value=current_val)
            self.head_vars[attr] = var
            
            entry = ttk.Entry(frame, textvariable=var, width=6)
            entry.pack(side=tk.LEFT)
            
            # 滑块 - 实时控制
            scale = ttk.Scale(frame, from_=0, to=1, variable=var, 
                             command=lambda v, a=attr: self.on_head_scale_change(v, a, True))
            scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            # 应用按钮
            btn = ttk.Button(frame, text="应用", width=4,
                            command=lambda a=attr: self.apply_head_value(a))
            btn.pack(side=tk.LEFT)
    
    def create_control_buttons(self):
        # 控制按钮框架
        btn_frame = ttk.Frame(self.main_frame)
        btn_frame.pack(fill=tk.X, padx=5, pady=10)
        
        # 全部应用按钮
        apply_all_btn = ttk.Button(btn_frame, text="应用全部舵机", 
                                 command=self.apply_all_values)
        apply_all_btn.pack(side=tk.LEFT, padx=5)
        
        # 复位按钮
        reset_btn = ttk.Button(btn_frame, text="复位所有舵机", 
                             command=self.reset_all_servos)
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        # 嘴部复位
        mouth_reset_btn = ttk.Button(btn_frame, text="复位嘴部", 
                                   command=self.mouth_ctrl.act_init_servo)
        mouth_reset_btn.pack(side=tk.LEFT, padx=5)
        
        # 头部复位
        head_reset_btn = ttk.Button(btn_frame, text="复位头部", 
                                  command=self.head_ctrl.act_init_servo)
        head_reset_btn.pack(side=tk.LEFT, padx=5)
    
    def on_mouth_scale_change(self, value, attr, realtime=False):
        # 当嘴部滑块值改变时更新变量
        value = float(value)
        rounded_value = round(value, 2)
        self.mouth_vars[attr].set(rounded_value)
        
        # 如果是实时控制模式，立即发送命令
        if realtime:
            setattr(self.mouth_ctrl, attr, rounded_value)
            self.mouth_ctrl.send()
            self.status_var.set(f"实时控制: 嘴部 {attr} = {rounded_value:.2f}")
    
    def on_head_scale_change(self, value, attr, realtime=False):
        # 当头部滑块值改变时更新变量
        value = float(value)
        rounded_value = round(value, 2)
        self.head_vars[attr].set(rounded_value)
        
        # 如果是实时控制模式，立即发送命令
        if realtime:
            setattr(self.head_ctrl, attr, rounded_value)
            self.head_ctrl.send()
            self.status_var.set(f"实时控制: 头部 {attr} = {rounded_value:.2f}")
    
    def apply_mouth_value(self, attr):
        # 应用嘴部舵机值
        try:
            value = float(self.mouth_vars[attr].get())
            if 0 <= value <= 1:
                setattr(self.mouth_ctrl, attr, value)
                self.mouth_ctrl.send()
                self.status_var.set(f"嘴部控制: {attr} = {value:.2f} 已应用")
            else:
                self.status_var.set("错误: 值必须在0到1之间")
        except ValueError:
            self.status_var.set("错误: 请输入有效的数字")
    
    def apply_head_value(self, attr):
        # 应用头部舵机值
        try:
            value = float(self.head_vars[attr].get())
            if 0 <= value <= 1:
                setattr(self.head_ctrl, attr, value)
                self.head_ctrl.send()
                self.status_var.set(f"头部控制: {attr} = {value:.2f} 已应用")
            else:
                self.status_var.set("错误: 值必须在0到1之间")
        except ValueError:
            self.status_var.set("错误: 请输入有效的数字")
    
    def apply_all_values(self):
        # 应用所有舵机值
        for attr in self.mouth_vars:
            self.apply_mouth_value(attr)
        
        for attr in self.head_vars:
            self.apply_head_value(attr)
        
        self.status_var.set("所有舵机值已应用")
    
    def reset_all_servos(self):
        # 复位所有舵机
        self.mouth_ctrl.act_init_servo()
        self.head_ctrl.act_init_servo()
        
        # 更新UI显示
        for attr, var in self.mouth_vars.items():
            var.set(getattr(self.mouth_ctrl, attr))
        
        for attr, var in self.head_vars.items():
            var.set(getattr(self.head_ctrl, attr))
        
        self.status_var.set("所有舵机已复位到初始位置")

if __name__ == "__main__":
    root = tk.Tk()
    app = ServoControlApp(root)
    root.geometry("1000x800")
    root.mainloop()