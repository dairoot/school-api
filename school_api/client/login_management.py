# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from school_api.client.api.login import Login
from school_api.config import LOGIN_SESSION_SAVE_TIME


class LoginManagement(object):
    """ 登录会话管理 """
    login = Login()

    def __init__(self, url, account, session, http):
        self.url = url
        self._http = http
        self.account = account
        self.session = session

    def session_management(self):
        ''' 登录会话管理 '''
        login_session = None
        if self._get_login_session():
            session_expires_time = LOGIN_SESSION_SAVE_TIME \
                - self._get_login_session_expires_time()

            if session_expires_time < 60 * 5:
                # 五分钟内，不检测登录会话是否过期
                login_session = self
            elif self.login.check_session():
                # 登录会话检测
                if 60 * 5 < session_expires_time < 60 * 10:
                    # 登录比较频繁的，更新会话时间 (例如：部门账号操作)
                    self.save_login_session()
                login_session = self
            else:
                # 会话过期, 删除会话
                self._del_login_session()

        return login_session

    def save_login_session(self):
        ''' 保存登录会话 '''
        key = self._get_login_session_key()
        cookie = self._http.cookies.get_dict()
        self.session.set(key, cookie, LOGIN_SESSION_SAVE_TIME)

    def _del_login_session(self):
        ''' 删除登录会话 '''
        key = self._get_login_session_key()
        self.session.delete(key)
        self._http.cookies.clear()

    def _get_login_session(self):
        ''' 获取登录会话 '''
        key = self._get_login_session_key()
        cookie = self.session.get(key)
        if not cookie:
            return None
        self._http.headers.update({'Referer': self.url})
        self._http.cookies.update(cookie)
        return True

    def _get_login_session_expires_time(self):
        """ 获取登录会话过期时间 """
        key = self._get_login_session_key()
        return self.session.expires_time(key)

    def _get_login_session_key(self):
        ''' 获取缓存登录会话的key '''
        key = '{}:{}:{}'.format('login_session', self.url, self.account)
        return key
