# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import inspect
import requests
from bs4 import BeautifulSoup

from school_api.client.api.base import BaseSchoolApi


def _is_api_endpoint(obj):
    return isinstance(obj, BaseSchoolApi)


class BaseSchoolClient(object):
    school_url = [
        {
            # 学生
            'SCORE_URL': '/xscj_gc.aspx?xh=',
            'INFO_URL': '/xsgrxx.aspx?gnmkdm=N121501&xh=',
            'SCHEDULE_URL': ['/xskbcx.aspx?gnmkdm=N121603&xh=', '/tjkbcx.aspx?gnmkdm=N121601&xh=']
        }, {
            # 教师
            'INFO_URL': '/lw_jsxx.aspx?gnmkdm=N122502&zgh=',
            'SCHEDULE_URL': ['', '/jstjkbcx.aspx?gnmkdm=N122303&zgh=']
        }, {
            # 部门
            'SCHEDULE_URL': ['', '/tjkbcx.aspx?gnmkdm=N120313&xh=']
        }
    ]

    def __init__(self, url, **kwargs):
        self.school = {
            'url': url,
            'debug': kwargs.get('debug'),
            'name': kwargs.get('name'),
            'exist_verify': kwargs.get('exist_verify', True),
            'lan_url': kwargs.get('lan_url'),
            'proxies': kwargs.get('proxies'),
            'use_proxy': kwargs.get('use_proxy'),
            'timeout': kwargs.get('timeout'),
            'login_url': kwargs.get('login_url', '/default2.aspx'),
            'school_url': kwargs.get('conf_url', self.school_url)
        }


class BaseUserClient(object):
    """docstring for BaseUserClient"""

    _proxy = None

    def __new__(cls, *args, **kwargs):
        self = super(BaseUserClient, cls).__new__(cls)
        self._http = requests.Session()
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, api in api_endpoints:
            api_cls = type(api)
            api = api_cls(self)
            setattr(self, name, api)
        return self

    def __init__(self, school, account, password, user_type):
        self._http.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/62.0.3202.89 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
        })
        self.account = account
        self.password = password
        self.school = school
        self.user_type = user_type
        self.base_url = self.school['url']

        if self.school['use_proxy']:
            self.set_proxy()

    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith(('http://', 'https://')):
            url = '{base}{endpoint}'.format(
                base=self.base_url,
                endpoint=url_or_endpoint
            )
        else:
            url = url_or_endpoint

        kwargs['timeout'] = kwargs.get('timeout', self.school['timeout'])
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

    def set_proxy(self):
        self.base_url = self.school['lan_url'] or self.base_url
        self._proxy = self.school['proxies']

    def get_view_state(self, url_suffix, **kwargs):
        res = self.get(url_suffix, allow_redirects=False, **kwargs)
        if res.status_code != 200:
            return None
        return self.get_view_state_from_html(res.text)

    def get_view_state_from_html(self, html):
        pre_soup = BeautifulSoup(html, "html.parser")
        view_state = pre_soup.find(
            attrs={"name": "__VIEWSTATE"})['value']
        return view_state

    def update_headers(self, headers_dict):
        self._http.headers.update(headers_dict)
