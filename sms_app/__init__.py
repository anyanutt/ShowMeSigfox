from flask import Flask, Blueprint

from .extensions import mongo
from sms_app.routes.user import user
from sms_app.routes.home import home
from sms_app.routes.data import data

def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    mongo.init_app(app)

    app.register_blueprint(user)
    app.register_blueprint(home)
    app.register_blueprint(data)

    return app