#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask

from .config import config
from .ext import db
from .index import bp as index
from .api import api, admin


def create_app(config_class='development'):
    '''应用程序创建工厂'''
    # 通过 static_folder 指定静态资源路径
    # 通过 template_folder 指定模板路径
    app = Flask(__name__, static_folder="../../dist/static", template_folder="../../dist")
    app.config.from_object(config[config_class])
    db.init_app(app)
    register_blueprints(app)
    return app


def register_blueprints(app):
    '''
    注册蓝本
    /api 博客API接口
    /admin 管理后台API接口
    '''
    app.register_blueprint(index, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(admin, url_prefix='/admin')
