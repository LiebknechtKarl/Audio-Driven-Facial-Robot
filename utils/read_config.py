import os
MASTER_DIC = os.path.dirname(os.path.dirname(__file__))
from pydub import AudioSegment
import pandas as pd

def get_wav_csv_config(wav_path, csv_path):
    audio = AudioSegment.from_wav(wav_path)
    ## 计算输出  wav&csv文件相关信息
    duration_ms = len(audio)                            # 获取音频文件的播放时长（以毫秒为单位）
    duration_s = duration_ms / 1000.0                   # 将时长转换为秒
    df = pd.read_csv(csv_path)                          # 读取 CSV 文件
    row_count = df.shape[0]                             # 获取行数
    FrameNumber = row_count/duration_s                  # 计算 每秒对应多少行

    return (duration_s, FrameNumber)
if __name__ == '__main__':

    csv_path = MASTER_DIC + '/material/csv/droid.csv'
    wav_path = MASTER_DIC + '/material/voice/droid.wav'

    (duration_s, FrameNumber) = get_wav_csv_config(wav_path, csv_path)
    print('时间:',duration_s,'\t帧率:',FrameNumber)