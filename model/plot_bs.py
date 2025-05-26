


import csv
import matplotlib.pyplot as plt



def csv2list(csv_path) :
    # column_index = 27  # CSV 文件的列索引（从 0 开始计数，第 27 列是索引 26）    21    22
    column_index = 22  # CSV 文件的列索引（从 0 开始计数，第 27 列是索引 26）

    # 初始化列表
    column_data = []

    # 打开并读取 CSV 文件
    with open(csv_path, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) > column_index:  # 确保行有足够的列
                try:
                    value = float(row[column_index])  # 将值转换为浮点数
                    column_data.append(value)
                except ValueError:
                    # 如果转换失败，跳过该行
                    continue   
    return column_data 
if __name__ == '__main__':

    # 加载 CSV 文件并读取第 27 列
    # filename = '/home/fu/Desktop/ubuntu_data/nlp/demo_51_qiangnao_voice/ula_files_250326/imi/src/ulaa_head/ulaa_head/csv/russian_welcome.csv'  # 替换为你的 CSV 文件名
    filename = '/home/fu/Desktop/ubuntu_data/nlp/demo_51_qiangnao_voice/dda/material/csv/liu.csv'  # 替换为你的 CSV 文件名

    column_data = csv2list(filename)

    # filename1 = '/home/fu/Desktop/ubuntu_data/nlp/demo_51_qiangnao_voice/ula_files_250326/imi/src/ulaa_head/ulaa_head/csv/static_valley_of_fear.csv'  # 替换为你的 CSV 文件名
    filename1 = '/home/fu/Desktop/ubuntu_data/nlp/demo_51_qiangnao_voice/dda/material/csv/art.csv'  # 替换为你的 CSV 文件名

    column_data1 = csv2list(filename1)


    # filename2 = '/home/fu/Desktop/ubuntu_data/nlp/demo_51_qiangnao_voice/ula_files_250326/imi/src/ulaa_head/ulaa_head/csv/video.csv'  # 替换为你的 CSV 文件名
    # column_data2 = csv2list(filename2)

    # 绘制图形
    plt.plot(column_data , label = 'liu')
    plt.plot(column_data1 , label = 'art')
    # plt.plot(column_data2)

    # 添加图例
    plt.legend()

    plt.title('Column 27 Data')
    plt.xlabel('Row Index')
    plt.ylabel('Value')
    plt.show()















