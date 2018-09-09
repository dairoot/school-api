# -*- coding: utf-8 -*-
import re


def get_tip(html):
    ''' 获取页面提示信息 '''
    tips = re.findall(r">alert\(\'(.*?)\'", html)
    if tips:
        return tips[0]
