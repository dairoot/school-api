from school_api import SchoolClient


conf = {
    'name': '广东科技学院',
    'code': 'gdst',
    'exist_verify': True,          # 是否存在验证码
    'login_url': '/default2.aspx',
    'login_view_state': {           # login_view_state 的存在可以避免 初始化学校时的获取
        'http://61.142.33.204/default2.aspx': 'dDw3OTkxMjIwNTU7Oz5vJ/yYUi9dD4fEnRUKesDFl8hEKA==',
        'http://61.142.33.204/default4.aspx': 'dDwxMTE4MjQwNDc1Ozs+MzFt0h81g6NGHTq1L9P2NfWUGLA=',
    },
    'lan_url': 'http://172.16.1.8',  # 内网地址
    'use_proxy': False,             # 是否优先使用代理
    'url_endpoint': None,           # 教务系统链接
    # 'proxies': {"http": "http://XXXX:XXXX@XXXX:3120/", }  # 代理存在时，请求失败则会切换成代理
}

# 先实例化一个学校，再实例化用户
GdstApi = SchoolClient('http://61.142.33.204', **conf)  # 注册一个学校A
GdouApi = SchoolClient(url='http://210.38.137.126:8016')    # 注册一个学校B


client_a = GdstApi.user_login('user', 'password', timeout=2)  # 学校A实例化一个学生a
client_b = GdstApi.user_login('user', 'password', user_type=1, timeout=2)  # 学校A实例化一个教师b
client_c = GdstApi.user_login('user', 'password', user_type=2)  # 学校A实例化一个部门教师c

# 获取 2017-2018学年1学期的 课表
schedule_data = client_b.get_schedule(schedule_year='2017-2018', schedule_term='1', timeout=5)
print(schedule_data)

# 获取 获取最新的 个人课表
schedule_data = client_a.get_schedule()

# 获取 2017-2018学年2学期的 班级课表
schedule_data = client_a.get_schedule(
    timeout=5, schedule_type=1, schedule_year='2017-2018', schedule_term='1')

# 获取 全部成绩
score_data = client_a.get_score()
# 获取 2017-2018学年1学期的 成绩
score_data = client_a.get_score(score_year='2017-2018', score_term='1', timeout=5)

# 获取 用户信息
info_data = client_a.get_info(timeout=5)
# print(info_data)

# 部门教师账号 获取学生班级课表
schedule_data = client_c.get_schedule(class_name='15软件本科2班', timeout=5)
print(schedule_data)
