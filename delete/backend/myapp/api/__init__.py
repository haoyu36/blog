#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
api: 用于博客请求的 API
admin: 用于管理后台请求的 API
'''

from flask import Blueprint
from flask_cors import CORS


api = Blueprint('api', __name__)
admin = Blueprint('admin', __name__)


CORS(api)
CORS(admin)


from . import resources, admins
