# coding=utf-8
# Created by OhBonsai at 2018/3/9
"""Entry point for the application"""

import os
import config

from flask import Flask
from app.models import configure_engine, init_db


class App(Flask):
    def __init__(self, name='app', config_file=None, *args, **kwargs):
        super(App, self).__init__(name, *args, **kwargs)
        self.config.from_pyfile(config.DEFAULT_CONF_PATH)

        if config_file:
            self.config.from_pyfile(config_file)

        if os.getenv("CONFIG_PATH"):
            pass

    def add_sqlalchemy(self):
        configure_engine(self.config['SQLALCHEMY_DATABASE_URI'])
        init_db()
        return self

    def add_cache(self):
        from app.api.cache import cache
        cache.init_app(self)
        return self

    def add_logger(self):
        from app.logger import logger
        logger.init_app(self)
        return self

    def add_tracer(self):
        from app.tracer import sentry
        sentry.init_app(self)
        return self

    def add_celery(self):
        return self


def create_app(*args, **kwargs):
    return App(*args, **kwargs)\
        .add_sqlalchemy()\
        .add_tracer()


def create_http_app(*args, **kwargs):
    return create_app(*args, **kwargs)\
        .add_logger()\
        .add_celery()


def create_celery_app():
    pass
