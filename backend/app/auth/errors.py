# -*- coding: utf-8 -*-
# @Time    : 2018/11/29 17:48
# @Author  : Yibin Sun
# @File    : errors.py
# @Software: PyCharm

from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES
# from app.auth.views import auth_bp


def api_abort(code, message=None, **kwargs):
    if message is None:
        message = HTTP_STATUS_CODES.get(code, '')
    print('api_abort message:', message)
    response = jsonify(code=code, message=message, **kwargs)
    response.status_code = code

    return response


def invalid_token():
    response = api_abort(401, error='invalid_token', error_description='Either the token was expired or invalid')
    response.headers['WWW-Authenticate'] = 'Bearer'
    return response


def token_missing():
    response = api_abort(401)
    response.headers['WWW-Authenticate'] = 'Bearer'
    return response


class ValidationError(ValueError):
    pass





