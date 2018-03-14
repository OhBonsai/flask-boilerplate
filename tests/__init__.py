# coding=utf-8
# Created by OhBonsai at 08/03/18.

from app.models import db

__all__ = ['setup_db', 'setup_app', 'teardown_db']


def setup_db(app):
    """Method used to build a database"""
    db.app = app
    db.create_all()


def teardown_db():
    """Method used to destroy a database"""
    db.session.remove()
    db.drop_all()
    db.session.bind.dispose()


def clean_db():
    """Clean all data, leaving schema as is

    Suitable to be run before each db-aware test. This is much faster than
    dropping whole schema an recreating from scratch.
    """
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())


def check_db_object(expected_result=None, model_cls=None):
    """
    Base function for checking Model class
    """
    db_obj = model_cls.query.get(1)
    for k, v in expected_result:
        assert db_obj.__getattribute__(k) == v
