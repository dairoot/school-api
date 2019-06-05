# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from school_api.client.api.login import Login
from school_api.config import LOGIN_SESSION_SAVE_TIME


class LoginManagement(object):
    """ 登录会话管理 """
    _http = None
    account = None
    session = None
    base_url = None
    url_token = ''

    login = Login()

    def session_management(self):
        ''' 登录会话管理 '''
        login_session = None
        if self._get_login_session():
            session_expires_time = LOGIN_SESSION_SAVE_TIME - self._get_login_session_expires_time()

            if session_expires_time < 60 * 5:
                # 五分钟内，不检测登录会话是否过期
                login_session = self
            elif self.login.check_session():
                # 登录会话检测有效
                if session_expires_time < 60 * 10:
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
        session = {
            "cookie": cookie,
            "url_token": self.url_token
        }
        self.session.set(key, session, LOGIN_SESSION_SAVE_TIME)

    def _get_login_session(self):
        ''' 获取登录会话 '''
        key = self._get_login_session_key()
        session = self.session.get(key)
        if not session:
            return False

        self.url_token = session['url_token']
        self._http.cookies.update(session['cookie'])
        return True

    def _del_login_session(self):
        ''' 删除登录会话 '''
        key = self._get_login_session_key()
        self.session.delete(key)
        self._http.cookies.clear()

    def _get_login_session_expires_time(self):
        """ 获取登录会话过期时间 """
        key = self._get_login_session_key()
        return self.session.expires_time(key)

    def _get_login_session_key(self):
        ''' 获取缓存登录会话的key '''
        key = '{}:{}:{}:{}'.format(self.school.code, 'login_session', self.base_url, self.user.account)
        return key
