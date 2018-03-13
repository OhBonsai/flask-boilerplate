# coding=utf-8
# Created by OhBonsai at 2018/3/13


def add_fixture(db_session, fixture):
    db_session.add(fixture)
    db_session.commit()


def add_fixtures(db_session, *fixtures):
    db_session.add_all(fixtures)
    db_session.commit()
