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

from flask import Blueprint

# 创建蓝图对象
api = Blueprint("api_v1_0", __name__)

# 导入蓝图视图
from easyops.api_v1_0 import index

from easyops.api_v1_0 import auth

from easyops.api_v1_0 import execute

from easyops.api_v1_0 import manage_host

from easyops.api_v1_0 import datasync

from easyops.api_v1_0 import storage

from easyops.api_v1_0 import user
