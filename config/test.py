# coding=utf-8
# Created by OhBonsai at 2018/3/15
from .default import BaseConfig
import os

"""
This config is just for unittest and apitest. In this mode, Backend and Sub Thread won't run
"""


class TestConfig(BaseConfig):
    CUR_ENV = "TEST"
    TESTING = True
    DEBUG = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BaseConfig.BASE_PATH, '..', 'test.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
