#!/usr/bin/env python
# coding:utf8
import os
import logging

from flask import (
    flash, redirect, render_template, url_for, request, session)

from easyops import db
from easyops.models import Users
from easyops.api_v1_0 import api
from easyops.api_v1_0.auth import get_user_last_login_history, get_user_login_history

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_AVATAR_DIR = os.path.join(os.path.dirname(BASE_DIR), "static/img/avatar")

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
    try:
        user = Users.query.filter_by(id=user_id).update(update_params)
        db.session.commit()
    except Exception as err:
        logging.error(err)
        flash("操作数据库更新失败")
    return redirect(url_for("api_v1_0.user"))

@api.route("/update_avatar", methods=["POST"])
def update_user_avatar():
    user_id = session.get("user_id")
    avatar_file = request.files.get("file")
    avatar_file_size = request.files.get("size")
    avatar_file_name = avatar_file.filename
    avatar_file_rename = "avatar_user" + str(user_id) + "." + avatar_file_name.split(".")[1]
    avatar_save_path= os.path.join(UPLOAD_AVATAR_DIR, avatar_file_rename) 
    avatar_path = os.path.join("/static/img/avatar", avatar_file_rename)
    try:
        avatar_file.save(avatar_save_path)
        user = Users.query.filter_by(id=user_id).update({"avatar": avatar_path})
        db.session.commit()
    except Exception as err:
        return "Save upload file {} failed, error: {}".format(avatar_file_name, err)
    return redirect(url_for("api_v1_0.user"))