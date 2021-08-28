# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2019 OneProCloud (Shanghai) Ltd
#
# Authors: XuXingZhuang xuxingzhuang@oneprocloud.com
#
# Copyright (c) 2019. This file is confidential and proprietary.
# All Rights Reserved, OneProCloud (Shanghai) Ltd(http://www.oneprocloud.com).)
#!/usr/bin/env python
# coding=utf-8
#

from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from easyops import db

class BaseModel(object):
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Users(BaseModel, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    @property
    def password(self):
        """获取password属性时被调用"""
        raise AttributeError('不可读')

    @password.setter
    def set_password(self, passwd):
        """设置password属性时被调用，设置密码加密"""
        self.password_hash = generate_password_hash(passwd)
    
    def check_password(self, passwd):
        """检查密码的正确性"""
        return check_password_hash(self.password_hash, passwd)

    def to_dict(self):
        """将对象转换成字典数据"""
        area_dict = {
            "aid": self.id,
            "aname": self.name
        }
        return area_dict


class AnsibleHosts(BaseModel, db.Model):
    __tablename__ = "ansible_hosts"
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(100))
    ipaddress = db.Column(db.String(100))
    port = db.Column(db.Integer, default=22)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    group = db.Column(db.String(100))