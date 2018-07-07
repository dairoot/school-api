# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from bs4 import BeautifulSoup
from school_api.client.api.base import BaseSchoolApi


class SchoolInfo(BaseSchoolApi):
    ''' 用户信息查询 部门教师不可用 '''

    def get_info(self, **kwargs):
        info_url = self.school_url['INFO_URL'] + self.account
        res = self._get(info_url, **kwargs)
        if res.status_code != 200:
            return None
        return SchoolInfoParse(self.user_type, res.content).user_info


class SchoolInfoParse():
    ''' 信息页面解析模块 '''

    def __init__(self, user_type, html):
        self.data = {}
        coding = 'gbk' if user_type else 'GB18030'
        self.soup = BeautifulSoup(html.decode(coding), "html.parser")
        [self._html_parse_of_student, self._html_parse_of_teacher][user_type]()

    def _html_parse_of_student(self):
        table = self.soup.find("table", {"class": "formlist"})
        if table:
            real_name = table.find(id="xm").text
            sex = table.find(id="lbl_xb").text
            grade = table.find(id="lbl_dqszj").text
            birth_date = table.find(id="lbl_csrq").text
            class_name = table.find(id="lbl_xzb").text
            faculty = table.find(id="lbl_xy").text
            specialty = table.find(id="lbl_zymc").text
            hometown = table.find(id="lbl_lydq").text
            enrol_time = table.find(id="lbl_rxrq").text
            id_card = table.find(id="lbl_sfzh").text
            self.data = {
                "real_name": real_name,
                "sex": sex,
                "grade": grade,
                "birth_date": birth_date,
                "class_name": class_name,
                "faculty": faculty,
                "specialty": specialty,
                "hometown": hometown,
                "enrol_time": enrol_time,
                "id_card": id_card
            }

    def _html_parse_of_teacher(self):
        table = self.soup.find(id="Table3")
        if table:
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
