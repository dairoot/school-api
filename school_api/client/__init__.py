from school_api.client.base import BaseUserClient, BaseSchoolClient
from school_api.client.api.schedule import Schedule
from school_api.client.api.user_info import SchoolInfo
from school_api.client.utils import UserType, ScheduleType, NullClass


def error_handle(func):
    def wrapper(self, **kwargs):
        if not self.school.debug:
            try:
                return func(self, **kwargs)
            except Exception as e:
                # 请求失败 销毁类方法
                return NullClass('{}: {}'.format(func.__name__, e))
        else:
            return func(self, **kwargs)
    return wrapper


class SchoolClient(BaseSchoolClient):

    def __init__(self, url, debug=False, conf_url=None):
        self.debug = debug
        self.url = url
        self._login_types = [u'学生', u'教师', u'部门']
        self.login_url_suffix = '/default4.aspx'
        self.school_url = conf_url or self.school_url

    def user_login(self, account, passwd, **kwargs):
        user = UserClient(self, account, passwd, **kwargs)
        return user.get_login()


class UserClient(BaseUserClient):

    schedule = Schedule()
    info = SchoolInfo()

    def __init__(self, school, account, passwd, **kwargs):
        self.account = account
        self.passwd = passwd
        self.school = school
        self.timeout = kwargs.get('timeout', 15)
        self.user_type = kwargs.get('user_type', UserType.STUDENT)

    @error_handle
    def get_login(self, **kwargs):
        return self.login(**kwargs)

    @error_handle
    def get_schedule(self, **kwargs):
        return self.schedule.get_schedule(**kwargs)

    @error_handle
    def get_info(self, **kwargs):
        return self.info.get_info(**kwargs)
