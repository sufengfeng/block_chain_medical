# config=utf-8
import os

from flask import Flask
from flask_login import LoginManager
from common import db
from model.block_model import Block

login_manager = LoginManager()


login_manager.login_view = "user.login"


def create_app(config_filename=None):

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')

    app = Flask(__name__,static_folder=static_dir, template_folder=templates_dir)
    login_manager.init_app(app)

    if config_filename is not None:
        app.config.from_pyfile(config_filename)
        configure_database(app)


    return app


def configure_database(app):
    db.init_app(app)


