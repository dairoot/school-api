# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from school_api.exceptions import SchoolException, LoginException, PermissionException


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
        def func(*args, **kwargs):
            return {'error': self.tip}
        return func

    def __nonzero__(self):
        return True


def error_handle(func):
    def wrapper(self, *args, **kwargs):
        if not self.school.use_ex_handle:
            result = func(self, *args, **kwargs)
        else:
            try:
                result = func(self, *args, **kwargs)

            except LoginException as reqe:
                result = LoginFail(str(reqe))

            except SchoolException as reqe:
                result = {'error': str(reqe)}

        return result
    return wrapper


class ApiPermissions():
    ''' 接口权限判断 '''

    def __init__(self, permission_list):
        self.permission_list = permission_list

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            func_object = args[0]
            if func_object.user.user_type not in self.permission_list:
                raise PermissionException(func_object.school.code, '暂无该接口权限')
            return func(*args, **kwargs)
        return wrapper


def get_time_list(class_time):
    ''' 上课时间处理 '''
    time_list = {1: [], 2: [], 3: [], 4: []}
    time_text = "{} ~ {}"
    for index, times in enumerate(class_time):
        if index % 2 == 0:
            time_list[1].append(time_text.format(times[0], times[1]))
            time_list[2].append(time_text.format(times[0], class_time[index+1][1]))

            if index < 8:
                time_list[3].append(time_text.format(times[0], class_time[index+2][1]))
                time_list[4].append(time_text.format(times[0], class_time[index+3][1]))
    return time_list
