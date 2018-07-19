# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import six

from school_api.utils import to_text, to_binary


class SchoolException(Exception):

    def __init__(self, name, school_code, errmsg):
        self.name = name
        self.errmsg = errmsg
        self.school_code = school_code

    def __str__(self):
        _repr = 'school_code:{school_code}, Error message: {name}，{msg}'.format(
            school_code=self.school_code,
            name=self.name,
            msg=self.errmsg
        )
        if six.PY2:
            return to_binary(_repr)
        else:
            return to_text(_repr)

    def __repr__(self):
        _repr = '{msg}'.format(
            msg=self.errmsg
        )
        if six.PY2:
            return to_binary(_repr)
        else:
            return to_text(_repr)


class LoginException(SchoolException):

    def __init__(self, school_code, errmsg):
        super(LoginException, self).__init__('登录接口', school_code, errmsg)


class IdentityException(LoginException):

    def __init__(self, school_code, errmsg):
        super(IdentityException, self).__init__(school_code, errmsg)


class CheckCodeException(LoginException):

    def __init__(self, school_code, errmsg):
        super(CheckCodeException, self).__init__(school_code, errmsg)


class ScheduleException(SchoolException):

    def __init__(self, school_code, errmsg):
        super(ScheduleException, self).__init__('课表接口', school_code, errmsg)


class ScoreException(SchoolException):

    def __init__(self, school_code, errmsg):
        super(ScoreException, self).__init__('成绩接口', school_code, errmsg)


class UserInfoException(SchoolException):

    def __init__(self, school_code, errmsg):
        super(UserInfoException, self).__init__('用户信息接口', school_code, errmsg)
