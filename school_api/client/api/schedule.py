from school_api.client.api.base import BaseSchoolApi
from school_api.client.api.schedule_parse import ScheduleParse
from school_api.client.utils import ScheduleType
from bs4 import BeautifulSoup
from urllib import parse


class Schedule(BaseSchoolApi):

    def _get_schedule(self, **kwargs):
        coding = ['GB18030', 'gbk'][self.user_type]

        res = self._get(self.schedule_url, **kwargs)
        if res.status_code != 200:
            return None
        schedule = ScheduleParse(res.content.decode(coding), self.schedule_type).get_schedule_dict()
        '''
        第一次请求的时候，教务系统默认返回最新课表
        如果设置了学年跟学期，匹配学年跟学期，不匹配则获取指定学年学期的课表
        '''
        if self.schedule_year and self.schedule_term:
            if self.schedule_year != schedule['schedule_year'] or self.schedule_term != schedule['schedule_term']:
                view_state = self._get_view_state_from_html(res.text)
                payload = {
                    '__VIEWSTATE': view_state,
                    ['xnd', 'xn'][self.schedule_type]: self.schedule_year,
                    ['xqd', 'xq'][self.schedule_type]: self.schedule_term
                }
                res = self._post(self.schedule_url, data=payload, **kwargs)
                if res.status_code != 200:
                    return None
                schedule = ScheduleParse(res.content.decode(coding), self.schedule_type).get_schedule_dict()
        return schedule

    def get_schedule(self, **kwargs):
        self.schedule_type = ScheduleType.CLASS if self.user_type else kwargs.get('schedule_type', ScheduleType.PERSON)
        self.schedule_year = kwargs.get('schedule_year')
        self.schedule_term = kwargs.get('schedule_term')
        self.schedule_url = self.school_url["SCHEDULE_URL"][self.schedule_type] + self.account
        print(self.schedule_year, self.schedule_term)
        kwargs.pop('schedule_type', None)
        kwargs.pop('schedule_year', None)
        kwargs.pop('schedule_term', None)
        return self._get_schedule(**kwargs)
