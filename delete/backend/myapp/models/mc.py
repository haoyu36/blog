import re
import os
import inspect
from functools import wraps
from pickle import UnpicklingError

from sqlalchemy.ext.serializer import loads, dumps
from walrus import Database as _Database


REDIS_URL = os.getenv('REDIS_URL')


__formaters = {}
percent_pattern = re.compile(r'%\w')
brace_pattern = re.compile(r'\{[\w\d\.\[\]_]+\}')
BUILTIN_TYPES = (int, bytes, str, float, bool)


class Database(_Database):
    def get2(self, name):
        rs = super().get(name)
        return loads(rs)

    def set2(self, name, value, ex=None, px=None, nx=False, xx=False):
        value = dumps(value)
        return super().set(name, value, ex=ex, px=px, nx=nx, xx=xx)


rdb = Database.from_url(REDIS_URL)


def formater(text):
    """
    >>> format('%s %s', 3, 2, 7, a=7, id=8)
    '3 2'
    >>> format('%(a)d %(id)s', 3, 2, 7, a=7, id=8)
    '7 8'
    >>> format('{1} {id}', 3, 2, a=7, id=8)
    '2 8'
    >>> class Obj: id = 3
    >>> format('{obj.id} {0.id}', Obj(), obj=Obj())
    '3 3'
    >>> class Obj: id = 3
    >>> format('{obj.id.__class__} {obj.id.__class__.__class__} {0.id} {1}', \
    >>> Obj(), 6, obj=Obj())
    "<type 'int'> <type 'type'> 3 6"
    """
    percent = percent_pattern.findall(text)
    brace = brace_pattern.search(text)
    if percent and brace:
        raise Exception('mixed format is not allowed')

    if percent:
        n = len(percent)
        return lambda *a, **kw: text % tuple(a[:n])
    elif '%(' in text:
        return lambda *a, **kw: text % kw
    else:
        return text.format


def format(text, *a, **kw):
    f = __formaters.get(text)
    if f is None:
        f = formater(text)
        __formaters[text] = f
    return f(*a, **kw)


def gen_key(key_pattern, arg_names, defaults, *a, **kw):
    return gen_key_factory(key_pattern, arg_names, defaults)(*a, **kw)


def gen_key_factory(key_pattern, arg_names, defaults):
    args = dict(zip(arg_names[-len(defaults):], defaults)) if defaults else {}
    if callable(key_pattern):
        names = inspect.getargspec(key_pattern)[0]

    def gen_key(*a, **kw):
        aa = args.copy()
        aa.update(zip(arg_names, a))
        aa.update(kw)
        if callable(key_pattern):
            key = key_pattern(*[aa[n] for n in names])
        else:
            key = format(key_pattern, *[aa[n] for n in arg_names], **aa)
        return key and key.replace(' ', '_'), aa
    return gen_key


def cache(key_pattern, expire=24 * 60 * 60):
    def deco(f):
        arg_names, varargs, varkw, defaults = inspect.getargspec(f)
        if varargs or varkw:
            raise Exception("do not support varargs")
        gen_key = gen_key_factory(key_pattern, arg_names, defaults)

        @wraps(f)
        def _(*a, **kw):
            key, args = gen_key(*a, **kw)
            if not key:
                return f(*a, **kw)
            force = kw.pop('force', False)
            r = rdb.get(key) if not force else None

            if r is None:
                r = f(*a, **kw)
                if r is not None:
                    if not isinstance(r, BUILTIN_TYPES):
                        r = dumps(r)
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
        _.original_function = f
        return _
    return deco


class Empty:

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
