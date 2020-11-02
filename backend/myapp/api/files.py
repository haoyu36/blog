# -*- coding: utf-8 -*-
'''
此模块提供文件API接口
'''

from flask import jsonify, request

from .schemas import files_schema, file_schema
from .auth import token_auth
from myapp.api import file as bp

from myapp.models import Files
from myapp.libs.file_cos import upload_cos
from myapp.libs.mc import cache
from myapp.libs.utils import humanize_bytes, get_md


MC_KEY_ONE_PAGE_FILES = 'files:{page}'
MC_KEY_HOMEFILE = 'files:homefile'


@bp.route('/<int:file_id>')
def get_file(file_id):
    '''返回指定文件'''
    file = Files.get_or_404(file_id)
    schema = file_schema(file)
    return jsonify(schema)


@bp.route('/page/<int:page>')
@cache(MC_KEY_ONE_PAGE_FILES)
def get_files(page):
    '''返回所文件，分页返回'''
    files = Files.get_files(page)
    schema = files_schema(files)
    return jsonify(schema)


@bp.route('/homefile')
@cache(MC_KEY_HOMEFILE)
def homefile():
    '''返回首页预览的3篇博客'''
    files = Files.query.order_by(Files.created_at.desc()).limit(3)
    files_lst = [file_schema(file) for file in files]
    return jsonify({'files': files_lst})


@bp.route('/upload', methods=['POST'])
@token_auth.login_required
def files_upload():
    f = request.files.get('file')
    pic = request.files.get('pic')
    if not f or not pic:
        return jsonify({'message': '请添加上传的文件'})
    filename = f.filename
    if Files.query.filter_by(filename=filename).first():
        return jsonify({'message': '上传文件已存在'})

    pic_md = get_md(pic.filename)
    upload_cos(pic, pic_md)

    file_md = get_md(f.filename)
    upload_cos(f, file_md)
    f.seek(0)
    size = humanize_bytes(f)

    author = request.form.get('author')
    intro = request.form.get('intro')

    Files.create(filename=filename, file_md=file_md, pic_md=pic_md,
                 author=author, size=size, intro=intro)

    return jsonify({'message': '文件上传成功'})


@bp.route('/delete/<int:file_id>')
@token_auth.login_required
def files_delete(file_id):
    obj = Files.get_or_404(file_id)
    obj.delete()
    return jsonify({'message': '文件删除成功'})


@bp.route('/update', methods=['POST'])
@token_auth.login_required
def files_update():
    data = request.get_json()
    file_id = data.get('id')
    obj = Files.get_or_404(file_id)
    obj.update(author=data.get('author'), intro=data.get('intro'))
    return jsonify({'message': '文件更新成功'})


@bp.route('/<int:file_id>/status', methods=['POST', 'DELETE'])
@token_auth.login_required
def status(file_id):
    file = Files.get_or_404(file_id)
    if request.method == 'POST':
        file.update(status=file.STATUS_ONLINE)
    elif request.method == 'DELETE':
        file.update(status=file.STATUS_UNPUBLISHED)
    return jsonify({'message': '文件状态更新成功'})
