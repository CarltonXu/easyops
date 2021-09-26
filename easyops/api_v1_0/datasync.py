#!/usr/bin/env python
# coding:utf8
import os
import time
import logging
import humanfriendly
import json
import tempfile

from re import findall
from functools import cmp_to_key
from sarge import run, Capture

from flask import (
    Blueprint, flash, Response, redirect,
    render_template, url_for, request, session)

from werkzeug.datastructures import Headers

from easyops import constants, db
from easyops.utils import utils
from easyops.libs.ansible.api import Task
from easyops.libs.rclone import rclone
from easyops.models import AnsibleHosts
from easyops.models import Storages
from easyops.api_v1_0 import api

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
host_cfg = os.path.join(os.path.dirname(BASE_DIR), "inventory.py")

obj_cfg = """[{name}]
type = {type}
provider = {provider}
region = {region}
access_key_id = {access_key_id}
secret_access_key = {secret_access_key}
storage_class = {storclass}
endpoint = {endpoint}
acl = {acl}
upload_cutoff = {upload_cutoff}
chunk_size = {chunk_size}
upload_checksum = {upload_checksum}
"""
sftp_cfg_path = os.environ['HOME'] + "/.config/rclone/rclone.conf"

def generate_temp_remote_cfg(remote_cfg):

    with tempfile.NamedTemporaryFile(mode='wt', delete=True) as cfg_file:
        cfg_file.write(remote_cfg)
        cfg_file.flush()
    return cfg_file.name

def sort_directory_list(a, b):
    if a['is_dir'] != b['is_dir']:
        if a['is_dir']:
            return -1
        else:
            return 1
    if a['name'] > b['name']:
        return 1
    elif a['name'] < b['name']:
        return -1
    return 0

def get_data(remote_cfg, remote_name, remote_type, path, begin, end):
    # TODO: exponential increase/backoff
    # make this configurable
    if remote_type == "sftp":
        remote_path = "{}{}".format(remote_name, "/" + path)
    else:
        remote_path = "{}{}".format(remote_name, path)
    chunk_size = 1000000
    current_pointer = begin

    while current_pointer <= end:
        if current_pointer + chunk_size > end:
            chunk_size = end - current_pointer
        elif current_pointer == end:
            chunk_size = 1

        with tempfile.NamedTemporaryFile(mode='wt', delete=True) as cfg_file:
            # TODO: unsure if the math here is right
            cmd = "rclone cat %s --config %s --offset %s --count %s" %(remote_path, cfg_file.name, str(current_pointer), str(chunk_size))
            print(cmd)
            print(begin, end, current_pointer, chunk_size)
            current_pointer += chunk_size
            cfg_file.write(remote_cfg)
            cfg_file.flush()
            p = run(cmd, stdout=Capture(), async_=False)
            data = p.stdout.read(100000)
            while data:
                print('Read chunk: %d bytes' % (len(data)))
                yield data
                data = p.stdout.read(100000)
            cfg_file.close()

def serve_file(remote_cfg, remote_name, remote_type, path):
    if remote_type == "sftp":
        remote_path = "{}{}".format(remote_name, "/" + path)
    else:
        remote_path = "{}{}".format(remote_name, path)
    file_metadata = rclone.with_config(remote_cfg).lsjson(remote_path).get("out")
    file_json = json.loads(file_metadata)[0]

    headers = Headers()

    status = 200
    size = file_json['Size']
    mime = file_json['MimeType']
    begin = 0
    end = size - 1

    if request.headers.has_key("Range"):
        status = 206
        ranges = findall(r"\d+", request.headers["Range"])
        begin = int(ranges[0])
        if len(ranges) > 1:
            end = int(ranges[1])

        # TODO: Is the math here correct?
        headers.add('Content-Range', 'bytes %s-%s/%s' % (begin, end, size))

    headers.add('Content-Length', end-begin + 1)
    headers.add('Accept-Ranges', 'bytes')

    rsp = Response(
        get_data(remote_cfg, remote_name, remote_type, path, begin, end),
        status,
        headers=headers,
        mimetype=mime,
        direct_passthrough=True,
    )
    return rsp

def read_sftp_remote_cfg(cfg_path):
    with open(cfg_path, 'r') as f:
        sftp_cfg = f.read()
    os.remove(cfg_path)
    return sftp_cfg

def get_remote_cfg(remote_name, remote_type=""):
    if remote_type == "sftp":
        if AnsibleHosts.query.filter_by(hostname=remote_name).first():
            remote_data = AnsibleHosts.query.filter_by(hostname=remote_name).first()
            if rclone.with_config("")._execute([
                "rclone", "config", "create",
                "%s"%(remote_data.hostname),
                "%s"%(remote_type),
                "user=%s"%(remote_data.username),
                "port=%s"%(remote_data.port),
                "host=%s"%(remote_data.ipaddress),
                "pass=%s"%(remote_data.password)
                ]).get("code") == 0:
                sftp_cfg = read_sftp_remote_cfg(sftp_cfg_path)
                return sftp_cfg
    else:
        if Storages.query.filter_by(name=remote_name).first():
            remote_data = Storages.query.filter_by(name=remote_name).first()
            return obj_cfg.format(**remote_data.__dict__)

def show_all_remotes():
    remotes_object_storages = Storages.query.all()
    remotes_sftp_storages = AnsibleHosts.query.all()
    return remotes_object_storages, remotes_sftp_storages

def is_directory(remote_cfg, remote_name, remote_type, path):
    if remote_type == "sftp":
        remote_path = "{}{}".format(remote_name, "/" + path)
    else:
        remote_path = "{}{}".format(remote_name, path)
    if rclone.with_config(remote_cfg).rmdir(remote_path,flags=["--dry-run"]).get("code") == 0:
        return True
    else:
        return False

def show_directory(remote_cfg, remote_name, remote_type, path):
    if remote_type == "sftp":
        remote_path = "{}{}".format(remote_name, "/" + path)
    else:
        remote_path = "{}{}".format(remote_name, path)
    file_list_data = rclone.with_config(remote_cfg).lsf(remote_path, flags=["--format", "psm"]).get("out").decode()
    file_list = []
    for item in file_list_data.split('\n'):
        if not item:
            continue
        item_tokens = item.strip().split(';')
        file_list.append({
            'name': item_tokens[0],
            'size': item_tokens[1],
            'type': item_tokens[2],
            'is_dir': item_tokens[2] == 'inode/directory',
            'human_size': humanfriendly.format_size(int(item_tokens[1]))
        })

    file_list.sort(key=cmp_to_key(sort_directory_list))

    path_tokens = path.split('/')
    path_links = []

    for i, token in enumerate(path_tokens):
        if not path == "/":
            token += "/"
        href = '/'.join(path_tokens[0:i+1])
        path_links.append((token, href))

    # TODO: show number of items or size?
    return render_template('datasync/_file_manager.html', remote=remote_name.split(":")[0], path_links=path_links, file_list=file_list)


@api.route("/datasync/",  defaults={"path": "", "remote": ""}, methods=["GET", "POST"])
@api.route("/datasync/<string:remote>/",  defaults={"path": ""}, methods=["GET", "POST"])
@api.route("/datasync/<string:remote>/<path:path>/", methods=["GET", "POST"])
def remote_home(remote, path):
    if request.method == "POST":
        remote_type = request.form.to_dict()["type"]
    else:
        if AnsibleHosts.query.filter_by(hostname=remote).first():
            remote_type = "sftp"
        else:
            remote_type = "s3"
    if not path:
        path = "/"
    if not remote:
        remote_objs, remote_sftps = show_all_remotes()
        return render_template("datasync/sync.html", remote_objs=remote_objs, remote_sftps=remote_sftps)
    remote_cfg = get_remote_cfg(remote, remote_type)
    remote = remote + ":"
    if is_directory(remote_cfg, remote, remote_type, path):
        return show_directory(remote_cfg, remote, remote_type, path)
    return serve_file(remote_cfg, remote, remote_type, path)