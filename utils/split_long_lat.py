# coding=utf-8
# @Time : 2022/9/15 12:34 PM
# @Author : 王思哲
# @File : split_long_lat.py
# @Software: PyCharm
'''
功能：百度地图得到的每个点的经纬度是连着的，以（long,lat）字符串形式呈现，该程序将其分离开，使得对于数据的计算更加容易。
'''
import time
import pandas as pd

try:
    st = time.perf_counter()
    # 读取原始数据
    raw_data = pd.read_csv('../source/data/long_lat_raw.csv', header=None)
    # 转换DataFrame->List,便于计算
    raw_data_list = raw_data.values.tolist()
    # 按逗号分割
    data_splited = [x[0].split(',') for x in raw_data_list]
    # 转回DataFrame
    data_finalized = pd.DataFrame(data_splited)
    # 结果写入csv文件保存
    data_finalized.to_csv("../source/data/long_lat_finalized.csv",index=False,header=None,encoding='utf-8-sig')
    # 查重
    # rr = np.array(data_splited).T
    # rr0 = collections.Counter(rr[0])
    # 查数据类型
    # print(rr0)
    # print(type(float(data_splited[0][0])), float(data_splited[0][0]))
    ed = time.perf_counter()
    print(f"[INFO] 经纬度分离工作完成，文件中共{len(data_splited)}行受影响，耗时 {ed - st} 秒.")
except Exception as e:
    raise e

