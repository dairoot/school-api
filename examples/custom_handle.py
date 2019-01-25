# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from school_api import SchoolClient
from school_api.exceptions import SchoolException, LoginException, IdentityException


school = SchoolClient('http://61.142.33.204', use_ex_handle=False)


def service_resp():
    def decorator(func):
        def warpper(*args, **kwargs):
            try:
                client = school.user_login(*args, **kwargs)
                data = func(client)
            except IdentityException as reqe:
                # 账号密码错误
                return {'error': reqe}
            except LoginException as reqe:
                # 登录失败 (包含以上错误)
                return {'error': reqe}
            except SchoolException as reqe:
                # 请求失败 (包含以上错误)
                return {'error': reqe}
            except Exception:
                # 模块报错 (包含以上错误)
                return {'error': '教务请求失败'}
            else:
                # 数据处理 (如：缓存)
                return data

        return warpper
    return decorator


@service_resp()
def bind_account(user):
    return user.get_info()


@service_resp()
def get_schedule(user):
    return user.get_schedule()


@service_resp()
def get_score(user):
    return user.get_score()


if __name__ == '__main__':
    account = 'user'
    password = 'password'
    data = bind_account(account, password, use_login_cookie=False)
    print(data)
