from flask import Blueprint

bp = Blueprint('auth', __name__)

from sms_app.auth import routes