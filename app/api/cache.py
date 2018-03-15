# coding=utf-8
# Created by OhBonsai at 2018/3/8
from flask_caching import Cache

cache = Cache(config=dict(CACHE_TYPE='simple'))
