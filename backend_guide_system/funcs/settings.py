# coding=utf-8
# @Time : 2022/11/8 11:55 PM
# @Author : 王思哲
# @File : settings.py
# @Software: PyCharm
import pandas as pd


class Settings:
    def __init__(self):
        pass

    def get_previous_settings(self):
        user_settings_file = pd.read_csv('./data/settings/user_settings.csv', header=None).values.tolist()
        previous_settings = str(user_settings_file[0][0])
        return previous_settings

    def set_current_settings(self, choose):
        df = pd.DataFrame([choose])
        df.to_csv('./data/settings/user_settings.csv', mode='w', index=False, header=False, encoding='utf-8')
