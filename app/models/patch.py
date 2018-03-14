# coding=utf-8
# Created by OhBonsai at 2018/3/7
from sqlalchemy.ext.declarative import declared_attr
from app.models import db


class BasePatch(object):
    """Base class with common attr"""

    @declared_attr
    def user_id(self):
        return db.Column(db.Integer, db.ForeignKey('user.id'))

    @declared_attr
    def user(self):
        return db.relationship('User')


class Tag(BasePatch):
    tag = db.Column(db.String(16))

    def __init__(self, user, tag):
        """
        :param user: User instance
        :param tag: name of this tag
        """
        super(Tag, self).__init__()
        self.user = user
        self.tag = tag


class Comment(BasePatch):
    comment = db.Column(db.String(1024))

    def __init__(self, user, comment):
        """
        :param user: User instance
        :param comment: comment db.String
        """
        super(Comment, self).__init__()
        self.user = user
        self.comment = comment


class Status(BasePatch):
    """There are some built-in Value: "deleted", "new"
    """
    status = db.Column(db.String(16))

    def __init__(self, user, status):
        """
        :param user: User instance
        :param status: The type of status (db.String, e,g. created)
        """
        super(Status, self).__init__()
        self.user = user
        self.status = status


class TagMixin(object):

    @declared_attr
    def tags(self):
        self.Tag = type(
            '{}_Tag'.format(self.__name__),
            (Tag, db.Model),
            dict(
                __tablename__='{0:s}_tag'.format(self.__tablename__),
                parent_id=db.Column(db.Integer, db.ForeignKey('{0:s}.id'.format(self.__tablename__))),
                parent=db.relationship(self)))
        return db.relationship(self.Tag)


class StatusMixin(object):
    @declared_attr
    def statuses(self):
        self.Status = type(
            '{}_Status'.format(self.__name__),
            (Status, db.Model),
            dict(
                __tablename__='{0:s}_status'.format(self.__tablename__),
                parent_id=db.Column(db.Integer, db.ForeignKey('{0:s}.id'.format(self.__tablename__))),
                parent=db.relationship(self)))
        return db.relationship(self.Status)

    def set_status(self, status):
        """
        Set status on object. Although this is a many-to-many db.relationship
        this makes sure that the parent object only has one status set.

        :param status: Name of the status
        """
        for _status in self.statuses:
            self.statuses.remove(_status)
        self.statuses.append(self.Status(user=None, status=status))
        db.session.commit()

    @property
    def get_status(self):
        """Get the current status.


        :return The status as a db.String
        """
        if not self.statuses:
            self.statuses.append(self.Status(user=None, status='new'))
        return self.statuses[0]


class CommentMixin(object):

    @declared_attr
    def comments(self):
        self.Comment = type(
            '{}_Comment'.format(self.__name__),
            (Comment, db.Model),
            dict(
                __tablename__='{0:s}_comment'.format(self.__tablename__),
                parent_id=db.Column(db.Integer, db.ForeignKey('{0:s}.id'.format(self.__tablename__))),
                parent=db.relationship(self)))
        return db.relationship(self.Comment)
