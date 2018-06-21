# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

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

        def echo_log(tip, msg):
            name = self.school.name or self.base_url
            error_info = '[{}]: {}，错误信息: {}'.format(name, tip, msg)
            logger.warning(error_info)

        if not self.school.debug:
            # 请求失败 销毁类方法
            try:
                return func(self, **kwargs)

            except exceptions.Timeout as e:
                tip = '教务系统[{}]函数请求超时'.format(func.__name__)
                echo_log(tip, e)
                return NullClass(tip)

            except Exception as e:
                tip = '教务系统[{}]函数报错'.format(func.__name__)
                echo_log(tip, e)
                raise
        else:
            return func(self, **kwargs)

    return wrapper

