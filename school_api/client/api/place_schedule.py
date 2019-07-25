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

    def get_schedule(self,
                     campus_list=None,
                     building_list=None,
                     classroom_type_list=None,
                     classroom_name_list=None,
                     filter_campus_list=None,
                     filter_building_list=None,
                     filter_classroom_type_list=None,
                     **kwargs):
        '''
        课表信息 获取入口
        生成器一旦报错则将退出：https://codeday.me/bug/20180125/124136.html
        除了解析异常其他报错均不抛出

        :param campus_list: 校区列表
        :param building_list: 楼号列表
        :param classroom_type_list: 教室类别列表
        :param classroom_name_list: 教室名称列表

        :param filter_campus_list: 排除校区列表
        :param filter_building_list: 排除楼号列表
        :param filter_classroom_type_list: 排除教室类别列表
        :param kwargs: requests 参数
        :yield: 生成器
        '''

        self.schedule_url = self.school_url['PLACE_SCHEDULE_URL'] + \
                            urlparse.quote(self.user.account.encode('gb2312'))

        if not self._update_payload(**kwargs):
            yield {'error': "获取教学场地课表失败"}
        else:
            # 遍历校区
            for campus in self.payload['campus_list']:
                if self._is_skip(campus["name"], campus_list, filter_name_list=filter_campus_list):
                    continue
                if not self._update_payload(campus, **kwargs):
                    continue

                # 遍历楼号
                for building in self.payload['building_list']:
                    kwargs['building'] = building
                    if self._is_skip(building["name"], building_list, filter_name_list=filter_building_list):
                        continue
                    if not self._update_payload(campus, **kwargs):
                        continue

                    # 遍历教室类别
                    for classroom_type in self.payload['classroom_type_list']:
                        kwargs['classroom_type'] = classroom_type
                        if self._is_skip(classroom_type["name"], classroom_type_list,
                                         filter_name_list=filter_classroom_type_list):
                            continue
                        if not self._update_payload(campus, **kwargs):
                            continue

                        # 遍历教室名称
                        for classroom_name in self.payload['classroom_name_list']:
                            if self._is_skip(classroom_name["name"], classroom_name_list):
                                continue

                            kwargs['classroom_name'] = classroom_name
                            # 请求接口获取课表数据
                            data = self._get_result(campus, **kwargs)
                            if data:
                                yield data

    def _get_result(self, campus, **kwargs):
        """ 处理请求结果，并返回 """
        try:
            res = self._get_api(campus, **kwargs)
        except ScheduleException:
            return

        schedule = ScheduleParse(res.text, self.time_list, ScheduleType.CLASS).get_schedule_dict()

        data = {
            "campus": campus["name"],
            "building": kwargs['building']["name"],
            "classroom_type": kwargs['classroom_type']["name"],
            "classroom_name": kwargs['classroom_name']["name"]
        }
        data.update(schedule)
        return data

    def _get_api(self, campus=None, **kwargs):
        """ 请求函数 """
        if self.payload and campus:
            building = kwargs.pop('building', None)
            classroom_type = kwargs.pop('classroom_type', None)
            classroom_name = kwargs.pop('classroom_name', None)
            data = {
                "Button1": "",
                "xq": self.payload['schedule_term'],
                "xn": self.payload['schedule_year'],
                "ddlXq": campus["value"],
                'ddllh': building["value"] if building else '',
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
        except RequestException:
            raise ScheduleException(self.code, '获取教学场地课表失败')
        return res

    def _update_payload(self, *args, **kwargs):
        # 更新提交参数 payload
        try:
            res = self._get_api(*args, **kwargs)
        except ScheduleException:
            return None

        try:
            self.payload = self._get_payload(res.text)
        except AttributeError:
            return None
        return True

    @staticmethod
    def _get_payload(html):
        ''' 获取课表提交参数 '''
        pre_soup = BeautifulSoup(html, "html.parser")
        view_state = pre_soup.find(attrs={"name": "__VIEWSTATE"})['value']
        searchbox = pre_soup.find("div", {"class": "searchbox"})

        schedule_year = searchbox.find("select", {"id": "xn"}).find(
            "option", {"selected": "selected"}).text
        schedule_term = searchbox.find("select", {"id": "xq"}).find(
            "option", {"selected": "selected"}).text

        campuses = searchbox.find(id='ddlXq').find_all('option')
        buildings = searchbox.find(id='ddllh').find_all('option')
        types = searchbox.find(id='ddlJslb').find_all('option')
        names = searchbox.find(id='ddlJsmc').find_all('option')

        campuses = [{"name": v.text, "value": v['value']} for v in campuses]
        buildings = [{"name": v.text, "value": v['value']} for v in buildings]
        types = [{"name": v.text, "value": v['value']} for v in types]
        names = [{"name": v.text, "value": v['value']} for v in names]

        payload = {
            'view_state': view_state,
            'schedule_term': schedule_term,
            'schedule_year': schedule_year,
            'campus_list': campuses,
            'building_list': buildings,
            'classroom_type_list': types,
            'classroom_name_list': names,
        }
        return payload

    @staticmethod
    def _is_skip(name, name_list, filter_name_list=None):
        ''' 检查是否跳过 '''
        if (name_list and name not in name_list) or (filter_name_list and name in filter_name_list):
            return True
        return None
