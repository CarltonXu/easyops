# vim: tabstop=4 shiftwidth=4 softtabstop=4
#
# Copyright 2019 OneProCloud (Shanghai) Ltd
#
# Authors: XuXingZhuang xuxingzhuang@oneprocloud.com
#
# Copyright (c) 2019. This file is confidential and proprietary.
# All Rights Reserved, OneProCloud (Shanghai) Ltd(http://www.oneprocloud.com).)
#
# coding:utf-8
#

import os
import redis

from flask import Flask
from config import config_map
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import CSRFProtect

# import sqlite3 db
# from easyops.database import db

# initialize sqlalchemy database object
db = SQLAlchemy()


# create redis connect object
redis_store = None

def create_app(config_name):
    """
    Create flask application object
    :param config_name: str config params module name ("develop", "product")
    :return:
    """

    app = Flask(__name__, instance_relative_config=True)

    # initialize config modules class
    config_class = config_map.get(config_name)
    app.config.from_object(config_class)

    # use init_app initialize db
    db.init_app(app)

    # initialize redis database
    global redis_store
    redis_store = redis.StrictRedis(host=config_class.REDIS_HOST,
                                    port=config_class.REDIS_PORT)

    # use flask-session, save session data into redis databases.
    Session(app)

    # add flask csrf protect
    # csrf = CSRFProtect(app)

    # register blueprint
    from easyops import api_v1_0
    app.register_blueprint(api_v1_0.api, url_prefix="/api/v1.0")

    return app
