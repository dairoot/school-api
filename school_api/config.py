# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

LOGIN_SESSION_SAVE_TIME = 3600 * 2

URL_PATH_LIST = [
    {
        # 学生
        "HOME_URL": "/xs_main.aspx?xh=",
        "SCORE_URL": [
            "/xscj_gc.aspx?xh=",
            "/xscj_gc2.aspx?xh=",
            "/Xscjcx.aspx?xh=",
            "/xscjcx.aspx?xh=",
            "/xscjcx_dq.aspx?xh="
        ],
        "INFO_URL": "/xsgrxx.aspx?gnmkdm=N121501&xh=",
        "SCHEDULE_URL": [
            "/xskbcx.aspx?gnmkdm=N121603&xh=",
            "/tjkbcx.aspx?gnmkdm=N121601&xh="
        ]
    },
    {
        # 教师
        "HOME_URL": "/js_main.aspx?xh=",
        "INFO_URL": "/lw_jsxx.aspx?gnmkdm=N122502&zgh=",
        "SCHEDULE_URL": ["", "/jstjkbcx.aspx?gnmkdm=N122303&zgh="]
    },
    {
        # 部门
        "HOME_URL": "/bm_main.aspx?xh=",
        "SCHEDULE_URL": ["", "/tjkbcx.aspx?gnmkdm=N120313&xh="],
        "PLACE_SCHEDULE_URL": "/kbcx_jxcd.aspx?gnmkdm=N120314&xh="
    }
]

CLASS_TIME = [
    ["8:30", "9:15"],
    ["9：20", "10:05"],
    ["10:25", "11:10"],
    ["11:15", "12:00"],
    ["14:40", "15:25"],
    ["15:30", "16:15"],
    ["16:30", "17:15"],
    ["17:20", "18:05"],
    ["19:30", "20:15"],
    ["20:20", "21:05"]
]
