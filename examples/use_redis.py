#!/usr/bin/env python
# -*- coding: utf-8 -*-

from redis import Redis


from school_api import SchoolClient
from school_api.session.redisstorage import RedisStorage

redis = Redis()
session = RedisStorage(redis)
conf = {
    'name': '广东科技学院',
    'code': 'gdst',
    'login_url_path': '/default2.aspx',  # 登录地址
    'session': session,
}


GdstApi = SchoolClient('http://61.142.33.204', **conf)
student = GdstApi.user_login('user', 'password', timeout=3)

info_data = student.get_info(timeout=5)
print(info_data)
