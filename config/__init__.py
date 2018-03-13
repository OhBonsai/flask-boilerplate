# coding=utf-8
# Created by OhBonsai at 2018/3/9
import os

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

PRO_CONF_PATH = '/etc/app/production.py'
DEFAULT_CONF_PATH = os.path.join(BASE_PATH, 'default.conf.py')
TESTING_CONF_PATH = os.path.join(BASE_PATH, 'test.conf.py')
