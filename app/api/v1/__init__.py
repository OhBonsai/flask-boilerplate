# coding=utf-8
# Created by OhBonsai at 08/03/18.
"""API V1 Blueprint"""

from flask import Blueprint
from flask_restful import Api
from app.api.cors import cors
from .route import API_ROUTES
from app.api.errors import register_error_handler


def register_api(app):
    """
    :param app: flask.Flask app
    """

    @app.before_request
    def require_something():
        # Do something before request in this method
        pass

    @app.after_request
    def change_something(response):
        return response

    cors.init_app(app)
    register_error_handler(app)

    api_v1_bp = Blueprint('api_v1', __name__)
    api_v1 = Api(api_v1_bp, prefix='/api/v1', catch_all_404s=True)
    for r in API_ROUTES:
        api_v1.add_resource(*r)

    app.register_blueprint(api_v1_bp)
