# coding=utf-8
# Created by OhBonsai at 08/03/18.
"""API V1 Blueprint"""

from flask import Blueprint
from app.core.error import WithErrorHandlerApi
from app.api.cors import cors
from .route import API_ROUTES


def register_api(app):
    """
    :param app: flask.Flask app
    """

    @app.before_request
    def require_something():
        # Do something before request in this method
        pass

    cors.init_app(app)
    api_v1_bp = Blueprint('api_v1', __name__)
    api_v1 = WithErrorHandlerApi(api_v1_bp, prefix='/api/v1')
    for r in API_ROUTES:
        api_v1.add_resource(*r)

    app.register_blueprint(api_v1)
