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

        schema = {'code': status_code, 'success': False, 'result': [], 'meta': meta}

        if model:
            if not model_fields:
                try:
                    model_fields = self.fields_registry[model.__tablename__]
                except AttributeError:
                    model_fields = self.fields_registry[model[0].__tablename__]
            schema['result'] = [marshal(model, model_fields)]
            schema['success'] = True

        response = jsonify(schema)
        # Axios can't capture other status_code except 200 :(
        response.status_code = 200
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
        """Handles GET request to post.

        :return List of posts (instance of flask.wrappers.Response)
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

        :return A post in JSON (instance of flask.wrappers.Response)
        """
        pass


class ApiVersionResource(Resource):
    """Resource for api version."""

    @staticmethod
    def get():
        """Handles GET request to api version.

        :return Api version in JSON
        """
        response = jsonify({
            'api_version': 'v1'
        })
        response.status_code = HTTP_STATUS_CODE_OK
        return response
