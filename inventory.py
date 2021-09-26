#!/usr/bin/env python
# coding:utf8

import json
import logging

from sqlalchemy import create_engine
from config import Config
from optparse import OptionParser

try:
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
except Exception as err:
    logging.error(err)

def query_ansible_hosts():
    """
    此函数作为调用时会自动从数据库获取所有主机信息，并传递给ansible作为动态inventory文件
    
    :return: {
        "all": {
            "children": [
                "dev",
                "prod"
            ]
        },
        "_meta": {
            hostvars: {
                "192.168.10.68": {
                    "ansible_user": "root",
                    "ansible_password": "root123.",
                }
            }
        },
        "dev": {
            "hosts": [
                "192.168.10.68",
                "192.168.10.69"
            ]
        },
        "prod": {
            "hosts": [
                "192.168.10.201",
                "192.168.10.202"
            ]
        }
    }
    """
    hosts = {}
    hostvars = {}
    try:
        remote_hosts = engine.execute("select * from ansible_hosts").fetchall()
    except Exception as err:
        logging.error(err)
    groups = ([i.group for i in remote_hosts if i.group != u""])
    for host in remote_hosts:
        hostvars[host.ipaddress] = {
            "ansible_user": host.username,
            "ansible_password": host.password,
            "ansible_port": host.port
            }
    hosts["all"] = {"children": groups}
    hosts["_meta"] = {"hostvars": hostvars}
    hosts["hosts"] = [host.ipaddress for host in remote_hosts if host.group == ""]
    for group in groups:
        hosts[group] = {}
        hosts[group]["hosts"] = []
        for host in remote_hosts:
            if host.group == group:
                hosts[group]["hosts"].append(host.ipaddress)

    return json.dumps(hosts,indent=3)

def main():
    parse = OptionParser()
    parse.add_option("-l", "--list", action="store_true", dest="list", default=False)
    (option, arges) = parse.parse_args()
    if option.list:
        ansible_hosts = query_ansible_hosts()
        print(ansible_hosts)
    else:
        print("others params.")

if __name__ == "__main__":
    main()