# -*- coding: utf-8 -*-

from base64 import b64encode
from test_basic import BaseTestCase


base_url = 'http://localhost:5000/api/'
admin_url = 'http://localhost:5000/admin/'


class APITestCase(BaseTestCase):

    def test_api_index(self):
        data = self.client.get(base_url).get_json()
        self.assertIn('api_version', data)
        self.assertIn('website', data)
        self.assertIn('api_base_url', data)

    def test_api_post(self):
        data = self.client.get(base_url + 'post/1').get_json()
        self.assertIn('title', data)
        self.assertIn('body', data)
        self.assertIn('intro', data)

    def test_api_posts(self):
        data = self.client.get(base_url + 'posts/1').get_json()
        self.assertIn('next_page', data)
        self.assertIn('posts', data)
        self.assertIn('total_pages', data)

    def test_api_tag_posts(self):
        data = self.client.get(base_url + 'tags/1/1').get_json()
        self.assertIn('next_page', data)
        self.assertIn('posts', data)
        self.assertIn('total_pages', data)

    def test_api_homepost(self):
        data = self.client.get(base_url + 'homepost').get_json()
        self.assertIn('posts', data)

    def test_api_tags(self):
        data = self.client.get(base_url + 'tags').get_json()
        self.assertIn('tags', data)

    def test_api_search(self):
        data = self.client.get(base_url + 'search').get_json()
        self.assertIn('posts', data)

    def test_api_archives(self):
        data = self.client.get(base_url + 'archives').get_json()
        self.assertIn('archives', data)

    def get_tokens(self):
        headers = {'Authorization': 'Basic ' + b64encode(
            ('haoyu:haoyu').encode('utf-8')).decode('utf-8')}
        res = self.client.post(admin_url + 'tokens', headers=headers)
        token = res.get_json()['token']
        return {'Authorization': f'Bearer {token}'}

    def test_admin_unauthorized(self):
        res = self.client.get(admin_url + 'ping')
        self.assertEqual(res.status_code, 401)

    def test_admin(self):
        headers = self.get_tokens()
        data = self.client.get(admin_url + 'ping', headers=headers).get_json()
        self.assertEqual(data['message'], 'pong')
