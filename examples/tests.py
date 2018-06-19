from school_api import SchoolClient


conf = {
    'debug': True,                 # 模块调试
    'lan_url': 'http://172.16.1.8',  # 内网地址
    'use_proxy': False,             # 是否优先使用代理
    'school_url': None,             # 教务系统链接
    'proxies': {"http": "http://gxgk:gxgkteam@tunnel.gxgk.cc:3120/", }  # 代理
}

# 先实例化一个学校，再实例化用户
GdstApi = SchoolClient(url='http://61.142.33.204', **conf)  # 注册一个学校A
GdouApi = SchoolClient(url='http://210.38.137.126:8016')    # 注册一个学校B


client_a = GdstApi.user_login('XXXX', 'XXXXXXXX', timeout=2)  # 学校A实例化一个学生
client_b = GdstApi.user_login('XXXX', 'XXXXXXXX', user_type=1)  # 学校A实例化一个教师
# client_c = GdstApi.user_login('XXXX', 'XXXXXXXX', user_type=1)  # 学校A实例化一个部门教师

# 获取 2017-2018学年1学期的 课表
schedule_data = client_b.get_schedule(schedule_year='2017-2018', schedule_term='1', timeout=5)
print (schedule_data)

# 获取 获取最新的 个人课表
schedule_data = client_a.get_schedule()

# 获取 2017-2018学年2学期的 班级课表
schedule_data = client_a.get_schedule(timeout=5, schedule_type=1, schedule_year='2017-2018', schedule_term='1')

# 获取 2017-2018学年1学期的 成绩
score_data = client_a.get_score(score_year='2017-2018', score_term='1', timeout=5)

# 获取 用户信息
info_data = client_a.get_info(timeout=5)
# print(info_data)

