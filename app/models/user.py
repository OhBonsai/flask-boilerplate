# coding=utf-8
# Created by OhBonsai at 2018/3/7
"""User model"""

from flask_bcrypt import (
    generate_password_hash,
    check_password_hash
)
from flask_login import UserMixin
from app.models.patch import (
    TagMixin,
    StatusMixin
)
from app.models import db

# User Group m2m db.relationship db.Table
user_group = db.Table('user_group', db.metadata,
                      db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                      db.Column('group_id', db.Integer(), db.ForeignKey('group.id')),
                      db.PrimaryKeyConstraint('user_id', 'group_id'))


class User(UserMixin, db.Model):
    """Implements the User model."""

    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))
    chinese_name = db.Column(db.String(32))
    email = db.Column(db.String(32))
    active = db.Column(db.Boolean(), default=True)
    my_groups = db.relationship('Group', backref='user', lazy='dynamic')
    groups = db.relationship('Group', secondary=user_group, backref=db.backref('users', lazy='dynamic'))

    def __init__(self, username, name=None):
        """
        :param username: Username for the user
        :param name: Name of the user
        """
        super(User, self).__init__()
        self.username = username
        self.name = name
        if not name:
            self.name = username

    def set_password(self, plaintext, rounds=12):
        password_hash = generate_password_hash(plaintext, rounds)
        self.password = password_hash

    def check_password(self, plaintext):
        return check_password_hash(self.password, plaintext)

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False


class Group(TagMixin, StatusMixin, db.Model):
    """Implements the Group model."""

    name = db.Column(db.String(32), unique=True)
    display_name = db.Column(db.String(64))
    description = db.Column(db.Text())
    user_id = db.Column(db.Integer, db.ForeignKey(u'user.id'))

    def __init__(self, name, display_name=None, description=None, user=None):
        super(Group, self).__init__()
        self.name = name
        self.display_name = display_name or name
        self.description = description or name
        self.user = user
