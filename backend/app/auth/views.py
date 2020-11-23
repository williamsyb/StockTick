# -*- coding: utf-8 -*-
# @Time    : 2018/11/28 11:12
# @Author  : Yibin Sun
# @File    : views.py
# @Software: PyCharm

from flask import Blueprint, make_response, jsonify, request
from app.models import User
from app.extensions import db
from app.auth.auth import api_abort, generate_token
from app.auth.errors import ValidationError
import traceback

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/oauth/token', methods=['POST'])
def auth_token():
    # print(request.headers.__dict__)
    print('request:', request)
    # print(request.form.to_dict())
    grant_type = request.form.get('grant_type')
    username = request.form.get('username')
    password = request.form.get('password')
    print('grant_type:', grant_type)
    print('username:', username)
    print('password:', password)
    ip = request.remote_addr
    print('>>>>>>>>>>>> ip:{}'.format(ip))
    user_agent = request.user_agent
    print('>>>>>>>>>>>> user_agent:{}'.format(user_agent))
    print('==========================================================')
    print(request.headers)
    print('==========================================================')
    print(request.headers.get('X-Real-Ip'))
    if grant_type is None or grant_type.lower() != 'password':
        return api_abort(code=400, message='The grant type must be password')
    # print('--------------------------')
    user = User.query.filter_by(username=username).first()
    if user is None or not user.validate_password(password):
        return api_abort(code=400, message='Either the username or password was invalid')
    # print('--------------------------')

    token, expiration = generate_token(user)
    response = jsonify({
        'access_token': token,
        'token_type': 'Bearer',
        'expires_in': expiration,
        'code': 200
    })
    response.headers['Cache-Control'] = 'no-store'
    response.headers['Pragma'] = 'no-cache'
    return response


@auth_bp.errorhandler(ValidationError)
def validation_error(e):
    return api_abort(400, e.args[0])
