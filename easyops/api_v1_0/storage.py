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

@api.route("/storage", methods=["GET"])
def storage_manage():
    storages = [{"name": "Google", "type": "Google Driver", "username": "carltonxu", "accesskey": "FdssDcjendnDNSDFsldl", "create_time": "Sun Aug 22 01:20:49 CST 2021"}]
    return render_template("storage/storage.html", storages_info=storages)

@api.route("/storage/type", methods=["POST"])
def get_storage_type():
    form = request.form
    storages_data = form.to_dict()
    storage_type = storages_data.get("storage_type")
    if storage_type == "s3":
        storage_provider = storages_data.get("storage_provider")
        if storage_provider == "Alibaba":
            return render_template("storage/_s3-aliyun.html")
        elif storage_provider == "s3-aws":
            pass
    else:
        response = make_response("暂不支持驱动类型", 500)
        return response

@api.route("/storage/add", methods=["POST"])
def add_storage():
    form = request.form
    storages_data = form.to_dict()
    storage_type = storages_data.get("storage_type")
    if storage_type == "s3":
        storage_provider = storages_data.get("storage_provider")
        return storages_data