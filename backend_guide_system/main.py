#!/usr/bin/python3
# coding=utf-8
# @Time : 2022/9/14 8:24 AM
# @Author : 王思哲
# @File : main.py.py
# @Software: PyCharm

import uvicorn
from fastapi import FastAPI, Form
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from algorithm.calcpath import CalcPath_DP

# 实例化
app=FastAPI()

# 处理跨域
# 配置允许域名
origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

# 处理跨域
# 配置允许域名列表、允许方法、请求头、cookie等
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加首页
@app.get("/")
def index():
    return "This is Home Page."

@app.get("/users")
def getUsers():
    return [{"id":"1","name":"hj"},{"id":"2","name":"wsz"}]

# 接受传入的地点列表，返回优化后的路线
@app.post("/guide")
def getPaths(bias=Form(None), num=Form(None)):
    # 接受表单数据，确保为int类型
    BIAS = int(bias)
    NUM = int(num)
    # 实例化
    alg = CalcPath_DP(bias=BIAS, num=NUM)
    # 运行算法 DP
    path_idx_list, path_num_list, path_length = alg.run()
    # 返回json格式数据
    return {"path_idx_list":path_idx_list,"path_num_list":path_num_list,"path_length":path_length}


#  返回图片
@app.post("/result")
async def download_files_stream():
    path_result_pic = open('data/res/path_result.png', mode="rb")
    return StreamingResponse(path_result_pic, media_type="image/png")


if __name__ == '__main__':
    uvicorn.run(app)
    # uvicorn.run(app, host='0.0.0.0', port=4554)
