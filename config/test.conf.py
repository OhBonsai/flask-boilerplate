# coding=utf-8
# Created by OhBonsai at 2018/3/13
import datetime
import os
TESTING = True

SECRET_KEY = b'\x12\x23'

BASE_PATH = os.path.realpath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_PATH, '..', 'test.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_ECHO = True


REMEMBER_COOKIE_DURATION = datetime.timedelta(7)

