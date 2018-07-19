# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from school_api.client.base import BaseUserClient, BaseSchoolClient
from school_api.client.api.login import Login
from school_api.client.api.score import Score
from school_api.client.api.schedule import Schedule
from school_api.client.api.user_info import UserlInfo
from school_api.client.utils import UserType, error_handle


class SchoolClient(BaseSchoolClient):

    def __init__(self, url, **kwargs):
        super(SchoolClient, self).__init__(url, **kwargs)

    def user_login(self, account, password, use_session=True, user_type=UserType.STUDENT, **kwargs):
        ''' 用户注册入口
        进行首次绑定操作时，请将use_session 设置为False，避免其他用户进行会话登录
        '''
        user = UserClient(self, account, password, user_type)
        user = user.user_login(use_session, **kwargs)
        return user


class UserClient(BaseUserClient):
    login = Login()
    score = Score()
    info = UserlInfo()
    schedule = Schedule()

    def __init__(self, school_object, account, password, user_type):
        super(UserClient, self).__init__(school_object, account, password, user_type)

    @error_handle
    def user_login(self, use_session, **kwargs):
        ''' 登录：通过SchoolClient类调用 '''
        if use_session and self.get_login_session():
            if self.login.check_session():
                return self
            # 会话过期, 删除会话
            self.del_login_session()
        self.login.get_login(self.school, **kwargs)
        self.save_login_session()
        return self

    @error_handle
    def get_schedule(self, **kwargs):
        return self.schedule.get_schedule(**kwargs)

    @error_handle
    def get_info(self, **kwargs):
        return self.info.get_info(**kwargs)

    @error_handle
    def get_score(self, **kwargs):
        return self.score.get_score(**kwargs)
