#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
import datetime
from school_api import SchoolClient


GdstApi = SchoolClient('http://210.38.137.126:8016')

user = os.getenv('GDOU_STUDENT_ACCOUNT', '')
password = os.getenv('GDOU_STUDENT_PASSWD', '')


def get_info():
    student = GdstApi.user_login(user, password)
    return student.get_info()


def get_schedule():
    student = GdstApi.user_login(user, password)
    data = student.get_schedule()
    week_day_text = ['日', '一', '二', '三', '四', '五', '六']
    description = datetime.datetime.now().strftime("%Y-%m-%d")

    # 获取第一周 星期一 的课表
    weeks = 1
    what_day = 1
    articles = [{
        'title': '第%d周-星期%s' % (weeks, week_day_text[what_day]),
        'description': description,
        'url': ''
    }]
    for i, section in enumerate(data['schedule'][what_day - 1]):
        for c in section:
            if weeks in c['weeks_arr']:
                section_time = '第%d,%d节' % (i * 2 + 1, i * 2 + c['section'])
                content = '%s  地点：%s\n课程：%s' % (section_time, c['place'], c['name'])
                articles.append({
                    'title': content,
                    'description': "",
                    'url': ''
                })
    return articles


def get_score():
    student = GdstApi.user_login(user, password)
    return student.get_score()
