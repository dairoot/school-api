# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging
from requests import exceptions

logger = logging.getLogger(__name__)


class UserType():
    ''' 用户类型参数 '''
    STUDENT = 0
    TEACHER = 1
    DEPT = 2


class ScheduleType():
    ''' 课表类型参数 '''
    PERSON = 0
    CLASS = 1


class NullClass():
    ''' 空类 将对象赋空 '''

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
            ''' 打印报错信息 '''
            name = self.school_cfg['name'] or self.base_url
            error_info = '[{}]: {}，错误信息: {}'.format(name, tip, msg)
            logger.warning(error_info)

        if self.school_cfg['debug']:
            return func(self, **kwargs)
        else:
            try:
                return func(self, **kwargs)

            except exceptions.Timeout as e:
                tip = '教务系统[{}]函数请求超时'.format(func.__name__)
                echo_log(tip, e)
                return NullClass(tip)

            except exceptions.ProxyError as e:
                tip = '教务系统[{}]代理连接超时'.format(func.__name__)
                echo_log(tip, e)
                return NullClass(tip)

            except Exception as e:
                tip = '教务系统[{}]函数报错'.format(func.__name__)
                echo_log(tip, e)
                raise

    return wrapper
