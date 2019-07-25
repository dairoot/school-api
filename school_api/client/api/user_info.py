# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from bs4 import BeautifulSoup
from requests import RequestException, TooManyRedirects
from school_api.client.api.base import BaseSchoolApi
from school_api.exceptions import UserInfoException


class UserlInfo(BaseSchoolApi):
    ''' 用户信息查询 部门教师不可用 '''

    def get_info(self, **kwargs):
        ''' 用户信息 获取入口 '''
        info_url = self.school_url['INFO_URL'] + self.user.account

        try:
            res = self._get(info_url, **kwargs)
        except TooManyRedirects:
            raise UserInfoException(self.code, '用户信息接口已关闭')
        except RequestException:
            raise UserInfoException(self.code, '获取用户信息失败')

        return UserlInfoParse(self.code, self.user.user_type, res.text).user_info


class UserlInfoParse():
    ''' 信息页面解析模块 '''

    def __init__(self, code, user_type, html):
        self.data = {}
        self.code = code
        self.soup = BeautifulSoup(html, "html.parser")
        [self._html_parse_of_student, self._html_parse_of_teacher][user_type]()

    def _html_parse_of_student(self):
        table = self.soup.find("table", {"class": "formlist"})
        if not table:
            raise UserInfoException(self.code, '获取学生用户信息失败')

        real_name = table.find(id="xm").text
        grade = table.find(id="lbl_dqszj").text
        class_name = table.find(id="lbl_xzb").text
        faculty = table.find(id="lbl_xy").text
        specialty = table.find(id="lbl_zymc").text
        enrol_time = table.find(id="lbl_rxrq").text
        education_level = table.find(id="lbl_CC").text
        eductional_systme = table.find(id="lbl_xz").text

        sfzh = table.find(id="lbl_sfzh")
        id_card = sfzh.text if sfzh else table.find(id="sfzh")['value']

        csrq = table.find(id="lbl_csrq")
        birth_date = csrq.text if csrq else table.find(id="csrq")['value']

        lydq = table.find(id="lbl_lydq")
        hometown = lydq.text if lydq else table.find(id="lydq")['value']

        xb = table.find(id='XB')
        sex = xb.find('option', attrs={'selected': 'selected'}).text if xb else table.find(id="lbl_xb").text

        self.data = {
            "real_name": real_name,
            "sex": sex,
            "grade": grade,
            "birth_date": None if birth_date == 'NULL' else birth_date.replace('/', '-'),
            "class_name": class_name,
            "faculty": faculty,
            "specialty": specialty,
            "hometown": hometown,
            "enrol_time": enrol_time.replace('/', '-'),
            "education_level": education_level,
            "eductional_systme": eductional_systme,
            "id_card": id_card
        }

    def _html_parse_of_teacher(self):
        table = self.soup.find(id="Table3")
        if not table:
            raise UserInfoException(self.code, '获取教师用户信息失败')

        real_name = table.find(id='xm').text
        sex = table.find(id='xb').text
        dept = table.find(id='bm').text
        position = table.find(id='zw').text
        associate_degree = table.find(id='xl').text
        positional_title = table.find(id='zc').text
        self.data = {
            "real_name": real_name,
            "sex": sex,
            "dept": dept,
            "position": position,
            "associate_degree": associate_degree,
            "positional_title": positional_title
        }

    @property
    def user_info(self):
        ''' 返回用户信息json格式 '''
        return self.data
