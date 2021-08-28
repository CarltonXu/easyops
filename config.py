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

import redis

class Config(object):
    SECRET_KEY = "XHS0I*Y9dfs9cshd9"
    SQLALCHEMY_DATABASE_URI = "mysql://easyops:easyopsPass@192.168.10.68:3306/easyops"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # This is a sqlite3 db configure section
    #DATABASE = "/Users/CarltonXu/workspace/codes/flask/easyops/instance/easyops.sqlite"
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    SESSION_TYPE = "redis"
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    SESSION_USER_SIGNER = True
    PERMANENT_SESSION_LIFETIME = 86400

class DevelopmentConfig(Config):
    DEBUG = True

class ProductConfig(Config):
    pass

config_map = {
    "develop": DevelopmentConfig,
    "product": ProductConfig
}
