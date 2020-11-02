import random

import requests
from locust import HttpLocust, TaskSet, task


url = 'http://haoyu36.cn/api/search'
res = requests.get(url).json()
id_lst = [i['id'] for i in res['posts']]


class BrowseBehavior(TaskSet):

    @task(3)
    def index_page(self):
        r = self.client.get('/')

    @task(40)
    def load_post(self):
        if not id_lst:
            return
        url = f'/post/{random.choice(id_lst)}'
        r = self.client.get(url)

    @task(5)
    def load_archives_page(self):
        r = self.client.get('/archives')

    @task(5)
    def load_tags_page(self):
        r = self.client.get('/tags')

    @task(5)
    def load_search_page(self):
        r = self.client.get('/search')

    @task(5)
    def load_homepost_page(self):
        r = self.client.get('/homepost')

    @task(5)
    def load_homefile_page(self):
        r = self.client.get('http://haoyu36.cn/file/homefile')

    @task(10)
    def load_posts(self):
        post_id = [1, 2, 3, 4]
        url = f'/posts/{random.choice(post_id)}'
        r = self.client.get(url)

    @task(5)
    def load_files_page(self):
        r = self.client.get('http://haoyu36.cn/file/page/1')


class BlogLocust(HttpLocust):
    task_set = BrowseBehavior
    host = "http://haoyu36.cn/api"
    min_wait = 2 * 1000
    max_wait = 10 * 1000
