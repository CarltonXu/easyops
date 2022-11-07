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
from sqlalchemy.orm import backref

class BaseModel(object):
    create_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)


class Users(BaseModel, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    register_time = db.Column(db.DateTime, default=datetime.now)
    is_login = db.Column(db.Boolean, default=False)

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

class Storages(BaseModel, db.Model):
    __tablename__ = 'storages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    type = db.Column(db.String(100))
    provider = db.Column(db.String(100))
    region = db.Column(db.String(100))
    access_key_id = db.Column(db.String(100))
    secret_access_key = db.Column(db.String(100))
    endpoint = db.Column(db.String(100))
    acl = db.Column(db.String(100))
    storclass = db.Column(db.String(100))
    upload_cutoff = db.Column(db.String(100))
    chunk_size = db.Column(db.String(100))
    upload_checksum = db.Column(db.Boolean, default=False)

class UsersLoginHistory(BaseModel,db.Model):
    __tablename__ = "users_login_history"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    user_id = db.Column(db.ForeignKey("users.id"), comment="用户id")
    login_time = db.Column(db.DateTime, default=datetime.now, comment="上次登录时间")
    login_ipaddress = db.Column(db.String(30), comment="登录ip")
    login_region = db.Column(db.String(30), comment="登录地址")
    user = db.relationship("Users", uselist=False, backref=backref("users_login_history", uselist=True))