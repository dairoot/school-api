# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re
from bs4 import BeautifulSoup
from requests import RequestException, TooManyRedirects

from school_api.client.api.base import BaseSchoolApi
from school_api.client.api.utils import get_alert_tip
from school_api.exceptions import ScoreException


class Score(BaseSchoolApi):
    ''' 学生成绩获取 '''

    def get_score(self, score_year=None, score_term=None, use_api=0, **kwargs):
        ''' 成绩信息 获取入口
        :param score_year: 成绩学年
        :param score_term: 成绩学期
        :param use_api:    0.接口1, 1.接口2, 2.接口3 ...
        :param kwargs: requests模块参数
        return
        '''
        score_url = self.school_url['SCORE_URL'][use_api] + self.user.account

        try:
            view_state = self._get_view_state(score_url, **kwargs)
        except TooManyRedirects:
            msg = '可能是成绩接口地址不对，请尝试更改use_api值'
            raise ScoreException(self.code, msg)
        except RequestException:
            msg = '获取成绩请求参数失败'
            raise ScoreException(self.code, msg)

        payload = {
            '__VIEWSTATE': view_state,
            'Button2': '在校学习成绩查询',
            'btn_zcj': '历年成绩',
            'btnCx': ' 查  询 ',
            'ddlXN': '',
            'ddlXQ': ''
        }
        try:
            res = self._post(score_url, data=payload, **kwargs)
        except TooManyRedirects:
            raise ScoreException(self.code, '成绩接口已关闭')
        except RequestException:
            raise ScoreException(self.code, '获取成绩信息失败')

        tip = get_alert_tip(res.text)
        if tip:
            raise ScoreException(self.code, tip)

        return ScoreParse(self.code, res.text, use_api).get_score(score_year, score_term)


class ScoreParse():
    ''' 成绩页面解析模块 '''

    def __init__(self, code, html, use_api):
        self.code = code
        self.use_api = use_api
        self.soup = BeautifulSoup(html, "html.parser")
        self._html_parse_of_score()

    def _html_parse_of_score(self):
        table = self.soup.find("table", {"id": re.compile("Datagrid1", re.IGNORECASE)})
        if not table:
            raise ScoreException(self.code, '获取成绩信息失败')

        rows = table.find_all('tr')
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
                "score": self.handle_data(score)
            }
            # 有其他成绩内容则输出
            makeup_score = cells[10].text
            retake_score = cells[11].text
            if makeup_score != '\xa0':
                # 补考成绩
                score_dict['bkcj'] = makeup_score
            if retake_score != '\xa0':
                # 重修成绩
                score_dict['cxcj'] = retake_score
            # 组装数组格式的数据备用
            self.score_info[year] = self.score_info.get(year, {})
            self.score_info[year][term] = self.score_info[year].get(term, [])
            self.score_info[year][term].append(score_dict)

    def get_score(self, year, term):
        ''' 返回成绩信息json格式 '''
        try:
            if not self.score_info:
                raise KeyError
            if year:
                if term:
                    return self.score_info[year][term]
                return self.score_info[year]
        except KeyError:
            raise ScoreException(self.code, '暂无成绩信息')

        return self.score_info

    @staticmethod
    def handle_data(data):
        try:
            return float(data)
        except ValueError:
            return data
