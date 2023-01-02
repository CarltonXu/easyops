#!/usr/bin/env python
# coding:utf8
import os
import logging

from flask import (
    redirect, render_template, send_from_directory,
    url_for, request, session, make_response)

from easyops import db
from easyops import csrf
from easyops.utils import utils
from easyops.controller.hosts.hosts import HostsManager
from easyops.api_v1_0 import api

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_DIR = os.path.join(os.path.dirname(BASE_DIR), "static/server_templates")

@api.route("/manage_host", methods=["GET"])
def manage_host():
    if request.method == "GET":
        hosts = HostsManager(user_id=session.get("user_id"))
        return render_template("manage_host/host.html", hosts_info=hosts.hosts)


@csrf.exempt
@api.route("/host/add", methods=["POST"])
def add_host():
    if request.method == "POST":
        form = request.form
        host_info = form.to_dict()
        hostname = host_info["hostname"]
        group = host_info["group"]
        ipaddress = host_info["ipaddress"]
        port = host_info["port"]
        username = host_info["username"]
        password = host_info["password"]
        user_id = session.get("user_id")
        host_params = {
            "hostname": hostname,
            "group": group,
            "ipaddress": ipaddress,
            "port": port,
            "username": username,
            "password": password,
        }
        if username and ipaddress and hostname and password:
            host = HostsManager(user_id=user_id, ipaddress=ipaddress)
            if host.check_host_exists():
                response = make_response("主机已存在，请添加其他主机", 500)
                return response
            if not host.add_host(**host_params):
                response = make_response("添加主机失败，请重试", 500)
                return response

        return redirect(url_for("api_v1_0.manage_host"))


@csrf.exempt
@api.route("/host/getexcel", methods=["GET"])
def get_excel():
    return send_from_directory(EXCEL_DIR, "servers_example.xlsx", as_attachment=True)


@csrf.exempt
@api.route("/host/batch_add", methods=["POST"])
def add_host_from_excel():
    file = request.files.get("file")
    file_size = request.files.get("filesize")
    upload_filename = file.filename
    save_filepath = os.path.join(EXCEL_DIR, "upload_" + upload_filename)
    user_id = session.get("user_id")
    try:
        file.save(save_filepath)
    except Exception as err:
        return "Save upload file {} failed.".format(upload_filename)
    batch_hosts = utils.insertServersFromExcel(save_filepath)
    host = HostsManager(user_id=user_id)
    import pdb
    pdb.set_trace()
    for k, v in batch_hosts.items():
        if not host.check_host_exists(ipaddress=v[1]):
            host_params = {
                "hostname": v[0],
                "ipaddress": v[1],
                "port": v[2],
                "username": v[3],
                "password": v[4],
                "group": v[5]
            }
            if not host.add_host(**host_params):
                logging.info("Add new %s host failed." % v[1])
                continue
        else:
            logging.warning("主机 %s 已存在" %(v[1]))
            continue

    return redirect(url_for("api_v1_0.manage_host"))
    

@csrf.exempt
@api.route("/host/delete", methods=["POST"])
def delete_host():
    if request.method == "POST":
        form = request.form  
        exec_hosts = [ form.to_dict()[h] for h in form.to_dict() ]
        user_id = session.get("user_id")
        host = HostsManager(user_id=user_id)
        for exec_host in exec_hosts:
            if not host.delete_host(ipaddress=exec_host):
                response = make_response("删除主机失败，请重试", 500)

                return response

        return redirect(url_for("api_v1_0.manage_host"))

@csrf.exempt
@api.route("/host/update", methods=["POST"])
def update_host():
    if request.method == "POST":
        form = request.form
        update_hosts = form.to_dict()
        ipaddress = update_hosts["ipaddress"]
        hostname = update_hosts["hostname"]
        group = update_hosts["group"]
        port = update_hosts["port"]
        username = update_hosts["username"]
        password = update_hosts["password"]
        update_params = {}
        user_id = session.get("user_id")
        if hostname:
            update_params["hostname"] = hostname
        if port:
            update_params["port"] = port
        if username:
            update_params["username"] = username
        if password:
            update_params["password"] = password
        update_params["group"] = group
        host = HostsManager(user_id=user_id, ipaddress=ipaddress)
        if not host.check_host_exists():
            response = make_response("主机不存在", 500)
            return response
        else:
            if not host.update_host(**update_params):
                response = make_response("更新数据信息失败，请重试", 501)
                return response

    return redirect(url_for("api_v1_0.manage_host"))