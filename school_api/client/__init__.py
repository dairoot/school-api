# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from school_api.client.base import BaseUserClient, BaseSchoolClient
from school_api.client.api.score import Score
from school_api.client.api.schedule import Schedule
from school_api.client.api.place_schedule import PlaceSchedule
from school_api.client.api.user_info import UserlInfo
from school_api.client.utils import UserType, error_handle, ApiPermissions


class SchoolClient(BaseSchoolClient):

    def user_login(self, account, password, **kwargs):
        ''' 用户注册入口
        进行首次绑定操作时，请将use_session 设置为False，避免其他用户进行会话登录
        :param account:  用户账号
        :param password: 用户密码
        :param user_type: 0.学生 1.教师 2.部门
        :param use_cookie: 是否使用会话登陆
        :param requests模块参数
        return
        '''
        use_cookie = True
        if not kwargs.pop('use_session', True) or not kwargs.pop('use_cookie', True):
            use_cookie = False
        user_type = kwargs.pop('user_type', UserType.STUDENT)
        user = UserClient(self, account, password, user_type)
        user = user.user_login(use_cookie, **kwargs)
        return user


class UserClient(BaseUserClient):
    score = Score()
    info = UserlInfo()
    schedule = Schedule()
    place_schedule = PlaceSchedule()

    @error_handle
    def user_login(self, use_cookie, **kwargs):
        ''' 登录：通过SchoolClient类调用 '''
        login_session = None
        if use_cookie:
            login_session = self.session_management()

        if login_session is None:
            self.login.get_login(self.school, **kwargs)
            self.save_login_session()
            login_session = self

        return login_session

    @error_handle
    def get_schedule(self, *args, **kwargs):
        return self.schedule.get_schedule(**kwargs)

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
