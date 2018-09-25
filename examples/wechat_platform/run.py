#!/usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import os
from flask import Flask, request, render_template
from flask_wechatpy import Wechat, wechat_required
from wechatpy.replies import create_reply, EmptyReply, TextReply
from utils import assemble_schedule, assemble_score
from school import School


app = Flask(__name__)
app.config['WECHAT_APPID'] = os.getenv('WECHAT_APPID', '')
app.config['WECHAT_SECRET'] = os.getenv('WECHAT_SECRET', '')
app.config['WECHAT_TOKEN'] = os.getenv('WECHAT_TOKEN', '')
app.config['DEBUG'] = True

user = os.getenv('GDST_STUDENT_ACCOUNT', '')
password = os.getenv('GDST_STUDENT_PASSWD', '')

wechat = Wechat(app)
school = School(user, password)


@app.route('/test_mp/msg/callback', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
@wechat_required
def wechat_handler():
    msg = request.wechat_msg
    reply = EmptyReply()
    if msg.type == 'text':

        if msg.content == '课表':
            schedule_year = '2015-2016'
            schedule_term = '2'
            schedule_data = school.schedule(schedule_year, schedule_term)
            if type(schedule_data) == dict and schedule_data.get('error'):
                reply = TextReply(content=schedule_data['error'], message=msg)
            else:
                data = assemble_schedule(schedule_data)
                reply = create_reply(data, message=msg)

        elif msg.content == '成绩':
            score_year = '2015-2016'
            score_term = '2'
            score_data = school.score(score_year, score_term)
            if type(score_data) == dict and score_data.get('error'):
                reply = TextReply(content=schedule_data['error'], message=msg)
            else:
                data = assemble_score(score_year, score_term, score_data)
                reply = create_reply(data, message=msg)

        elif msg.content == '绑定':
            content = "<a>点击绑定</a>"
            reply = TextReply(content=content, message=msg)

        else:
            reply = TextReply(content=msg.content, message=msg)

    return reply


@app.route('/get_schedule')
def get_schedule_page():
    schedule_year = '2015-2016'
    schedule_term = '2'
    schedule_data = school.schedule(schedule_year, schedule_term)
    print(schedule_data)
    return render_template(
        "schedule.html",
        schedule_type=0, weeks=1,
        schedule_info=schedule_data['schedule'])


@app.route('/access_token')
def access_token():
    return "access token: {}".format(wechat.access_token)


if __name__ == '__main__':
    app.run()
