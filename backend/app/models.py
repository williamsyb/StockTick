# -*- coding: utf-8 -*-
# @Time    : 2018/10/30 17:26
# @Author  : Yibin Sun
# @File    : models.py
# @Software: PyCharm
from .extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return 'ID:{} - {}'.format(self.id, self.username)

