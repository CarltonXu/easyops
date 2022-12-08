#!/usr/bin/env python
# coding:utf8
import os
import logging

from flask import redirect, render_template, url_for, request, session, make_response

from easyops import csrf
from easyops.controller.storages.storages import StoragesManager
from easyops.api_v1_0 import api

@csrf.exempt
@api.route("/storage", methods=["GET"])
def storage_manage():
    user_id = session.get("user_id")
    storages = StoragesManager(user_id=user_id)
    return render_template("storage/storage.html", storages_info=storages.storages)

@csrf.exempt
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

@csrf.exempt
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
    user_id = session.get("user_id")
    storages = StoragesManager(user_id=user_id, storage_name=name, access_key_id=access_key_id)

    storage_args = {
        "name": name,
        "type": storage_type,
        "provider": provider,
        "region": region,
        "access_key_id": access_key_id,
        "secret_access_key": secret_access_key,
        "endpoint": endpoint,
        "acl": storacl,
        "storclass": storclass,
        "upload_cutoff": upload_cutoff,
        "chunk_size": chunk_size,
        "upload_checksum": bool(checksum),
        "user_id": user_id
    }

    if storage_type == "s3":
        if storages.exists_storage():
            response = make_response("已经存在的存储", 500)
        if storages.create_storage(**storage_args):
            return redirect(url_for("api_v1_0.storage_manage"))
        else:
            response = make_response("添加主机失败，请重试", 500)
        return response

@csrf.exempt
@api.route("/storage/delete", methods=["POST"])
def delete_storage():
    form = request.form
    user_id = session.get("user_id")
    storages = [ form.to_dict()[h] for h in form.to_dict() ]
    for stor_name in storages:
        try:
            storage = StoragesManager(user_id=user_id, storage_name=stor_name)
            if storage.delete_storage()["code"] == 0:
                logging.debug("Delete %s storage successful." % stor_name)
        except Exception as err:
            logging.error(err)
            response = make_response("操作数据库删除主机失败", 500)
            return response
        return redirect(url_for("api_v1_0.storage_manage"))