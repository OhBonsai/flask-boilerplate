# coding=utf-8
# Created by OhBonsai at 08/03/18.
"""This module holds version 1 of the Blog API."""

from flask import (
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
    Resource
)
from sqlalchemy import (
    desc,
    not_
)

from app.core.define import HTTP_STATUS_CODE_OK
from app.models import (
    db,
    Pager
)
from app.models.blog import Post
from app.schema.schema import PostSchema
from app.api.cache import cache
from app.api.errors import InvalidRequest, NoPermission


class ResourceMixin(object):
    """Mixin for API resources."""

    # Schemas for database model resources
    schema_registry = {
        'post': PostSchema,
    }

    def to_json(self, instance, schema=None, meta=None, status_code=HTTP_STATUS_CODE_OK):
        """Create json response from a database models.

        :param instance: Instance of a database model
        :param meta: Dictionary holding any metadata for the result
        :param schema: Schema of this model
        :param status_code: Integer used as status_code in the response

        :return Response in json format (instance of flask.wrappers.Response)
        """

        if not meta:
            meta = dict()

        result = {'status': status_code, 'success': False, 'result': None}

        if instance:
            if not schema:
                try:
                    schema = self.schema_registry[instance.__tablename__]()
                except AttributeError:
                    # if instance is list object
                    schema = self.schema_registry[instance[0].__tablename__](many=True)

            result['result'] = schema.dump(instance).data
            result['success'] = True

        if meta:
            result['meta'] = meta

        response = jsonify(result)
        # Axios can't capture other status_code except 200 :(
        response.status_code = 200
        return response


class PostDetailResource(ResourceMixin, Resource):

    @login_required
    def delete(self, pk):
        post = Post.all_with_acl().filter(
            not_(Post.Status.status == 'deleted'),
            Post.Status.parent,
            Post.id == pk).order_by(Post.updated_at.desc()).first()

        if post:
            db.session.delete(post)
            db.session.commit()
            return jsonify("delete success")

        raise NoPermission("can't delete post with out permission")


class PostListResource(ResourceMixin, Resource):
    """Resource for listing posts."""

    paginate = True

    def __init__(self):
        super(PostListResource, self).__init__()

    @cache.memoize(timeout=(60 * 60))
    @login_required
    def get(self):
        """
        @api {get} /posts Read data of posts
        @apiVersion 0.0.1
        @apiName GetPosts
        @apiGroup Post
        @apiPermission login

        @apiDescription 该<code>API</code>支持分页

        @apiSuccess {Object[]} result               List of posts.
        @apiSuccess {Number}   id                   Post id.
        @apiSuccess {String}   created_at           Post create time.
        @apiSuccess {String}   updated_at           Post update time.
        @apiSuccess {String}   title                Post tile.
        @apiSuccess {String}   sub                  Post sub title.
        @apiSuccess {String}   author               Post author name.
        @apiSuccess {String}   content              Post content list.
        @apiSuccess {Object[]} comments             Comment List
        @apiSuccess {String}   comments.comment     Comment String.
        @apiSuccess {String}   comments.created_at  Comment create time.
        @apiSuccess {String}   comments.updated_at  Comment update time.

        @apiError NotAuthenticated  Need login before access this api

        @apiErrorExample Response (example):
        HTTP/1.1 401 Not Authenticated
        {
          "code": 401,
          "success": false,
          "result": "NoAccessRight"
        }
        """

        query = Post.all_with_acl().filter(
            not_(Post.Status.status == 'deleted'),
            Post.Status.parent).order_by(Post.updated_at.desc())

        paginate_query, pager = Pager.paginate(query)
        result = self.to_json(paginate_query.all(), meta=pager.args)
        return result

    @login_required
    def post(self):
        """Handles POST request to the resource.

        Returns:
            A sketch in JSON (instance of flask.wrappers.Response)
        """
        json = request.get_json()
        if json is None:
            raise InvalidRequest("can't load your json request")

        # don't need catch ValidationError. auto return json response in error handler
        data = PostSchema().load(json).data
        post = Post(**data, user=current_user)
        post.status.append(post.Status(user=current_user, status='new'))
        post.grant_all_permission(user=current_user)
        db.session.add(post)
        db.session.commit()
        return self.to_json(post)


class ApiVersionResource(Resource):
    """Resource for api version."""

    @staticmethod
    def get():
        """
        @api {get} /version Get app information
        @apiVersion 0.0.1
        @apiName GetVersion
        @apiGroup Common
        @apiPermission none

        @apiSuccess {Object}  result     Response result.
        @apiSuccess {String}  version    Current api version.
        """
        response = jsonify({
            'version': 'v1'
        })
        response.status_code = HTTP_STATUS_CODE_OK
        return response
