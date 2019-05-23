# -*- coding: utf-8 -*-
'''
    @Time       : 2016 - 2018
    @Author     : dairoot
    @Email      : 623815825@qq.com
    @description: 课表解析
'''
from __future__ import absolute_import, unicode_literals

import re
import six
from bs4 import BeautifulSoup


class BaseScheduleParse():
    ''' 课表页面解析模块 '''

    def __init__(self, html, time_list, schedule_type):
        self.schedule_year = ''
        self.schedule_term = ''
        self.time_list = time_list
        self.schedule_type = schedule_type
        self.schedule_list = [[], [], [], [], [], [], []]

        soup = BeautifulSoup(html, "html.parser")
        option_args = soup.find_all("option", {"selected": "selected"})
        if option_args:
            self.schedule_year = option_args[0].text
            self.schedule_term = option_args[1].text
            table = soup.find("table", {"id": "Table6"}) if \
                schedule_type == 1 else soup.find("table", {"id": "Table1"})
            trs = table.find_all('tr')
            self.html_parse(trs)

    def html_parse(self, trs):
        """
        :param n+1: 为周几
        :param i-1: 为第几节
        :param arr: ["课程", "时间", "姓名", "地点", "节数", "周数数组"]
        :param row_arr: 为周几第几节 的课程信息
        :param rowspan: 表示该课程有几节课
        :return:
        """
        pattern = r'^\([\u2E80-\u9FFF]{1,3}\d+\)'
        # 每天最多有10节课, 数据从2到12, (i-1) 代表是第几节课 (偶数节 不获取)
        for i in range(2, 12, 2):
            tds = trs[i].find_all("td")
            # 去除无用数据，比如(上午, 第一节...  等等)
            if i in [2, 6, 10]:
                tds.pop(0)
            tds.pop(0)
            # 默认获取7天内的课表(周一到周日) tds 长度为7
            for day, day_c in enumerate(tds):
                row_arr = []
                if day_c.text != u' ':
                    td_str = day_c.__unicode__()
                    rowspan = 2 if 'rowspan="2"' in td_str else 1
                    td_main = re.sub(r'<td align="Center".*?>', '', td_str)[:-5]

                    for text in td_main.split('<br/><br/>'):
                        course_arr = self._get_td_course_info(text)
                        if course_arr[0] and not re.match(pattern, course_arr[0]):
                            course_arr[1] = self._get_weeks_text(course_arr[1])
                            weeks_arr = self._get_weeks_arr(course_arr[1])
                            row_arr.append(course_arr + [rowspan, weeks_arr])
                self.schedule_list[day].append(row_arr)

    def get_schedule_dict(self):
        ''' 返回课表数据 字典格式 '''
        all_schedule = [[], [], [], [], [], [], []]
        color = ['green', 'blue', 'purple', 'red', 'yellow']

        for day, day_schedule in enumerate(self.schedule_list):
            for section, section_schedule in enumerate(day_schedule):
                section_schedule_dict = []
                color_index = (day * 3 + section + 1) % 5
                for schedule in section_schedule:
                    if schedule:
                        section_schedule_dict.append({
                            "color": color[color_index],
                            "name": schedule[0],
                            "weeks_text": schedule[1],
                            "teacher": schedule[2],
                            "place": schedule[3],
                            "section": schedule[4],
                            "weeks_arr": schedule[5],
                            "time": self.time_list[schedule[4]][section]
                        })
                all_schedule[day].append(section_schedule_dict)

        schedule_data = {
            'schedule_term': self.schedule_term,
            'schedule_year': self.schedule_year,
            'schedule': all_schedule
        }
        return schedule_data

    def _get_weeks_text(self, class_time):
        ''' 课程周数文本 '''
        if not self.schedule_type:
            weeks_text = re.findall(r"{(.*)}", class_time)[0]
        else:
            # 2节/周
            # 2节/单周(7-7)
            # 1-10,13-18(1,2)
            if '2节/' in class_time:
                weeks_text = class_time if '(' in class_time else class_time + '(1-18)'
            else:
                weeks_text = class_time.split('(')[0]
        return weeks_text

    @staticmethod
    def _get_weeks_arr(weeks_text):
        """
        将上课时间 转成 数组形式
        :param class_time: 上课时间
        :param weeks_text: 课程周数文本
        :param weeks_arr: 上课周数数组
        :return:
        """
        weeks_arr = []
        step = 2 if '单' in weeks_text or '双' in weeks_text else 1
        for split_text in weeks_text.split(','):
            weeks = re.findall(r'(\d{1,2})-(\d{1,2})', split_text)

            if weeks:
                weeks_arr += range(int(weeks[0][0]), int(weeks[0][1]) + 1, step)
            else:
                weeks_arr += [int(split_text)]

        return weeks_arr

    @staticmethod
    def _get_td_course_info(text):
        ''' 获取td标签的课程信息 '''
        text = re.sub(r'<[/]{0,1}font[^>]*?>', '', text)
        text = re.sub(r'^<br/>', '', text)

        if six.PY2:
            # 以下兼容 python2 版本解析处理
            text = re.sub(r'</br></br></br>$', '', text)
            text = text.replace('<br>', '<br/>')

        info_arr = []
        for k in text.split('<br/>'):
            if k not in ['选修', '公选', '必修', '限选', '任选']:
                info_arr.append(k)

        info_arr = info_arr[:4:]
        if len(info_arr) == 3:
            # 没有上课地点的情况
            info_arr.append('')
        return info_arr


class ScheduleParse(BaseScheduleParse):
    ''' 课表节数合并 '''

    def __init__(self, html, time_list, schedule_type=0):
        BaseScheduleParse.__init__(self, html, time_list, schedule_type)
        self.merger_same_schedule()

    def merger_same_schedule(self):
        """
        :param day_schedule: 一天的课程
        :param section_schedule: 一节课的课程
        :return:
        """
        for day_schedule in self.schedule_list:
            self._merger_day_schedule(day_schedule)

    def _merger_day_schedule(self, day_schedule):
        """
        将同一天相邻的相同两节课合并
        例如：[[["英语", "2节/双周(14-14)", "姓名", "1-301", "2", "[7,8]"],[...]],
        [["英语", "2节/双周(14-14)", "姓名", "1-301", "2", "[7,8]"],[...]]]
        合并为： 课程节数修改
        [[["英语", "2节/双周(14-14)", "姓名", "1-301", "4", "[7,8]"],[...]],
        [[...]]]
        """
        # 先合并 同一节课的相同课程
        for section_schedule in day_schedule:
            self._merger_section_schedule(section_schedule)

        # 再合并 同一天相邻的相同两节课合并
        day_slen = len(day_schedule)
        for i in range(day_slen - 1):
            for last_i, last_schedule in enumerate(day_schedule[i]):
                for next_i, next_schedule in enumerate(day_schedule[i + 1]):
                    if last_schedule and next_schedule:
                        # 课程名 上课地点 上课时间 教师名
                        if last_schedule[0] == next_schedule[0] and \
                            last_schedule[1] == next_schedule[1] and \
                                last_schedule[2] == next_schedule[2] and\
                                last_schedule[3] == next_schedule[3]:

                            day_schedule[i][last_i][4] += day_schedule[i + 1][next_i][4]
                            day_schedule[i + 1][next_i] = []

    @staticmethod
    def _merger_section_schedule(section_schedule):
        """
        将同一节课的相同课程合并
        例如：[["英语", "2节/单周(7-7)", "姓名", "1-301", "2", "[7]"],
         ["英语", "2节/双周(8-8)", "姓名", "1-301", "2", "[8]"]]
         合并为：课程时间修改
         [["英语", "2节/单周(7-7),2节/双周(8-8)", "姓名", "1-301", "2", "[7,8]"]]
        """
        section_slen = len(section_schedule)
        for i in range(section_slen):
            for j in range(i + 1, section_slen):
                if section_schedule[i] and section_schedule[j]:
                    # 课程名 一样时
                    if section_schedule[i][0] == section_schedule[j][0]:
                        # 并且上课时间不同，上课地点 一样时
                        if section_schedule[i][1] != section_schedule[j][1] and \
                                section_schedule[i][3] == section_schedule[j][3]:
                            section_schedule[j][5] += section_schedule[i][5]
                            section_schedule[j][1] += ',' + section_schedule[i][1]
                            section_schedule[i] = []

                        # 课程名和上课时间一样时 将上一个赋为空
                        if section_schedule[i] and section_schedule[i][1] == section_schedule[j][1]:
                            section_schedule[i] = []
