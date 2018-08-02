正方系统 Python SDK。

[![Build Status](https://travis-ci.org/dairoot/school-api.svg?branch=master)](https://travis-ci.org/dairoot/school-api)

## Usage
```Shell
$ pip install git+git://github.com/dairoot/school-api.git
```

```Python
from school_api import SchoolClient

# 先实例化一个学校，再实例化用户
GdouApi = SchoolClient(url='http://210.38.137.126:8016')
student = GdouApi.user_login('2014xxxx', 'xxxx', timeout=5)
schedule_data = student.get_schedule()
print(schedule_data)
```
使用示例参见 [examples](examples/)

## Function

- [x] 成绩查询
- [x] 课表查询
- [x] 用户信息查询
- [x] 教学场地课表查询（可用于空教室查询）

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
| priority_porxy| False     | 是否优先使用代理    |
| proxies       | None      | 代理               |
| url_endpoint  | `略`      | 学校接口地址列表    |
| class_time_list| `略`     | 上课时间列表        |
| timeout       | 10        | 全局请求延时        |
| login_view_state  | {}    | 学校登录页面的view_state(`唯一`)  |
| session       | MemoryStorage | 缓存工具(推荐使用redis) |

## User permissions

<table>
    <tr align="center">
        <td rowspan="2">类型 \权限</td>
        <td colspan="2">个人课表类型</td>
        <td colspan="3">班级课表类型</td>
        <td rowspan="2">个人信息</td>
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
    </tr>
    <tr align="center">
        <td>教师</td>
        <td></td>
        <td></td>
        <td></td>
        <td>√</td>
        <td></td>
        <td>√</td>
    </tr>
    <tr align="center">
        <td>部门</td>
        <td></td>
        <td></td>
        <td>√</td>
        <td></td>
        <td>√</td>
        <td></td>
    </tr>
</table>