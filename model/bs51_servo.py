

def map_range(x, from_min, from_max, to_min, to_max):
    '''
    线性映射函数，将 x 从 from_min-from_max 线性映射到 to_min-to_max 区间
    '''
    if from_min > from_max:
        from_min, from_max = from_max, from_min
        to_min, to_max = to_max, to_min

    x = max(min(x, from_max), from_min)
    from_range = from_max - from_min
    to_range = to_max - to_min
    mapped_value = (x - from_min) * (to_range / from_range) + to_min

    return mapped_value



def manual_model(bs_dict, rpy_angles):

    # ======================================= 头部控制 =======================================
    # 眼皮--二自由度
    left_blink = bs_dict["EyeBlinkLeft"] # 0.8*map_range(bs_dict["EyeBlinkLeft"], 0, 0.8, 0.44, 0) + 0.2*map_range(bs_dict["EyeWideLeft"], 0, 1, 0.44, 1)
    right_blink = bs_dict["EyeBlinkRight"] # 0.8*map_range(bs_dict["EyeBlinkRight"], 0, 0.8, 0.44, 0) + 0.2*map_range(bs_dict["EyeWideRight"], 0, 1, 0.44, 1)

    # 眼球--四自由度
    left_eye_level = map_range(1.3*(bs_dict["EyeLookOutLeft"] - bs_dict["EyeLookInLeft"]), -1, 1 , 0 , 1)
    right_eye_level = left_eye_level # map_range(1.3*(bs_dict["EyeLookInRight"] - bs_dict["EyeLookOutRight"]), -1, 1, 0, 1)
    # left_eye_erect = map_range(1.3*(bs_dict["EyeLookDownLeft"] - bs_dict["EyeLookUpLeft"])-0.3, -1, 1, 0, 1)
    # right_eye_erect = map_range(1.3*(bs_dict["EyeLookDownRight"] - bs_dict["EyeLookUpRight"])-0.3, -1, 1, 0, 1)
    left_eye_erect = 0.5
    right_eye_erect = 0.5
    # 眉毛四自由度
    left_eyebrow_erect = map_range(bs_dict["BrowInnerUp"], 0, 1, 0.01, 0.99)
    right_eyebrow_erect = map_range(bs_dict["BrowInnerUp"], 0, 1, 0.01, 0.99)
    left_eyebrow_level = map_range(bs_dict["BrowDownLeft"], 0, 1, 0.2, 1)
    right_eyebrow_level = map_range(bs_dict["BrowDownRight"], 0, 1, 0.2, 1) 

    # 头部--三自由度
    head_dian =  map_range(rpy_angles[0], -45, 45, 0, 1)  
    head_yao =   map_range(rpy_angles[1], -45, 45, 0, 1)
    head_bai =   map_range(rpy_angles[2], -45, 45, 1, 0)


    # ======================================= 嘴部控制 =======================================
    # jawOpenLeft          = 1.5*map_range(bs_dict['JawOpen'], 0, 0.6, 0, 1) 
    # jawOpenRight         = 1.5*map_range(bs_dict['JawOpen'], 0, 0.6, 0, 1) 
    # jawOpenLeft          = 1.5*map_range(bs_dict['JawOpen'], 0, 0.6, -0.2, 0) 
    # jawOpenRight         = 1.5*map_range(bs_dict['JawOpen'], 0, 0.6, -0.2, 0) 

    # jawOpenLeft          = 1.5*map_range(bs_dict['JawOpen'], 0, 0.6, -0.2, 1) 
    # jawOpenRight         = 1.5*map_range(bs_dict['JawOpen'], 0, 0.6, -0.2, 1) 
    jawOpenLeft          = map_range(bs_dict['JawOpen'], 0.1, 0.45, 0.01, 1) 
    jawOpenRight         = map_range(bs_dict['JawOpen'], 0.1, 0.45, 0.01, 1) 

    # jawBackLeft          = map_range(10*(bs_dict['JawForward'] + 1.5*bs_dict['JawLeft'] - 1.5*bs_dict['JawRight']), -0.5, 0.5, 0, 1)
    # jawBackRight         = map_range(10*(bs_dict['JawForward'] + 1.5*bs_dict['JawRight']- 1.5*bs_dict['JawLeft']) , -0.5, 0.5, 0, 1)
    jawBackLeft          = 0.5
    jawBackRight         = 0.5
    # jawBackLeft          = map_range(10*(bs_dict['JawForward'] + 1.5*bs_dict['JawLeft'] - 1.5*bs_dict['JawRight']), -0.5, 0.5, -0.2, 1)
    # jawBackRight         = map_range(10*(bs_dict['JawForward'] + 1.5*bs_dict['JawRight']- 1.5*bs_dict['JawLeft']) , -0.5, 0.5, -0.2, 1)    
    # jawBackLeft          = map_range(10*(bs_dict['JawForward'] + 1.5*bs_dict['JawLeft'] - 1.5*bs_dict['JawRight']), -0.5, 0.5, -0.2, 0)
    # jawBackRight         = map_range(10*(bs_dict['JawForward'] + 1.5*bs_dict['JawRight']- 1.5*bs_dict['JawLeft']) , -0.5, 0.5, -0.2, 0)    

    mouthUpperUpLeft     = map_range(bs_dict['MouthUpperUpLeft'] , 0, 1, 0.76, 0) + map_range(bs_dict['MouthPucker'], 0.4, 1, 0, 0.24) 
    mouthUpperUpRight    = map_range(bs_dict['MouthUpperUpRight'], 0, 1, 0.76, 0) + map_range(bs_dict['MouthPucker'], 0.4, 1, 0, 0.24) 
    # mouthUpperUpLeft     = map_range(bs_dict['MouthUpperUpLeft'] , 0, 1, 0.76, 0) + map_range(bs_dict['MouthPucker'], 0.4, 1, 0, 0) 
    # mouthUpperUpRight    = map_range(bs_dict['MouthUpperUpRight'], 0, 1, 0.76, 0) + map_range(bs_dict['MouthPucker'], 0.4, 1, 0, 0) 

    # mouthLowerDownLeft   = map_range(bs_dict['MouthLowerDownLeft'] , 0, 0.8, 0, 0.8) + map_range(bs_dict['MouthPucker'], 0, 1, 0.2, 0) 
    # mouthLowerDownRight  = map_range(bs_dict['MouthLowerDownRight'], 0, 0.8, 0, 0.8) + map_range(bs_dict['MouthPucker'], 0, 1, 0.2, 0) 
    mouthLowerDownLeft   = map_range(bs_dict['MouthLowerDownLeft'] , 0, 0.8, 0, 0.8) + map_range(bs_dict['MouthPucker'], 0, 1, 0, -0.2) 
    mouthLowerDownRight  = map_range(bs_dict['MouthLowerDownRight'], 0, 0.8, 0, 0.8) + map_range(bs_dict['MouthPucker'], 0, 1, 0, -0.2) 

    mouthCornerUpLeft    = map_range((bs_dict['MouthSmileLeft']  + bs_dict['MouthLeft']  ), 0 ,1, 0, 0.77) + map_range(bs_dict['MouthPucker'], 0.1, 1, 0.23, 0) 
    mouthCornerUpRight   = map_range((bs_dict['MouthSmileRight'] + bs_dict['MouthRight'] ), 0 ,1, 0, 0.77) + map_range(bs_dict['MouthPucker'], 0.1, 1, 0.23, 0) 
    # mouthCornerUpLeft    = map_range((bs_dict['MouthSmileLeft']  + bs_dict['MouthLeft']  ), 0 ,1, 0, 0.77) + map_range(bs_dict['MouthPucker'], 0.1, 1, 0, 0) 
    # mouthCornerUpRight   = map_range((bs_dict['MouthSmileRight'] + bs_dict['MouthRight'] ), 0 ,1, 0, 0.77) + map_range(bs_dict['MouthPucker'], 0.1, 1, 0, 0) 


    mouthCornerDownLeft  = map_range(bs_dict['MouthStretchLeft']  , 0, 0.5, 0.5 , 0) 
    mouthCornerDownRight = map_range(bs_dict['MouthStretchRight'] , 0, 0.5, 0.5 , 0) 
    # mouthCornerDownLeft  = map_range(bs_dict['MouthStretchLeft']  , 0, 0.5, 0, 0) 
    # mouthCornerDownRight = map_range(bs_dict['MouthStretchRight'] , 0, 0.5, 0 , 0) 





    # print('jawOpenLeft',jawOpenLeft,bs_dict["BrowInnerUp"],'-----------------------------------------')


    head = [left_blink, left_eye_erect, left_eye_level, left_eyebrow_erect, left_eyebrow_level, right_blink, right_eye_erect, right_eye_level, right_eyebrow_erect, right_eyebrow_level, head_dian, head_yao, head_bai]
    
    mouth = [mouthUpperUpLeft, mouthUpperUpRight, mouthLowerDownLeft, mouthLowerDownRight, mouthCornerUpLeft, mouthCornerUpRight, mouthCornerDownLeft, mouthCornerDownRight, jawOpenLeft, jawOpenRight, jawBackLeft, jawBackRight]

    return head, mouth


