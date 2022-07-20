from typing import Optional

import qiniu
import requests
from app.core.config import settings


def qiniu_upload(data, key):
    ak = settings.QINIU_ACCESS_KEY
    sk = settings.QINIU_SECRET_KEY
    q = qiniu.Auth(access_key=ak, secret_key=sk)
    token = q.upload_token(bucket=settings.bucket_domain, key=key, expires=3600)
    ret, res = qiniu.put_data(up_token=token, key=key, data=data)
    return ret, res


def generate_access_url(file: str):
    access_key = settings.QINIU_ACCESS_KEY
    secret_key = settings.QINIU_SECRET_KEY

    q = qiniu.Auth(access_key, secret_key)
    bucket_domain = settings.bucket_domain

    # 有两种方式构造base_url的形式
    base_url = f'https://{bucket_domain}/{file}'

    # 或者直接输入url的方式下载
    # base_url = 'http://domain/key'

    # 可以设置token过期时间
    private_url = q.private_download_url(base_url, expires=3600)
    # r=requests.get(private_url)
    # print(r.status_code)
    # print(private_url)
    return private_url


def get_bucket_info():
    ak = settings.QINIU_ACCESS_KEY
    sk = settings.QINIU_SECRET_KEY
    q = qiniu.Auth(access_key=ak, secret_key=sk)
    bucket_domain = settings.bucket_name
    bucket = qiniu.BucketManager(q)
    ret, info = bucket.bucket_info(bucket_domain)
    print(ret)
    print(info)


def get_prefix_list(prefix: Optional[str] = None):
    ak = settings.QINIU_ACCESS_KEY
    sk = settings.QINIU_SECRET_KEY
    q = qiniu.Auth(access_key=ak, secret_key=sk)
    bucket_name = settings.bucket_name
    bucket = qiniu.BucketManager(q)
    if not prefix:
        prefix = 'miro/pics/ava'
    # 列举条目
    limit = 10
    # 列举出除'/'的所有文件以及以'/'为分隔的所有前缀
    delimiter = None
    # 标记
    marker = None
    ret, eof, info = bucket.list(bucket_name, prefix, marker, limit, delimiter)
    files = ret['items']
    if len(files) > 0:
        for file in files:
            print(file['key'])
