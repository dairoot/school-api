# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from six.moves.urllib import parse
from requests import RequestException, TooManyRedirects

from school_api.check_code import CHECK_CODE
from school_api.utils import to_binary, to_text
from school_api.client.api.base import BaseSchoolApi
from school_api.client.api.utils import get_alert_tip, get_view_state_from_html
from school_api.exceptions import IdentityException, CheckCodeException, LoginException, \
    OtherException


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

        # 处理登录结果
        try:
            self._handle_login_result(res)
        except CheckCodeException:
            try:
                # 验证码错误时，再次登录
                res = self._get_api(*args, **kwargs)
            except RequestException:
                raise LoginException(self.code, '教务系统请求异常')
            else:
                self._handle_login_result(res)

        return True

    def _handle_login_result(self, res):
        ''' 处理页面弹框信息 '''
        if res is True:
            # 登录成功
            return
        tip = get_alert_tip(res.text)
        if tip:
            if tip == '验证码不正确！！':
                raise CheckCodeException(self.code, tip)
            raise IdentityException(self.code, tip)
        raise LoginException(self.code, '教务系统请求异常')

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
        try:
            res = self._post(login_url, data=payload, **kwargs)
        except TooManyRedirects:
            # 302跳转 代表登录成功
            return True
        return res

    def check_session(self):
        """ 检查登陆会话是否有效 """
        account = parse.quote(self.user.account.encode('gb2312'))
        try:
            self._head(self.school_url['HOME_URL'] + account)
        except RequestException:
            return False

        return True
