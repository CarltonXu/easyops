#!/usr/bin/env python
# coding:utf8

import functools
import logging
import datetime
import json

from io import BytesIO

from flask import (
    flash, g, redirect, render_template, request, url_for, session, make_response)

from easyops import csrf
from easyops.forms.form import LoginForm, RegisterForm
from easyops.controller.users.users import UsersManager
from easyops.api_v1_0 import api
from easyops.libs.verify_code.verify_code import get_verify_code

@api.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    user = UsersManager(user_id=user_id)

    if user_id is None:
        g.user = None
    else:
        g.user = user.user


@api.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = request.form["username"]
            password = request.form["password"]
            verify_code_string = request.form["verify_code"].lower()
            login_ipaddress = request.form["login_ipaddress"]
            login_region = json.loads(request.form["login_region"])["province"]
            user = UsersManager(username=username)
            resp_user_info = user.check_user_exsits()
            remember_me = request.form.get("remember")
            if resp_user_info["response_code"] == 1001:
                resp = user.check_user_password(password)
                if resp["response_code"] == 1002:
                    resp_verify_code = user.verify_login_code(session, verify_code_string)
                    if resp_verify_code["response_code"] == 1006:
                        if session.get("user_id") is None:
                           login_time = datetime.datetime.now() 
                           resp = user.set_user_login_history(login_time, login_ipaddress, login_region)

                        session.clear()
                        session["user_id"] = resp_user_info["user_id"]
                        if remember_me:
                            session.permanent = True
                        return redirect(url_for("api_v1_0.index"))
                    else:
                        flash(resp_verify_code["errormsg"])
                else:
                    flash(resp["errormsg"])
        else:
            flash(form)

    if session.get("user_id") is not None:
        return redirect(url_for("api_v1_0.index"))
    else:
        return render_template("auth/login.html", form=form)


@api.route("/logout", methods=["GET", "POST"])
def logout():
    print(session)
    if session.get("user_id") is not None:
        user = UsersManager(user_id=session.get("user_id"))
        user.set_user_login_state(False)
    session.clear()
    return redirect(url_for("api_v1_0.login"))


@api.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = request.form.get("username")
            password = request.form.get("password")
            repassword = request.form.get("repassword")
            if password != repassword:
                errormsg = "两次密码输入不一致"
            else:
                errormsg = None
            user = UsersManager(username=username)
            if user.check_user_exsits().get("response_code") == 1001:
                errormsg = "用户 %s 已经注册，请直接登陆" % (username)
                flash(errormsg)

                return redirect(url_for("api_v1_0.login"))

            if errormsg is None:
                register_time = datetime.datetime.now()
                avatar = "/static/img/avatar/avatar.jpeg"
                user.create_user(username, password, register_time, avatar)

                return redirect(url_for("api_v1_0.login"))

            flash(errormsg)

    return render_template("auth/register.html", form=form)

@csrf.exempt
@api.route("/resetpassword", methods=["GET", "POST"])
def resetpassword():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        resetpassword = request.form.get("resetpassword")
        errormsg = None
        user = UsersManager(username=username)
        if user is None:
            errormsg = "用户 %s 已经不存在，请注册后登陆" % (username)
            return redirect(url_for("api_v1_0.register"))
        import pdb
        pdb.set_trace()
        if errormsg is None:
            try:
                if user.check_user_password(password).get("response_code") != 3003:
                    user.set_user_password(resetpassword)
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