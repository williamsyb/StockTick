# -*- coding:UTF-8 -*-
import logging

import yaml
from flask import Flask, request
from .config import Config
from .models import User
import os
from logging.handlers import RotatingFileHandler
from .extensions import cors, db
from app.apis.v1.resources import api_v1
from app.auth.views import auth_bp

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    # if config_name is None:
    #     config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('stock')
    app.config.from_object(Config)

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    return app


def register_blueprints(app):
    modules = (
        (api_v1, '/api/v1'),
        (auth_bp, '/auth')
    )
    for _blue_print, url_prefix in modules:
        app.register_blueprint(_blue_print, url_prefix=url_prefix)


def register_extensions(app):
    cors.init_app(app, supports_credentials=True, resources={r"/*": {'origins': '*'}})
    db.init_app(app)


def register_logging(app):
    class RequestFormatter(logging.Formatter):

        def format(self, record):
            record.url = request.url
            record.remote_addr = request.remote_addr
            return super(RequestFormatter, self).format(record)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = RotatingFileHandler(os.path.join(basedir, 'log/stock_bar.log'),
                                       maxBytes=10 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # if not app.debug:
    app.logger.addHandler(file_handler)


def read_yaml(config_name, config_path):
    """
    config_name:需要读取的配置内容
    config_path:配置文件路径
    """
    if config_name and config_path:
        with open(config_path, 'r', encoding='utf-8') as f:
            conf = yaml.safe_load(f.read())
        if config_name in conf.keys():
            return conf[config_name.upper()]
        else:
            raise KeyError('未找到对应的配置信息')
    else:
        raise ValueError('请输入正确的配置名称或配置文件路径')
