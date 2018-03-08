# coding=utf-8
# Created by OhBonsai at 2018/3/8
"""This module implements common exception handler"""

from flask_restful import Api
import logging

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

    def __init__(self):
        super(BaseError, self).__init__()
        exception_logger.info(self.message)

    @property
    def data(self):
        return {'code': self.status, 'result': self.message}


class InstanceNotFound(Exception):
    code = 404
    prefix = "Can't found"

    def __init__(self, pk='', model=''):
        self.message = "{} {} which pk is {}!".format(self.prefix, model, pk)
        super(InstanceNotFound, self).__init__()
