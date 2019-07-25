正方系统 Python SDK。

[![Build Status](https://travis-ci.org/dairoot/school-api.svg?branch=master)](https://travis-ci.org/dairoot/school-api)
[![Scrutinizer Code Quality](https://scrutinizer-ci.com/g/dairoot/school-api/badges/quality-score.png?b=master)](https://scrutinizer-ci.com/g/dairoot/school-api/?branch=master)
[![codecov](https://codecov.io/gh/dairoot/school-api/branch/master/graph/badge.svg)](https://codecov.io/gh/dairoot/school-api)
[![pypi](https://img.shields.io/pypi/v/school-api.svg)](https://pypi.org/project/school-api/)
[![Downloads](https://pepy.tech/badge/school-api)](https://pepy.tech/project/school-api)

## Usage
```Shell
$ pip install School-Api
```

```Python
from school_api import SchoolClient

# 先实例化一个学校，再实例化用户
school = SchoolClient(url='http://210.38.137.126:8016')
user = school.user_login('2014xxxx', 'xxxx')
schedule_data = user.get_schedule()
print(schedule_data)
```
[ 线上测试接口](http://server.dairoot.cn)

[【阅读文档】](https://dairoot.github.io/school-api/) 使用示例参见 [examples](examples/)

## Api Function

| Api               |  Description  | Argument        |
| :--------         | :-----        | :----           |
| user_login        | 登陆函数      | account, password, user_type=1, use_cookie_login=True   |
| get_schedule      | 课表查询      | schedule_year=None, schedule_term=None, schedule_type=None   |
| get_score         | 成绩查询      | score_year=None, score_term=None, use_api=0   |
| get_info          | 用户信息查询  |          |
| get_place_schedule| 教学场地课表查询（可用于空教室查询） |campus_list=None, building_list=None, classroom_type_list=None, classroom_name_list=None, filter_campus_list=None, filter_building_list=None, filter_classroom_type_list=None   |


## School-Api Options

| Option    | Default        |  Description       |
| :--------  | :-----        | :----      |
| url        | 不存在默认值  | 教务系统地址(`必填`) |
| name      | NULL          | 学校名称 |
| code      | NULL          | 学校英文缩写 |
| login_url_path| /default2.aspx   | 登录地址路径 |
| lan_url       | None      | 内网地址            |
| exist_verify  | True      | 是否存在验证码      |
| use_ex_handle | True      | 是否使用异常处理    |
| priority_proxy| False     | 是否优先使用代理    |
| proxies       | None      | 代理地址           |
| url_path_list  | `略`      | 学校接口地址列表    |
| class_time_list| `略`     | 上课时间列表        |
| timeout       | 10        | 全局请求延时        |
| session       | MemoryStorage | 缓存工具(推荐使用redis) |

## User permissions

<table>
    <tr align="center">
        <td rowspan="2">用户 \权限</td>
        <td colspan="2">个人课表类型</td>
        <td colspan="3">班级课表类型</td>
        <td rowspan="2">个人信息</td>
        <td rowspan="2">成绩信息</td>
    </tr>
    <tr align="center">
        <td>学生课表</td>
        <td>教师课表</td>
        <td>学生课表</td>
        <td>教师课表</td>
        <td>教学场地课表</td>
    </tr>
    <tr align="center">
        <td>学生</td>
        <td>√</td>
        <td></td>
        <td>√</td>
        <td></td>
        <td></td>
        <td>√</td>
        <td>√</td>
    </tr>
    <tr align="center">
        <td>教师</td>
        <td></td>
        <td></td>
        <td></td>
        <td>√</td>
        <td></td>
        <td>√</td>
        <td></td>
    </tr>
    <tr align="center">
        <td>部门</td>
        <td></td>
        <td></td>
        <td>√</td>
        <td></td>
        <td>√</td>
        <td></td>
        <td></td>
    </tr>
</table>
