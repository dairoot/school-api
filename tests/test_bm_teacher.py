#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

cur_path = os.path.abspath(__file__)
parent = os.path.dirname
sys.path.append(parent(parent(cur_path)))

from school_api import SchoolClient
import unittest


class TestBmTeacher(unittest.TestCase):
    BM_TEACHER_ACCOUNT = os.getenv('GDST_BM_TEACHER_ACCOUNT', '')
    BM_TEACHER_PASSWD = os.getenv('GDST_BM_TEACHER_PASSWD', '')
    GdstApi = SchoolClient('http://61.142.33.204')
    bm_teacher = GdstApi.user_login(BM_TEACHER_ACCOUNT, BM_TEACHER_PASSWD,  user_type=2, timeout=3)

    def setUp(self):
        print('正在执行\033[1;35m %s \033[0m函数。' % self._testMethodName)

    def tearDown(self):
        pass

    def test_schedule(self):
        schedule_data = self.bm_teacher.get_schedule(class_name='15软件本科2班', timeout=5)
        print(schedule_data)

    def test_place_schedule(self):
        for schedule_data in self.bm_teacher.get_place_schedule(campus_list=[u"本部"], timeout=5):
            print(schedule_data)
            break


if __name__ == '__main__':
    unittest.main()
