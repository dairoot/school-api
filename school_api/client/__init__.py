from school_api.client.base import BaseSchoolClient


class SchoolClient(BaseSchoolClient):
    """docstring for SchoolApi"""

    def __init__(self, url):
        self.BASE_URL = url
        self.login_url_suffix = '/default4.aspx'
        self._login_types = [u'学生', u'教师', u'部门']

    def get_login(self, account, passwd, user_type=0):
        view_state = self._get_view_state(self.login_url_suffix)
        payload = {
            '__VIEWSTATE': view_state,
            'TextBox1': account.encode('gb2312'),
            'TextBox2': passwd,
            'RadioButtonList1': self._login_types[user_type].encode('gb2312'),
            'Button1': u' 登 录 '.encode('gb2312')
        }
        self._update_headers({'Referer': self.BASE_URL+self.login_url_suffix})
        res = self.post(self.login_url_suffix, data=payload)
        return self

