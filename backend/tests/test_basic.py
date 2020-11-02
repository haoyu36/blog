# -*- coding: utf-8 -*-

import time
import unittest
from random import randint

from faker import Faker
from flask import current_app

from myapp import create_app, db
from myapp.libs.mc import rdb
from myapp.models import AdminUser, Files, Post, PostTag, Tag


def test_fake():
    '''生成虚拟测试数据'''
    fake = Faker('zh_CN')
    for _ in range(1, 21):
        Post.create(title=fake.sentence(),
                    body=fake.text(500), intro=fake.text(50))
    for i in ['python', 'vim', 'bbq']:
        Tag.create(name=i)

    p_counts = Post.query.count()
    t_counts = Tag.query.count()
    for i in range(1, p_counts+1):
        for p in range(1, randint(1, t_counts)+1):
            PostTag.create(post_id=i, tag_id=p)

    AdminUser.create(username='haoyu', password='haoyu', is_admin=True)
    AdminUser.create(username='test', password='test')

    Files.create(filename='a.pdf', size='194k', author='haoyu')
    Files.create(filename='b.pdf', size='1434M', author='haoyu')


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        '''每个测试之前执行'''
        self.app = create_app('testing')    # 创建Flask应用
        self.app_context = self.app.app_context()    # 激活Flask应用上下文
        self.app_context.push()
        self.client = self.app.test_client()    # 创建客户端测试对象
        db.create_all()    # 创建所有数据库表
        test_fake()    # 创建虚拟博客数据

    def tearDown(self):
        '''每个测试之后执行'''
        db.session.remove()
        db.drop_all()    # 删除所有数据库表
        try:
            rdb.delete(*rdb.keys('*'))    # 删除所有redis缓存
        except:
            pass
        self.app_context.pop()    # 退出Flask应用上下文

    def test_basic_app_exists(self):
        self.assertFalse(current_app is None)

    def test_basic_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
