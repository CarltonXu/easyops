#!/usr/bin/env python
# coding:utf8
import os
import logging

from flask import (
    Blueprint, flash, redirect, render_template, send_from_directory,
    url_for, request, session, make_response)

from werkzeug.security import check_password_hash, generate_password_hash

from easyops import redis_store, constants, db
from easyops.utils import utils
from easyops.utils.response_code import RET
from easyops.libs.ansible.api import Task
from easyops.models import Users, UsersLoginHistory
from easyops.api_v1_0 import api
from easyops.api_v1_0.auth import get_user_last_login_history, get_user_login_history

@api.route("/user", methods=["GET", "POST"])
def user():
    user_id = session.get("user_id")
    if request.method == "GET":
        users_info = Users.query.filter_by(id=user_id).first()
        last_login_info = get_user_last_login_history(user_id=user_id).get("user_history")
        logins_info = get_user_login_history(user_id=user_id).get("user_history")
        return render_template("user/user.html",
                                users_info=users_info,
                                last_login_info=last_login_info,
                                logins_info=logins_info)