# coding=utf-8
# Created by OhBonsai at 2018/3/7
"""Entry point for the application"""

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_restful import Api
from flask_wtf import CSRFProtect


def register_something():
    pass


def create_app():
    app = Flask(__name__)
    return app


def create_celery_app():
    return None

