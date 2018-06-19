from school_api.client.api.base import BaseSchoolApi
from school_api.client.api.schedule_parse import ScheduleParse
from school_api.client.utils import ScheduleType
from bs4 import BeautifulSoup
from urllib import parse


class Schedule(BaseSchoolApi):

    def _get_schedule(self, schedule_type=None, schedule_year=None, schedule_term=None, **kwargs):
        coding = ['GB18030', 'gbk'][self.user_type]
        # print (coding)
        res = self._get(self.schedule_url, **kwargs)
        # print (res.text)
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

    def _get_schedule_by_bm(self, class_name, school_year, school_term, **kwargs):
        res = self._get(self.schedule_url, **kwargs)
        if res.status_code != 200:
            return None
        pre_soup = BeautifulSoup(res.content.decode('gbk'), "html.parser")
        schedule_view_state = pre_soup.find(attrs={"name": "__VIEWSTATE"})['value']
        schedule_id_list = pre_soup.find(id='kb').find_all('option')
        schedule_id = [name['value'] for name in schedule_id_list if name.get_text() == class_name]
        # 获取班级课表
        payload = {
            '__VIEWSTATE': schedule_view_state,
            'xn': school_year,
            'xq': school_term,
            'kb': schedule_id
        }
        res = self._post(self.schedule_url, data=payload)
        if res.status_code != 200:
            return None
        schedule = ScheduleParse(res.content.decode('gbk'), self.schedule_type).get_schedule_dict()
        return schedule

    def get_schedule(self, **kwargs):
        self.schedule_type = ScheduleType.CLASS if self.user_type else kwargs.get('schedule_type', ScheduleType.PERSON)
        self.schedule_year = kwargs.get('schedule_year')
        self.schedule_term = kwargs.get('schedule_term')
        self.schedule_url = self.school_url["SCHEDULE_URL"][self.schedule_type] + \
            parse.quote(self.account.encode('gb2312'))
        print(self.user_type, self.schedule_type)
        if self.user_type != 2:
            return self._get_schedule(**kwargs)
        else:
            return self._get_schedule_by_bm(**kwargs)
