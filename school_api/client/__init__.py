# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from school_api.utils import to_text, ObjectDict
from school_api.config import URL_PATH_LIST, CLASS_TIME
from school_api.client.base import BaseUserClient
from school_api.client.api.score import Score
from school_api.client.api.schedule import Schedule
from school_api.client.api.place_schedule import PlaceSchedule
from school_api.client.api.user_info import UserlInfo
from school_api.client.utils import UserType, error_handle, ApiPermissions, get_time_list
from school_api.session.memorystorage import MemoryStorage


class SchoolClient(object):
    ''' 学校实例 '''

    def __init__(self, url, name=None, code=None, use_ex_handle=True, exist_verify=True, lan_url=None, proxies=None,
                 priority_proxy=False, timeout=10, login_url_path='/default2.aspx', url_path_list=URL_PATH_LIST,
                 class_time_list=CLASS_TIME, session=MemoryStorage):
        school = {
            'code': code,
            'lan_url': lan_url,
            'proxies': proxies,
            'timeout': timeout,
            'name': to_text(name),
            'login_url': login_url_path,
            'url_path_list': url_path_list,
            'exist_verify': exist_verify,
            'use_ex_handle': use_ex_handle,
            'priority_proxy': priority_proxy,
            'time_list': get_time_list(class_time_list)
        }
        self.base_url = url.split('/default')[0] if url[-4:] == 'aspx' else url
        self.session = session(school['code'])
        self.school = ObjectDict(school)

    def user_login(self, account, password, use_login_cookie=True ,**kwargs):
        ''' 用户登录入口
        进行首次绑定操作时，请将 use_login_cookie 设置为False，避免其他用户进行会话登录
        :param account:  用户账号
        :param password: 用户密码
        :param user_type: 0.学生 1.教师 2.部门
        :param use_login_cookie: 是否使用会话登陆
        :param requests模块参数
        return 用户实例
        '''
        user_type = kwargs.pop('user_type', UserType.STUDENT)
        user = UserClient(self, account, password, user_type)
        user = user.user_login(use_login_cookie, **kwargs)
        return user


class UserClient(BaseUserClient):
    ''' 用户实例 '''

    score = Score()
    info = UserlInfo()
    schedule = Schedule()
    place_schedule = PlaceSchedule()

    @error_handle
    def user_login(self, use_login_cookie, **kwargs):
        ''' 登录：通过SchoolClient类调用 '''
        login_session = None
        if use_login_cookie:
            login_session = self.session_management()

        if login_session is None:
            self.login.get_login(self.school, **kwargs)
            self.save_login_session()
            login_session = self

        return login_session

    @error_handle
    def get_schedule(self, *args, **kwargs):
        return self.schedule.get_schedule(*args, **kwargs)

    @error_handle
    @ApiPermissions([UserType.STUDENT, UserType.TEACHER])
    def get_info(self, **kwargs):
        return self.info.get_info(**kwargs)

    @error_handle
    @ApiPermissions([UserType.STUDENT])
    def get_score(self, *args, **kwargs):
        return self.score.get_score(*args, **kwargs)

    @error_handle
    @ApiPermissions([UserType.DEPT])
    def get_place_schedule(self, *args, **kwargs):
        return self.place_schedule.get_schedule(*args, **kwargs)
