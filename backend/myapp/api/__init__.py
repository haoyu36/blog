# -*- coding: utf-8 -*-
'''
api: 用于博客请求的 API
admin: 用于管理后台请求的 API
file: 用于文件请求的 API
'''


from flask import Blueprint
from flask_cors import CORS    # Flask-CORS 用于处理跨源资源共享


api = Blueprint('api', __name__)
admin = Blueprint('admin', __name__)
file = Blueprint('file', __name__)

CORS(api)
CORS(admin)
CORS(file)

from . import blog, admins, files
