from school_api.client.api.base import BaseSchoolApi
from school_api.client.api.schedule_parse import ScheduleParse
from bs4 import BeautifulSoup
from urllib import parse


class Schedule(BaseSchoolApi):

    def get_schedule(self, **kwargs):
        schedule_func = [self.__get_student_schedule,
                         self.__get_teacher_schedule,
                         self.__get_dept_class_schedule]
        return schedule_func[self.user_type](**kwargs)

    def __get_student_schedule(self, schedule_type=None, **kwargs):
        """
        获取学生个人课表
        :return: 返回学生个人课表信息字典
        """
        schedule_type = schedule_type or self.schedule_type
        url = self.school_url["PERSON_SCHEDULE_URL"] + self.account
        
        # url = 'http://61.142.33.2' + self.school_url["PERSON_SCHEDULE_URL"] + self.account
        
        res = self._get(url, **kwargs)
        if res.status_code != 200:
            return None
        schedule = ScheduleParse(res.content.decode('GB18030')).get_schedule_dict()
        return schedule

    def __get_dept_class_schedule(self, class_name, school_year, school_term):
        """
        通过部门账号获取 学生班级课表
        :return: 返回学生班级课表信息字典
        """
        pass

    def __get_teacher_schedule(self):
        """
        获取教师课表
        :return: 返回教师课表信息字典
        """
        url = self.school_url["CLASS_SCHEDULE_URL"] + self.account
        res = self._get(url, allow_redirects=False)
        if res.status_code != 200:
            return None
        schedule = ScheduleParse(res.content.decode('gbk'), 'class').get_schedule_dict()
        return schedule
