import logging
from requests import exceptions


logger = logging.getLogger(__name__)


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
            tip = '[{}]: 教务系统[{}]]函数'.format(self.school.name or self.BASE_URL, func.__name__)
            try:
                return func(self, **kwargs)
            except exceptions.Timeout as e:
                err_info = tip + '请求超时，错误信息: {}'.format(e)
                logger.warning(err_info)
                return NullClass(err_info)
            except Exception as e:
                err_info = tip + '报错，错误信息: {}'.format(e)
                logger.warning(err_info)
                return NullClass(err_info)
        else:
            return func(self, **kwargs)
    return wrapper
