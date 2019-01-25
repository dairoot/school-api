#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

cur_path = os.path.abspath(__file__)
parent = os.path.dirname
sys.path.append(parent(parent(cur_path)))

from school_api import SchoolClient
import unittest


class TestTeacher(unittest.TestCase):
    TEACHER_ACCOUNT = os.getenv('GDST_TEACHER_ACCOUNT', '')
    TEACHER_PASSWD = os.getenv('GDST_TEACHER_PASSWD', '')
    GdstApi = SchoolClient('http://61.142.33.204')
    teacher = GdstApi.user_login(TEACHER_ACCOUNT, TEACHER_PASSWD,  user_type=1, timeout=3)

    def setUp(self):
        print('正在执行\033[1;35m %s \033[0m函数。' % self._testMethodName)

    def tearDown(self):
        pass

    def test_schedule(self):
        schedule_data = self.teacher.get_schedule(
            schedule_year='2017-2018', schedule_term='1', timeout=5)
        print(schedule_data)

    def test_info(self):
        info_data = self.teacher.get_info(timeout=5)
        print(info_data)


if __name__ == '__main__':
    unittest.main()
