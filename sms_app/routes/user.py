from flask import Blueprint, render_template, redirect, url_for, jsonify
from bson.objectid import ObjectId
import datetime

from sms_app.extensions import mongo 
from sms_app.functions import timeToStr, sortTimeAsc, sortTimeDec

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
    devices_cursor = devices_collection.find()
    devices = []
    for i in devices_cursor:
        if 'lastseen' in i:
            i['lastseen'] = timeToStr(i['lastseen'])
        else:
            i['lastseen'] = 'No last Activity'
        devices.append(i)
    return render_template('devices.html', devices=devices)

@user.route('/devices/<oid>')
def device_idv_page(oid):
    devices_collection = mongo.db.devices
    device = devices_collection.find_one({ '_id' : ObjectId(oid) })
    if 'lastseen' in device:
        device['lastseen'] = timeToStr(device['lastseen'])
    else:
        device['lastseen'] = 'No last Activity'

    messages_collection = mongo.db.messages
    messages_cursor = messages_collection.find({ 'sigfox_id' : device['sigfox_id'] })
    messages = []
    for i in messages_cursor:
        i['time'] = timeToStr(i['time'])
        messages.append(i)
    messages = sortTimeDec(messages)

    fields = []
    if len(messages) > 0:
        fields = messages[0].keys()

    variables_collection = mongo.db.variables
    variables = variables_collection.find({ 'dev_id' : oid })

    return render_template('dev_idv.html', device=device, messages=messages, fields=fields, variables=variables)

@user.route('/data')
def datapage():
    return render_template('data.html')

@user.route('/account')
def accountpage():
    return render_template('data.html')