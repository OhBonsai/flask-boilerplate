# coding=utf-8
# Created by OhBonsai at 2018/3/7

"""This module is for management of the Sketch application."""

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

from sketch import create_app
from sketch.models import db_session
from sketch.models import drop_all