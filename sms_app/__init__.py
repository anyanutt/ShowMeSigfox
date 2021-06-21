from flask import Flask, Blueprint

from .extensions import mongo
from sms_app.views.main import main
from sms_app.views.home import home

def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)
    print(app.config)

    mongo.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(home)

    return app