#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from random import randint

from faker import Faker

from .models import Post, Tag, PostTag, AdminUser, Files


# 定义虚拟博客标签
tag_lst = ['python', 'vim', 'bbq']


def fake():
    '''生成虚拟博客数据'''

    fake = Faker('zh_CN')
    for i in range(1, 21):
        Post.create(title=fake.sentence(), body=fake.text(2000),
                    html_body=fake.text(2000), intro=fake.text(100))
        time.sleep(1)
    for i in tag_lst:
        Tag.create(name=i)
    p_counts = Post.query.count()
    t_counts = Tag.query.count()
    for i in range(1, p_counts+1):
        for p in range(1, randint(1, t_counts)+1):
            PostTag.create(post_id=i, tag_id=p)
    Files.create(name='a.pdf', size='194k')
    AdminUser.create_user(username='haoyu', password='haoyu')


def test_fake():
    '''生成虚拟测试博客数据'''

    fake = Faker('zh_CN')
    for i in range(1, 9):
        Post.create(title=fake.sentence(), body=fake.text(20),
                    html_body=fake.text(20), intro=fake.text(10))
    for i in tag_lst:
        Tag.create(name=i)
    p_counts = Post.query.count()
    t_counts = Tag.query.count()
    for i in range(1, p_counts+1):
        for p in range(1, randint(1, t_counts)+1):
            PostTag.create(post_id=i, tag_id=p)
    Files.create(name='a.pdf', size='194k')
    AdminUser.create_user(username='haoyu', password='haoyu')
