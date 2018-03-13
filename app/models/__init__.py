# coding=utf-8
# Created by OhBonsai at 2018/3/7
"""This package handles setting up and providing the database connection."""

from flask_login import current_user
from flask_sqlalchemy import BaseQuery, SQLAlchemy, Model
from flask_restful import reqparse
from sqlalchemy import (
    Column,
    DateTime,
    func,
    Integer
)
from sqlalchemy.ext.declarative import declared_attr
from app.api.errors import NoPermission


class AclBaseQuery(BaseQuery):
    """query_cls = AclBaseQuery. So All query in orm will execute get_with_acl"""

    def get_with_acl(self, model_id):
        """ Get a instance with permission

        :param model_id:  the integer pk id of model
        :return: model instance
        """

        obj = self.get(model_id)
        if not obj:
            raise LookupError
        try:
            if obj.get_status.status == 'deleted':
                raise LookupError
        except AttributeError:
            # It doesn't matter when model hadn't status field
            pass
        if obj.is_public:
            return obj
        if not obj.has_permission(user=current_user, permission='read'):
            raise NoPermission
        return obj


class Pager(object):
    """Util for paginate"""

    parser = reqparse.RequestParser()\
        .add_argument('page', type=int, default=1, store_missing=True)\
        .add_argument('size', type=int, default=10, store_missing=True)

    def __init__(self, page, count, size):
        self.count = count
        self.size = size
        self.page = page
        self.offset = (page - 1) * size

    @classmethod
    def paginate(cls, query):
        params = cls.parser.parse_args()

        count = query.count()
        page = params.get('page')
        size = params.get('size')

        pager = cls(page, count, size)
        return query.limit(size).offset(pager.offset), pager

    @property
    def args(self):
        return {
            'total': self.count,
            'size': self.size,
            'page': self.page,
            'offset': self.offset
        }


class BaseModel(Model):
    """Base class of models, It adds common models which are `id`, `created_at`, `updated_at`
    And provide common method  `get_or_create`
    """

    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(), default=func.now())
    updated_at = Column(DateTime(), default=func.now(), onupdate=func.now())

    @classmethod
    def get_or_create(cls, **kwargs):
        """Get or create a database object.

        :param kwargs: model field:value dict
        :return: a model instance
        """

        instance = cls.query.filter_by(**kwargs).first()
        if not instance:
            instance = cls(**kwargs)
            db.session.add(instance)
            db.session.commit()
        return instance

    @classmethod
    def get(cls, id):
        return cls.query().get(id)

    @classmethod
    def exists(cls, **kw):
        return cls.query(**kw).first() is not None

    def apply_kwargs(self, kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

        return self

db = SQLAlchemy(model_class=BaseModel,
                query_class=AclBaseQuery,
                session_options=dict(expire_on_commit=False))

from .user import User, Group
from .blog import Post
