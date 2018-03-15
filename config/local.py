# coding=utf-8
# Created by OhBonsai at 2018/3/15
from .default import BaseConfig
import os


class LocalConfig(BaseConfig):
    CUR_ENV = "LOCAL"
    TESTING = False
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BaseConfig.BASE_PATH, '..', 'database.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True

