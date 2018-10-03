#!/usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import six
import datetime


def assemble_schedule(schedule_data):
    """ 组装课表回复数据 """
    week_day_text = ['日', '一', '二', '三', '四', '五', '六']
    strf = "%Y年%m月%d日"
    if six.PY2:
        strf = strf.encode("utf-8")
    description = datetime.datetime.now().strftime(strf)

    # 获取第一周 星期一 的课表
    weeks = 1
    what_day = 1
    articles = [{
        'title': '第%d周-星期%s' % (weeks, week_day_text[what_day]),
        'description': description,
        'url': ''
    }]
    for i, section in enumerate(schedule_data['schedule'][what_day - 1]):
        for c in section:
            if weeks in c['weeks_arr']:
                section_time = '第%d,%d节' % (i * 2 + 1, i * 2 + c['section'])
                content = '%s  地点：%s\n课程：%s' % (
                    section_time, c['place'], c['name'])
                articles.append({
                    'title': content,
                    'description': "",
                    'url': ''
                })
    articles.append({
        'title': '点击这里：查看完整课表',
        'description': '',
        'url': 'https://open.dairoot.cn/get_schedule?'
    })
    return articles


def assemble_score(score_year, score_term, score_data):
    articles = [{
        'title': '期末成绩单',
        'description': '【第%s学年第%s学期】' % (score_year, score_term)
    }]
    for n, c in enumerate(score_data):
        if n > 5:
            break
        print(c)
        articles.append({
            'title': "课程：%s\n学分：%s 成绩：%s" % (c['lesson_name'], c['credit'],  c['score']),
        })
    articles.append({
        'title': '点击这里：查看完整成绩',
        'description': '',
        'url': ''
    })
    return articles
