# coding=utf-8
# Created by OhBonsai at 2018/3/7
"""User model"""

from flask_bcrypt import (
    generate_password_hash,
    check_password_hash
)
from flask_login import UserMixin
from sqlalchemy.types import (
    Boolean,
    String,
    Text
)
from sqlalchemy import (
    Column,
    PrimaryKeyConstraint,
    ForeignKey,
    Integer,
    Table
)
from sqlalchemy.orm import (
    backref,
    relationship
)

from app.models import BaseModel
from app.models.patch import (
    TagMixin,
    StatusMixin
)


# User Group m2m relationship table
user_group = Table('user_group', BaseModel.metadata,
                   Column('user_id', Integer(), ForeignKey('user.id')),
                   Column('group_id', Integer(), ForeignKey('group.id')),
                   PrimaryKeyConstraint('user_id', 'group_id'))


class User(UserMixin, BaseModel):
    """Implements the User model."""

    username = Column(String(32), unique=True)
    password = Column(String(32))
    chinese_name = Column(String(32))
    email = Column(String(32))
    active = Column(Boolean(), default=True)
    my_groups = relationship('Group', backref='user', lazy='dynamic')
    groups = relationship('Group', secondary=user_group, backref=backref('users', lazy='dynamic'))

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


class Group(TagMixin, StatusMixin, BaseModel):
    """Implements the Group model."""

    name = Column(String(32), unique=True)
    display_name = Column(String(64))
    description = Column(Text())
    user_id = Column(Integer, ForeignKey(u'user.id'))

    def __init__(self, name, display_name=None, description=None, user=None):
        super(Group, self).__init__()
        self.name = name
        self.display_name = display_name or name
        self.description = description or name
        self.user = user
