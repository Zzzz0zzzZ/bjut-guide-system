# 北工大校园导航系统

## 主要功能

1、选择校园多个地点，根据算法求解出最短路线，返回并展示给用户

2、详细步行路线显示（精准到十字路口）

2、记录待办事项，支持截止日期设置，实时提醒；

3、待办事项支持多端协同记录([网页端](http://152.136.154.181:4547/todo/login)、[手机端](https://github.com/Zzzz0zzzZ/bjut-guide-system/releases/tag/v1.0.0))

4、课表显示、天气提醒

## 项目构建

项目打包借助HBuilderX，发[安卓包](https://github.com/Zzzz0zzzZ/bjut-guide-system/releases/tag/v1.0.0)

### 前端

Vue 3 + Vant 3

### 后端

FastAPI

### 算法

规划算法：动态规划（DP）、蚁群算法（ACO）

自动舍弃算法：K-means

## 项目部署

### 移动端部署

1、前端项目打包

```shell
npm run build
```

2、将打包生成的`dist`文件夹中的内容，复制到创建好的HbuilderX H5+App项目中(替换)

3、云打包，等待生成`.apk`文件

4、打包完成，手机安装即可。

### 服务器部署

1、把后端项目`scp`到服务器上

```shell
cd 到项目文件夹下
scp -r backend_guide_system 你的服务器:服务器文件存放地点
```

2、在服务器目录下，安装后端所需环境

```shell
# 清华源, 快！
pip install -r requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

3、为`.py`文件赋予运行权限

```shell
# 建议对于所有的.py文件进行：
chmod 777 xxx.py	# xxx是文件名
# 或者：
chmod +x xxx.py
```

4、使用命令，永久运行`.py`文件

```shell
# 使用python3解释器
nohup python3 -u main.py > log.out 2>&1 &
```

5、查看日志 & 结束运行

（1）查看日志

```shell
# 同级目录下
cat log.out
```

（2）结束运行

```shell
ps -ef | grep python	# 找到对应的pid号，杀死进程
kill -9 pid号
```

