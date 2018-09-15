# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import six.moves.urllib.parse as urlparse

from bs4 import BeautifulSoup
from requests import RequestException

from school_api.client.api.base import BaseSchoolApi
from school_api.client.api.utils.schedule_parse import ScheduleParse
from school_api.client.utils import ScheduleType
from school_api.exceptions import ScheduleException


class PlaceSchedule(BaseSchoolApi):
    schedule_url = None
    payload = None

    def get_schedule(self, campus_list=None, classroom_type_list=None, classroom_name_list=None, **kwargs):
        ''' 课表信息 获取入口
        返回一个生成器，生成器一旦报错则将退出：https://codeday.me/bug/20180125/124136.html
        除了解析异常其他报错均不抛出
        '''
        self.schedule_url = self.school_url['PLACE_SCHEDULE_URL'] + \
            urlparse.quote(self.account.encode('gb2312'))

        if not self._update_payload(**kwargs):
            yield {'error': "获取教学场地课表失败"}
        else:
            # 遍历校区
            for campus in self.payload['campus_list']:
                if campus_list and campus["name"] not in campus_list:
                    continue
                if not self._update_payload(campus, **kwargs):
                    continue
                # 遍历教室类别
                for classroom_type in self.payload['classroom_type_list']:
                    if classroom_type_list and classroom_type["name"] not in classroom_type_list:
                        continue
                    if not self._update_payload(campus, classroom_type=classroom_type, **kwargs):
                        continue
                    # 遍历教室名称
                    for classroom_name in self.payload['classroom_name_list']:
                        if classroom_name_list and classroom_name["name"] not in classroom_name_list:
                            continue
                        try:
                            res = self._get_api(
                                campus, classroom_type=classroom_type,
                                classroom_name=classroom_name, **kwargs)
                        except ScheduleException:
                            continue

                        schedule = ScheduleParse(
                            res.content.decode('GB18030'),
                            self.time_list,
                            ScheduleType.CLASS
                        ).get_schedule_dict()

                        data = {
                            "campus": campus["name"],
                            "classroom_type": classroom_type["name"],
                            "classroom_name": classroom_name["name"]
                        }
                        data.update(schedule)
                        yield data

    def _get_api(self, campus=None, **kwargs):
        """ 请求函数 """
        if self.payload and campus:
            classroom_type = kwargs.pop('classroom_type', None)
            classroom_name = kwargs.pop('classroom_name', None)
            data = {
                "Button1": "",
                "xq": self.payload['schedule_term'],
                "xn": self.payload['schedule_year'],
                "ddlXq": campus["value"],
                "ddlJslb": classroom_type["value"].encode('gb2312') if classroom_type else '',
                "ddlJsmc": classroom_name["value"].encode('gb2312') if classroom_name else '',
                "__VIEWSTATE": self.payload['view_state'],
            }
            _request = self._post
        else:
            data = ""
            _request = self._get

        try:
            res = _request(self.schedule_url, data=data, **kwargs)
            if res.status_code != 200:
                raise RequestException
        except RequestException:
            raise ScheduleException(self.code, '获取教学场地课表失败')
        return res

    def _update_payload(self, *args, **kwargs):
        try:
            res = self._get_api(*args, **kwargs)
        except ScheduleException:
            return None
        self.payload = self._get_payload(res.text)
        return True

    @staticmethod
    def _get_payload(html):
        pre_soup = BeautifulSoup(html, "html.parser")
        view_state = pre_soup.find(attrs={"name": "__VIEWSTATE"})['value']
        searchbox = pre_soup.find("div", {"class": "searchbox"})

        schedule_year = searchbox.find("select", {"id": "xn"}).find(
            "option", {"selected": "selected"}).text
        schedule_term = searchbox.find("select", {"id": "xq"}).find(
            "option", {"selected": "selected"}).text

        campus = searchbox.find(id='ddlXq').find_all('option')
        type_list = searchbox.find(id='ddlJslb').find_all('option')
        name_list = searchbox.find(id='ddlJsmc').find_all('option')
        campus_list = [{"name": v.text, "value": v['value']} for v in campus]
        type_list = [{"name": v.text, "value": v['value']} for v in type_list]
        name_list = [{"name": v.text, "value": v['value']} for v in name_list]
        payload = {
            'view_state': view_state,
            'schedule_term': schedule_term,
            'schedule_year': schedule_year,
            'campus_list': campus_list,
            'classroom_type_list': type_list,
            'classroom_name_list': name_list,
        }
        return payload
