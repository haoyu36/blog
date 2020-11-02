# -*- coding: utf-8 -*-
'''
为了方便在配置中切换，使用 Python 类组织多个不同类别的配置
然后通过配置名称获取对应的配置类
'''

import os
from datetime import timedelta


class Config:
    '''基础配置'''
    SQLALCHEMY_RECORD_QUERIES = True    # 用于显式禁用或启用查询记录
    SQLALCHEMY_TRACK_MODIFICATIONS = False    # 禁用跟踪对象的修改并发出信号
    SQLALCHEMY_COMMIT_TEARDOWN = True    # 自动提交
    SECRET_KEY = os.getenv('SECRET_KEY')    # 用于安全签名会话cookie的密钥
    REDIS_URL = 'redis://localhost:6379'


class DevelopmentConfig(Config):
    '''开发使用的配置'''
    FLASK_DEBUG = 1    # 是否启用调试模式
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URI')    # 用于连接的数据库URI
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)    # 设置静态文件缓存过期时间
    TEMPLATES_AUTO_RELOAD = True    # 渲染模版自动加载
    JSON_AS_ASCII = False    # 取消将对象序列化为ASCII编码的JSON
    PER_PAGE = 6
    FILE_PAGE = 6


class ProductionConfig(Config):
    '''生产使用的配置'''
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    PER_PAGE = 10    # 博客分页数
    FILE_PAGE = 15    # 文件分页数


class TestingConfig(Config):
    '''测试使用的配置'''
    TESTING = True    # 启用测试模式
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI')
    PER_PAGE = 6
    FILE_PAGE = 6


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}
