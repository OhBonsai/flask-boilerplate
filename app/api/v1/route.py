# coding=utf-8
# Created by OhBonsai at 08/03/18.
"""URL routes for experimental API resources."""

from .resource import (
    PostListResource,
    ApiVersionResource
)


API_ROUTES = [
    (PostListResource, '/posts'),
    (ApiVersionResource, '/version')
]
