#!/usr/bin/env python
# coding:utf8

import functools
import logging
import datetime

from io import BytesIO

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, session, make_response)
from werkzeug.security import check_password_hash, generate_password_hash

from easyops import redis_store, constants, db
from easyops.utils.response_code import RET
from easyops.models import Users, UsersLoginHistory
from easyops.api_v1_0 import api
from easyops.libs.verify_code.verify_code import get_verify_code


@api.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        login_ipaddress = request.form["login_ipaddress"]
        login_region = request.form["login_region"]
        verify_code_string = request.form["verify_code"].lower()
        resp_user_info = check_user_exsits(username)
        remember_me = request.form.get("remember")
        if resp_user_info["response_code"] == 1001:
            resp = check_user_password(username, password)
            if resp["response_code"] == 1002:
                resp_verify_code = verify_login_code(session, verify_code_string)
                if resp_verify_code["response_code"] == 1006:
                    if session.get("user_id") is None:
                       login_time = datetime.datetime.now() 
                       resp = set_user_login_history(username, login_time, login_ipaddress, login_region)

                    session.clear()
                    session["user_id"] = resp_user_info["user_id"]
                    if remember_me:
                        session.permanent = True
                    user_avatar_path = get_user_avatar_path(session.get("user_id")).get("user_avatar_path")
                    resp = make_response(render_template("index.html", user_avatar_path=user_avatar_path))
                    if remember_me:
                        resp.set_cookie("username", username, max_age=1296000)
                        resp.set_cookie("password", password, max_age=1296000)
                    else:
                        resp.delete_cookie("username")
                        resp.delete_cookie("password")
                    return resp
                else:
                    flash(resp_verify_code["errormsg"])
            else:
                flash(resp["errormsg"])
        else:
            flash(resp_user_info["errormsg"])

    if session.get("user_id") is not None:
        user_avatar_path = get_user_avatar_path(session.get("user_id")).get("user_avatar_path")
        return render_template("index.html", user_avatar_path=user_avatar_path)
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
        repassword = request.form.get("repassword")
        if password != repassword:
            errormsg = "两次密码输入不一致"
        else:
            errormsg = None
        try:
            user = Users.query.filter_by(username=username).first()
        except Exception as err:
            logging.warn(err)
            errormsg = "数据库查询失败"
        else:
            if user is not None:
                errormsg = "用户 %s 已经注册，请直接登陆" % (username)
                flash(errormsg)
                return redirect(url_for("api_v1_0.login"))
        if errormsg is None:
            register_time = datetime.datetime.now()
            try:
                au = Users(username=username,
                register_time=register_time,
                avatar="/static/img/avatar/avatar.jpeg")
                au.set_password = password
                db.session.add(au)
                db.session.commit()
                return redirect(url_for("api_v1_0.login"))
            except Exception as err:
                errormsg = "注册 %s 用户失败，请重新注册" % (username)
        flash(errormsg)

    return render_template("auth/register.html")


@api.route("/resetpassword", methods=["GET", "POST"])
def resetpassword():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        resetpassword = request.form.get("resetpassword")
        errormsg = None
        try:
            user = Users.query.filter_by(username=username).first()
        except Exception as err:
            logging.warn(err)
            errormsg = "数据库查询失败"
        else:
            if user is None:
                errormsg = "用户 %s 已经不存在，请注册后登陆" % (username)
                return redirect(url_for("api_v1_0.register"))
        if errormsg is None:
            try:
                if user.check_password(password):
                    user.set_password = resetpassword
                    db.session.add(user)
                    db.session.commit()
                    return redirect(url_for("api_v1_0.user"))
                else:
                    errormsg = "老密码不正确，请重新输入"
            except Exception as err:
                errormsg = "修改 %s 密码失败，请重新修改" % (username)
        return errormsg, 302

    return redirect(url_for("api_v1_0.user"))


@api.route("/code", methods=["GET"])
def verify_code():
    image, code = get_verify_code()
    buf = BytesIO()
    image.save(buf, 'jpeg')
    buf_str = buf.getvalue()
    response = make_response(buf_str)
    response.headers['Content-Type'] = 'image/gif'
    session['image'] = code
    return response

@api.route("/history")
def get_user_login_history():
    pass


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

def verify_login_code(session, verify_code_string):
    errormsg = None
    if session.get("image") is not None:
        if session.get('image').lower() != verify_code_string:
            errormsg = "验证码失败"
            res_code = 4001
        else:
            errormsg = "验证成功"
            res_code = 1006
    else:
        errormsg = "获取验证码错误"
        res_code = 4002

    return {
        "response_code": res_code,
        "errormsg": errormsg
    }

def get_user_avatar_path(user_id):
    errormsg = None
    try:
        user = Users.query.filter_by(id=user_id).first()
    except Exception as err:
        logging.error(err)
        errormsg = "数据库查询失败"
        res_code = 3001
    else:
        if user is None:
            errormsg = "用户不存在"
            res_code = 3002
            user_id = None
        else:
            res_code = 1001
            user_avatar_path = user.avatar

    return {
        "response_code": res_code,
        "errormsg": errormsg,
        "user_avatar_path": user_avatar_path
    }

def check_user_exsits(user):
    errormsg = None
    try:
        user = Users.query.filter_by(username=user).first()
    except Exception as err:
        logging.error(err)
        errormsg = "数据库查询失败"
        res_code = 3001
    else:
        if user is None:
            errormsg = "用户不存在, 请注册后再登陆使用"
            res_code = 3002
            user_id = None
        else:
            res_code = 1001
            user_id = user.id

    return {
        "response_code": res_code,
        "errormsg": errormsg,
        "user_id": user_id,
    }

def check_user_password(user, password):
    errormsg = None
    try:
        user = Users.query.filter_by(username=user).first()
    except Exception as err:
        logging.error(err)
        errormsg = err
        res_code = 3001
    else:
        if not user.check_password(password):
            errormsg = "密码不正确"
            res_code = 3003
        else:
            res_code = 1002
    
    return {
        "response_code": res_code,
        "errormsg": errormsg
    }


def check_user_login(user):
    errormsg = None
    try:
        user = Users.query.filter_by(username=user).first()
    except Exception as err:
        logging.error(err)
        errormsg = err
        res_code = 3001

    else:
        if not user.is_login:
            errormsg = "用户未登录"
            res_code = 3004
        else:
            res_code = 1003

    return {
        "response_code": res_code,
        "errormsg": errormsg
    }


def set_user_login_history(username, login_time, login_ipaddress, login_region):
    errormsg = None
    try:
        user = Users.query.filter_by(username=username).first()
        user_login_info = UsersLoginHistory(
            login_time=login_time,
            login_ipaddress=login_ipaddress,
            login_region=login_region,
            user_id=user.id, 
        )
        if check_user_login(username)["response_code"] == 3004:
            user.is_login = True
        db.session.add(user_login_info, user)
        db.session.commit()
    except Exception as err:
        errormsg = "操作数据库失败，请检查数据库."
        res_code = 3001
    else:
        res_code = 1004
    
    return {
        "response_code": res_code,
        "errormsg": errormsg
    }
def get_user_login_history(username=None, user_id=None):
    errormsg = None
    try:
        if username is not None:
            user = Users.query.filter_by(username=username).first()
            user_id = user.id
        if user_id is not None:
            user_id = user_id
        users_login_info = UsersLoginHistory.query.filter_by(
            user_id=user_id).order_by(UsersLoginHistory.id.desc()).all()
    except Exception as err:
        errormsg = "操作数据库失败，请检查数据库."
        res_code = 3001
    else:
        res_code = 1005

    return {
        "response_code": res_code,
        "errormsg": errormsg,
        "user_history": users_login_info
    }

    
def get_user_last_login_history(username=None, user_id=None):
    errormsg = None
    try:
        if username is not None:
            user = Users.query.filter_by(username=username).first()
            user_id = user.id
        if user_id is not None:
            user_id = user_id
        user_info = UsersLoginHistory.query.filter_by(
            user_id=user_id).order_by(UsersLoginHistory.id.desc()).offset(1).first()
    except Exception as err:
        errormsg = "操作数据库失败，请检查数据库."
        res_code = 3001
    else:
        res_code = 1005
    
    if user_info:
        user_history = {
            "last_login_time": user_info.login_time,
            "last_login_ipaddress": user_info.login_ipaddress,
            "last_login_region": user_info.login_region
        }
    else:
        user_history = {
            "last_login_time": "初次登陆",
            "last_login_ipaddress": "初次登陆",
            "last_login_region": "初次登陆"
        }

    return {
        "response_code": res_code,
        "errormsg": errormsg,
        "user_history": user_history
    }