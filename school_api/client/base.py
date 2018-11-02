# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import inspect
import requests

from school_api.client.utils import get_time_list
from school_api.client.api.base import BaseSchoolApi

from school_api.client.api.utils import get_view_state_from_html
from school_api.client.login_management import LoginManagement
from school_api.session.memorystorage import MemoryStorage
from school_api.utils import to_text, ObjectDict
from school_api.config import URL_ENDPOINT, CLASS_TIME


def _is_api_endpoint(obj):
    return isinstance(obj, BaseSchoolApi)


class BaseSchoolClient(object):

    def __init__(self, url, **kwargs):
        url = url.split('/default')[0] if url[-4:] == 'aspx' else url
        class_time_list = kwargs.get('class_time_list') or CLASS_TIME
        time_list = get_time_list(class_time_list)

        self.school = {
            'url': url,
            'debug': kwargs.get('debug'),
            'name': to_text(kwargs.get('name')),
            'code': kwargs.get('code'),
            'use_ex_handle': kwargs.get('use_ex_handle', True),
            'exist_verify': kwargs.get('exist_verify', True),
            'lan_url': kwargs.get('lan_url'),
            'proxies': kwargs.get('proxies'),
            'priority_porxy': kwargs.get('priority_porxy'),
            'timeout': kwargs.get('timeout', 10),
            'login_url': kwargs.get('login_url_path', '/default2.aspx'),
            'url_endpoint': kwargs.get('url_endpoint') or URL_ENDPOINT,
            'time_list': time_list
        }
        storage = kwargs.get('session', MemoryStorage)
        self.session = storage(self.school['code'])
        self.school = ObjectDict(self.school)


class BaseUserClient(LoginManagement):
    """docstring for BaseUserClient"""

    _proxy = None

    def __new__(cls, *args):
        self = super(BaseUserClient, cls).__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, api in api_endpoints:
            api_cls = type(api)
            api = api_cls(self)
            setattr(self, name, api)
        return self

    def __init__(self, school, account, password, user_type):
        self._http = requests.Session()

        self.account = to_text(account)
        self.password = password
        self.user_type = user_type
        self.school = school.school
        self.base_url = self.school.url
        self.session = school.session
        super(BaseUserClient, self).__init__(self.base_url + self.school.login_url,
                                             self.account, self.session, self._http)
        self._http.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/62.0.3202.89 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': self.base_url + self.school.login_url
        })
        if self.school.priority_porxy:
            self.set_proxy()

    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith(('http://', 'https://')):
            url = '{base}{endpoint}'.format(
                base=self.base_url,
                endpoint=url_or_endpoint
            )
        else:
            url = url_or_endpoint

        kwargs['timeout'] = kwargs.get('timeout', self.school.timeout)
        res = self._http.request(
            method=method,
            url=url,
            proxies=self._proxy,
            **kwargs
        )
        return res

    def get(self, url, **kwargs):
        return self._request(
            method='GET',
            url_or_endpoint=url,
            **kwargs
        )

    def post(self, url, **kwargs):
        return self._request(
            method='POST',
            url_or_endpoint=url,
            **kwargs
        )

    def head(self, url, **kwargs):
        return self._request(
            method='HEAD',
            url_or_endpoint=url,
            **kwargs
        )

    def set_proxy(self):
        """ 设置代理 """
        self.school.priority_porxy = True
        self.base_url = self.school.lan_url or self.base_url
        self._proxy = self.school.proxies
        self._http.headers.update({
            'Referer': self.base_url + self.school.login_url
        })

    def get_view_state(self, url_suffix, **kwargs):
        """ 获取页面 view_state 值"""
        res = self.get(url_suffix, allow_redirects=False, **kwargs)
        res.raise_for_status()
        if res.status_code == 302:
            raise requests.TooManyRedirects

        return get_view_state_from_html(res.text)
