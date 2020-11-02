# -*- coding: utf-8 -*-
"""
此模块提供博客API接口
"""

from itertools import groupby

from flask import jsonify, url_for

from .schemas import post_schema, posts_schema, tag_schema
from myapp.api import api as bp
from myapp.models import Post, PostTag, Tag
from myapp.libs.mc import cache


MC_KEY_POSTS_SEARCH = 'api:post_search'
MC_KEY_POSTS_ARCHIVES = 'api:post_archives'
MC_KEY_ONE_POST = 'api:one_post:{post_id}'
MC_KEY_ONE_PAGE_POSTS = 'api:page_posts:{page}'
MC_KEY_POSTS_BY_TAG = 'api:posts_by_tag:{tag_id}_{page}'
MC_KEY_TAGS = 'api:tags'
MC_KEY_TAG_LST = 'api:tag_lst'
MC_KEY_HOMEPOST = 'api:homepost'


@bp.route('/')
def index():
    '''API版本及相关信息'''
    return jsonify({
        "api_version": "1.0",
        "website": "http://haoyu36.cn",
        "api_base_url": url_for('.index', _external=True),
    })


@bp.route('/post/<int:post_id>')
@cache(MC_KEY_ONE_POST)
def post(post_id):
    '''返回单篇博客'''
    post = Post.get_or_404(post_id)
    schema = post_schema(post)
    return jsonify(schema)


@bp.route('/posts/<int:page>')
@cache(MC_KEY_ONE_PAGE_POSTS)
def posts(page):
    '''返回所有博客，分页返回'''
    posts = Post.get_posts(page)
    schema = posts_schema(posts)
    return jsonify(schema)


@bp.route('/tags/<int:tag_id>/<int:page>')
@cache(MC_KEY_POSTS_BY_TAG)
def tag_posts(tag_id, page):
    '''返回指定标签下所有博客，分页返回'''
    posts = PostTag.get_posts_by_tag(tag_id, page)
    schema = posts_schema(posts)
    return jsonify(schema)


@bp.route('/tags')
@cache(MC_KEY_TAGS)
def tags():
    '''返回所有标签相关信息'''
    tag_lst = [tag_schema(tag) for tag in Tag.query.all()]
    return jsonify({'tags': tag_lst})


@bp.route('/tag-lst')
@cache(MC_KEY_TAG_LST)
def tag_lst():
    '''以列表形式获取标签名'''
    lst = [tag.name for tag in Tag.query.all()]
    return jsonify({'tags': lst})


@bp.route('/homepost')
@cache(MC_KEY_HOMEPOST)
def homepost():
    '''返回首页预览的3篇博客'''
    posts = Post.query.order_by(Post.created_at.desc()).limit(3)
    posts_lst = [post_schema(post) for post in posts]
    return jsonify({'posts': posts_lst})


@bp.route('/search')
@cache(MC_KEY_POSTS_SEARCH)
def search():
    '''返回所有博客，用于前端搜索'''
    posts_lst = []
    for post in Post.query.all():
        posts_lst.append({
            'id': post.id,
            'title': post.title,
            'intro': post.intro,
            'created_at': post.created_at,
            'tags': [tag_schema(tag) for tag in post.tags],
            'html': post.html,
        })
    return jsonify({'posts': posts_lst})


@bp.route('/archives')
@cache(MC_KEY_POSTS_ARCHIVES)
def archives():
    '''用于归档页面，按年份排序'''
    dic = {}
    query = Post.query.filter(Post.created_at).order_by(Post.id.desc())
    for year, items in groupby(query, grouper):
        lst = dic.get(year, []) + arc(items)
        lst = sorted(lst, key=lambda x: x['created_at'], reverse=True)
        dic[year] = lst
    archives = sorted(dic.items(), reverse=True)
    return jsonify({'archives': archives})


def grouper(item):
    return item.created_at.year


def arc(items):
    lst = []
    for p in items:
        lst.append({
            'id': p.id,
            'title': p.title,
            'created_at': p.created_at
        })
    return lst
