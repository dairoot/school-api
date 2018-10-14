## 接口方法

| Api               |  描述         | 参数             |
| :--------         | :-----        | :----           |
| [user_login](api/登陆接口.md)        | 登陆函数      | account, password, user_type=1, use_session=True   |
| [get_schedule](api/课表接口.md)      | 课表查询      | schedule_year=None, schedule_term=None, schedule_type=None   |
| [get_score](api/成绩接口.md)         | 成绩查询      | score_year=None, score_term=None, use_api=0   |
| [get_info](api/用户信息.md)          | 用户信息查询  |          |
| [get_place_schedule](api/教学场地.md)| 教学场地课表查询（可用于空教室查询） |campus_list=None, building_list=None, classroom_type_list=None, classroom_name_list=None, filter_campus_list=None, filter_building_list=None, filter_classroom_type_list=None   |


## 接口权限

<table>
    <tr align="center">
        <td rowspan="2">用户\权限</td>
        <td colspan="2">个人课表类型</td>
        <td colspan="3">班级课表类型</td>
        <td rowspan="2">个人信息</td>
        <td rowspan="2">成绩信息</td>
    </tr>
    <tr align="center">
        <td>学生</td>
        <td>教师</td>
        <td>学生</td>
        <td>教师</td>
        <td>教学场地</td>
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