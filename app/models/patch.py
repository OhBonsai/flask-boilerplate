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


class Comment(BasePatch):
    comment = Column(String(1024))

    def __init__(self, user, comment):
        """
        :param user: User instance
        :param comment: comment string
        """
        super(Comment, self).__init__()
        self.user = user
        self.tag = comment


class Status(BasePatch):
    """There are some built-in Value: "deleted", "new"
    """
    status = Column(String(16))

    def __init__(self, user, status):
        """
        :param user: User instance
        :param status: The type of status (string, e,g. created)
        """
        super(Status, self).__init__()
        self.user = user
        self.status = status


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
            '{}Status'.format(self.__name__),
            (Status, BaseModel),
            dict(
                __tablename__='{0:s}_status'.format(self.__tablename__),
                parent_id=Column(Integer, ForeignKey('{0:s}.id'.format(self.__tablename__))),
                parent=relationship(self)))
        return relationship(self.Status)


    def set_status(self, status):
        """
        Set status on object. Although this is a many-to-many relationship
        this makes sure that the parent object only has one status set.

        :param status: Name of the status
        """
        for _status in self.status:
            self.status.remove(_status)
        self.status.append(self.Status(user=None, status=status))
        db_session.commit()

    @property
    def get_status(self):
        """Get the current status.


        :return The status as a string
        """
        if not self.status:
            self.status.append(self.Status(user=None, status=u'new'))
        return self.status[0]


class CommentMixin(object):

    @declared_attr
    def comment(self):
        self.Comment = type(
            '{}Comment'.format(self.__name__),
            (Tag, BaseModel),
            dict(
                __tablename__='{0:s}_comment'.format(self.__tablename__),
                parent_id=Column(Integer, ForeignKey('{0:s}.id'.format(self.__tablename__))),
                    parent=relationship(self)))
        return relationship(self.Comment)

