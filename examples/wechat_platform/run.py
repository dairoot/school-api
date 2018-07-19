#!/usr/bin/env python
# encoding: utf-8
from __future__ import absolute_import, unicode_literals

import os
from flask import Flask, request
from flask_wechatpy import Wechat, wechat_required
from wechatpy.replies import create_reply, EmptyReply, TextReply
from school import get_schedule


app = Flask(__name__)
app.config['WECHAT_APPID'] = os.getenv('WECHAT_APPID', '')
app.config['WECHAT_SECRET'] = os.getenv('WECHAT_SECRET', '')
app.config['WECHAT_TOKEN'] = os.getenv('WECHAT_TOKEN', '')
app.config['DEBUG'] = True
wechat = Wechat(app)


@app.route('/', methods=['GET', 'POST'])
@wechat_required
def wechat_handler():
    msg = request.wechat_msg
    reply = EmptyReply()
    if msg.type == 'text':
        if msg.content == '课表':
            data = get_schedule()
            reply = create_reply(data, message=msg)
        elif msg.content == '成绩':
            reply = EmptyReply()
        else:
            reply = TextReply(content=msg.content, message=msg)

    return reply


@app.route('/access_token')
def access_token():
    return "access token: {}".format(wechat.access_token)


if __name__ == '__main__':
    app.run()
