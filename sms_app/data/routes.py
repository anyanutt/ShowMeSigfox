from flask import render_template, flash, redirect, url_for, request

from sms_app.data import bp

from sms_app.models import Message

@bp.route('/uplink', methods=['POST'])
def uplink():
    if Message.register(request.json):
        return ('Success', 200)
    return ('Bad Request', 400)