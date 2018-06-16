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

    def _get_view_state_from_html(self, html):
        return self._client.get_view_state_from_html(html)

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
    def school_url(self):
        return self._client.school.school_url[self.user_type]
