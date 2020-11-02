# -*- coding: utf-8 -*-
'''
定义数据的返回格式
'''

from flask import url_for
from myapp.models import PostTag


def tag_schema(obj):
    '''返回单个标签的数据
    :obj: 标签对象
    '''
    return {
        'id': obj.id,
        'name': obj.name,
        'count': PostTag.get_count_by_tag(obj.id),
        'url': url_for('api.tag_posts', tag_id=obj.id, page=1, _external=True),
    }


def post_schema(obj):
    '''返回单篇博客的数据
    :obj: 博客对象
    '''
    return {
        'id': obj.id,
        'title': obj.title,
        'intro': obj.intro,
        'body': obj.body,
        'html': obj.html,
        'toc': obj.toc,
        'status': obj.status,
        'created_at': obj.created_at,
        'tag_lst': [t.name for t in obj.tags],
        'tags': [tag_schema(tag) for tag in obj.tags],
        'url': url_for('api.post', post_id=obj.id, _external=True)
    }


def posts_schema(obj):
    '''返回一页博客的数据
    :obj: sqlalchemy 的博客分页对象
    '''
    info = {
        'present_page': obj.page,             # 当前页页数
        'total_pages': obj.pages,                 # 博客总页数
        'per_page_counts': obj.per_page,        # 每页博客数
        'total_posts': obj.total,               # 总博客数
        'next_page': obj.next_num,           # 下一页页数
        'prev_page': obj.prev_num,           # 上一页页数
    }
    posts_lst = [post_schema(post) for post in obj.items]
    return dict({'posts': posts_lst}, **info)


def file_schema(obj):
    '''返回单个文件的数据
    :obj: 文件对象
    '''
    return {
        'id': obj.id,
        'filename': obj.filename,
        'size': obj.size,
        'author': obj.author,
        'pic_url': obj.pic_url,
        'file_url': obj.file_url,
        'intro': obj.intro,
        'created_at': obj.created_at,
        'status': obj.status,
    }


def files_schema(obj):
    '''返回一页文件的数据
    :obj: sqlalchemy 的分页文件对象
    '''
    info = {
        'present_page': obj.page,
        'total_pages': obj.pages,
        'per_page_counts': obj.per_page,
        'total_files': obj.total,
        'next_page': obj.next_num,
        'prev_page': obj.prev_num,
    }
    files_lst = [file_schema(file) for file in obj.items]
    return dict({'files': files_lst}, **info)
