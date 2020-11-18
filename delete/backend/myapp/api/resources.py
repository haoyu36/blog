#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
此模块提供博客API接口
"""

from flask import jsonify, url_for
from sqlalchemy import extract

from . import api as bp
from .utils import get_url
from .schemas import post_schema, posts_schema, tags_schema, files_schema
from ..models import Post, PostTag
from ..models.mc import cache


MC_KEY_POSTS_BY_SEARCH = 'posts:post_search'
MC_KEY_POSTS_BY_ARCHIVES = 'posts:post_arch'
MC_KEY_FILES = 'files:all_files'


@bp.route('/')
def index():
    '''API版本及相关信息'''
    return jsonify({
        "api_version": "1.0",
        "website": "http://haoyu36.cn",
        "api_base_url": url_for('.index', _external=True),
    })


@bp.route('/post/<int:post_id>')
def get_post(post_id):
    '''返回单篇博客'''
    post = Post.get_or_404(post_id)
    schema = post_schema(post)
    return jsonify(schema)


@bp.route('/posts/<int:page>')
def get_posts(page):
    '''返回所有博客，分页返回'''
    posts = Post.get_posts(page)
    schema = posts_schema(posts, 'api.get_posts')
    return jsonify(schema)


@bp.route('/tags/<int:tag_id>/<int:page>')
def tag_posts(tag_id, page):
    '''返回指定标签下所有博客，分页返回'''
    posts = PostTag.get_posts_by_tag(tag_id, page)
    schema = posts_schema(posts, 'api.tag_posts', tag_id=tag_id)
    return jsonify(schema)


@bp.route('/tags')
def tags():
    '''返回所有标签相关信息'''
    tag_lst = tags_schema()
    return jsonify({'tags': tag_lst})


@bp.route('/search')
@cache(MC_KEY_POSTS_BY_SEARCH)
def search():
    '''返回所有博客相关信息，用于前端搜索'''
    posts = Post.query.all()
    posts_lst = [post_schema(post) for post in posts]
    return jsonify({'posts': posts_lst})


month_lst = ['一月', '二月', '三月', '四月', '五月', '六月',
             '七月', '八月', '九月', '十月', '十一月', '十二月']


@bp.route('/archives')
@cache(MC_KEY_POSTS_BY_ARCHIVES)
def archives():
    '''用于归档页面，按月份排序'''
    post_lst = []
    for i in range(12, 0, -1):
        mon_lst = []
        query = Post.query.filter(extract('month', Post.created_at) == i).order_by(
                    Post.created_at.desc()).all()
        if not query:
            continue
        for p in query:
            mon_lst.append({'id': p.id, 'title': p.title, 'created_at': p.created_at})
        month = month_lst[i - 1]
        post_lst.append({'month': month, 'posts': mon_lst})
    return jsonify({'posts': post_lst})


@bp.route('/files')
@cache(MC_KEY_FILES)
def get_files():
    '''获取所有文件相关信息'''
    file_lst = files_schema()
    return jsonify({'files': file_lst})


@bp.route('/download/<path:filename>')
def files_download(filename):
    '''获取文件下载url'''
    file_url = get_url(filename)
    return jsonify({'url': file_url})
