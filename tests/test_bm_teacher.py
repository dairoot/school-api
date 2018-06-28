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
    BM_TEACHER_ACCOUNT = os.getenv('BM_TEACHER_ACCOUNT', '')
    BM_TEACHER_PASSWD = os.getenv('BM_TEACHER_PASSWD', '')
    GdstApi = SchoolClient('http://61.142.33.204')
    bm_teacher = GdstApi.user_login(BM_TEACHER_ACCOUNT, BM_TEACHER_PASSWD,  user_type=2, timeout=3)

    def setUp(self):
        print('\033[1;35m -- \033[0m')

    def tearDown(self):
        pass

    def test_schedule(self):
        schedule_data = self.bm_teacher.get_schedule(class_name='15软件本科2班', timeout=5)
        print(schedule_data)


if __name__ == '__main__':
    unittest.main()
