# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from bs4 import BeautifulSoup
from school_api.client.api.base import BaseSchoolApi


class Score(BaseSchoolApi):
    ''' 学生成绩获取 ''' 

    def get_score(self, score_year=None, score_term=None, **kwargs):
        score_url = self.school_url['SCORE_URL'] + self.account
        view_state = self._get_view_state(score_url)
        payload = {
            '__VIEWSTATE': view_state,
            'Button2': u'在校学习成绩查询',
            'ddlXN': '',
            'ddlXQ': ''
        }
        res = self._post(score_url, data=payload, **kwargs)
        if res.status_code != 200:
            return None
        return ScoreParse(res.content).get_score(score_year, score_term)


class ScoreParse():
    ''' 成绩页面解析模块 '''

    def __init__(self, html):
        self.soup = BeautifulSoup(html.decode('GB18030'), "html.parser")
        self._html_parse_of_score()

    def _html_parse_of_score(self):
        rows = self.soup.find("table", {"id": "Datagrid1"}).find_all('tr')
        rows.pop(0)
        self.score_info = {}
        for row in rows:
            cells = row.find_all("td")
            # 学年学期
            year = cells[0].text
            term = cells[1].text
            # 课程名
            lesson_name = cells[3].text.strip()
            credit = cells[6].text.strip() or 0
            point = cells[7].text.strip() or 0
            score = cells[8].text.strip() or 0
            score_dict = {
                "lesson_name": lesson_name,
                "credit": float(credit),
                "point": float(point),
                "score": float(score)
            }
            # 有其他成绩内容则输出
            makeup_score = cells[10].text
            retake_score = cells[11].text
            if makeup_score != u'\xa0':
                # 补考成绩
                score_dict['bkcj'] = makeup_score
            if retake_score != u'\xa0':
                # 重修成绩
                score_dict['cxcj'] = retake_score
            # 组装数组格式的数据备用
            self.score_info[year] = self.score_info.get(year, {})
            self.score_info[year][term] = self.score_info[year].get(term, [])
            self.score_info[year][term].append(score_dict)

    def get_score(self, year, term):
        ''' 返回成绩信息json格式 '''
        if year:
            if term:
                return self.score_info[year][term]
            return self.score_info[year]
        return self.score_info
