# coding=utf-8
# @Time : 2022/10/31 2:25 AM
# @Author : 王思哲
# @File : autopath.py
# @Software: PyCharm
'''
如果用户选择的点超过了数量阈值, 则会有限选择距离近的点为用户规划路线
'''
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd

class AutoPather:
    def __init__(self, chosen_list: list):
        # 所有的点
        self.coordinate = pd.read_csv('./data/read/long_lat_finalized.csv', header=None).values.tolist()
        # 用户原始选择的点(过多)
        self.chosen_list_xy = np.array(self.coordinate)[chosen_list].tolist()
        self.chosen_list = chosen_list
        self.num = len(chosen_list)

    def model_forward(self):
        # 动态判断需要聚几类 funcs()
        N_ClUSTERS = self.get_clusters()
        # Kmeans模型
        model = KMeans(n_clusters=N_ClUSTERS)
        y_pred = model.fit_predict(self.chosen_list_xy)
        # 得到第一个点是哪一类，以第一个点做为起始点，作为必选
        start_type = y_pred[0]
        # 得到优化后的列表
        type_eq_list = np.array(self.chosen_list)[y_pred == start_type].tolist()

        return type_eq_list

    def get_clusters(self):
        n_clus = 1
        if self.num < 30:
            n_clus = 2
        elif self.num < 40:
            n_clus = 3
        elif self.num < 45:
            n_clus = 4
        else:
            n_clus = 5
        return n_clus
