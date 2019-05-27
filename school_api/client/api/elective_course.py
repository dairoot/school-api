# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from bs4 import BeautifulSoup
from requests import RequestException
from pylsy import pylsytable

from school_api.client.api.base import BaseSchoolApi
from school_api.client.api.utils import get_alert_tip
from school_api.exceptions import ElectiveCourseException


class ElectiveCourse(BaseSchoolApi):
    elective_course_url = None

    def get_elective_course(self, show_json=False, **kwargs):
        self.elective_course_url = self.school_url["ELECTIVE_COURSE_URL"] + self.user.account
        try:
            res = self._get(self.elective_course_url, **kwargs)
        except RequestException:
            raise ElectiveCourseException(self.code, '获取选课列表失败')

        return ElectiveCourseParse(self.code, res.text).get_data(show_json)

    def set_elective_course(self, course_id, **kwargs):
        ''' 选课操作 '''
        self.elective_course_url = self.school_url["ELECTIVE_COURSE_URL"] + self.user.account
        view_state = self._get_view_state(self.elective_course_url, **kwargs)
        payload = {
            "__VIEWSTATE": view_state,
            "ddl_xqbs": "1",
            course_id: "on",
            "Button1": "  提交  ".encode('gb2312')
        }
        try:
            res = self._post(self.elective_course_url, data=payload, **kwargs)
        except RequestException:
            raise ElectiveCourseException(self.code, '选课失败')

        data = ElectiveCourseParse(self.code, res.text).get_data(show_json=True)
        tip = get_alert_tip(res.text)
        return {"tip": tip, "selected_data": data["selected_data"]}


class ElectiveCourseParse():
    ''' 选修课页面解析模块 '''

    def __init__(self, code, html):
        self.code = code
        self.soup = BeautifulSoup(html, "html.parser")

    def get_data(self, show_json):
        table = self.soup.find_all("table", {"class": "datelist"})
        optional_row = table[0].find_all('tr')
        selected_row = table[1].find_all('tr')
        data = {"optional_data": [], "selected_data": []}
        # 获取可选的选修课
        for row in optional_row:
            data["optional_data"].append(self._get_optional_data(row))

        # 获取自己已选的选修课
        for row in selected_row:
            data["selected_data"].append(self._get_selected_data(row))

        if not show_json:
            data = self.show_text(data)

        return data

    @staticmethod
    def show_text(data):
        text = ''
        for t in data:
            title = data[t].pop(0)
            table = pylsytable(title)
            for line in data[t]:
                for i in range(len(title)):
                    table.append_data(title[i], line[i])
            text += "{}\n{}".format(t, table.__str__())
        return text

    @staticmethod
    def _get_optional_data(row):
        cells = row.find_all("td")
        lesson_name = cells[2].text
        lesson_name = lesson_name[:12] + '...' if len(lesson_name) > 11 else lesson_name
        teacher_name = cells[4].text
        class_time = cells[5].text
        class_place = cells[6].text
        capacity = cells[10].text
        residue = cells[12].text
        lesson = cells[0].find("input")
        lesson_id = lesson["name"] if lesson else "课程id"
        r_c = "{}/{}".format(residue, capacity)
        return [lesson_id, lesson_name, class_time[:7], teacher_name[:4], class_place, r_c]

    @staticmethod
    def _get_selected_data(row):
        cells = row.find_all("td")
        lesson_name = cells[1].text
        teacher_name = cells[2].text
        class_time = cells[7].text
        class_place = cells[8].text
        return [lesson_name, teacher_name, class_time, class_place]
