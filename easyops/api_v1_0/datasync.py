#!/usr/bin/env python
# coding:utf8

from flask import (render_template, request, session)


from easyops import csrf
from easyops.controller.datasync.datasync import DataSyncManager
from easyops.api_v1_0 import api

@csrf.exempt
@api.route("/datasync/", defaults={"path": "", "remote": ""}, methods=["GET", "DELETE", "POST"])
@api.route("/datasync/<string:remote>/", defaults={"path": ""}, methods=["GET", "DELETE", "POST"])
@api.route("/datasync/<string:remote>/<path:path>/", methods=["GET", "DELETE", "POST"])
def remote_home(remote, path):
    user_id = session.get("user_id")
    datasync = DataSyncManager(user_id=user_id, remote_name=remote, remote_path=path)
    if request.method == "POST" or request.method == "DELETE":
        remote_type = request.form.to_dict()["type"]
    else:
        datasync.get_hosts()
        datasync.ipaddress = datasync.hosts[0].ipaddress
        if datasync.check_host_exists():
            remote_type = "sftp"
        else:
            remote_type = "s3"
    datasync.remote_type = remote_type

    if not path:
        path = "/"

    datasync.path = path
    if not remote:
        remote_objs, remote_sftps = datasync.get_all_datasync_remotes()
        return render_template("datasync/sync.html", remote_objs=remote_objs, remote_sftps=remote_sftps)

    datasync.remote_cfg = datasync.get_remote_cfg()
    datasync.remote_name = remote + ":"
    if request.method == "DELETE":
        datasync.delete_remote_file_or_directory()
        prev_path = path[0:path.rfind('/', 1)]
        if path == prev_path:
            path = "/"
        else:
            path = prev_path
        datasync.path = path
        remote_info = datasync.show_directory()
        return render_template("datasync/_file_manager.html",
                                remote=remote_info.get("remote"),
                                path_links=remote_info.get("path_links"),
                                file_list=remote_info.get("file_list"))
    else:
        datasync.path = path
        if datasync.is_directory():
            remote_info = datasync.show_directory()
            return render_template("datasync/_file_manager.html",
                                    remote=remote_info.get("remote"),
                                    path_links=remote_info.get("path_links"),
                                    file_list=remote_info.get("file_list"))
        return datasync.serve_file()