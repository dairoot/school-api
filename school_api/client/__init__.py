from school_api.client.base import BaseSchoolClient
from school_api.client.api.schedule import Schedule
from school_api.utils import UserType, ScheduleType
import re
from bs4 import BeautifulSoup, SoupStrainer


class SchoolClient(BaseSchoolClient):
    """docstring for SchoolApi"""
    schedule = Schedule()

    def __init__(self, url, **kwargs):
        self.BASE_URL = url
        self.login_url_suffix = '/default4.aspx'
        self._login_types = [u'学生', u'教师', u'部门']

    def get_login(self, account, passwd, **kwargs):
        self.account = account
        self.passwd = passwd
        self.user_type = kwargs.get('user_type', UserType.STUDENT)
        self.schedule_type = kwargs.get('schedule_type', ScheduleType.PERSON)

        view_state = self._get_view_state(self.login_url_suffix)
        payload = {
            '__VIEWSTATE': view_state,
            'TextBox1': account.encode('gb2312'),
            'TextBox2': passwd,
            'RadioButtonList1': self._login_types[self.user_type].encode('gb2312'),
            'Button1': u' 登 录 '.encode('gb2312')
        }
        self._update_headers({'Referer': self.BASE_URL+self.login_url_suffix})
        res = self.post(self.login_url_suffix, data=payload, allow_redirects=False)
        # 登录成功之后，教务系统会返回 302 跳转
        if not res.status_code == 302:
            page_soup = BeautifulSoup(res.text, "html.parser",
                                      parse_only=SoupStrainer("script"))
            alert = page_soup.getText()
            tip = re.findall(r'[^()\']+', page_soup.getText())[1]
        return self
