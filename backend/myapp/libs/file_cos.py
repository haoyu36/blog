# -*- coding: utf-8 -*-
'''
加载文件上传的配置及方法，使用对象存储在腾讯云服务上
'''

import os
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client


# 从配置文件中读取文件相关配置
region = os.getenv('FILE_REGION')
secret_id = os.getenv('FILE_SECRET_ID')
secret_key = os.getenv('FILE_SECRET_KEY')
bucket = os.getenv('FILE_BUCKET')

# 获取客户端对象
config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key)
client = CosS3Client(config)

# 云端文件的根地址
FILE_SITE = f'https://{bucket}.cos.{region}.myqcloud.com/'


def upload_cos(fp, md):
    '''上传文件到云端对象存储'''
    response = client.put_object(
        Bucket=bucket,
        Body=fp,
        Key=md,
    )
    return response['ETag']


def delete_cos(md):
    '''删除云端文件'''
    response = client.delete_object(
        Bucket=bucket,
        Key=md
    )
    return response
