#!/usr/bin/env python
# coding:utf8
import os
import time
import logging
from easyops.utils import utils

from flask import (
    flash, redirect, render_template, url_for, request, session)

from easyops.libs.ansible.api import Task
from easyops.models.models import AnsibleHosts 
from easyops.api_v1_0 import api

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
host_cfg = os.path.join(os.path.dirname(BASE_DIR), "inventory.py")

runner = Task(inventory=host_cfg)

@api.route("/overview", methods=["GET"])
def overview():
    user_id = session.get("user_id")
    if user_id is not None:
        return render_template("overview/overview.html")
    else:
        return redirect(url_for("api_v1_0.login"))


@api.route("/execute", methods=["GET", "POST"])
def execute():
    user_id = session.get("user_id")
    if request.method == "POST":
        form = request.form
        execute_info = form.to_dict()
        module = execute_info["module"]
        command = execute_info["cmd"]
        host = execute_info["host"]
        if not utils.check_ip(host):
            flash("Ipaddress is invalid.")
            return render_template("execute/remote.html")
        if host:
            runner.run(hosts=host, module=module, args=command)
            exec_rets = runner.get_result(host)
            if exec_rets["success"]:
                [exec_rets["success"].pop(x) for x in list(exec_rets["success"].keys()) if x != host]
            return render_template("execute/_results.html", results=exec_rets, host=host)
        else:
            flash("Not found some args.")
            return render_template("execute/_results.html")
    else:
        remote_hosts = AnsibleHosts.query.filter_by(user_id=user_id).all()
        return render_template("execute/remote.html", remote_hosts=remote_hosts)

@api.route("/execute/host_details", methods=["GET", "POST"])
def execute_host_details():
    if request.method == "POST":
        form = request.form
        execute_info = form.to_dict()
        module = execute_info["module"]
        command = execute_info["cmd"]
        host = execute_info["host"]
        if not utils.check_ip(host):
            flash("Ipaddress is invalid.")
            return "<h1 style='color:red;'>Checked [{0}] ipaddress is invalid</h1>".format(host)
        if host:
            runner.run(hosts=host, module=module, args=command)
            exec_rets = runner.get_result(host)
            [exec_rets["success"].pop(x) for x in list(exec_rets["success"].keys()) if x != host]
            if exec_rets["success"]:
                exec_rets = utils.get_host_details(host, exec_rets)
            return render_template("manage_host/_host_details.html", results=exec_rets, host=host)
        else:
            flash("Not found some args.")
            return redirect(url_for("api_v1_0.manage_host"))
    else:
        return redirect(url_for("api_v1_0.manage_host"))