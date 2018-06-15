# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class BaseSchoolApi(object):
    """ WeChat API base class """

    def __init__(self, client=None):
        self._client = client

    def _get(self, url, **kwargs):
        return self._client.get(url, **kwargs)

    def _post(self, url, **kwargs):
        return self._client.post(url, **kwargs)

    @property
    def account(self):
        return self._client.account

    @property
    def password(self):
        return self._client.password

    @property
    def user_type(self):
        return self._client.user_type

    def schedule_type(self):
        return self._client.schedule_type

    @property
    def conf_url(self):
        urls = [
            {
                'SCORE_URL': '/xscj_gc.aspx?xh=',
                'PERSON_SCHEDULE_URL': "/xskbcx.aspx?gnmkdm=N121603&xh=",
                'CLASS_SCHEDULE_URL': ''

            }, {
                'CLASS_SCHEDULE_URL': '/jstjkbcx.aspx?gnmkdm=N122303&zgh='
            }, {
                'SCHEDULE_URL': ''
            }
        ]
        return urls[self.user_type]
