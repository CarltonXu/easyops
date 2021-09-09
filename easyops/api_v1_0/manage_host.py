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
from easyops.models import AnsibleHosts
from easyops.api_v1_0 import api

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_DIR = os.path.join(os.path.dirname(BASE_DIR), "static/server_templates")


@api.route("/manage_host", methods=["GET"])
def manage_host():
    if request.method == "GET":
        hosts_info = AnsibleHosts.query.all()
        return render_template("manage_host/host.html", hosts_info=hosts_info)


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
        if username and ipaddress and hostname and password:
            query_ipaddr = AnsibleHosts.query.filter_by(ipaddress=ipaddress).first()
            if query_ipaddr is None:
                try:
                    add_host = AnsibleHosts(
                        hostname=hostname,
                        ipaddress=ipaddress,
                        port=port,
                        username=username,
                        password=password,
                        group=group
                    )
                    db.session.add(add_host)
                    db.session.commit()
                except Exception as err:
                    logging.error(err)
                    response = make_response("添加主机失败，请重试", 500)
                return redirect(url_for("api_v1_0.manage_host"))
            else:
                response = make_response("主机已经存在, 请添加其他主机", 500)
            return response
        return redirect(url_for("api_v1_0.manage_host"))


@api.route("/host/getexcel", methods=["GET"])
def get_excel():
    return send_from_directory(EXCEL_DIR, "servers_example.xlsx", as_attachment=True)


@api.route("/host/batch_add", methods=["POST"])
def add_host_from_excel():
    file = request.files.get("file")
    file_size = request.files.get("filesize")
    upload_filename = file.filename
    save_filepath = os.path.join(EXCEL_DIR, "upload_" + upload_filename)
    try:
        file.save(save_filepath)
    except Exception as err:
        return "Save upload file {} failed.".format(upload_filename)
    batch_hosts = utils.insertServersFromExcel(save_filepath)
    for k, v in batch_hosts.items():
        query_ipaddr = AnsibleHosts.query.filter_by(ipaddress=v[1]).first()
        if query_ipaddr is None:
            try:
                add_host = AnsibleHosts(
                    hostname=v[0],
                    ipaddress=v[1],
                    port=v[2],
                    username=v[3],
                    password=v[4],
                    group=v[5]
                )
                db.session.add(add_host)
                db.session.commit()
            except Exception as err:
                logging.error(err)
        else:
            logging.warning("主机 %s 已存在" %(query_ipaddr))
            continue

    return redirect(url_for("api_v1_0.manage_host"))
    

@api.route("/host/delete", methods=["POST"])
def delete_host():
    if request.method == "POST":
        form = request.form  
        exec_hosts = [ form.to_dict()[h] for h in form.to_dict() ]
        for host in exec_hosts:
            try:
                del_host = AnsibleHosts.query.filter_by(ipaddress=host).first()
                db.session.delete(del_host)
                db.session.commit()
                logging.debug("Delete %s hosts successful." % host)
            except Exception as err:
                logging.error(err)

        return redirect(url_for("api_v1_0.manage_host"))

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
        if hostname:
            update_params["hostname"] = hostname
        if port:
            update_params["port"] = port
        if username:
            update_params["username"] = username
        if password:
            update_params["password"] = password
        update_params["group"] = group
        try:
            upd_host = AnsibleHosts.query.filter_by(ipaddress=ipaddress).update(update_params)
            db.session.commit()
        except Exception as err:
            logging.error(err)
        return redirect(url_for("api_v1_0.manage_host"))