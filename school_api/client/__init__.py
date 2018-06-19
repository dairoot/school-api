from school_api.client.base import BaseUserClient, BaseSchoolClient
from school_api.client.api.score import Score
from school_api.client.api.schedule import Schedule
from school_api.client.api.user_info import SchoolInfo
from school_api.client.utils import UserType, ScheduleType, NullClass, error_handle


class SchoolClient(BaseSchoolClient):

    def __init__(self, url, **kwargs):
        self.url = url
        self.login_url_suffix = '/default4.aspx'
        self.name = kwargs.get('name')
        self.debug = kwargs.get('debug')
        self.lan_url = kwargs.get('lan_url')
        self.proxies = kwargs.get('proxies')
        self.use_proxy = kwargs.get('use_proxy')
        self.school_url = kwargs.get('conf_url') or self.school_url

    def user_login(self, account, passwd, user_type=UserType.STUDENT, **kwargs):
        user = UserClient(self, account, passwd, user_type)
        user.user_login(**kwargs)
        return user

class UserClient(BaseUserClient):

    score = Score()
    info = SchoolInfo()
    schedule = Schedule()

    def __init__(self, school, account, passwd, user_type, **kwargs):
        self.account = account
        self.passwd = passwd
        self.school = school
        self.user_type = user_type
        self.BASE_URL = self.school.url
        if self.school.use_proxy:
            self.set_proxy()

    @error_handle
    def user_login(self, **kwargs):
        return self.get_login(**kwargs)

    @error_handle
    def get_schedule(self, **kwargs):
        return self.schedule.get_schedule(**kwargs)

    @error_handle
    def get_info(self, **kwargs):
        return self.info.get_info(**kwargs)

    @error_handle
    def get_score(self, **kwargs):
        return self.score.get_score(**kwargs)
