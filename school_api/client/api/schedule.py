# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from six.moves.urllib import parse

from bs4 import BeautifulSoup
from requests import RequestException, TooManyRedirects

from school_api.client.api.base import BaseSchoolApi
from school_api.client.api.utils import get_alert_tip, get_view_state_from_html
from school_api.client.api.utils.schedule_parse import ScheduleParse
from school_api.client.utils import ScheduleType, UserType
from school_api.utils import to_text
from school_api.exceptions import ScheduleException


class Schedule(BaseSchoolApi):
    schedule_type = None
    schedule_year = None
    schedule_term = None
    schedule_url = None

    def get_schedule(self, schedule_year=None, schedule_term=None, schedule_type=None, **kwargs):
        ''' 课表信息 获取入口
        :param schedule_year: 课表学年
        :param schedule_term: 课表学期
        :param schedule_type: 0.个人课表 1.班级课表
        :param kwargs: requests模块参数
        :return:
        '''
        self.schedule_type = ScheduleType.CLASS if self.user.user_type \
            else schedule_type or ScheduleType.PERSON
        self.schedule_year = schedule_year
        self.schedule_term = str(schedule_term) if schedule_term else schedule_term
        self.schedule_url = self.school_url["SCHEDULE_URL"][self.schedule_type]

        if self.user.user_type != UserType.DEPT:
            self.schedule_url += self.user.account
            data = self._get_api(**kwargs)
        else:
            self.schedule_url += parse.quote(self.user.account.encode('gb2312'))
            data = self._get_api_by_bm(**kwargs)
        if self.schedule_term and self.schedule_year and (
                self.schedule_term != data["schedule_term"] or self.schedule_year != data["schedule_year"]):
            raise ScheduleException(self.code, '暂无课表信息')
        return data

    def _get_api(self, **kwargs):

        try:
            res = self._get(self.schedule_url, **kwargs)
        except TooManyRedirects:
            raise ScheduleException(self.code, '课表接口已关闭')
        except RequestException:
            raise ScheduleException(self.code, '获取课表请求参数失败')

        tip = get_alert_tip(res.text)
        if tip:
            raise ScheduleException(self.code, tip)

        schedule = ScheduleParse(res.text, self.time_list, self.schedule_type).get_schedule_dict()
        # 第一次请求的时候，教务系统默认返回当前学年学期课表
        # 如果设置了学年跟学期，则获取指定学年学期的课表
        if self.schedule_year and self.schedule_term and (
                self.schedule_year != schedule['schedule_year'] or self.schedule_term != schedule['schedule_term']):

            payload = self._get_payload(res.text)

            try:
                res = self._post(self.schedule_url, data=payload, **kwargs)
            except RequestException:
                raise ScheduleException(self.code, '获取课表信息失败')

            schedule = ScheduleParse(
                res.text,
                self.time_list,
                self.schedule_type
            ).get_schedule_dict()

        return schedule

    def _get_api_by_bm(self, class_name, **kwargs):
        ''' 部门教师 查询学生班级课表 共3个请求'''

        # steps 1: 获取课表页面 参数信息
        try:
            res = self._get(self.schedule_url, **kwargs)
        except RequestException:
            raise ScheduleException(self.code, '获取课表请求参数失败')

        # steps 2: 选择课表 学年学期
        if self.schedule_year and self.schedule_term:
            payload = self._get_payload(res.text)
            try:
                res = self._post(self.schedule_url, data=payload, **kwargs)
            except RequestException:
                raise ScheduleException(self.code, '获取课表请求参数失败')

        # steps 3: 获取课表数据
        payload = self._get_payload_by_bm(res.text, class_name)
        try:
            res = self._post(self.schedule_url, data=payload, **kwargs)
        except RequestException:
            raise ScheduleException(self.code, '获取课表信息失败')

        schedule = ScheduleParse(res.text, self.time_list, self.schedule_type).get_schedule_dict()
        return schedule

    def _get_payload(self, html):
        ''' 获取课表post 的参数 '''
        view_state = get_view_state_from_html(html)
        payload = {
            '__VIEWSTATE': view_state,
            ['xnd', 'xn'][self.schedule_type]: self.schedule_year,
            ['xqd', 'xq'][self.schedule_type]: self.schedule_term
        }
        return payload

    def _get_payload_by_bm(self, html, class_name):
        ''' 提取页面参数用于请求课表 '''
        pre_soup = BeautifulSoup(html, "html.parser")
        view_state = pre_soup.find(attrs={"name": "__VIEWSTATE"})['value']
        schedule_id_list = pre_soup.find(id='kb').find_all('option')
        class_name = to_text(class_name)
        for name in schedule_id_list:
            if name.text == class_name:
                schedule_id = name['value']
                break
        else:
            raise ScheduleException(self.code, '暂无该班级课表信息')

        # 获取班级课表
        payload = {
            '__VIEWSTATE': view_state,
            'kb': schedule_id
        }
        return payload
