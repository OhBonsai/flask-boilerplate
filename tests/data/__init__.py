# coding=utf-8
# Created by OhBonsai at 2018/3/13


def add_fixtures(db, *fixtures):
    db.session.add_all(fixtures)
    db.session.commit()
