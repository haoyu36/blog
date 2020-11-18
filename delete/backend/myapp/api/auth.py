#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from . import admin as bp
from .errors import error_response
from ..models import AdminUser


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(username, password):
    '''检查用户名和密码'''
    user = AdminUser.query.filter_by(username=username).first()
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    '''获取jwt令牌，需传入认证用户及密码'''
    token = g.current_user.get_jwt()
    return jsonify({'token': token})


@basic_auth.error_handler
def basic_auth_error():
    '''用于在认证失败返回错误响应'''
    return error_response(401)


@token_auth.verify_token
def verify_token(token):
    '''检查用户请求是否有token，且在有效期内'''
    g.current_user = AdminUser.verify_jwt(token) if token else None
    return g.current_user is not None


@token_auth.error_handler
def token_auth_error():
    '''Token Auth 认证失败返回错误响应'''
    return error_response(401)
