# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re
import logging
import requests
from bs4 import BeautifulSoup, SoupStrainer
from school_api.client.api.base import BaseSchoolApi
from school_api.client.utils import NullClass

logger = logging.getLogger(__name__)


class Login(BaseSchoolApi):
    ''' 登录模块 '''

    def _login(self, **kwargs):
        # 登录请求
        login_types = [u'学生', u'教师', u'部门']
        view_state = self._get_view_state(self.school_url['LOGIN_URL'], **kwargs)
        payload = {
            '__VIEWSTATE': view_state,
            'TextBox1': self.account.encode('gb2312'),
            'TextBox2': self.password,
            'RadioButtonList1': login_types[self.user_type].encode('gb2312'),
            'Button1': u' 登 录 '.encode('gb2312')
        }
        self._update_headers({'Referer': self.base_url + self.school_url['LOGIN_URL']})
        res = self._post(self.school_url['LOGIN_URL'], data=payload,
                         allow_redirects=False, **kwargs)
        return res

    def get_login(self, school, **kwargs):
        ''' 登录入口 与 异常处理 '''
        try:
            res = self._login(**kwargs)
        except requests.exceptions.Timeout as e:
            if school['proxies'] and not school['use_proxy']:
                logger.warning("[%s]: 教务系统外网异常，切换内网代理，错误信息: %s", school['name'] or self.base_url, e)
                # 使用内网代理
                school['use_proxy'] = True
                self._set_proxy()
                res = self._login(**kwargs)
            else:
                logger.warning("[%s]: 教务系统登陆失败，错误信息: %s", school['name'] or self.base_url, e)
                return NullClass('登陆失败')

        # 登录成功之后，教务系统会返回 302 跳转
        if res and res.status_code != 302:
            page_soup = BeautifulSoup(res.text, "html.parser", parse_only=SoupStrainer("script"))
            tip = re.findall(r'[^()\']+', page_soup.getText())[1]
            return NullClass(tip)
        return None
