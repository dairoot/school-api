#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from redis import Redis
from school_api import SchoolClient
from school_api.session.redisstorage import RedisStorage

redis = Redis()
session = RedisStorage(redis)


class School():
    conf = {
        'session': session
    }
    GdstApi = SchoolClient('http://61.142.33.204', **conf)

    def __init__(self, user, password):
        self.student = self.GdstApi.user_login(user, password)

    def info(self):
        return self.student.get_info()

    def schedule(self, schedule_year=None, schedule_term=None):
        return self.student.get_schedule(schedule_year, schedule_term, schedule_type=1)

    def score(self, score_year=None, score_term=None):
        return self.student.get_score(score_year, score_term)
