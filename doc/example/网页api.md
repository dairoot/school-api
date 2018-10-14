## 网页 api


```python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from flask import Flask, request, jsonify
from school_api import SchoolClient

app = Flask(__name__)
school = SchoolClient('http://61.142.33.204')


@app.route('/get_info')
def get_info():
    # 获取存用户信息
    # http://127.0.0.1:5000/get_info?account=XXX&passwd=XXX
    account = request.args.get("account")
    passwd = request.args.get("passwd")
    user = school.user_login(account, passwd)
    return jsonify(user.get_info())


@app.route('/get_score')
def get_score():
    # 获取成绩
    # http://127.0.0.1:5000/get_score?account=XXX&passwd=XXX
    account = request.args.get("account")
    passwd = request.args.get("passwd")
    user = school.user_login(account, passwd)
    return jsonify(user.get_score())


@app.route('/get_schedule')
def get_schedule():
    # 获取课表
    # http://127.0.0.1:5000/get_schedule?account=XXX&passwd=XXX
    account = request.args.get("account")
    passwd = request.args.get("passwd")
    user = school.user_login(account, passwd)
    schedule_year = '2015-2016'
    schedule_term = '2'
    schedule_data = user.get_schedule(schedule_year, schedule_term)
    return jsonify(schedule_data)


if __name__ == '__main__':
    app.run()
```