# coding=utf-8
# Created by OhBonsai at 2018/3/15
import os
import datetime

from .meta import ConfigRestrictMeta


basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig(object, metaclass=ConfigRestrictMeta):
    SECRET_KEY = b'\x12\x23'
    BASE_PATH = os.path.realpath(os.path.dirname(__file__))
    REMEMBER_COOKIE_DURATION = datetime.timedelta(7)
