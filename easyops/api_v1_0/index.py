# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2019 OneProCloud (Shanghai) Ltd
#
# Authors: XuXingZhuang xuxingzhuang@oneprocloud.com
#
# Copyright (c) 2019. This file is confidential and proprietary.
# All Rights Reserved, OneProCloud (Shanghai) Ltd(http://www.oneprocloud.com).)
#!/usr/bin/env python
# coding:utf-8
#

import functools

from flask import session, redirect, url_for, g, render_template


from easyops.models.models import Users
from easyops.controller.users.users import UsersManager

from . import api

@api.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    user = UsersManager(user_id=user_id)

    if user_id is None:
        g.user = None
    else:
        g.user = user.user


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('api_v1_0.login'))

        return view(**kwargs)

    return wrapped_view

@api.route("/index", methods=["GET"])
@login_required
def index():
    user_id = session.get("user_id")
    user = UsersManager(user_id=user_id)
    avatar_path = user.get_user_avatar_path()
    return render_template("index.html", avatar_path=avatar_path)

@api.route("/overview", methods=["GET"])
@login_required
def overview():
    user_id = session.get("user_id")
    if user_id is not None:
        return render_template("overview/overview.html")
    else:
        return redirect(url_for("api_v1_0.login"))