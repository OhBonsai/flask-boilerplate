# coding=utf-8
# Created by OhBonsai at 2018/3/13
import sys

from flask_script import Manager, prompt_bool
from flask_migrate import stamp
from app.app import create_app
from app.models import db


manager = Manager(help="Perform database operations")


@manager.command
def create():
    """ Initialize the database by creating the necessary tables and indices """

    # create all tables and indices
    db.create_all()
    # create alembic version table
    stamp()


@manager.command
def drop():
    """ Drops database tables """
    verified = prompt_bool(
        'Do you really want to drop all the database tables?')
    if verified:
        sys.stdout.write('All tables dropped. Database is now empty.\n')
        db.drop_all()


@manager.command
def bootstrap():
    """ Bootstrap the database with some initial data """
    pass  # TODO
