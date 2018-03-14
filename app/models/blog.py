"""This module implements the models for the Blog core system."""

from app.models.acl import AccessControlMixin
from app.models.patch import CommentMixin, StatusMixin, TagMixin
from app.models import db


class Post(AccessControlMixin, StatusMixin, CommentMixin, TagMixin, db.Model):
    """Implements the Post model.
    """

    title = db.Column(db.String(32))
    sub = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey(u'user.id'))
    user = db.relationship('User', backref='posts', lazy='select')
    content = db.Column(db.Text())

    def __init__(self, title, sub, user, content):
        """Initialize the Sketch object.

        Args:
        :param title: The title of the post
        :param sub: The subtitle of the post
        :param user: A user
        :param content: Content db.String
        """
        super(Post, self).__init__()
        self.title = title
        self.sub = sub
        self.user = user
        self.content = content

    def __repr__(self):
        return self.title
