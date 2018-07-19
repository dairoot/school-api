# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re
from bs4 import BeautifulSoup
from requests import RequestException
from school_api.client.api.base import BaseSchoolApi
from school_api.check_code import check_code
from school_api.exceptions import IdentityException, CheckCodeException, LoginException


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
        args = (school.login_url, school.exist_verify)
        try:
            res = self._login(*args, **kwargs)
        except RequestException:
            if school.proxies and not school.use_proxy:
                # 使用内网代理
                self._set_proxy()
                try:
                    res = self._login(*args, **kwargs)
                    if res.status_code != 302:
                        raise LoginException(self.code, '教务系统异常，使用代理登录失败')
                except RequestException:
                    raise LoginException(self.code, '教务系统异常，使用代理登录失败')
            else:
                raise LoginException(self.code, '教务系统外网异常')

        return self._get_login_result(res, *args, **kwargs)

    def _get_login_result(self, res, *args, **kwargs):
        # 登录成功之后，教务系统会返回 302 跳转
        if res.status_code == 500:
            raise LoginException(self.code, '教务系统请求异常')
        elif res.status_code != 302:
            page_soup = BeautifulSoup(res.text, "html.parser")
            alert_soup = page_soup.find_all('script')[-1]
            tip = re.findall(r'[^()\']+', alert_soup.text)[1]

            if tip == '验证码不正确！！':
                # 再次登录
                res = self._login(*args, **kwargs)
                if res.status_code != 302:
                    raise CheckCodeException(self.code, tip)

            raise IdentityException(self.code, tip)

    def check_session(self):

        try:
            res = self._head(self.school_url['HOME_URL'] + self.account)
            if res.status_code != 200:
                raise RequestException
        except RequestException:
            raise LoginException(self.code, '验证登录会话失败')

        return True
