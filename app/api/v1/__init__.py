# coding=utf-8
# Created by OhBonsai at 08/03/18.
"""API Blueprint"""

from flask_restful import Api
from flask import Blueprint

from app.api.v1.resource import (
    ApiVersion,
    PostListResource
)

api_v1_bp = Blueprint('api_v1', __name__)
api_v1 = Api(api_v1_bp)
