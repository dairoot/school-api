正方系统 Python SDK。

## 使用示例

```Python
from school_api import SchoolClient

# 先实例化一个学校，再实例化用户
GdouApi = SchoolClient(url='http://61.142.33.204')
student = GdouApi.user_login('2014xxxx', 'xxxx', timeout=5)
schedule_data = student.get_schedule()
print(schedule_data)
```
使用示例参见 [examples](examples/)

## School-Api Options

| Option    | Default        |  Description       |
| :--------  | :-----        | :----      |
| url        | 不存在默认值  | 外网登录地址(`必填`) |
| name      | 空            | 学校名称 |
| debug     | False         | 模块调试   |
| login_url_path| /default2.aspx   | 登录地址路径 |
| lan_url       | None      | 内网地址            |
| exist_verify  | True      | 是否存在验证码      |
| use_proxy     | False     | 是否优先使用代理    |
| proxies       | None      | 代理                |
| school_url    | `略`      | 学校接口地址        |
| timeout       | 10        | 全局请求延时        |
| login_view_state  | {}    | 学校登录页面的view_state(`唯一`)  |
| session       | MemoryStorage | 缓存工具(推荐使用redis) |