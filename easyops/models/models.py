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
    id = db.Column(db.Integer, primary_key=True, comment="用户ID")
    username = db.Column(db.String(32), unique=True, nullable=False, comment="用户名")
    password_hash = db.Column(db.String(120), nullable=False, comment="密码")
    register_time = db.Column(db.DateTime, default=datetime.now, comment="注册时间")
    is_login = db.Column(db.Boolean, default=False, comment="登录标志位")
    active = db.Column(db.Boolean, default=True, comment="激活状态")
    email = db.Column(db.String(120), comment="邮箱")
    phone = db.Column(db.String(20), comment="手机号")
    phonenumber = db.Column(db.String(11), comment="手机号码")
    sex = db.Column(db.INTEGER, default=1, comment="用户性别（1男 2女 3未知）")
    avatar = db.Column(db.String(100), comment="头像路径")
    

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
    id = db.Column(db.Integer, primary_key=True, comment="主机ID")
    user_id = db.Column(db.ForeignKey("users.id"), comment="关联用户ID")
    hostname = db.Column(db.String(100), comment="主机名称")
    ipaddress = db.Column(db.String(100), comment="IP地址")
    access_type = db.Column(db.Integer, default=1, comment="访问类型 (1密码, 2密钥)")
    port = db.Column(db.Integer, default=22, comment="端口")
    username = db.Column(db.String(100), comment="访问用户名")
    password = db.Column(db.String(100), comment="访问密码")
    group = db.Column(db.String(100), comment="所属组")
    user = db.relationship("Users", uselist=False, backref=backref("ansible_hosts", uselist=True))

class Storages(BaseModel, db.Model):
    __tablename__ = 'storages'
    id = db.Column(db.Integer, primary_key=True, comment="存储ID")
    user_id = db.Column(db.ForeignKey("users.id"), comment="关联用户ID")
    name = db.Column(db.String(100), comment="存储名称")
    type = db.Column(db.String(100), comment="存储类型")
    provider = db.Column(db.String(100), comment="提供商")
    region = db.Column(db.String(100), comment="区域")
    access_key_id = db.Column(db.String(100), comment="访问key")
    secret_access_key = db.Column(db.String(100), comment="访问密钥")
    endpoint = db.Column(db.String(100), comment="访问端点")
    acl = db.Column(db.String(100), comment="访问权限")
    storclass = db.Column(db.String(100), comment="存储提供类型")
    upload_cutoff = db.Column(db.String(100), comment="上传大小")
    chunk_size = db.Column(db.String(100), comment="切分大小")
    upload_checksum = db.Column(db.Boolean, default=False, comment="上传校验")
    user = db.relationship("Users", uselist=False, backref=backref("storages", uselist=True))

class UsersLoginHistory(BaseModel,db.Model):
    __tablename__ = "users_login_history"
    id = db.Column(db.Integer, primary_key=True, comment="主键")
    user_id = db.Column(db.ForeignKey("users.id"), comment="用户id")
    login_time = db.Column(db.DateTime, default=datetime.now, comment="上次登录时间")
    login_ipaddress = db.Column(db.String(30), comment="登录ip")
    login_region = db.Column(db.String(128), comment="登录地址")
    user = db.relationship("Users", uselist=False, backref=backref("users_login_history", uselist=True))