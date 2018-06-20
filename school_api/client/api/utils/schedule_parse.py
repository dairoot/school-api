#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup


class ScheduleParse(object):
    COlOR = ['green', 'blue', 'purple', 'red', 'yellow']
    TIME_LIST = {
        # 连续上一节课
        1: [
            '8:30 ~ 9:15', '10:25 ~ 11:10', '14:40 ~ 15:25',
            '16:30 ~ 17:15', '19:30 ~ 20:30'
        ],
        # 连续上两节课
        2: [
            '8:30 ~ 10:05', '10:25 ~ 12:00', '14:40 ~ 16:15',
            '16:30 ~ 18:05', '19:30 ~ 21:05'
        ],
        # 连续上三节课
        3: ['8:30 ~ 11:10', '', '14:40 ~ 17:15'],
        # 连续上四节课
        4: ['8:30 ~ 12:00', '10:25 ~ 16:15', '14:40 ~ 18:05', '16:30 ~ 21:05']
    }

    def __init__(self, html, schedule_type=0):
        self.schedule_list = [[], [], [], [], [], [], []]
        self.schedule_dict = [[], [], [], [], [], [], []]
        self.schedule_type = schedule_type
        soup = BeautifulSoup(html, "html.parser")
        option_args = soup.find_all("option", {"selected": "selected"})
        self.schedule_year = option_args[0].text
        self.schedule_term = option_args[1].text
        table = soup.find("table", {"id": "Table6"}) if \
            schedule_type == 1 else soup.find("table", {"id": "Table1"})
        trs = table.find_all('tr')
        self.__html_parse(trs)

    def __html_parse(self, trs):
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
            if i == 2 or i == 6 or i == 10:
                tds.pop(0)
            tds.pop(0)
            # 默认获取7天内的课表(周一到周日)
            for day in range(7):
                row_arr = []
                if tds[day].text != u' ':
                    td_str = str(tds[day])
                    rowspan = 2 if 'rowspan="2"' in td_str else 1
                    td_main = re.sub(r'<td align="Center".*?>', '', td_str)[:-5]
                    for text in td_main.split('<br/><br/>'):
                        text = re.sub(r'<[/]{0,1}font[^>]*?>', '', text)
                        text = re.sub(r'^<br/>', '', text)
                        arr = [k for k in text.split('<br/>')][:4:]
                        if len(arr) == 3:
                            # 没有上课地点的情况
                            arr.append('')
                        if arr[0] and not re.match(pattern, arr[0]):
                            weeks_arr = self.__get_weeks_arr(arr[1])
                            row_arr.append(arr + [rowspan, weeks_arr])
                self.schedule_list[day].append(row_arr)

    def get_schedule_list(self):
        return self.schedule_list

    def get_schedule_dict(self):
        for day, day_schedule in enumerate(self.schedule_list):
            for section, section_schedule in enumerate(day_schedule):
                section_schedule_dict = []
                color_index = (day * 3 + section + 1) % 5
                for schedule in section_schedule:
                    if schedule:
                        section_schedule_dict.append({
                            "color": self.COlOR[color_index],
                            "name": schedule[0],
                            "weeks_txt": schedule[1],
                            "teacher": schedule[2],
                            "place": schedule[3],
                            "section": schedule[4],
                            "weeks_arr": schedule[5],
                            "time": self.TIME_LIST[schedule[4]][section]
                        })
                self.schedule_dict[day].append(section_schedule_dict)
                
        schedule_data = {
            'schedule_term': self.schedule_term,
            'schedule_year': self.schedule_year,
            'schedule': self.schedule_dict
        }
        return schedule_data

    def __get_weeks_arr(self, class_time):
        """
        将上课时间 转成 数组形式
        :param class_time: 上课时间
        :param weeks_text: 上课周数文本
        :param weeks_arr: 上课周数数组
        :return:
        """
        weeks_arr = []
        if not self.schedule_type:
            weeks_text = re.findall("{(.*)}", class_time)[0]
        else:
            # 2节/周
            # 2节/单周(7-7)
            # 1-10,13-18(1,2)
            if '2节/' in class_time:
                weeks_text = class_time if '(' in class_time else class_time + '(1-18)'
            else:
                weeks_text = class_time.split('(')[0]

        step = 2 if u'单' in weeks_text or u'双' in weeks_text else 1
        for split_text in weeks_text.split(','):
            weeks = re.findall(r'(\d{1,2})-(\d{1,2})', split_text)
            weeks_arr += range(int(weeks[0][0]), int(weeks[0][1]) + 1,
                               step) if weeks else [int(split_text)]
        return weeks_arr
