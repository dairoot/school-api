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


def error_handle(func):
    def wrapper(self, **kwargs):

        def echo_log(tip, msg):
            ''' 打印报错信息 '''
            name = self.school.name or self.base_url
            error_info = '[{}]: {}，错误信息: {}'.format(name, tip, msg)
            logger.warning(error_info)
            return {'status': False, 'err_msg': tip}

        if self.school.debug:
            return func(self, **kwargs)
        else:
            try:
                return func(self, **kwargs)
            except exceptions.ConnectTimeout as reqe:
                tip = '教务系统[{}]函数请求超时'.format(func.__name__)
                return echo_log(tip, reqe)

            except exceptions.Timeout as reqe:
                tip = '教务系统[{}]函数请求超时'.format(func.__name__)
                return echo_log(tip, reqe)

            except exceptions.ProxyError as reqe:
                tip = '教务系统[{}]代理连接超时'.format(func.__name__)
                return echo_log(tip, reqe)

            except Exception as reqe:
                tip = '教务系统[{}]函数报错'.format(func.__name__)
                echo_log(tip, reqe)
                raise

    return wrapper
