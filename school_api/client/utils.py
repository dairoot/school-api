import requests


class UserType():
    STUDENT = 0
    TEACHER = 1
    DEPT = 2


class ScheduleType():
    PERSON = 0
    CLASS = 1


class NullClass():

    def __init__(self, tip=''):
        self.tip = tip

    def __str__(self):
        return self.tip

    def __getattr__(self, name):
        def func(**kwargs):
            return self
        return func


def error_handle(func):
    def wrapper(self, **kwargs):
        if not self.school.debug:
            # 请求失败 销毁类方法
            try:
                return func(self, **kwargs)
            except requests.exceptions.ConnectTimeout:
                return NullClass('{}: {} {}'.format(func.__name__, self.school.url, '请求超时'))
            except requests.exceptions.ReadTimeout:
                return NullClass('{}: {} {}'.format(func.__name__, self.school.url, '请求超时'))
            except Exception as e:
                return NullClass('{}: {}'.format(func.__name__, e))
        else:
            return func(self, **kwargs)
    return wrapper
