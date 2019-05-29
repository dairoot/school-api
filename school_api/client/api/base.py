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

    def _head(self, url, **kwargs):
        return self._client.head(url, **kwargs)

    def _get_view_state(self, url, **kwargs):
        return self._client.get_view_state(url, **kwargs)

    def _switch_proxy(self):
        return self._client.switch_proxy()

    def _update_url_token(self, url_token):
        return self._client.update_url_token(url_token)

    @property
    def code(self):
        return self._client.school.code

    @property
    def user(self):
        return self._client.user

    @property
    def school_url(self):
        return self._client.school.url_path_list[self.user.user_type]

    @property
    def time_list(self):
        return self._client.school.time_list
