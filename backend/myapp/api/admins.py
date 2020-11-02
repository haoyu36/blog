# -*- coding: utf-8 -*-
'''
此模块提供管理后台API接口
'''

from flask import jsonify, request

from .auth import token_auth
from myapp.api import admin as bp
from myapp.models import Post


@bp.route('/ping')
@token_auth.login_required
def ping():
    '''测试用户权限'''
    return jsonify({'message': 'pong'})


@bp.route('/post/<int:post_id>/status', methods=['POST', 'DELETE'])
@token_auth.login_required
def status(post_id):
    '''更新博客的状态'''
    post = Post.get_or_404(post_id)
    if request.method == 'POST':
        post.update(status=Post.STATUS_ONLINE)
    elif request.method == 'DELETE':
        post.update(status=Post.STATUS_UNPUBLISHED)
    return jsonify({'message': '博客状态更新成功'})


@bp.route('/post', methods=['POST'])
@token_auth.login_required
def update_post():
    '''创建或更新一篇博客'''
    data = request.get_json()
    tags = data.pop('tag_lst')
    data['tags'] = list(tags) if tags else []
    Post.create_or_update(**data)
    return jsonify({'message': '博客创建或更新成功'})


@bp.route('/post/<int:post_id>', methods=['DELETE'])
@token_auth.login_required
def delete(post_id):
    '''删除一篇博客'''
    post = Post.get_or_404(post_id)
    post.delete()
    return jsonify({'message': '博客删除成功'})
