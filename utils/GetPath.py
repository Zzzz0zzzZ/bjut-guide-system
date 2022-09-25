# coding=utf-8
# @Time : 2022/9/16 10:11 AM
# @Author : 王思哲
# @File : GetPath.py
# @Software: PyCharm
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl

# 设置显示中文字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]

# 定义无穷大值
inf = 10e7

class GetPath_DP:
    def __init__(self, bias, num, city_selected_list):
        # 加载字典，用于结果输出
        self.num_place_dict = pd.read_csv('../source/data/num_place_dict.csv', header=None).values.tolist()
        # 加载距离矩阵 ndarray
        self.dist_matrix = np.load('../source/data/dist_matrix.npy')
        self.point = self.dist_matrix[bias:bias + num, bias:bias + num]
        # 加载地点坐标 二维list
        self.coordinate = pd.read_csv('../source/data/long_lat_finalized.csv', header=None).values.tolist()
        # 地点数量 int
        self.cityNum = num
        # 常量
        self.bias = bias
        self.num = num
        #
        self.city_selected_list = city_selected_list

    def getMinDistance(self, dp):
        """
        得到动态规划后的列表
        :param point: 城市距离矩阵 ndarray
        :param cityNum: 城市数量 int
        :return: dp列表 list
        """
        column = 1 << (self.cityNum - 1)  # dp数组的列数
        # 初始化dp数组第一列
        # 当集合V为空集时，cis = 从当前点i到起点s的距离	也就是距离数组中第i个点到起点s（默认为0）的距离
        for i in range(self.cityNum):
            dp[i][0] = self.point[i][0]
        # 更新dp数组，先列再行
        # j代表顶点集V，二进制表示，如: j=12 代表 1100
        # 遍历每一顶点种集合情况
        for j in range(1, column):
            for i in range(0, self.cityNum):
                dp[i][j] = inf
                if i == 0:
                    if (j << 1) & 1 == 1:
                        continue
                elif i >= 0:
                    if ((j >> (i - 1)) & 1) == 1:
                        continue
                for k in range(1, self.cityNum):
                    if ((j >> (k - 1)) & 1) == 0:
                        continue
                    if dp[i][j] > self.point[i][k] + dp[k][j ^ (1 << (k - 1))]:
                        dp[i][j] = self.point[i][k] + dp[k][j ^ (1 << (k - 1))]
        print("dp.shape", dp.shape, "dp.type", type(dp))
        return dp

    def isVisited(self, visited):
        """
        判断结点是否都以访问但不包括0号结点
        :param visited: 访问数组 ndarray
        :param cityNum: 城市数量 int
        :return: 布尔值
        """
        for i in range(1, self.cityNum):
            if visited[i] == False:
                return False
        return True

    def getPath(self, dp):
        """
        根据dp表，得到路线
        :param point: 城市距离矩阵 ndarray
        :param cityNum: 城市数量 int
        :return: 动态规划最优路径 list
        """
        # self.city_selected_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        path = []  # 存储最短路径
        column = 1 << (self.cityNum - 1)  # dp数组的列数
        visited = np.zeros(self.cityNum, dtype=np.bool_)  # 标记访问数组
        for i in range(len(visited)):
            visited[i] = True
        for i in self.city_selected_list:
            visited[i] = False
        # column = 1 << (len(city_selected_list))
        # visited = np.zeros(len(city_selected_list), dtype=np.bool_)
        pioneer = 0  # 前驱节点编号
        min = inf
        S = column - 1

        # 把起点结点编号加入容器
        # path.append(city_selected_list[0])
        while self.isVisited(visited) == False:
            for i in self.city_selected_list:
            # for i in range(1, self.cityNum):
                if visited[i] == False and (S & (1 << (i - 1))) != 0:
                    if min > self.point[i][pioneer] + dp[i][(S ^ (1 << (i - 1)))]:
                        min = self.point[i][pioneer] + dp[i][(S ^ (1 << (i - 1)))]
                        temp = i
            pioneer = temp
            path.append(pioneer)
            print(f"path:  {path}")
            print("#"*100)
            visited[pioneer] = True
            S = S ^ (1 << (pioneer - 1))
            min = inf
        return path

    def path_draw(self, path, length):
        '''
        根据路径结果，画出推荐路线图
        :param path: 结果路径 |type: list
        :param num_place_dict: 地点{编号:名称}字典 |type: list
        :param coordinate: 地点坐标 |type: list
        :return: none
        '''
        # data = pd.read_csv('../source/data/long_lat_finalized.csv', header=None).values.tolist()
        data = np.array(self.coordinate)
        # print(data.shape)
        fig, ax = plt.subplots()
        x = data[:, 0]
        y = data[:, 1]
        ax.scatter(x, y, linewidths=0.1)
        ax.set_title(f"北京工业大学校园导航-推荐路线 总长度:{length}米")
        # for i, txt in enumerate(range(0, len(data))):
        #   ax.annotate(txt, (x[i], y[i]))
        for i in range(0, len(data)):
            ax.annotate(self.num_place_dict[i][0], (x[i], y[i]))
        # 获取路径点的x,y列表
        x0 = x[path]
        y0 = y[path]

        for i in range(len(path) - 1):
            plt.quiver(x0[i], y0[i], x0[i + 1] - x0[i], y0[i + 1] - y0[i], color='r', width=0.005, angles='xy', scale=1,
                       scale_units='xy')
        plt.quiver(x0[-1], y0[-1], x0[0] - x0[-1], y0[0] - y0[-1], color='r', width=0.005, angles='xy', scale=1,
                   scale_units='xy')
        plt.show()

    def dynamicProgramming(self):
        """
        动态规划算法
        :param cityNum: 城市数量 int
        :param point: 城市距离矩阵 ndarray
        :return: 最小距离 double 运行时间 double
        """
        start = time.perf_counter()  # 程序开始时间
        dp = self.getMinDistance(np.zeros((self.cityNum, 1 << (self.cityNum - 1))))  # 计算dp列表以及最短路径的值
        # np.save('../source/data/dp_list_20_cities', dp)
        path = self.getPath(dp)  # 获取最优路径，保存在path中，根据动态规划公式反向找出最短路径结点列表
        # print(path)
        end = time.perf_counter()  # 程序结束时间
        print(f'[INFO] 动态规划算法，{self.cityNum} 个地点，算法耗时 {end - start} 秒')

        path_length = round(dp[self.city_selected_list[0]][int("1111111111111",2) - 1], 2)
        # return path, round(dp[0][(1 << (self.cityNum - 1)) - 1], 2)
        return path, path_length

    def run(self):
        '''
        暴露给类外调用的方法，运行动态规划算法
        :return: 规划后路径节点列表 |type:list 规划后路径名称列表 |type:list 路径长度 |type:float
        '''
        BIAS = self.bias
        NUM = self.num
        # DP
        path, length = self.dynamicProgramming()
        # 输出文字结果
        print("路线为：", end="")
        for idx, pt in enumerate(path):
            print(f'[{self.num_place_dict[pt + BIAS][0]}]->', end="")
        print(f'[{self.num_place_dict[path[0] + BIAS][0]}]')
        print(f'路线总长度：{length}米')
        # 绘制路线图
        path_draw_list = [p + BIAS for p in path]
        self.path_draw(path_draw_list, length)
        # print(f'[INFO] 总耗时 {ed - st} 秒')

if __name__ == "__main__":
    #c_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    c_list = [1, 2 , 4, 5, 6, 7, 9, 11, 12, 13, 14]
    c_list = [2, 3, 4, 5, 6, 7, 8, 9, 10]
    a = GetPath_DP(10, 15, city_selected_list=c_list)
    a.run()
