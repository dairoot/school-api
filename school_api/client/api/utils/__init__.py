# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup


def get_tip(html):
    ''' 获取页面提示信息 '''
    tips = re.findall(r">alert\(\'(.*?)\'", html)
    if tips:
        return tips[0]


def get_view_state_from_html(html):
    ''' 获取 __VIEWSTATE 值 '''
    pre_soup = BeautifulSoup(html, "html.parser")
    view_state = pre_soup.find(
        attrs={"name": "__VIEWSTATE"})['value']
    return view_state
