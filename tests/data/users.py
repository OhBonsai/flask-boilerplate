# coding=utf-8
# Created by OhBonsai at 2018/3/13
# -*- coding: utf-8 -*-
from faker import Faker

from app.models.user import User


def test_admin():
    u = User(username='sketch')
    u.email = 'youjiantao@gridsum.com'
    u.is_admin = True
    u.set_password("123456")
    u.admin = True
    return u


def test_user():
    u = User(username='test')
    u.email = 'youjiantao@gridsum.com'
    u.set_password("123456")
    u.admin = True
    return u


def test_users(n=50):
    fake = Faker()
    fake.seed(42)

    users = []
    for i in range(n):
        u = User(username=fake.name())
        u.email = fake.email()
        u.set_password(fake.password())
        users.append(u)

    return users


def sketch(**kwargs):
    user = User(username="sketch")
    user.email = "youjiantao@gridsum.com"
    user.set_password("123456")
    user.is_admin = True
    return user.apply_kwargs(kwargs)


def lotus(**kwargs):
    user = User(username="sketch")
    user.email = "youjiantao@gridsum.com"
    user.set_password("123456")
    return user.apply_kwargs(kwargs)
