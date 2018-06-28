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
        return user.user_login(**kwargs) or user


class UserClient(BaseUserClient):
    login = Login()
    score = Score()
    info = SchoolInfo()
    schedule = Schedule()

    def __init__(self, school, account, password, user_type):
        super(UserClient, self).__init__(school, account, password, user_type)

    @error_handle
    def user_login(self, **kwargs):
        return self.login.get_login(self.school_cfg, **kwargs)

    @error_handle
    def get_schedule(self, **kwargs):
        return self.schedule.get_schedule(**kwargs)

    @error_handle
    def get_info(self, **kwargs):
        return self.info.get_info(**kwargs)

    @error_handle
    def get_score(self, **kwargs):
        return self.score.get_score(**kwargs)
