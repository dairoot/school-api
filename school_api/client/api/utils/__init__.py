# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import re
from bs4 import BeautifulSoup
from school_api.exceptions import OtherException


def get_alert_tip(html):
    ''' 获取页面提示信息 '''
    tips = re.findall(r">alert\(\'(.*?)\'", html)
    if tips:
        return tips[0]
    return None


def get_view_state_from_html(html):
    ''' 获取 __VIEWSTATE 值 '''
    pre_soup = BeautifulSoup(html, "html.parser")
    view_state_soup = pre_soup.find(attrs={"name": "__VIEWSTATE"})
    try:
        view_state = view_state_soup['value']
    except TypeError:
        raise OtherException('', '获取view_state失败')

    return view_state
