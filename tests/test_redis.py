#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import unittest
from redis import Redis

cur_path = os.path.abspath(__file__)
parent = os.path.dirname
sys.path.append(parent(parent(cur_path)))


from school_api import SchoolClient
from school_api.session.redisstorage import RedisStorage


class TestStudent(unittest.TestCase):
    redis = Redis()
    session = RedisStorage(redis)
    conf = {
        'name': '广东科技学院',
        'code': 'gdst',
        'login_url_path': '/default2.aspx', # 登录地址
        # 'exist_verify': False,            # 是否存在验证码
        'session': session,
    }

    STUDENT_ACCOUNT = os.getenv('GDST_STUDENT_ACCOUNT', '')
    STUDENT_PASSWD = os.getenv('GDST_STUDENT_PASSWD', '')

    GdstApi = SchoolClient('http://61.142.33.204', **conf)
    student = GdstApi.user_login(STUDENT_ACCOUNT, STUDENT_PASSWD, timeout=3)

    def setUp(self):
        print('正在执行\033[1;35m %s \033[0m函数。' % self._testMethodName)

    def tearDown(self):
        pass

    def test_info(self):
        info_data = self.student.get_info(timeout=5)
        print(info_data)


if __name__ == '__main__':
    unittest.main()
