"""This module implements the models for the Blog core system."""


import json

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
from sqlalchemy.orm import relationship


from app.models import BaseModel
from app.models.acl import AccessControlMixin
from app.models.patch import CommentMixin
from app.models.patch import StatusMixin


class Post(AccessControlMixin, StatusMixin, CommentMixin, BaseModel):
    """Implements the Post model.
    """

    title = Column(String(32))
    sub = Column(String(128))
    user_id = Column(Integer, ForeignKey(u'user.id'))
    user = relationship('User', backref='posts', lazy='select')
    content = Column(Text())

    def __init__(self, title, sub, user, content):
        """Initialize the Sketch object.

        Args:
        :param title: The title of the post
        :param sub: The subtitle of the post
        :param user: A user
        :param content: Content String
        """
        super(Post, self).__init__()
        self.title = title
        self.sub = sub
        self.user = user
        self.content = content

    def __repr__(self):
        return self.title
