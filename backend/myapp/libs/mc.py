# -*- coding: utf-8 -*-
'''
使用 redis 实现一个缓存装饰器
可以依据被装饰函数的参数格式化缓存的键

In [1]: MC_KEY = '{name}{id}'

In [2]: @test_gen_key(MC_KEY)
   ...: def test(name, id):pass

In [3]: test('haoyu', id=1)
key: haoyu1
args: {'name': 'haoyu', 'id': 1}

In [4]: test('haoyu', id=2)
key: haoyu2
args: {'name': 'haoyu', 'id': 2}
'''

import os
import inspect
from functools import wraps
from pickle import UnpicklingError

from walrus import Database
from sqlalchemy.ext.serializer import loads, dumps


rdb = Database.from_url(os.getenv('REDIS_URL'))
KEY_EXPIRE = 10 * 24 * 3600    # 缓存过期时间


def test_gen_key(key_pattern):
    '''测试缓存键的生成'''
    def deco(f):
        arg_names, varargs, varkw, defaults, *_ = inspect.getfullargspec(f)
        if varargs or varkw:
            raise Exception("do not support varargs")
        gen_key = gen_key_factory(key_pattern, arg_names, defaults)
        @wraps(f)
        def _(*a, **kw):
            key, args = gen_key(*a, **kw)
            print(f'key: {key}')
            print(f'args: {args}')
        return _
    return deco


def gen_key_factory(key_pattern, arg_names, defaults):
    args = dict(zip(arg_names[-len(defaults):], defaults)) if defaults else {}

    def gen_key(*a, **kw):
        aa = args.copy()
        aa.update(zip(arg_names, a))
        aa.update(kw)
        key = key_pattern.format(**aa)
        return key and key.replace(' ', '_'), aa
    return gen_key


def cache(key_pattern, expire=KEY_EXPIRE):
    def deco(f):
        arg_names, varargs, varkw, defaults, *_ = inspect.getfullargspec(f)
        # 不支持函数可变参数
        if varargs or varkw:
            raise Exception("do not support varargs")
        gen_key = gen_key_factory(key_pattern, arg_names, defaults)

        @wraps(f)
        def _(*a, **kw):
            key, args = gen_key(*a, **kw)
            if not key:
                return f(*a, **kw)
            r = rdb.get(key)

            if r is None:
                res = f(*a, **kw)
                if res is not None:
                    r = dumps(res)
                    rdb.set(key, r, expire)
                else:
                    r = dumps(empty)
                    rdb.set(key, r, expire)
            try:
                r = loads(r)
            except (TypeError, UnpicklingError):
                pass
            if isinstance(r, Empty):
                r = None
            return r
        return _
    return deco


class Empty:
    '''实例出一个空对象'''

    def __call__(self, *a, **kw):
        return empty

    def __nonzero__(self):
        return False

    def __contains__(self, item):
        return False

    def __repr__(self):
        return '<Empty Object>'

    def __str__(self):
        return ''

    def __eq__(self, v):
        return isinstance(v, Empty)

    def __getattr__(self, name):
        if not name.startswith('__'):
            return empty
        raise AttributeError(name)

    def __len__(self):
        return 0

    def __getitem__(self, key):
        return empty

    def __setitem__(self, key, value):
        pass

    def __delitem__(self, key):
        pass

    def __iter__(self):
        return self

    def __next__(self):
        raise StopIteration

    def next(self):
        raise StopIteration


empty = Empty()
