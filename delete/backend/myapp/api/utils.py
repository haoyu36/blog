#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client


# 从配置文件中读取敏感配置
region = os.getenv('FILE_REGION')
secret_id = os.getenv('FILE_SECRET_ID')
secret_key = os.getenv('FILE_SECRET_KEY')
bucket = os.getenv('FILE_BUCKET')

# 获取客户端对象
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
client = CosS3Client(config)


def upload_cos(fp, filename):
    '''上传文件到云端对象存储'''
    response = client.put_object(
        Bucket=bucket,
        Body=fp,
        Key=filename,
    )
    return response['ETag']


def get_url(filename):
    '''获取文件下载链接'''
    response = client.get_presigned_download_url(
        Bucket=bucket,
        Key=filename,
        Expired=300,
    )
    return response


def delete_cos(filename):
    '''删除云端文件'''
    response = client.delete_object(
        Bucket=bucket,
        Key=filename
    )
    return response


def humanize_bytes(fp, precision=2):
    '''友好表示文件大小'''
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
