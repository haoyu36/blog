# -*- coding: utf-8 -*-
'''
先要进行 Basic Auth 认证， 如果用户名和密码正确，则生成 token 并以 JSON 格式返回
'''

from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth

from myapp.api import admin as bp
from myapp.libs.errors import api_abort
from myapp.models import AdminUser


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
    '''认证失败时返回错误响应'''
    return api_abort(401, message='用户名或密码错误')


@token_auth.verify_token
def verify_token(token):
    '''检查用户是否是管理员'''
    g.current_user = AdminUser.verify_jwt(token) if token else None
    if not g.current_user:
        return False
    return g.current_user.is_admin == 1


@token_auth.error_handler
def token_auth_error():
    '''Token Auth 认证失败返回错误响应'''
    return api_abort(401, message='token 无效或已过期')
