# -*- coding: utf-8 -*-
"""This module implements common exception handler"""

from werkzeug.exceptions import HTTPException, InternalServerError
from flask import jsonify
import logging
from marshmallow import ValidationError


exception_logger = logging.getLogger('exception_logger')


class NoPermission(Exception):
    pass


class InvalidRequest(Exception):
    pass


def register_error_handler(app):
    """
    Register error handlers on the given app

    :type app: flask.Flask
    """

    @app.errorhandler(400)
    @app.errorhandler(401)
    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(405)
    @app.errorhandler(500)
    def handle_http_error(e):
        if not isinstance(e, HTTPException):
            e = InternalServerError()

        data = getattr(e, 'data', None)
        if data:
            message = data['message']
        else:
            message = e.description

        exception_logger.exception(e)
        return jsonify(message=message), e.code

    @app.errorhandler(422)
    def handle_bad_request(err):
        # webargs attaches additional metadata to the `data` attribute
        data = getattr(err, 'data')
        if data:
            # Get validations from the ValidationError object
            messages = data['exc'].messages
        else:
            messages = ['Invalid request']

        return jsonify(messages=messages), 422

    @app.errorhandler(TypeError)
    @app.errorhandler(ValueError)
    def raise_bad_request(e):
        exception_logger.exception(e)
        return jsonify(message=e.args), 400

    @app.errorhandler(LookupError)
    def raise_not_found(e):
        exception_logger.exception(e)
        return jsonify(message=e.args[0]), 404

    @app.errorhandler(AttributeError)
    def raise_some_server_error(e):
        exception_logger.exception(*e.args)
        return jsonify(message=e.args[0])

    @app.errorhandler(NoPermission)
    def raise_no_permission(e):
        exception_logger.exception(*e.args)
        return jsonify(message=e.args[0])

    @app.errorhandler(ValidationError)
    def raise_request_validate_error(e):
        exception_logger.exception(*e.args)
        return jsonify(message=e.args)

    @app.errorhandler(InvalidRequest)
    def raise_request_validate_error(e):
        exception_logger.exception(*e.args)
        return jsonify(message=e.args)
