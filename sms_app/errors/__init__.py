from flask import Blueprint

bp = Blueprint('errors', __name__)

from sms_app.errors import handlers