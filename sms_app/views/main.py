from flask import Blueprint, render_template, redirect, url_for

from sms_app.extensions import mongo

main = Blueprint('main', __name__)

menu = {
    "Devices": "devices",
    "Data" : "data"
}
        

@main.context_processor
def populate_menu():
    return dict(menu = menu)

@main.route('/')
def mainpage():
    return redirect(url_for('main.devicespage'))

@main.route('/devices')
def devicespage():
    devices_collection = mongo.db.devices
    devices = devices_collection.find()
    return render_template('devices.html', devices=devices)

@main.route('/data')
def datapage():
    return render_template('data.html')