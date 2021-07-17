from flask import Blueprint

bp = Blueprint('main', __name__)

from sms_app.main import routes