#!/usr/bin/env python
# -*- coding: utf-8 -*-


from base64 import b64encode
from test_basic import BaseTestCase


base_url = 'http://localhost:5000/admin/'


class ADMINTestCase(BaseTestCase):
    '''测试管理后台'''

    def get_tokens(self):
        headers = {'Authorization': 'Basic ' + b64encode(
                    ('haoyu:haoyu').encode('utf-8')).decode('utf-8')}
        res = self.client.post(base_url + 'tokens', headers=headers)
        token = res.get_json()['token']
        return {'Authorization': f'Bearer {token}'}

    def test_admin_unauthorized(self):
        res = self.client.get(base_url + 'post/1')
        self.assertEqual(res.status_code, 401)

    def test_admin_get_post(self):
        headers = self.get_tokens()
        data = self.client.get(base_url + 'post/1', headers=headers).get_json()
        self.assertIn('title', data)

    def test_admin_put_post(self):
        headers = self.get_tokens()
        data = {
            'body': 'abc',
            'html_body': '<pabc</p>',
            'id': 1,
            'intro': 'abc',
            'title': 'abc'
        }
        res = self.client.put(base_url + 'post/1', data=data, headers=headers)
        self.assertEqual(res.status_code, 204)
        data = self.client.get(base_url + 'post/1', headers=headers).get_json()
        self.assertEqual(data['title'], 'abc')

    def test_admin_write_post(self):
        headers = self.get_tokens()
        data = {
            'body': 'abc',
            'html_body': '<pabc</p>',
            'intro': 'abc',
            'title': 'abc'
        }
        res = self.client.post(base_url + 'post/write', data=data, headers=headers)
        self.assertEqual(res.status_code, 204)

    def test_admin_delete_post(self):
        headers = self.get_tokens()
        res = self.client.delete(base_url + 'post/1', headers=headers)
        self.assertEqual(res.status_code, 204)

    def test_admin_get_posttag(self):
        headers = self.get_tokens()
        data = self.client.get(base_url + 'posttag/1', headers=headers).get_json()
        self.assertIn('tags', data)

    def test_admin_tags(self):
        data = self.client.get(base_url + 'tags').get_json()
        self.assertIn('tags', data)
