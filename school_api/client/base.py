# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import inspect
import requests

from school_api.utils import to_text, ObjectDict
from school_api.client.api.base import BaseSchoolApi
from school_api.client.api.utils import get_view_state_from_html
from school_api.client.login_management import LoginManagement


def _is_api_endpoint(obj):
    return isinstance(obj, BaseSchoolApi)


class BaseUserClient(LoginManagement):
    """docstring for BaseUserClient"""

    _proxy = None
    url_token = ''

    def __new__(cls, *args):
        self = super(BaseUserClient, cls).__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, api in api_endpoints:
            api_cls = type(api)
            api = api_cls(self)
            setattr(self, name, api)
        return self

    def __init__(self, school_obj, account, password, user_type):
        self._http = requests.Session()
        self.school = school_obj.school
        self.base_url = school_obj.base_url
        self.session = school_obj.session
        self.user = ObjectDict({
            'account': to_text(account),
            'password': password,
            'user_type': user_type,
            'proxy_state': False
        })
        self._http.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/62.0.3202.89 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': self.base_url + self.school.login_url
        })
        if self.school.priority_proxy:
            self.switch_proxy(True)

    def _request(self, url_suffix, **kwargs):

        url = '{base}{url_token}{url_suffix}'.format(
            base=self.base_url,
            url_suffix=url_suffix,
            url_token=self.url_token
        )
        kwargs['timeout'] = kwargs.get('timeout', self.school.timeout)
        res = self._http.request(
            url=url,
            proxies=self._proxy,
            allow_redirects=False,
            **kwargs
        )

        res.raise_for_status()
        if res.status_code == 302:
            raise requests.TooManyRedirects

        return res

    def get(self, url, **kwargs):
        return self._request(url, method='GET', **kwargs)

    def post(self, url, **kwargs):
        return self._request(url, method='POST', **kwargs)

    def head(self, url, **kwargs):
        return self._request(url, method='HEAD', **kwargs)

    def switch_proxy(self, init=False):
        """ 设置代理 """
        self.user.proxy_state = True
        self.base_url = self.school.lan_url or self.base_url
        self._proxy = self.school.proxies
        self._http.headers.update({
            'Referer': self.base_url + self.school.login_url
        })
        if not init:
            # 非初始化，检查是否存在有效会话登录会话
            return self.session_management()

    def get_view_state(self, url_suffix, **kwargs):
        """ 获取页面 view_state 值"""
        res = self.get(url_suffix, **kwargs)
        return get_view_state_from_html(res.text)

    def update_url_token(self, url_token):
        # 兼容含token的教务系统请求地址 http://xxx.xxx/(35yxiq45pv0ojz45wcopgz45)/Default2.aspx
        self.url_token = url_token
