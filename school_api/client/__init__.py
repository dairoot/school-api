# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from school_api.client.base import BaseUserClient, BaseSchoolClient
from school_api.client.api.score import Score
from school_api.client.api.schedule import Schedule
from school_api.client.api.place_schedule import PlaceSchedule
from school_api.client.api.user_info import UserlInfo
from school_api.client.utils import UserType, error_handle


class SchoolClient(BaseSchoolClient):

    def user_login(self, account, password, **kwargs):
        ''' 用户注册入口
        进行首次绑定操作时，请将use_session 设置为False，避免其他用户进行会话登录
        '''
        use_session = kwargs.pop('use_session', True)
        user_type = kwargs.pop('user_type', UserType.STUDENT)
        user = UserClient(self, account, password, user_type)
        user = user.user_login(use_session, **kwargs)
        return user


class UserClient(BaseUserClient):
    score = Score()
    info = UserlInfo()
    schedule = Schedule()
    place_schedule = PlaceSchedule()

    @error_handle
    def user_login(self, use_session, **kwargs):
        ''' 登录：通过SchoolClient类调用 '''
        login_session = None
        if use_session:
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
    def get_info(self, **kwargs):
        return self.info.get_info(**kwargs)

    @error_handle
    def get_score(self, *args, **kwargs):
        return self.score.get_score(*args, **kwargs)

    def get_place_schedule(self, *args, **kwargs):
        return self.place_schedule.get_schedule(*args, **kwargs)
