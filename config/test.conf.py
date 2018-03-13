# coding=utf-8
# Created by OhBonsai at 2018/3/13
import datetime
TESTING = True

SECRET_KEY = b'\x12\x23'

SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True


REMEMBER_COOKIE_DURATION = datetime.timedelta(7)

