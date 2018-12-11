# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup
from school_api.exceptions import SchoolException


def get_alert_tip(html):
    ''' 获取页面提示信息 '''
    tips = re.findall(r">alert\(\'(.*?)\'", html)
    if tips:
        return tips[0]


def get_view_state_from_html(html):
    ''' 获取 __VIEWSTATE 值 '''
    pre_soup = BeautifulSoup(html, "html.parser")
    view_state_soup = pre_soup.find(attrs={"name": "__VIEWSTATE"})
    try:
        view_state = view_state_soup['value']
    except TypeError:
        raise SchoolException('view_state','', '获取view_state失败')

    return view_state
