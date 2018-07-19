# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from school_api.exceptions import SchoolException, LoginException


class UserType():
    ''' 用户类型参数 '''
    STUDENT = 0
    TEACHER = 1
    DEPT = 2


class ScheduleType():
    ''' 课表类型参数 '''
    PERSON = 0
    CLASS = 1


class LoginFail():
    ''' 登录失败返回错误信息 '''

    def __init__(self, tip=''):
        self.tip = tip

    def __getattr__(self, name):
        def func(**kwargs):
            return {'error': self.tip}
        return func

    def __nonzero__(self):
        return True


def error_handle(func):
    def wrapper(self, *args, **kwargs):
        if not self.school.use_ex_handle:
            return func(self, *args, **kwargs)
        else:
            try:
                return func(self, *args, **kwargs)

            except LoginException as reqe:
                return LoginFail(reqe)

            except SchoolException as reqe:
                return {'error': reqe}
    return wrapper
