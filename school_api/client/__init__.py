# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from school_api.client.base import BaseUserClient, BaseSchoolClient
from school_api.client.api.login import Login
from school_api.client.api.score import Score
from school_api.client.api.schedule import Schedule
from school_api.client.api.place_schedule import PlaceSchedule
from school_api.client.api.user_info import UserlInfo
from school_api.client.utils import UserType, error_handle
from school_api.config import LOGIN_SESSION_SAVE_TIME


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
    login = Login()
    score = Score()
    info = UserlInfo()
    schedule = Schedule()
    place_schedule = PlaceSchedule()

    @error_handle
    def user_login(self, use_session, **kwargs):
        ''' 登录：通过SchoolClient类调用 '''
        login_session = None
        if use_session and self.get_login_session():
            session_expires_time = LOGIN_SESSION_SAVE_TIME \
                - self.get_login_session_expires_time()

            if session_expires_time < 60 * 5:
                # 五分钟内，不检测登录会话是否过期
                login_session = self
            elif self.login.check_session():
                # 登录会话检测
                if 60 * 5 < session_expires_time < 60 * 10:
                    # 登录比较频繁的，更新会话时间 (例如：部门账号操作)
                    self.save_login_session()
                login_session = self
            # 会话过期, 删除会话
            self.del_login_session()

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
