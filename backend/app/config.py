# -*- coding:UTF-8 -*-
import os
import sys

base_dir = os.path.abspath(os.path.dirname(__file__))
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class Config:
    REDIS_PORT = 6379
    REDIS_HOST = 'localhost'
    DB_NAME = os.path.join(base_dir, 'data.sqlite')
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(base_dir, 'data.sqlite')

    REDIS_KEY_PREFIX = 'STOCK_BAR_'
    REDIS_KEY_EXPIRE = 60 * 60 * 2
    # REDIS_KEY_EXPIRE = 10
    CACHE_RAW_KEY = 'raw'
    CACHE_1MIN = '1min'
    CACHE_5MIN = '5min'
    CACHE_10MIN = '10min'

