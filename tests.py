from school_api import SchoolClient
from conf import *


conf = {
    'name': '广东科技学院',
    'debug': False,                 # 模块调试
    'lan_url': 'http://172.16.1.8',  # 内网地址
    'use_proxy': False,             # 是否优先使用代理
    'school_url': None,             # 教务系统链接
    'proxies': {"http": "http://gxgk:gxgkteam@tunnel.gxgk.cc:3120/", }  # 代理
}

# 先实例化一个学校，再实例化用户
GdstApi = SchoolClient('http://61.142.33.204', **conf)
TestApi = SchoolClient('http://61.142.33.2', **conf)

student = GdstApi.user_login(STUDENT_ACCOUNT, STUDENT_PASSWD, timeout=3)
teacher = GdstApi.user_login(TEACHER_ACCOUNT, TEACHER_PASSWD, user_type=1, timeout=3)
bm_teacher = GdstApi.user_login(BM_TEACHER_ACCOUNT, BM_TEACHER_PASSWD, user_type=2, timeout=3)

student_test = TestApi.user_login(STUDENT_ACCOUNT, STUDENT_PASSWD, timeout=3)


def test_student_query():
    schedule_data = student.get_schedule(schedule_year='2017-2018', schedule_term='1', timeout=5)
    schedule_data = student.get_schedule(
        schedule_type=1, schedule_year='2017-2018', schedule_term='1')
    score_data = student.get_score(score_year='2017-2018', score_term='1', timeout=5)
    info_data = student.get_info(timeout=5)


def test_teacher_query():
    schedule_data = teacher.get_schedule(schedule_year='2017-2018', schedule_term='1', timeout=5)
    info_data = teacher.get_info(timeout=5)


def test_bm_teacher_query():
    schedule_data = bm_teacher.get_schedule(class_name='15软件本科2班', timeout=5)


def test_fail():
    schedule_data = student_test.get_schedule(
        schedule_year='2017-2018', schedule_term='1', timeout=5)
    schedule_data = student_test.get_schedule(
        schedule_type=1, schedule_year='2017-2018', schedule_term='1')
    score_data = student_test.get_score(score_year='2017-2018', score_term='1', timeout=5)
    info_data = student_test.get_info(timeout=5)
