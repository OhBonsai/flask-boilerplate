# coding=utf-8
# Created by OhBonsai at 2018/3/7
"""This package handles setting up and providing the database connection."""

from flask import abort
from flask_login import current_user
from flask_sqlalchemy import BaseQuery
from sqlalchemy import (
    create_engine,
    Column,
    DateTime,
    func,
    Integer
)
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker
)
from sqlalchemy.ext.declarative import (
    as_declarative,
    declared_attr
)

from sketch.core.define import (
    HTTP_STATUS_CODE_NOT_FOUND,
    HTTP_STATUS_CODE_FORBIDDEN
)


engine = None
session_maker = sessionmaker()
db_session = scoped_session(session_maker)


def configure_engine(uri):
    """configure and setup the database session"""

    global engine, session_maker, db_session
    engine = create_engine(uri)
    db_session.remove()
    session_maker.configure(autocommit=False, autoflush=False, bind=engine, query_cls=AclBaseQuery)


def init_db():
    """Init db based on models implement BaseModel. It will setup db on the first run"""

    BaseModel.metadata.create_all(bind=engine)
    # base model query is AclBaseQuery
    BaseModel.query = db_session.query_property()
    return BaseModel


def drop_all():
    """Drop all table"""
    BaseModel.metadata.drop_all(bind=engine)


class AclBaseQuery(BaseQuery):
    """query_cls = AclBaseQuery. So All query in orm will execute get_with_acl"""

    def get_with_acl(self, model_id):
        """ Get a instance with permission

        :param model_id:  the integer pk id of model
        :return: model instance
        """

        obj = self.get(model_id)
        if not obj:
            abort(HTTP_STATUS_CODE_NOT_FOUND)
        try:
            if obj.get_status.status == 'deleted':
                abort(HTTP_STATUS_CODE_NOT_FOUND)
        except AttributeError:
            # It doesn't matter when model hadn't status field
            pass
        if obj.is_public:
            return obj
        if not obj.has_permission(user=current_user, permission='read'):
            abort(HTTP_STATUS_CODE_FORBIDDEN)
        return obj


@as_declarative()
class BaseModel(object):
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
            db_session.add(instance)
            db_session.commit()
        return instance



