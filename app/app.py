# coding=utf-8
# Created by OhBonsai at 2018/3/9
"""Entry point for the application"""
import os
import sys

from config import config

from flask import Flask
from flask_migrate import Migrate
from app.models import db


class App(Flask):
    def __init__(self, name='app', env_level="LOCAL", config_file=None, *args, **kwargs):
        super(App, self).__init__(name, *args, **kwargs)

        if os.environ.get('SKETCH_CONFIG_FILE'):
            config_file = os.environ.get('SKETCH_CONFIG_FILE')

        if config_file:
            os.environ['SKETCH_SETTINGS'] = config_file
            try:
                self.config.from_envvar('SKETCH_SETTINGS')
            except IOError:
                sys.stderr.write(
                    'Config file {} does not exist.\n'.format(config_file)
                )
                sys.exit(1)
            return

        if os.environ.get('SKETCH_CUR_ENV'):
            env_level = os.environ.get('SKETCH_CUR_ENV')

        self.config.from_object(config[env_level])

    def add_sqlalchemy(self):
        db.init_app(self)
        migrate = Migrate()
        migrate.init_app(self, db)
        return self

    def add_login(self):
        from app.api.login import login_manager
        login_manager.init_app(self)
        return self

    def add_api(self):
        from app.api.v1 import register_api
        register_api(self)
        return self

    def add_cache(self):
        from app.api.cache import cache
        cache.init_app(self)
        return self

    def add_logger(self):
        from app.logger import register_logger
        register_logger(self)
        return self

    def add_tracer(self):
        from app.tracer import sentry
        sentry.init_app(self)
        return self

    def add_celery(self):
        return self

    def add_consul(self):
        from app.consul import register_consul
        register_consul(self)
        return self


def create_app(*args, **kwargs):
    return App(*args, **kwargs)\
        .add_sqlalchemy()\
        .add_login()\
        .add_tracer()


def create_http_app(*args, **kwargs):
    return create_app(*args, **kwargs)\
        .add_logger()\
        .add_celery()


def create_api_app(*args, **kwargs):
    from app.api.v1 import register_api

    app = create_http_app('app.api', *args, **kwargs)
    app.add_cache()
    register_api(app)

    if app.config.get('CUR_ENV') in ["QA", "PROD"]:
        app.add_consul()
    return app


def create_qa_app(*args, **kwargs):
    pass


def create_celery_app():
    pass
