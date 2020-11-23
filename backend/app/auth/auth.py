# -*- coding: utf-8 -*-
# @Time    : 2018/11/29 17:37
# @Author  : Yibin Sun
# @File    : auth.py
# @Software: PyCharm

from functools import wraps
from flask import g, current_app, request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from app.auth.errors import api_abort, invalid_token, token_missing
from app.models import User


def generate_token(user):
    expiration = 3600
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    token = s.dumps({'id': user.id}).decode('ascii')
    return token, expiration


def validate_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except (BadSignature, SignatureExpired):
        return False
    user = User.query.get(data['id'])
    if user is None:
        return False
    g.current_user = user
    return True


def get_token():
    # print('get_token. headers:', request.headers)
    if 'Authorization' in request.headers:
        try:
            # print("request.headers['Authorization']:", request.headers['Authorization'])
            token_type, token = request.headers['Authorization'].split(None, 1)
            # print('token_type:{}, token:{}'.format(token_type, token))
        except ValueError:
            token_type = token = None
    else:
        token_type = token = None

    return token_type, token


def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token_type, token = get_token()
        if request.method != 'OPTIONS':
            if token_type is None or token_type.lower() != 'bearer':
                return api_abort(400, 'The token type must be bearer')
            if token is None:
                return token_missing()
            if not validate_token(token):
                return invalid_token()
        return f(*args, **kwargs)

    return decorated
