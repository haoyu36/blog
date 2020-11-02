# -*- coding: utf-8 -*-
'''
用于开发时生成虚拟数据
'''

import time
from random import randint

from faker import Faker
from myapp.models import AdminUser, Files, Post, PostTag, Tag


def fake():
    fake = Faker('zh_CN')
    for _ in range(1, 21):
        Post.create(title=fake.sentence(), body=fake.text(500), intro=fake.text(50))
        time.sleep(1)    # 博客需要根据创建时间排序

    for i in ['python', 'vim', 'bbq']:
        Tag.create(name=i)

    # 关联博客与标签
    post_counts = Post.query.count()
    tag_counts = Tag.query.count()
    for p in range(1, post_counts + 1):
        for t in range(1, randint(1, tag_counts) + 1):
            PostTag.create(post_id=p, tag_id=t)

    AdminUser.create(username='haoyu', password='haoyu', is_admin=True)
    AdminUser.create(username='test', password='test')

    Files.create(filename='a.pdf', size='194k', author='haoyu')
    Files.create(filename='b.pdf', size='1434M', author='haoyu')
