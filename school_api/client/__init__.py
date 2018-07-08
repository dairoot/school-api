# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from school_api.client.base import BaseUserClient, BaseSchoolClient
from school_api.client.api.login import Login
from school_api.client.api.score import Score
from school_api.client.api.schedule import Schedule
from school_api.client.api.user_info import SchoolInfo
from school_api.client.utils import UserType, error_handle


class SchoolClient(BaseSchoolClient):

    def __init__(self, url, **kwargs):
        super(SchoolClient, self).__init__(url, **kwargs)

    def user_login(self, account, password, user_type=UserType.STUDENT, **kwargs):
        user = UserClient(self, account, password, user_type)

        # 读取缓存会话
        if user.get_login_session():
            return user

        user = user.user_login(**kwargs) or user
        if isinstance(user, UserClient):
            # 保存会话
            user.save_login_session()

        return user


class UserClient(BaseUserClient):
    login = Login()
    score = Score()
    info = SchoolInfo()
    schedule = Schedule()

    def __init__(self, school_object, account, password, user_type):
        super(UserClient, self).__init__(school_object, account, password, user_type)

    @error_handle
    def user_login(self, **kwargs):
        return self.login.get_login(self.school, **kwargs)

    @error_handle
    def get_schedule(self, **kwargs):
        return self.schedule.get_schedule(**kwargs)

    @error_handle
    def get_info(self, **kwargs):
        return self.info.get_info(**kwargs)

    @error_handle
    def get_score(self, **kwargs):
        return self.score.get_score(**kwargs)
