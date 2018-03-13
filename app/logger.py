# coding=utf-8
# Created by OhBonsai at 2018/3/9
import logging


class Logger(object):

    def init_app(self, app):
        logging.basicConfig(level=logging.DEBUG)


logger = Logger()
