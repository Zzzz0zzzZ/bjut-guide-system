# coding=utf-8
# @Time : 2022/10/17 5:31 PM
# @Author : 王思哲
# @File : getcourse.py
# @Software: PyCharm
import pandas as pd
import time


class GetCourse:
    def __init__(self):
        self.course_data = pd.read_csv('./data/course/courese_20020203.csv', header=None)
        self.course_time_list = ['00:00:00', '08:00:00', '09:55:00', '13:30:00', '15:25:00', '23:59:59']

    def get_weekdays(self):
        """
        :return: week_index
        """
        local_time = time.localtime(time.time())  # 获取当前时间的时间元组
        week_index = local_time.tm_wday  # 获取时间元组内的tm_wday值

        return week_index

    def get_course(self):
        '''
        获取即将要上的课
        :return: status, notice
        '''
        # 获取星期几 0-6代表周一到周日
        today = self.get_weekdays()
        # 获得那一天的课表
        today_classes = self.course_data[today]
        # 现在的时间
        time_now = f'{time.localtime().tm_hour}:{time.localtime().tm_min}:{time.localtime().tm_sec}'
        # 看在哪个时间段里
        course_id = 0
        for i in range(len(self.course_time_list) - 1):
            std_time_1 = time.strptime(self.course_time_list[i], '%H:%M:%S')
            std_time_2 = time.strptime(self.course_time_list[i+1], '%H:%M:%S')
            now_time = time.strptime(time_now, '%H:%M:%S')
            if now_time >= std_time_1 and now_time <= std_time_2:
                course_id = i
        # 返回信息： 有下一节课返回[课程名称]  没有课则返回[无]
        notice = today_classes[course_id]
        notice = "没课啦，好好休息吧！" if notice == '无' else notice

        return notice