#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import render_template
from flask.blueprints import Blueprint


bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    '''返回博客主页'''
    return render_template('index.html')


@bp.route('/admin')
def admin():
    '''返回管理后台主页'''
    return render_template('admin.html')
