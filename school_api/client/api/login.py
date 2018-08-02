# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re
from six.moves.urllib import parse
from requests import RequestException
from school_api.client.api.base import BaseSchoolApi
from school_api.check_code import CHECK_CODE
from school_api.exceptions import IdentityException, CheckCodeException, LoginException


class Login(BaseSchoolApi):
    ''' 登录模块 '''

    def get_login(self, school, **kwargs):
        ''' 登录入口 与 异常处理 '''
        args = (school.login_url, school.exist_verify)
        try:
            res = self._get_api(*args, **kwargs)
        except RequestException:
            if school.proxies and not school.use_proxy:
                # 使用内网代理
                self._set_proxy()
                try:
                    res = self._get_api(*args, **kwargs)
                except RequestException:
                    raise LoginException(self.code, '教务系统异常，使用代理登录失败')
            else:
                raise LoginException(self.code, '教务系统外网异常')

        self._handle_login_result(res, *args, **kwargs)

    def _get_api(self, login_url, exist_verify, **kwargs):
        # 登录请求
        code = ''
        login_types = ['学生', '教师', '部门']
        view_state = self._get_login_view_state(**kwargs)
        if exist_verify:
            res = self._get('/CheckCode.aspx')
            code = CHECK_CODE.verify(res.content)
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
            'Button1': ' 登 录 '.encode('gb2312')
        }

        self._update_headers({'Referer': self.base_url + login_url})
        res = self._post(login_url, data=payload,
                         allow_redirects=False, **kwargs)
        return res

    def _handle_login_result(self, res, *args, **kwargs):
        # 登录成功之后，教务系统会返回 302 跳转
        if res.status_code == 500:
            raise LoginException(self.code, '教务系统请求异常')
        elif res.status_code != 302:
            tip = self._get_login_result_tip(res.text)
            if tip == '验证码不正确！！':
                # 首次验证码错误，则再次登录
                res = self._get_api(*args, **kwargs)
                if res.status_code != 302:
                    tip = self._get_login_result_tip(res.text)
                    if tip == '验证码不正确！！':
                        raise CheckCodeException(self.code, tip)
            raise IdentityException(self.code, tip)

    def _get_login_result_tip(self, html):
        """ 获取获取html的弹框提示信息 """
        tips = re.findall(r"alert\(\'(.*?)\'", html)
        if tips:
            return tips[0]
        raise LoginException(self.code, '教务系统请求异常')

    def check_session(self):
        """ 检查登陆会话是否有效 """
        account = parse.quote(self.account.encode('gb2312'))
        try:
            res = self._head(self.school_url['HOME_URL'] + account)
            if res.status_code != 200:
                raise RequestException
        except RequestException:
            return False

        return True
