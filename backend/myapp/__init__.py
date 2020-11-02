# -*- coding: utf-8 -*-
'''
应用程序创建工厂
'''

from flask import Flask

from myapp.config import config
from myapp.index import index
from myapp.api import api, admin, file
from myapp.libs.ext import db
from myapp.libs.errors import api_abort


def create_app(config_class='development'):
    # 通过 static_folder 指定静态资源路径
    # 通过 template_folder 指定模板路径
    app = Flask(__name__, static_folder="../../dist/static", template_folder="../../dist")
    app.config.from_object(config[config_class])    # 读取当前环境配置配置
    db.init_app(app)
    register_blueprints(app)
    register_errors(app)
    return app


def register_blueprints(app):
    '''注册程序蓝本'''
    app.register_blueprint(index, url_prefix='/')
    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(file, url_prefix='/file')


def register_errors(app):
    '''全局错误处理'''
    @app.errorhandler(401)
    @app.errorhandler(404)
    @app.errorhandler(500)
    def error(e):
        return api_abort(e.code)
