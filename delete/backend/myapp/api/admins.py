#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
此模块提供管理后台API接口
"""


from flask import jsonify, request
from flask.views import MethodView

from . import admin as bp
from .auth import token_auth
from .utils import upload_cos, delete_cos, humanize_bytes
from .schemas import posts_schema, files_schema
from ..models import Post, Tag, Files


class PostAdminAPI(MethodView):
    '''获取，修改，删除一篇博客'''
    decorators = [token_auth.login_required]

    def get(self, post_id):
        p = Post.get_or_404(post_id)
        schema = {
            'id': p.id,
            'title': p.title,
            'intro': p.intro,
            'body': p.body,
            'html_body': p.html_body,
            }
        return jsonify(schema)

    def put(self, post_id):
        post = Post.get_or_404(post_id)
        if request.get_json():
            data = request.get_json()
        else:
            data = request.form
        ok, post = Post.create_or_update(**data)
        return '', 204

    def delete(self, post_id):
        post = Post.get_or_404(post_id)
        post.delete()
        return '', 204


class PostTagAPI(MethodView):
    '''获取，修改一篇博客的标签'''
    decorators = [token_auth.login_required]

    def get(self, post_id):
        post = Post.get_or_404(post_id)
        tag_lst = [t.name for t in post.tags]
        return jsonify({'tags': tag_lst})

    def post(self, post_id):
        post = Post.get_or_404(post_id)
        tag_lst = list(request.get_json()['tags'])
        post.update_tags(tag_lst)
        return '', 204


bp.add_url_rule('/post/<int:post_id>', view_func=PostAdminAPI.as_view('post_edit'),
                methods=['GET', 'PUT', 'DELETE'])

bp.add_url_rule('/posttag/<int:post_id>', view_func=PostTagAPI.as_view('posttag_edit'),
                methods=['GET', 'POST'])


@bp.route('/tags')
def get_tags():
    '''以列表形式获取标签列表，用于前端选择'''
    lst = Tag.get_all_tag()
    return jsonify({'tags': lst})


@bp.route('/post/write',  methods=['POST'])
@token_auth.login_required
def post_write():
    '''上传新博客'''
    if request.get_json():
        data = request.get_json()
    else:
        data = request.form
    ok, post = Post.create_or_update(**data)
    return '', 204


@bp.route('/posts/<int:page>')
def posts_admin(page):
    '''获取所有博客，分页展示'''
    posts = Post.get_posts(page)
    schema = posts_schema(posts)
    return jsonify(schema)


@bp.route('/upload', methods=['POST'])
def files_upload():
    f = request.files.get('file')
    if Files.query.filter_by(name=f.filename).first():
        return '上传文件已存在'
    upload_cos(f, f.filename)
    f.seek(0)
    size = humanize_bytes(f)
    Files.create(name=f.filename, size=size)
    return "上传成功"


@bp.route('/delete/<int:file_id>')
def files_delete(file_id):
    obj = Files.query.get(file_id)
    obj.delete()
    delete_cos(obj.name)
    return '删除成功'


@bp.route('/files')
def get_files():
    '''获取所有文件信息'''
    file_lst = files_schema()
    return jsonify({'files': file_lst})
