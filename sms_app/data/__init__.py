from flask import Blueprint

bp = Blueprint('data', __name__)

from sms_app.data import routes