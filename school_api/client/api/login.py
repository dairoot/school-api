# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re
import logging
import requests
from bs4 import BeautifulSoup
from school_api.client.api.base import BaseSchoolApi
from school_api.check_code import check_code

logger = logging.getLogger(__name__)
logging.basicConfig()


class LoginFail(dict):
    ''' 登录失败返回错误信息 '''

    def __init__(self, tip=''):
        self.tip = tip

    def __getattr__(self, name):
        def func(**kwargs):
            return {'status': False, 'err_msg': self.tip}
        return func


class Login(BaseSchoolApi):
    ''' 登录模块 '''

    def _login(self, login_url, exist_verify, **kwargs):
        # 登录请求
        code = ''
        login_types = [u'学生', u'教师', u'部门']
        view_state = self._get_login_view_state(**kwargs)

        if exist_verify:
            res = self._get('/CheckCode.aspx')
            code = check_code.verify(res.content)
            print('code', code)

        account = self.account.encode('gb2312')
        payload = {
            '__VIEWSTATE': view_state,
            'txtUserName': account,
            'TextBox1': account,
            'TextBox2': self.password,
            'TextBox3': code,
            'txtSecretCode': code,
            'RadioButtonList1': login_types[self.user_type].encode('gb2312'),
            'Button1': u' 登 录 '.encode('gb2312')
        }

        self._update_headers({'Referer': self.base_url + login_url})
        res = self._post(login_url, data=payload, allow_redirects=False, **kwargs)
        return res

    def get_login(self, school, **kwargs):
        ''' 登录入口 与 异常处理 '''
        args = (school['login_url'], school['exist_verify'])

        try:
            res = self._login(*args, **kwargs)
        except requests.exceptions.Timeout as e:
            name = school['name'] or self.base_url
            if school['proxies'] and not school['use_proxy']:
                logger.warning("[%s]: 教务系统外网异常，切换内网代理，错误信息: %s", name, e)
                # 使用内网代理
                self._set_proxy()
                res = self._login(*args, **kwargs)
            else:
                logger.warning("[%s]: 教务系统登陆失败，错误信息: %s", name, e)
                return LoginFail('登陆失败')

        return self._get_login_result(res, *args, **kwargs)

    def _get_login_result(self, res, *args, **kwargs):
        # 登录成功之后，教务系统会返回 302 跳转
        if res.status_code == 500:
            return LoginFail('服务器500报错')
        elif res.status_code != 302:
            page_soup = BeautifulSoup(res.text, "html.parser")
            alert_soup = page_soup.find_all('script')[-1]
            tip = re.findall(r'[^()\']+', alert_soup.text)[1]

            if tip == '验证码不正确！！':
                # 再次登录
                res = self._login(*args, **kwargs)
                if res.status_code == 302:
                    return None

            return LoginFail(tip)
