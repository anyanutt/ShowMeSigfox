from flask import Blueprint, request

from sms_app.extensions import mongo

data = Blueprint('data', __name__)

@data.route('/uplink', methods=['POST'])
def add_message():
    messages_collection = mongo.db.messages
    content = request.json
    messages_collection.insert_one(content)
    return ('', 200)