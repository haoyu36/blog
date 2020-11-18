#!/usr/bin/env python
# -*- coding: utf-8 -*-


from test_basic import BaseTestCase


base_url = 'http://localhost:5000/api/'


class APITestCase(BaseTestCase):

    def test_api_index(self):
        data = self.client.get(base_url).get_json()
        self.assertIn('api_version', data)
        self.assertIn('website', data)
        self.assertIn('api_base_url', data)

    def test_api_get_post(self):
        data = self.client.get(base_url + 'post/1').get_json()
        self.assertIn('title', data)
        self.assertIn('html_body', data)
        self.assertIn('intro', data)

    def test_api_get_posts(self):
        data = self.client.get(base_url + 'posts/1').get_json()
        self.assertIn('next_page_url', data)
        self.assertIn('posts', data)
        self.assertIn('pages', data)

    def test_api_tag_posts(self):
        data = self.client.get(base_url + 'tags/1/1').get_json()
        self.assertIn('next_page_url', data)
        self.assertIn('posts', data)
        self.assertIn('pages', data)

    def test_api_tags(self):
        data = self.client.get(base_url + 'tags').get_json()
        self.assertIn('tags', data)

    def test_api_search(self):
        data = self.client.get(base_url + 'search').get_json()
        self.assertIn('posts', data)

    def test_api_archives(self):
        data = self.client.get(base_url + 'archives').get_json()
        self.assertIn('posts', data)

    def test_api_get_files(self):
        data = self.client.get(base_url + 'files').get_json()
        self.assertIn('files', data)
