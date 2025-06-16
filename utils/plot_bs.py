import csv
import matplotlib.pyplot as plt
import os,sys
MASTER_DIC = os.path.dirname(os.path.dirname(__file__))
sys.path.append(MASTER_DIC)
def csv2list(csv_path, column_index) :

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
    filename = MASTER_DIC + '/material/csv/droid.csv'  # 替换为你的 CSV 文件名
    column_index = 22  # CSV 文件的列索引（从 0 开始计数，第 27 列是索引 26）

    column_data = csv2list(filename, column_index)

    # 绘制图形
    plt.plot(column_data )

    # 添加图例
    plt.legend()

    plt.title('Column 27 Data')
    plt.xlabel('Row Index')
    plt.ylabel('Value')
    plt.show()