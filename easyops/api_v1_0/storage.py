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
from easyops.models import Storages
from easyops.api_v1_0 import api

@api.route("/storage", methods=["GET"])
def storage_manage():
    storages = Storages.query.all()
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
        elif storage_provider == "TencentCOS":
            return render_template("storage/_s3-tencent.html")
        elif storage_provider == "AWS":
            return render_template("storage/_s3-aws.html")
    else:
        response = make_response("暂不支持驱动类型", 500)
        return response

@api.route("/storage/add", methods=["POST"])
def add_storage():
    form = request.form
    storages_data = form.to_dict()
    name = storages_data.get("storage_name")
    storage_type = storages_data.get("storage_type")
    provider = storages_data.get("storage_provider")
    region = storages_data.get("region")
    access_key_id = storages_data.get("access_key_id")
    secret_access_key = storages_data.get("secret_access_key")
    endpoint = storages_data.get("endpoint")
    storacl = storages_data.get("storage_acl")
    storclass = storages_data.get("storage_class")
    upload_cutoff_unit = storages_data.get("storage_upload_cutoff_unit")
    upload_cutoff = storages_data.get("storage_upload_cutoff") + upload_cutoff_unit
    chunk_size_unit = storages_data.get("storage_chunk_size_unit")
    chunk_size = storages_data.get("storage_chunk_size") + chunk_size_unit
    checksum = storages_data.get("storage_checksum").upper()
    
    if storage_type == "s3":
        storage = Storages(
            name=name,
            type=storage_type,
            provider=provider,
            region=region,
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            endpoint=endpoint,
            acl=storacl,
            storclass=storclass,
            upload_cutoff=upload_cutoff,
            chunk_size=chunk_size,
            upload_checksum=bool(checksum)
        )

        try:
            if Storages.query.filter_by(name=name).first() or Storages.query.filter_by(access_key_id=access_key_id).first():
                response = make_response("已经存在的存储", 500)
                return response
            db.session.add(storage) 
            db.session.commit()
        except Exception as err:
            logging.error(err)
            response = make_response("添加主机失败，请重试", 500)
            return response
        return redirect(url_for("api_v1_0.storage_manage"))

@api.route("/storage/delete", methods=["POST"])
def delete_storage():
    form = request.form
    storages = [ form.to_dict()[h] for h in form.to_dict() ]
    for stor_name in storages:
        try:
            del_stor = Storages.query.filter_by(name=stor_name).first()
            db.session.delete(del_stor)
            db.session.commit()
            logging.debug("Delete %s storage successful." % stor_name)
        except Exception as err:
            logging.error(err)
            response = make_response("操作数据库删除主机失败", 500)
            return response
        return redirect(url_for("api_v1_0.storage_manage"))