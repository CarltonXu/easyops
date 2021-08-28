#!/usr/bin/env python
# coding:utf8

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session)
from werkzeug.security import check_password_hash, generate_password_hash

from easyops import redis_store, constants, db
from easyops.utils.response_code import RET
from easyops.models import Users
from easyops.api_v1_0 import api


@api.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        errormsg = None
        try:
            user = Users.query.filter_by(username=username).first()
        except Exception as err:
            logging.error(err)
            errormsg = "数据库查询失败"
        else:
            if user is None:
                errormsg = "用户不存在, 请注册后再登陆使用"
            elif not user.check_password(password):
                errormsg = "密码不正确"

        if errormsg is None:
            session.clear()
            session["user_id"] = user.id

            return render_template("index.html")

        flash(errormsg)

    if session.get("user_id") is not None:
        return render_template("index.html")
    else:
        return render_template("auth/login.html")


@api.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("api_v1_0.login"))


@api.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        errormsg = None
        try:
            user = Users.query.filter_by(username=username).first()
        except Exception as err:
            logging.warn(err)
            errormsg = "数据库查询失败"
        else:
            if user is not None:
                errormsg = "用户 %s 已经注册，请直接登陆" % (username)
                return redirect(url_for("api_v1_0.login"))
        if errormsg is None:
            try:
                au = Users(username=username)
                au.set_password = password
                db.session.add(au)
                db.session.commit()
            except Exception as err:
                errormsg = "注册 %s 用户失败，请重新注册" % (username)
                render_template("auth/register.html")
            return redirect(url_for("api_v1_0.login"))
        flash(errormsg)

    return render_template("auth/register.html")


@api.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = Users.query.filter_by(id=user_id).first()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('api_v1_0.login'))

        return view(**kwargs)

    return wrapped_view
