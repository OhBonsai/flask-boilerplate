# coding=utf-8
# Created by OhBonsai at 2018/3/8
"""This module holds app model schema."""


from marshmallow.fields import (
    Integer,
    Function,
    DateTime,
    Nested
)
from marshmallow.validate import (
    Length
)

from app.schema.plus import String, Schema, NotEmpty


class StatusSchema(Schema):
    id = Integer(dump_only=True)
    created_at = DateTime(dump_only=True)
    updated_at = DateTime(dump_only=True)

    status = String(strip=True, validate=Length(max=16))


class CommentSchema(Schema):
    id = Integer(dump_only=True)
    created_at = DateTime(dump_only=True)
    updated_at = DateTime(dump_only=True)

    comment = String(strip=True, validate=Length(max=1024))


class TagSchema(Schema):
    id = Integer(dump_only=True)
    created_at = DateTime(dump_only=True)
    updated_at = DateTime(dump_only=True)

    tag = String(strip=True, validate=Length(max=16))


class PostSchema(Schema):
    id = Integer(dump_only=True)
    created_at = DateTime(dump_only=True)
    updated_at = DateTime(dump_only=True)

    author = Function(lambda o: o.user.name)
    title = String(required=True, strip=True, validate=[NotEmpty(), Length(min=1, max=32)])
    sub = String(required=True, strip=True, validate=Length(max=128))
    content = String(required=True, validate=NotEmpty())

    comments = Nested(CommentSchema, only=('created_at', 'comment', 'updated_at'), many=True)
    # status = Nested(StatusSchema, only=('created_at', 'comment'), many=True)

