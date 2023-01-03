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

from easyops.utils import utils
from easyops.controller.hosts.hosts import HostsManager
from easyops.controller.storages.storages import StoragesManager
from easyops.controller.users.users import UsersManager

import functools

from flask import session, redirect, url_for, g, render_template, jsonify

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
    system_usages = utils.get_local_usages()
    hosts = HostsManager(user_id=user_id)
    storages = StoragesManager(user_id=user_id)
    if user_id is not None:
        return render_template("overview/overview.html",
                                usages=system_usages,
                                hosts_num=len(hosts.hosts),
                                storages_num=len(storages.storages))
    else:
        return redirect(url_for("api_v1_0.login"))

@api.route("/resources/usages", methods=["GET"])
@login_required
def resource_usages():
    system_usages = utils.get_local_usages()
    return jsonify(system_usages)

@api.route("/resources/network_speed", methods=["GET"])
@login_required
def resource_netio_speed():
    networks_speed = utils.get_network_speed()
    return jsonify(networks_speed)

@api.route("/resources/login_info", methods=["GET"])
@login_required
def resources_login_info():
    user_id = session.get("user_id")
    users = UsersManager(user_id=user_id)
    users_login_info = users.get_user_login_history_count()
    return jsonify(users_login_info)