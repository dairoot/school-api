# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from six.moves.urllib import parse
from requests import RequestException
from school_api.client.api.base import BaseSchoolApi
from school_api.client.api.utils import get_alert_tip, get_view_state_from_html
from school_api.check_code import CHECK_CODE
from school_api.exceptions import IdentityException, CheckCodeException, LoginException, OtherException
from school_api.utils import to_binary, to_text


class Login(BaseSchoolApi):
    ''' 登录模块 '''

    def get_login(self, school, **kwargs):
        ''' 登录入口 与 异常处理 '''
        args = (school.login_url, school.exist_verify)
        try:
            res = self._get_api(*args, **kwargs)
        except OtherException as reqe:
            raise LoginException(self.code, to_text(str(reqe)))

        except RequestException:
            if school.proxies and not self.user.proxy_state:
                # 使用内网代理
                if self._switch_proxy():
                    # 存在内网代理会话
                    return True
                try:
                    res = self._get_api(*args, **kwargs)
                except RequestException:
                    raise LoginException(self.code, '教务系统异常，切用代理登录失败')
            else:

                if self.user.proxy_state:
                    raise LoginException(self.code, '教务系统异常，使用代理登录失败')
                else:
                    raise LoginException(self.code, '教务系统外网异常')

        self._handle_login_result(res, *args, **kwargs)

    def _get_login_payload(self, login_url, **kwargs):
        ''' 获取登录页面的 请求参数'''
        try:
            kwargs['timeout'] = 3
            res = self._get(login_url, **kwargs)
        except RequestException:

            # 首次请求可能出现 Connection aborted
            res = self._get(login_url, **kwargs)

        url_info = res.url.split(login_url)[0].split('/(')
        if len(url_info) == 2:
            self._update_url_token('/(' + url_info[1])

        view_state = get_view_state_from_html(res.text)

        return {'__VIEWSTATE': view_state}

    def _get_api(self, login_url, exist_verify, **kwargs):
        # 登录请求
        code = ''
        login_types = ['学生', '教师', '部门']
        login_payload = self._get_login_payload(login_url, **kwargs)
        if exist_verify:
            res = self._get('/CheckCode.aspx')
            if res.content[:7] != to_binary('GIF89aH'):
                raise CheckCodeException(self.code, "验证码获取失败")
            code = CHECK_CODE.verify(res.content)

        account = self.user.account.encode('gb2312')
        payload = {
            'txtUserName': account,
            'TextBox1': account,
            'TextBox2': self.user.password,
            'TextBox3': code,
            'txtSecretCode': code,
            'RadioButtonList1': login_types[self.user.user_type].encode('gb2312'),
            'Button1': ' 登 录 '.encode('gb2312')
        }
        payload.update(login_payload)

        res = self._post(login_url, data=payload,
                         allow_redirects=False, **kwargs)
        return res

    def _handle_login_result(self, res, *args, **kwargs):
        # 登录成功之后，教务系统会返回 302 跳转
        if res.status_code == 500:
            raise LoginException(self.code, '教务系统请求异常')
        elif res.status_code != 302:
            tip = self._get_login_result_tip(res.text)
            check_code_error_tip = '验证码不正确！！'
            if tip == check_code_error_tip:
                # 首次验证码错误，则再次登录
                res = self._get_api(*args, **kwargs)
                if res.status_code != 302:
                    tip = self._get_login_result_tip(res.text)
                    if tip == check_code_error_tip:
                        raise CheckCodeException(self.code, tip)
                else:
                    return True
            raise IdentityException(self.code, tip)
        return True

    def _get_login_result_tip(self, html):
        """ 获取获取html的弹框提示信息 """
        tip = get_alert_tip(html)
        if tip:
            return tip

        raise LoginException(self.code, '教务系统请求异常')

    def check_session(self):
        """ 检查登陆会话是否有效 """
        account = parse.quote(self.user.account.encode('gb2312'))
        try:
            res = self._head(self.school_url['HOME_URL'] + account)
            if res.status_code != 200:
                raise RequestException
        except RequestException:
            return False

        return True
