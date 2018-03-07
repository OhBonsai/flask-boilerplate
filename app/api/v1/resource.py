# coding=utf-8
# Created by OhBonsai at 08/03/18.
"""This module holds version 1 of the Blog API."""


from flask import (
    abort,
    current_app,
    jsonify,
    request
)
from flask_login import (
    current_user,
    login_required
)
from flask_restful import (
    fields,
    marshal,
    reqparse,
    Resource
)
from sqlalchemy import (
    desc,
    not_
)

from app.core.define import *
from app.models import db_session
from app.models.blog import Post


def bad_request(message):
    """Function to set custom error message for HTTP 400 requests.

    :param message: Message as string to return to the client.
    :return Response object (instance of flask.wrappers.Response)
    """
    response = jsonify({'message': message})
    response.status_code = HTTP_STATUS_CODE_BAD_REQUEST
    return response


class ResourceMixin(object):
    """Mixin for API resources."""
    
    # Schemas for database model resources
    user_fields = {'username': fields.String}
    
    status_fields = {
        'id': fields.Integer,
        'status': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    comment_fields = {
        'comment': fields.String,
        'user': fields.Nested(user_fields),
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }

    tag_fields = {
        'tag': fields.String,
        'user': fields.Nested(user_fields),
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }
    
    post_fields = {
        'id': fields.Integer,
        'title': fields.String,
        'user': fields.Nested(user_fields),
        'sub': fields.String,
        'content': fields.String,
        'created_at': fields.DateTime,
        'updated_at': fields.DateTime
    }
    
    fields_registry = {
        'user': user_fields,
        'post': post_fields,
        'post_comment': comment_fields,
        'post_tag': tag_fields
    }

    def to_json(self,
                model,
                model_fields=None,
                meta=None,
                status_code=HTTP_STATUS_CODE_OK):
        """Create json response from a database models.

        :param model: Instance of a database model
        :param model_fields: Dictionary describing the resulting schema
        :param meta: Dictionary holding any metadata for the result
        :param status_code: Integer used as status_code in the response

        :return Response in json format (instance of flask.wrappers.Response)
        """

        if not meta:
            meta = dict()

        schema = {'meta': meta, 'objects': []}

        if model:
            if not model_fields:
                try:
                    model_fields = self.fields_registry[model.__tablename__]
                except AttributeError:
                    model_fields = self.fields_registry[model[0].__tablename__]
            schema['objects'] = [marshal(model, model_fields)]

        response = jsonify(schema)
        response.status_code = status_code
        return response


class PostListResource(ResourceMixin, Resource):
    """Resource for listing posts."""

    def __init__(self):
        super(PostListResource, self).__init__()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('title', type=str, required=True)
        self.parser.add_argument('sub', type=str, required=False)
        self.parser.add_argument('content', type=str, required=True)

    @login_required
    def get(self):
        """Handles GET request to the resource.

        Returns:
            List of posts (instance of flask.wrappers.Response)
        """

        posts = Post.all_with_acl().filter(
            not_(Post.Status.status == 'deleted'),
            Post.Status.parent).order_by(Post.updated_at.desc())
        paginated_result = posts.paginate(1, 10, False)
        meta = {
            'next': paginated_result.next_num,
            'previous': paginated_result.prev_num,
            'offset': paginated_result.page,
            'limit': paginated_result.per_page
        }
        if not paginated_result.has_prev:
            meta['previous'] = None
        if not paginated_result.has_next:
            meta['next'] = None
        result = self.to_json(paginated_result.items, meta=meta)
        return result

    @login_required
    def post(self):
        """Handles POST request to the resource.

        Returns:
            A post in JSON (instance of flask.wrappers.Response)
        """
        pass
