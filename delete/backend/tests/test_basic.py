#!/usr/bin/env python
# -*- coding: utf-8 -*-


import unittest

from flask import current_app

from myapp import create_app, db
from myapp.fake import test_fake
from myapp.models import rdb


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        '''每个测试之前执行'''
        self.app = create_app('testing')            # 创建Flask应用
        self.app_context = self.app.app_context()   # 激活Flask应用上下文
        self.app_context.push()
        self.client = self.app.test_client()        # 创建客户端测试对象
        db.create_all()                             # 创建所有数据库表
        test_fake()                                 # 创建虚拟博客数据

    def tearDown(self):
        '''每个测试之后执行'''
        db.session.remove()
        db.drop_all()                               # 删除所有数据库表
        try:
            rdb.delete(*rdb.keys('*'))              # 删除所有redis缓存
        except:
            pass
        self.app_context.pop()                      # 退出Flask应用上下文

    def test_basic_app_exists(self):
        self.assertFalse(current_app is None)

    def test_basic_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])