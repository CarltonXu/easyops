import os
import humanfriendly
import json
import tempfile
import logging

from re import findall
from functools import cmp_to_key
from sarge import run, Capture

from flask import (Response, request)

from werkzeug.datastructures import Headers

from easyops.controller.hosts.hosts import HostsManager
from easyops.controller.storages.storages import StoragesManager
from easyops.libs.rclone import rclone
from easyops.utils import utils


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
host_cfg = os.path.join(os.path.dirname(BASE_DIR), "inventory.py")


class DataSyncManager(StoragesManager, HostsManager):
    def __init__(self, user_id=None, host_id=None, remote_cfg=None,
                 remote_type=None, remote_name=None, remote_path=None,
                 path=None):
        StoragesManager.__init__(self, user_id=user_id)
        HostsManager.__init__(self, user_id=user_id)
        self.user_id = user_id
        self.host_id = host_id 
        self.remote_type = remote_type
        self.remote_name = remote_name
        self.remote_cfg = remote_cfg
        self.remote_path = remote_path
        self.path = path
        self.obj_cfg = """[{name}]
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
        self.sftp_cfg_path = os.environ["HOME"] + "/.config/rclone/rclone.conf"
        self.host_cfg = host_cfg
        self.chunk_size = 1000000
    
    def check_storage_exists(self):
        for s in self.storages:
            if self.remote_name == s.name:
                return self.remote_name

        return False

    def get_all_datasync_remotes(self):
        return self.storages, self.hosts

    def generate_temp_remote_cfg(self):
        with tempfile.NamedTemporaryFile(mode='wt', delete=True) as cfg_file:
            cfg_file.write(self.remote_cfg)
            cfg_file.flush()

        return cfg_file.name
    
    def get_remote_path(self):
        if self.remote_type == "sftp":
            self.remote_path = "{}{}".format(self.remote_name, "/" + self.path)
        else:
            self.remote_path = "{}{}".format(self.remote_name, self.path)
        
        return self.remote_path
    
    
    def get_data(self, begin, end):
        # TODO: exponential increase/backoff
        # make this configurable

        self.get_remote_path()
        current_pointer = begin
    
        with tempfile.NamedTemporaryFile(mode='wt', delete=True) as cfg_file:
            cfg_file.write(self.remote_cfg)
            cfg_file.flush()
            while current_pointer <= end:
                if current_pointer + self.chunk_size > end:
                    self.chunk_size = end - current_pointer
                elif current_pointer == end:
                    self.chunk_size = 1
    
                # TODO: unsure if the math here is right
                cmd = "rclone cat %s --config %s --offset %s --count %s" %(
                    self.remote_path, cfg_file.name, str(current_pointer),
                    str(self.chunk_size)
                    )

                print(cmd)
                print(begin, end, current_pointer, self.chunk_size)
                current_pointer += self.chunk_size
                p = run(cmd, stdout=Capture(), async_=False)
                data = p.stdout.read(100000)
                while data:
                    print('Read chunk: %d bytes' % (len(data)))
                    yield data
                    data = p.stdout.read(100000)
            cfg_file.close()
    
    def serve_file(self):
        self.get_remote_path()
        file_metadata = rclone.with_config(
            self.remote_cfg).lsjson(
            self.remote_path).get("out")

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
            self.get_data(begin, end),
            status,
            headers=headers,
            mimetype=mime,
            direct_passthrough=True,
        )
        return rsp
    
    def read_sftp_remote_cfg(self):
        with open(self.sftp_cfg_path, 'r') as f:
            sftp_cfg = f.read()
        return sftp_cfg
    
    def delete_sftp_remote(self):
        exec_resp = rclone.with_config("")._execute([
            "rclone", "config", "delete", "%s" % (self.remote_name)
            ])
        if exec_resp.get("code") == 0:
            return exec_resp

        return exec_resp.get("code")

    
    def get_remote_cfg(self):
        if self.remote_type == "sftp":
            remote_data = self.hosts[0]
            if remote_data is not None:
                if rclone.with_config("")._execute([
                    "rclone", "config", "create",
                    "%s"%(remote_data.hostname),
                    "%s"%(self.remote_type),
                    "user=%s"%(remote_data.username),
                    "port=%s"%(remote_data.port),
                    "host=%s"%(remote_data.ipaddress),
                    "pass=%s"%(remote_data.password)
                    ]).get("code") == 0:
                    sftp_cfg = self.read_sftp_remote_cfg()
                    self.delete_sftp_remote()
                    return sftp_cfg
        else:
            remote_data = self.get_storages()
            if remote_data is not None:
                return self.obj_cfg.format(**remote_data[0].__dict__)
    
    
    def is_directory(self):
        self.get_remote_path()
        if rclone.with_config(
            self.remote_cfg).rmdir(
            self.remote_path, flags=["--dry-run"]).get("code") == 0:

            return True
        else:
            return False
    
    def delete_remote_file_or_directory(self):
        self.get_remote_path()
        if self.is_directory():
            exec_code = rclone.with_config(
                self.remote_cfg).rmdir(
                self.remote_path).get("code")
        else:
            exec_code = rclone.with_config(
                self.remote_cfg).delete(
                self.remote_path).get("code")
    
        return exec_code
    
    
    def show_directory(self):
        self.get_remote_path()
        file_list_data = rclone.with_config(
            self.remote_cfg).lsf(
            self.remote_path,
            flags=["--format", "psm"]).get("out").decode()

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
    
        file_list.sort(key=cmp_to_key(utils.sort_directory_list))
    
        path_tokens = self.path.split('/')
        path_links = []
    
        for i, token in enumerate(path_tokens):
            if not self.path == "/":
                token += "/"
            href = '/'.join(path_tokens[0:i+1])
            path_links.append((token, href))
    
        # TODO: show number of items or size?
        return {
            "remote": self.remote_name.split(":")[0],
            "path_links": path_links,
            "file_list": file_list
        }