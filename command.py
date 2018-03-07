# coding=utf-8
# Created by OhBonsai at 2018/3/7

"""This module is for management of the application."""

from flask_migrate import MigrateCommand
from flask_script import (
    Command,
    Manager,
    Server,
    Option,
    prompt_bool,
    prompt_pass
)
from sqlalchemy.exc import IntegrityError

from app import create_app
from app.models import db_session
from app.models import drop_all