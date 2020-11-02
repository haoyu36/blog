# -*- coding: utf-8 -*-
'''
一个简单的爬虫，爬取博客内书籍信息
不集成到博客项目中，需在本地爬取好后在管理后台上传
'''

import os
import json
from lxml import html
import requests


UA = 'Mozilla/5.0 (Macintosh Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'  # noqa
headers = {'User-Agent': UA}

dirname = os.getcwd()
json_path = os.path.join(dirname, 'results.json')
img_path = os.path.join(dirname, 'img')

if not os.path.exists(img_path):
    os.makedirs(img_path)


def search_book(url):
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return
    root = html.fromstring(res.text.strip())
    book_site = root.xpath("//div[@class='result']//a[@class='nbg']/@href")[0]
    return book_site


def crawl(url):
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return
    root = html.fromstring(res.text.strip())
    pic_url = root.xpath("//a[@class='nbg']/@href")[0]
    author = root.xpath("//div[@id='info']/a/text()")[0]
    title = root.xpath("//span[@property='v:itemreviewed']/text()")[0]
    intro = root.xpath("//div[@class='indent']//div[@class='intro']//text()")

    return {
        'pic_url': pic_url,
        'author': author.replace(' ', '').replace('\n', ''),
        'title': title,
        'intro': ''.join(intro).replace(' ', '').replace('\n', '')
    }


def write_to_json(data):
    with open(json_path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, indent=2, ensure_ascii=False) + '\n')


def save_image(data):
    res = requests.get(data.get('pic_url'), headers=headers)
    if res.status_code != 200:
        return
    file_path = f'{img_path}/{data.get("title")}.jpg'
    with open(file_path, 'wb') as f:
        f.write(res.content)


def main(book):
    url = f'https://www.douban.com/search?cat=1001&q={book}'
    book_site = search_book(url)
    if not book_site:
        return 'crawl error'
    data = crawl(book_site)
    save_image(data)
    write_to_json(data)


if __name__ == '__main__':
    for book in ['编程人生', '编码', '代码整洁之道']:
        main(book)
