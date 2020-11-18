#!/usr/bin/env python
# -*- coding: utf-8 -*-

from myapp.models import Post, Tag, PostTag, AdminUser, Files
from myapp.models.utils import NotAllowedException
from test_basic import BaseTestCase


class BasicsTestCase(BaseTestCase):

    def test_models_Post(self):
        p = Post.get(1)
        self.assertTrue(p.title)
        self.assertTrue(p.intro)
        self.assertTrue(p.body)

    def test_models_Post_create(self):
        ok, _ = Post.create_or_update(title='xx', body='xxx')
        self.assertTrue(ok)

    def test_models_Post_delete(self):
        Post.get(2).delete()
        p = Post.get(2)
        self.assertFalse(p)

    def test_models_Post_update(self):
        Post.create_or_update(id=1, title='xxx')
        p = Post.get(1)
        self.assertEqual(p.title, 'xxx')

    def test_models_Post_tags(self):
        t = Post.get(1).tags
        self.assertTrue(t)

    def test_models_Post_get_posts(self):
        p = Post.get_posts().items
        self.assertTrue(p)

    def test_models_Tag_get(self):
        t = Tag.get(1)
        self.assertTrue(t.name)

    def test_models_Tag_create(self):
        Tag.create(name='xx')
        t = Tag.get_by_name('xx')
        self.assertEqual(t.name, 'xx')

    def teat_models_Tag_delete(self):
        with self.assertRaises(NotAllowedException):
            Tag.get(1).delete()

    def teat_models_Tag_update(self):
        with self.assertRaises(NotAllowedException):
            Tag.get(1).update(name='xxxx')

    def test_models_Tag_all_tag(self):
        tag_lst = Tag.get_all_tag()
        self.assertTrue(tag_lst)

    def test_models_PostTag_get(self):
        p = PostTag.get(1)
        self.assertTrue(p.post_id)
        self.assertTrue(p.tag_id)

    def test_models_PostTag_create(self):
        ok, _ = PostTag.create(post_id=100, tag_id=100)
        self.assertTrue(ok)

    def test_models_PostTag_delete(self):
        PostTag.get(2).delete()
        p = PostTag.get(2)
        self.assertFalse(p)

    def test_models_PostTag_update(self):
        PostTag.create_or_update(id=1, post_id=100, tag_id=100)
        p = PostTag.get(1)
        self.assertEqual(p.post_id, 100)

    def test_models_AdminUser_create(self):
        AdminUser.create_user(username='xxx', password='xxx')
        user = AdminUser.query.filter_by(username='xxx').first()
        self.assertTrue(user)

    def test_models_Files_get(self):
        f = Files.get(1)
        self.assertTrue(f.name)
        self.assertTrue(f.size)
