from flask import Blueprint, render_template, redirect, url_for, jsonify
from bson.objectid import ObjectId

from sms_app.extensions import mongo

user = Blueprint('user', __name__)

""" might still come in handy
@user.context_processor
def populate_menu():
    return dict(menu = menu)
"""

@user.route('/')
def mainpage():
    return redirect(url_for('user.devicespage'))

@user.route('/devices')
def devicespage():
    devices_collection = mongo.db.devices
    devices = devices_collection.find()
    return render_template('devices.html', devices=devices)

@user.route('/devices/<oid>')
def device_idv_page(oid):
    devices_collection = mongo.db.devices
    messages_collection = mongo.db.messages
    device = devices_collection.find_one({ '_id' : ObjectId(oid) })
    messages_cur = messages_collection.find( { 'dev_id' : device['dev_id']} )
    messages = []
    for i in messages_cur:
        messages.append(i)
    return render_template('dev_idv.html', device=device, messages=messages)

@user.route('/data')
def datapage():
    return render_template('data.html')