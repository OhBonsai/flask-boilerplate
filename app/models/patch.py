# coding=utf-8
# Created by OhBonsai at 2018/3/7
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer
)

from sqlalchemy.types import String

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from app.models import (
    BaseModel,
    db_session
)


class BasePatch(object):
    """Base class with common attr"""

    @declared_attr
    def user_id(self):
        return Column(Integer, ForeignKey('user.id'))

    @declared_attr
    def user(self):
        return relationship('User')


class Tag(BasePatch):
    tag = Column(String(16))

    def __init__(self, user, tag):
        """
        :param user: User instance
        :param tag: name of this tag
        """
        super(Tag, self).__init__()
        self.user = user
        self.tag = tag


class Status(BasePatch):
    status = Column(String(16))

    def __init__(self, user, tag):
        """
        :param user: User instance
        :param status: The type of status (string, e,g. created)
        """
        super(Status, self).__init__()
        self.user = user
        self.tag = tag


class TagMixin(object):

    @declared_attr
    def tags(self):
        self.Tag = type(
            '{}Label'.format(self.__name__),
            (Tag, BaseModel),
            dict(
                __tablename__='{0:s}_tag'.format(self.__tablename__),
                parent_id=Column(Integer, ForeignKey('{0:s}.id'.format(self.__tablename__))),
                parent=relationship(self)))
        return relationship(self.Tag)


class StatusMixin(object):
    @declared_attr
    def status(self):
        self.Status = type(
            '{}Label'.format(self.__name__),
            (Tag, BaseModel),
            dict(
                __tablename__='{0:s}_status'.format(self.__tablename__),
                parent_id=Column(Integer, ForeignKey('{0:s}.id'.format(self.__tablename__))),
                parent=relationship(self)))
        return relationship(self.Status)
