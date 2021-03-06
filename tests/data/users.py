# coding=utf-8
# Created by OhBonsai at 2018/3/13
# -*- coding: utf-8 -*-
from faker import Faker

from app.models.user import User, Group


def create_admin():
    u = User(username='sketch')
    u.email = 'letbonsaibe@gmail.com'
    u.is_admin = True
    u.set_password("123456")
    u.admin = True
    return u


def create_user():
    u = User(username='test')
    u.email = 'letbonsaibe@gmail.com'
    u.set_password("123456")
    u.admin = True
    return u


def create_group():
    g = Group(name='test')
    return g


def create_users(n=50):
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
    user.email = "letbonsaibe@gmail.com"
    user.set_password("123456")
    user.is_admin = True
    return user.apply_kwargs(kwargs), "123456"


def lotus(**kwargs):
    user = User(username="sketch")
    user.email = "letbonsaibe@gmail.com"
    user.set_password("123456")
    return user.apply_kwargs(kwargs), "123456"

