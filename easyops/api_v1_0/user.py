#!/usr/bin/env python
# coding:utf8
import os
import logging
import random
import string

from flask import (
    redirect, render_template, url_for, request, session)

from easyops import csrf
from easyops.api_v1_0 import api
from easyops.controller.users.users import UsersManager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_AVATAR_DIR = os.path.join(os.path.dirname(BASE_DIR), "static/img/avatar")

@csrf.exempt
@api.route("/user", methods=["GET", "POST"])
def user():
    user_id = session.get("user_id")
    if request.method == "GET":
        user = UsersManager(user_id=user_id)
        last_login_info = user.get_user_last_login_history().get("user_history")
        logins_info = user.get_user_login_history().get("user_history")
        return render_template("user/user.html",
                                users_info=user.user,
                                last_login_info=last_login_info,
                                logins_info=logins_info)

@csrf.exempt
@api.route("/update_user", methods=["POST"])
def update_user():
    user_id = session.get("user_id")
    form = request.form
    email = form.get("person_email")
    phone = form.get("person_phone_number")
    sex = form.get("person_sex")
    update_params = {
        "email": email,
        "phonenumber": phone,
        "sex": sex
    }
    user = UsersManager(user_id=user_id)
    user.update_user_info(update_params)
    return redirect(url_for("api_v1_0.user"))

@csrf.exempt
@api.route("/update_avatar", methods=["POST"])
def update_user_avatar():
    user_id = session.get("user_id")
    user = UsersManager(user_id=user_id)
    avatar_file = request.files.get("file")
    avatar_img_suffix = "." + avatar_file.filename.split(".")[1]
    avatar_file_name = "".join(random.sample(string.ascii_letters + string.digits, 8)) + avatar_img_suffix
    avatar_save_path = os.path.join(UPLOAD_AVATAR_DIR, avatar_file_name) 
    avatar_path = os.path.join("/static/img/avatar", avatar_file_name)
    try:
        avatar_file.save(avatar_save_path)
        user.set_user_avatar(avatar_path)
    except Exception as err:
        return "Save upload file {} failed, error: {}".format(avatar_file_name, err)
    return redirect(url_for("api_v1_0.user"))