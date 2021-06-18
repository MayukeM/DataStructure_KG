import os
import pandas as pd
import numpy as np

def get_train_data_list(path):
    getpath = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    getpath = ('/').join(getpath.split('\\'))
    with open(getpath + path, 'r') as f:
        data = pd.DataFrame(f)
        train_data = np.array(data)  # 先将数据框转换为数组
        train_data_list = train_data.tolist()  # 其次转换为列表
    for i, item in enumerate(train_data_list):
        train_data_list[i] = item[0].split(',')

    return train_data_list