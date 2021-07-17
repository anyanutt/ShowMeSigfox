from flask import Flask
from config import Config

from sms_app.extensions import mongo, login, mail, bootstrap, moment

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    mongo.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    
    from sms_app.auth import bp as auth
    app.register_blueprint(auth, url_prefix='/auth')
    
    from sms_app.errors import bp as errors
    app.register_blueprint(errors)
    
    from sms_app.main import bp as main
    app.register_blueprint(main)

    from sms_app.data import bp as data
    app.register_blueprint(data)

    app.jinja_env.cache = {}

    return app