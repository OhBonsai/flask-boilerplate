# coding=utf-8
# Created by OhBonsai at 2018/3/13

import base64

from werkzeug.datastructures import Headers


def auth_for(user):
    return basic_auth(user.username, user.password)


def basic_auth(username, password):
    headers = Headers()
    headers.add('Authorization', 'Basic ' + base64.b64encode(username + ':' + password))
    return headers
