# -*- coding: utf-8 -*-
'''
定义 API 错误响应函数
'''

from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def api_abort(status_code, message=None, **kwargs):
    '''
    :status_code: 错误响应的状态码
    :message: 错误提示信息
    '''
    payload = {
        'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error'),
        'status_code': status_code
    }
    if message:
        payload['message'] = message
    response = jsonify(payload, **kwargs)
    response.status_code = status_code
    return response
