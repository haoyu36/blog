# -*- coding: utf-8 -*-
'''
项目路由入口，返回 SPA 页面
'''

from flask import render_template, jsonify
from flask.blueprints import Blueprint


index = Blueprint('index', __name__)


@index.route('/ping')
def ping():
    '''测试后端路由'''
    return jsonify({'message': 'hello'})


@index.route('/')
def blog():
    '''返回博客主页'''
    return render_template('index.html')


@index.route('/admin')
def admin():
    '''返回管理后台主页'''
    return render_template('admin.html')


@index.route('/jianli')
def jianli():
    '''个人简历，不集成到博客中'''
    return render_template('jianli.html')
