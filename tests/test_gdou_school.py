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

    STUDENT_ACCOUNT = os.getenv('GDOU_STUDENT_ACCOUNT', '')
    STUDENT_PASSWD = os.getenv('GDOU_STUDENT_PASSWD', '')
    GdouApi = SchoolClient('http://210.38.137.126:8016')
    student = GdouApi.user_login(STUDENT_ACCOUNT, STUDENT_PASSWD, timeout=3)

    def setUp(self):
        print('正在执行\033[1;35m %s \033[0m函数。' % self._testMethodName)

    def tearDown(self):
        pass

    def test_schedule(self):
        schedule_data = self.student.get_schedule(
            schedule_year='2017-2018', schedule_term='1', timeout=5)
        print(schedule_data)

    # def test_score(self):
    #     score_data = self.student.get_score(score_year='2017-2018', score_term='1', timeout=5)
    #     print(score_data)

    def test_info(self):
        info_data = self.student.get_info(timeout=5)
        print(info_data)


if __name__ == '__main__':
    unittest.main()
