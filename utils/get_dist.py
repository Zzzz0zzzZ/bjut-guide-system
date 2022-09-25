# coding=utf-8
# @Time : 2022/9/15 1:21 PM
# @Author : 王思哲
# @File : get_dist.py
# @Software: PyCharm
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import numpy as np
import time

class CalcDist:
    def __init__(self):
        self.data = pd.read_csv('../source/data/long_lat_finalized.csv', header=None).values.tolist()
        self.data_num = len(self.data)
        self.dist = []

    def get_dist(self):
        '''
        计算任意两点间距离，保存距离矩阵
        :return: self.dict |type: numpy.array
        '''
        res = []
        for i in range(self.data_num):
            for j in range(self.data_num):
                res.append(self.haversine(
                    float(self.data[i][0]),
                    float(self.data[i][1]),
                    float(self.data[j][0]),
                    float(self.data[j][1])
                ))
        self.dist = np.array(res).reshape(self.data_num, -1)
        return self.dist

    def save_dist(self):
        '''
        计算距离矩阵，保存为txt和npy两种文件形式，并返回矩阵
        :return: res |type: numpy.array
        '''
        st = time.perf_counter()
        # 计算距离矩阵
        res = self.get_dist()
        # 保存.txt供查看，.npy供后续加载
        np.savetxt('../source/data/dist_matrix.txt', np.c_[res], fmt='%d', delimiter='\t')
        np.save('../source/data/dist_matrix', res)
        ed = time.perf_counter()
        print(f"[INFO] 距离计算工作完成，结果矩阵大小为{res.shape}，耗时 {ed - st} 秒.")
        return res

    def haversine(self, lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        :return 单位 m
        """
        # 将十进制度数转化为弧度
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

        # haversine公式
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        r = 6371  # 地球平均半径，单位为公里
        return c * r * 1000

if __name__ == "__main__":
    calc_dist = CalcDist()
    calc_dist.save_dist()