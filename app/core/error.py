# coding=utf-8
# Created by OhBonsai at 2018/3/8
"""This module implements common exception handler"""

import logging

from flask_restful import (Api)
from marshmallow.validate import ValidationError as _ValidationError

from app.core.define import (
    HTTP_STATUS_CODE_NOT_FOUND,
    HTTP_STATUS_CODE_FORBIDDEN
)


exception_logger = logging.getLogger('exception_logger')


class WithErrorHandlerApi(Api):
    """Subclass of Api, Centralized processing exception"""

    def handle_error(self, e):
        """Rewrite Api.handle_error method.

        :param e: Exception
        :return: Json format response
        """
        if isinstance(e, BaseError):
            return self.make_response(e.data, 200)

        return self.make_response("Exception {} has not handler, args is {}".
                                  format(e.__class__, str(e.args)), 500)


class BaseError(Exception):
    status = 500

    @property
    def data(self):
        return {'status': self.status, 'success': False, 'result': self.message}


# Shall we patch marshmallow.validate.ValidationError TODO
class ValidationError(BaseError, _ValidationError):
    status = 400

    def __init__(self, *args, **kwargs):
        super(ValidationError, self).__init__(self, *args, **kwargs)
        # init self.message in ValidationError
        exception_logger.info(self.message)


class InstanceNotFound(BaseError):
    status = HTTP_STATUS_CODE_NOT_FOUND

    def __init__(self, pk='', model=''):
        self.message = "Can't found {} which pk is {}!".format(model, pk)
        exception_logger.info(self.message)


class NoPermission(BaseError):
    status = HTTP_STATUS_CODE_FORBIDDEN

    def __init__(self, pk='', model=''):
        self.message = "no permission in {} which pk is {}!".format(model, pk)
        exception_logger.info(self.message)
