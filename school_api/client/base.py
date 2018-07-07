# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import inspect
import requests
from bs4 import BeautifulSoup

from school_api.client.api.base import BaseSchoolApi
from school_api.session.memorystorage import MemoryStorage
from school_api.utils import to_text


def _is_api_endpoint(obj):
    return isinstance(obj, BaseSchoolApi)


class BaseSchoolClient(object):
    school_url = [
        {
            # 学生
            'SCORE_URL': '/xscj_gc.aspx?xh=',
            'INFO_URL': '/xsgrxx.aspx?gnmkdm=N121501&xh=',
            'SCHEDULE_URL': [
                '/xskbcx.aspx?gnmkdm=N121603&xh=',
                '/tjkbcx.aspx?gnmkdm=N121601&xh='
            ]
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

        self.school_cfg = {
            'url': url,
            'debug': kwargs.get('debug'),
            'name': kwargs.get('name'),
            'exist_verify': kwargs.get('exist_verify', True),
            'lan_url': kwargs.get('lan_url'),
            'proxies': kwargs.get('proxies'),
            'use_proxy': kwargs.get('use_proxy'),
            'timeout': kwargs.get('timeout', 10),
            'login_url': kwargs.get('login_url_path', '/default2.aspx'),
            'school_url': kwargs.get('conf_url', self.school_url)
        }
        storage = kwargs.get('session', MemoryStorage)
        self.session = storage(self.school_cfg['name'])
        self.init_login_view_state(kwargs.get('login_view_state', {}))

    def init_login_view_state(self, login_view_state):
        '''
        获取登录的 view_state 学校变量
        当该值存在的时候，不请求， 首先请求在初始化学校的时候
        若学生登录时，无该值，则调用该函数。
        '''
        for url_key, view_state in login_view_state.items():
            # self.session.set('login_view:'+url_key, view_state)
            pass


class BaseUserClient(object):
    """docstring for BaseUserClient"""

    _proxy = None

    def __new__(cls, *args, **kwargs):
        self = super(BaseUserClient, cls).__new__(cls)
        api_endpoints = inspect.getmembers(self, _is_api_endpoint)
        for name, api in api_endpoints:
            api_cls = type(api)
            api = api_cls(self)
            setattr(self, name, api)
        return self

    def __init__(self, school, account, password, user_type):
        self._http = requests.Session()
        self._http.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/62.0.3202.89 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
        })
        self.account = to_text(account)
        self.password = password
        self.user_type = user_type
        self.school_cfg = school.school_cfg
        self.base_url = self.school_cfg['url']
        self.session = school.session

        if self.school_cfg['use_proxy']:
            self.set_proxy()

    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith(('http://', 'https://')):
            url = '{base}{endpoint}'.format(
                base=self.base_url,
                endpoint=url_or_endpoint
            )
        else:
            url = url_or_endpoint

        kwargs['timeout'] = kwargs.get('timeout', self.school_cfg['timeout'])
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
        self.school_cfg['use_proxy'] = True
        self.base_url = self.school_cfg['lan_url'] or self.base_url
        self._proxy = self.school_cfg['proxies']

    def update_headers(self, headers_dict):
        self._http.headers.update(headers_dict)

    def get_view_state(self, url_suffix, **kwargs):
        res = self.get(url_suffix, allow_redirects=False, **kwargs)
        if res.status_code != 200:
            return None
        return self.get_view_state_from_html(res.text)

    @staticmethod
    def get_view_state_from_html(html):
        pre_soup = BeautifulSoup(html, "html.parser")
        view_state = pre_soup.find(
            attrs={"name": "__VIEWSTATE"})['value']
        return view_state

    def get_login_session(self):
        ''' 获取登录会话 '''
        url = self.base_url + self.school_cfg['login_url']
        key = '{}:{}:{}'.format('login_session', url, self.account)
        cookie = self.session.get(key)
        if not cookie:
            return None
        url = self.base_url + self.school_cfg['login_url']
        self.update_headers({'Referer': url})
        self._http.cookies.update(cookie)
        return True

    def save_login_session(self):
        ''' 保存登录会话 '''
        url = self.base_url + self.school_cfg['login_url']
        key = '{}:{}:{}'.format('login_session', url, self.account)
        cookie = self._http.cookies.get_dict()
        self.session.set(key, cookie, 3600)

    def get_login_view_state(self, **kwargs):
        ''' 获取登录的view_state '''
        base_key = 'login_view:' + self.base_url + self.school_cfg['login_url']
        if not self.session.get(base_key):
            view_state = self.get_view_state(self.school_cfg['login_url'], **kwargs)
            self.session.set(base_key, view_state)
        return self.session.get(base_key)
