# -*- coding: utf-8 -*-

import hashlib


class NotAllowedException(Exception):
    pass


def get_md(filename):
    md = hashlib.sha224(filename.encode('utf8')).hexdigest()
    return md


def humanize_bytes(fp, precision=2):
    '''表示文件大小'''
    bytesize = len(fp.read())
    abbrevs = (
        (1 << 50, 'PB'),
        (1 << 40, 'TB'),
        (1 << 30, 'GB'),
        (1 << 20, 'MB'),
        (1 << 10, 'kB'),
        (1, 'bytes')
    )
    if bytesize == 1:
        return '1 byte'
    for factor, suffix in abbrevs:
        if bytesize >= factor:
            break
    return '%.*f %s' % (precision, bytesize / factor, suffix)
