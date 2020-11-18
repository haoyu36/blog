#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import url_for
from ..models import Post, Tag, PostTag, Files


def post_schema(obj):
    '''以字典格式返回单篇博客相关数据'''
    data = {
        'id': obj.id,
        'title': obj.title,
        'intro': obj.intro,
        'body': obj.body,
        'html_body': obj.html_body,
        'created_at': obj.created_at,
        'tags': tags_schema(obj),
        'url': url_for('api.get_post', post_id=obj.id, _external=True)
        }
    return data


def tags_schema(obj=None):
    '''
    如果传入博客对象，返回博客标签信息
    否则返回所有标签信息
    '''
    tag_lst = []
    if obj:
        ss = Post.get(obj.id).tags
    else:
        ss = Tag.query.all()
    for t in ss:
        dic = {
            'id': t.id,
            'name': t.name,
            'count': int(PostTag.get_count_by_tag(t.id)),
            'url': url_for('api.tags', _external=True) + '/' + str(t.id) + '/1',
        }
        tag_lst.append(dic)
    return tag_lst


def files_schema():
    file_lst = []
    for f in Files.query.order_by(Files.created_at.desc()).all():
        dic = {
            'id': f.id,
            'name': f.name,
            'size': f.size,
        }
        file_lst.append(dic)
    return file_lst


def posts_schema(posts, method=None, tag_id=None):
    '''
    以字典形式返回一页博客相关数据
    :param posts: 博客的分页对象
    :param method: 传入构造方法，返回完整 url，否则返回数字
    :param tag_id: 返回指定标签下博客时 url 的构造参数
    '''

    if not method:
        present_page_url = posts.page
        next_page_url = posts.next_num
        prev_page_url = posts.prev_num
    else:
        present_page_url = url_for(method, **{'tag_id': tag_id, 'page': posts.page},
                                   _external=True)
        next_page_url = url_for(method, **{'tag_id': tag_id, 'page': posts.next_num},
                                _external=True) if posts.next_num else None
        prev_page_url = url_for(method, **{'tag_id': tag_id, 'page': posts.prev_num},
                                _external=True) if posts.prev_num else None

    info = {
        'present_page_url': present_page_url,     # 当前页 url
        'pages': posts.pages,                     # 博客总页数
        'per_page_counts': posts.per_page,        # 每页博客数
        'total_posts': posts.total,               # 总博客数
        'next_page_url': next_page_url,           # 下一页 url
        'prev_page_url': prev_page_url,           # 上一页 url
        }
    posts_lst = [post_schema(post) for post in posts.items]
    return dict({'posts': posts_lst}, **info)
