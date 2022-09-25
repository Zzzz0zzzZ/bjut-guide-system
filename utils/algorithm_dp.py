import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pylab import mpl

# 设置显示中文字体
mpl.rcParams["font.sans-serif"] = ["SimHei"]

# 定义无穷大值
inf = 10e7


def getMinDistance(point, cityNum, dp):
  """
  得到动态规划后的列表
  :param point: 城市距离矩阵 ndarray
  :param cityNum: 城市数量 int
  :return: dp列表 list
  """
  column = 1 << (cityNum - 1) # dp数组的列数
  # 初始化dp数组第一列
  for i in range(cityNum): 
    dp[i][0] = point[i][0]
  # 更新dp数组，先列再行
  for j in range(1, column): 
    for i in range(0, cityNum):
      dp[i][j] = inf
      if i == 0:
        if (j << 1) & 1 == 1:
          continue
      elif i >= 0:
        if ((j >> (i - 1)) & 1) == 1 :
          continue
      for k in range(1, cityNum):
        if ((j >> (k - 1)) & 1) == 0:
          continue
        if dp[i][j] > point[i][k] + dp[k][j ^ (1 << (k - 1))]:
          dp[i][j] = point[i][k] + dp[k][j ^ (1 << (k - 1))]
  return dp

def isVisited(visited, cityNum):
  """
  判断结点是否都以访问但不包括0号结点
  :param visited: 访问数组 ndarray
  :param cityNum: 城市数量 int
  :return: 布尔值
  """
  for i in range(1, cityNum):
    if visited[i] == False:
      return False
  return True

def getPath(point, cityNum, dp):
  """
  判断结点是否都以访问但不包括0号结点
  :param point: 城市距离矩阵 ndarray
  :param cityNum: 城市数量 int
  :return: 动态规划最优路径 list
  """
  path = [] # 存储最短路径
  column = 1 << (cityNum - 1) # dp数组的列数
  visited = np.zeros(cityNum, dtype=np.bool_) # 标记访问数组
  pioneer = 0 # 前驱节点编号
  min = inf
  S = column - 1
  # 把起点结点编号加入容器
  path.append(0)
  while isVisited(visited, cityNum) == False:
    for i in range(1, cityNum):
      if visited[i] == False and (S & (1 << (i - 1))) != 0:
        if min > point[i][pioneer] + dp[i][(S ^ (1 << (i - 1)))]:
          min = point[i][pioneer] + dp[i][(S ^ (1 << (i - 1)))]
          temp = i
    pioneer = temp
    path.append(pioneer)
    visited[pioneer] = True
    S = S ^ (1 << (pioneer - 1))
    min = inf
  return path

def path_draw(path, num_place_dict, coordinate):
  '''
  根据路径结果，画出推荐路线图
  :param path: 结果路径 |type: list
  :param num_place_dict: 地点{编号:名称}字典 |type: list
  :param coordinate: 地点坐标 |type: list
  :return: none
  '''
  # data = pd.read_csv('../source/data/long_lat_finalized.csv', header=None).values.tolist()
  data = np.array(coordinate)
  # print(data.shape)
  fig, ax = plt.subplots()
  x = data[:, 0]
  y = data[:, 1]
  ax.scatter(x, y, linewidths=0.1)
  ax.set_title("北京工业大学校园导航-推荐路线")
  # for i, txt in enumerate(range(0, len(data))):
  #   ax.annotate(txt, (x[i], y[i]))
  for i in range(0, len(data)):
    ax.annotate(num_place_dict[i][0], (x[i], y[i]))
  # 获取路径点的x,y列表
  x0 = x[path]
  y0 = y[path]

  for i in range(len(path) - 1):
    plt.quiver(x0[i], y0[i], x0[i + 1] - x0[i], y0[i + 1] - y0[i], color='r', width=0.005, angles='xy', scale=1,
               scale_units='xy')
  plt.quiver(x0[-1], y0[-1], x0[0] - x0[-1], y0[0] - y0[-1], color='r', width=0.005, angles='xy', scale=1,
             scale_units='xy')
  plt.show()

def dynamicProgramming(cityNum, point):
  """
  动态规划算法
  :param cityNum: 城市数量 int
  :param point: 城市距离矩阵 ndarray
  :return: 最小距离 double 运行时间 double
  """
  start = time.perf_counter() # 程序开始时间
  dp = getMinDistance(point, cityNum, np.zeros((cityNum, 1 << (cityNum - 1)))) # 计算dp列表以及最短路径的值
  path = getPath(point, cityNum, dp) # 获取最优路径，保存在path中，根据动态规划公式反向找出最短路径结点列表
  # print(path)
  end = time.perf_counter() # 程序结束时间
  print(f'[INFO] 动态规划算法，{cityNum} 个地点，算法耗时 {end-start} 秒')
  return path, round(dp[0][(1 << (cityNum - 1)) - 1], 2)

  
if __name__ == "__main__":
  st = time.perf_counter()
  # 常量
  BIAS = 10
  NUM = 20
  # 加载字典，用于结果输出
  num_place_dict = pd.read_csv('../source/data/num_place_dict.csv', header=None).values.tolist()
  # 加载距离矩阵 ndarray
  dist_matrix = np.load('../source/data/dist_matrix.npy')
  point = dist_matrix[BIAS:BIAS + NUM, BIAS:BIAS + NUM]
  # 加载地点坐标 二维list
  coordinate = pd.read_csv('../source/data/long_lat_finalized.csv', header=None).values.tolist()
  # 地点数量 int
  cityNum = NUM
  ######################################################################################################
  # DP
  path, length = dynamicProgramming(cityNum, point)
  ######################################################################################################
  # 输出文字结果
  print("路线为：", end="")
  for idx, pt in enumerate(path):
    print(f'[{num_place_dict[pt+BIAS][0]}]->',end="")
  print(f'[{num_place_dict[path[0]+BIAS][0]}]')
  print(f'路线总长度：{length}米')
  # 绘制路线图
  path_draw_list = [p+BIAS for p in path]
  path_draw(path_draw_list, num_place_dict=num_place_dict, coordinate=coordinate)
  ed = time.perf_counter()
  print(f'[INFO] 总耗时 {ed - st} 秒')