# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class BaseSchoolAPI(object):
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