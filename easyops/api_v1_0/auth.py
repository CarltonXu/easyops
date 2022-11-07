#!/usr/bin/env python
# coding:utf8

import functools
import logging
import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session)
from werkzeug.security import check_password_hash, generate_password_hash

from easyops import redis_store, constants, db
from easyops.utils.response_code import RET
from easyops.models import Users, UsersLoginHistory
from easyops.api_v1_0 import api


@api.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        login_ipaddress = request.form["login_ipaddress"]
        login_region = request.form["login_region"]
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
        if errormsg is None and not user.is_login:
            session.clear()
            session["user_id"] = user.id

            login_time = datetime.datetime.now()
            try:
                user_login_info = UsersLoginHistory(
                    login_time=login_time,
                    login_ipaddress=login_ipaddress,
                    login_region=login_region,
                    user_id=user.id, 
                )
                user.is_login = True
                db.session.add(user_login_info, user)
                db.session.commit()
            except Exception as err:
                errormsg = "操作数据库失败，请检查数据库."
            user_info = UsersLoginHistory.query.filter_by(user_id=user.id).order_by(UsersLoginHistory.id.desc()).offset(1).first()
            return render_template("index.html",
                                    last_login_time=user_info.login_time,
                                    last_login_ipaddress=user_info.login_ipaddress,
                                    last_login_region=user_info.login_region)
        elif user.is_login:
            user_info = UsersLoginHistory.query.filter_by(user_id=user.id).order_by(UsersLoginHistory.id.desc()).offset(1).first()
            if user_info:
                return render_template("index.html",
                                        last_login_time=user_info.login_time,
                                        last_login_ipaddress=user_info.login_ipaddress,
                                        last_login_region=user_info.login_region)
            else:
                return render_template("index.html",
                                        last_login_time="初次登陆",
                                        last_login_ipaddress="初次登陆",
                                        last_login_region="初次登陆")

        flash(errormsg)

    if session.get("user_id") is not None:
        user_info = UsersLoginHistory.query.filter_by(user_id=session.get("user_id")).order_by(UsersLoginHistory.id.desc()).offset(1).first()
        return render_template("index.html",
                                last_login_time=user_info.login_time,
                                last_login_ipaddress=user_info.login_ipaddress,
                                last_login_region=user_info.login_region)
    else:
        return render_template("auth/login.html")


@api.route("/logout", methods=["GET", "POST"])
def logout():
    user = Users.query.filter_by(id=session.get("user_id")).first()
    try:
        user.is_login = False
        db.session.add(user)
        db.session.commit()
    except Exception as err:
        err
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
            register_time = datetime.datetime.now()
            try:
                au = Users(username=username,
                register_time=register_time)
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
