# coding=utf-8
# Created by OhBonsai at 2018/3/13


import os
import random
import shutil

import pytest

import config
from app.models import db
from app import create_api_app
from app.app import App

from tests import setup_db, teardown_db, clean_db
from tests.data import users


@pytest.fixture(scope="function")
def seeded_random():
    """
    Calls random.seed() with a constant to ensure that random always returns
    the same results.
    """

    random.seed(1234)


@pytest.fixture(scope="session")
def application():
    """Global skylines application fixture

    Initialized with testing config file.
    """
    yield create_api_app(config_file=config.TESTING_CONF_PATH)


@pytest.fixture(scope="session")
def database(application):
    """Creates clean database schema and drops it on teardown

    Note, that this is a session scoped fixture, it will be executed only once
    and shared among all tests. Use `db` fixture to get clean database before
    each test.
    """
    assert isinstance(application, App)

    setup_db(app)
    yield db
    teardown_db()


@pytest.fixture(scope="function")
def db_session(database, application):
    """Provides clean database before each test. After each test,
    session.rollback() is issued.

    Also, database will be bootstrapped with some initial data.

    Return sqlalchemy session.
    """
    assert isinstance(application, App)

    with app.app_context():
        clean_db()
        yield database.session
        database.session.rollback()


@pytest.fixture(scope="function")
def test_admin(db_session):
    """
    Creates a test admin
    """
    user = users.test_admin()
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture(scope="function")
def test_user(db_session):
    """
    Creates a single test user
    """
    user = users.test_user()
    db_session.add(user)
    db_session.commit()
    return user


@pytest.fixture(scope="function")
def test_users(db_session):
    """
    Creates 50 test users
    """
    _users = users.test_users()
    for user in _users:
        db_session.add(user)
    db_session.commit()
    return _users
