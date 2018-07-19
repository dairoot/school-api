#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

cur_path = os.path.abspath(__file__)
parent = os.path.dirname
sys.path.append(parent(parent(cur_path)))

from school_api import SchoolClient
import unittest


class TestStudent(unittest.TestCase):

    conf = {
        'name': '广东科技学院',
        'login_view_state': {           # 登录的view_state(可空)
            'http://61.142.33.204/default2.aspx': 'dDw3OTkxMjIwNTU7Oz5vJ/yYUi9dD4fEnRUKesDFl8hEKA==',
            'http://61.142.33.204/default4.aspx': 'dDwxMTE4MjQwNDc1Ozs+h4dTkZuJcYarQdE7xNFUBMsLO/w='
        },
        'lan_url': 'http://172.16.1.8',  # 内网地址
        'login_url_path': '/default2.aspx',  # 登录地址
        'exist_verify': True,           # 是否存在验证码
        'priority_porxy': False,        # 是否优先使用代理
        'url_endpoint': None,           # 教务系统链接
        # 'proxies': {"http": "http://xxxx:xxxx@xxxx.xxxx.xxxx:xxxx/", }  # 代理
    }

    STUDENT_ACCOUNT = os.getenv('GDST_STUDENT_ACCOUNT', '')
    STUDENT_PASSWD = os.getenv('GDST_STUDENT_PASSWD', '')
    GdstApi = SchoolClient('http://61.142.33.204', **conf)
    student = GdstApi.user_login(STUDENT_ACCOUNT, STUDENT_PASSWD, timeout=3)

    def setUp(self):
        print('正在执行\033[1;35m %s \033[0m函数。' % self._testMethodName)

    def tearDown(self):
        pass

    def test_schedule(self):
        schedule_data = self.student.get_schedule(
            schedule_year='2017-2018', schedule_term='1', timeout=5)
        print(schedule_data)

    def test_score(self):
        score_data = self.student.get_score(score_year='2017-2018', score_term='1', timeout=5)
        print(score_data)

    def test_info(self):
        info_data = self.student.get_info(timeout=5)
        print(info_data)


if __name__ == '__main__':
    unittest.main()
