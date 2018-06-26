正方系统 Python SDK。

## 使用示例

```Python
from school_api import SchoolClient

# 先实例化一个学校，再实例化用户
GdouApi = SchoolClient(url='http://210.38.137.126:8016')
student = GdouApi.user_login('2014xxxx', 'xxxx', timeout=5)
schedule_data = student.get_schedule()
print(schedule_data)
```
使用示例参见 [examples](examples/)
