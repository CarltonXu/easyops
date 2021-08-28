#!/usr/bin/env python
# coding:utf8
import os
import time
import logging
from easyops.utils import utils

from flask import (
    Blueprint, flash, redirect, render_template, url_for, request, session)

from easyops import constants, db
from easyops.libs.ansible.api import Task
from easyops.models import AnsibleHosts 
from easyops.api_v1_0 import api

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
host_cfg = os.path.join(os.path.dirname(BASE_DIR), "inventory.py")

@api.route("/datasync", methods=["GET", "POST"])
def sync():
    return render_template("datasync/sync.html")