from time import time
import jwt
import bcrypt
from bson.objectid import ObjectId
from flask import current_app
from flask_login import UserMixin

from sms_app import mongo, login
from sms_app.functions import timeToStr, sortTimeDec

@login.user_loader
def load_user(email):
    u = User.get_by_email(email)
    if not u:
        return None
    return u

class User(UserMixin):
    collection = mongo.db.users

    def __init__(self, email, password, verified=False, **kwargs):
        self.email = email
        self.password = password
        self.verified = verified

    def get_id(self):
        return self.email

    @staticmethod
    def gen_password(string):
        return bcrypt.hashpw(string.encode('utf-8'), bcrypt.gensalt())

    @classmethod
    def get_by_email(cls, email):
        data = cls.collection.find_one({ 'email' : email})
        if data:
            return cls(**data)

    @classmethod
    def get_by_id(cls, _id):
        data = cls.collection.find_one({ '_id' : _id })
        if data:
            return cls(**data)

    @classmethod
    def login_valid(cls, email, password):
        verify_user = cls.get_by_email(email)
        if verify_user:
            return bcrypt.checkpw(password.encode('utf-8'), verify_user.password)
        return False

    @classmethod
    def register(cls, email, password):
        user = cls.get_by_email(email)
        if user is None:
            new_user = cls(email, cls.gen_password(password), False)
            new_user.add_user()
            return True
        else:
            return False

    @classmethod
    def verify(cls, email):
        user = cls.get_by_email(email)
        user.verified = True
        cls.collection.update_one({'email': user.email},  {"$set": { "verified": user.verified }} )

    @staticmethod
    def remove(_id):
        devices = Device.get_list_by_uid(_id)
        for device in devices:
            Device.delete_device(device['_id'])
        User.delete_user(_id)
        return True

    def reset_password(self, password):
        self.password = self.gen_password(password)
        self.collection.update_one({'email': self.email},  {"$set": { "password": self.password }} )

    def get_reset_password_token(self, expiration=600):
        return jwt.encode(
            {'reset_password': self.email, 'exp': time() + expiration},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            email = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.get_by_email(email)

    def jsonify(self):
        return {
            "email" : self.email,
            "password" : self.password,
            "verified" : self.verified
        }

    def add_user(self):
        self.collection.insert_one(self.jsonify())

    @staticmethod
    def delete_user(_id):
        User.collection.delete_one({ '_id' : ObjectId(_id) })

class Device:
    collection = mongo.db.devices

    def __init__(self, sigfox_id, dev_name, user_id):
        self.sigfox_id = sigfox_id
        self.dev_name = dev_name
        self.user_id = user_id
    
    @classmethod
    def register(cls, sigfox_id, dev_name, user_id):
        device = cls(sigfox_id, dev_name, user_id)
        device.add_device()
        return True

    @staticmethod
    def remove(_id):
        Message.delete_messages_by_id(_id)
        Variable.delete_variables_by_id(_id)
        Device.delete_device(_id)        
        return True
    
    def jsonify(self):
        return {
            "sigfox_id" : self.sigfox_id,
            "dev_name" : self.dev_name,
            "user_id" : self.user_id
        }

    def add_device(self):
        self.collection.insert_one(self.jsonify())

    @staticmethod
    def delete_device(_id):
        Device.collection.delete_one({ '_id' : ObjectId(_id) })

    @staticmethod
    def get_by_id(_id):
        device = Device.collection.find_one({ '_id' : ObjectId(_id) })
        if device:
            if 'lastseen' in device:
                device['lastseen'] = timeToStr(device['lastseen'])
            else:
                device['lastseen'] = 'No last Activity'
        return device

    @staticmethod
    def get_by_sid(sid):
        device = Device.collection.find_one({ 'sigfox_id' : sid })
        if device:
            if 'lastseen' in device:
                device['lastseen'] = timeToStr(device['lastseen'])
            else:
                device['lastseen'] = 'No last Activity'
        return device

    @staticmethod
    def get_cursor_by_uid(uid):
        return Device.collection.find({ 'user_id' : str(uid) })

    @staticmethod
    def get_list_by_uid(uid):
        curs = Device.get_cursor_by_uid(uid)
        devices = []
        for i in curs:
            if 'lastseen' in i:
                i['lastseen'] = timeToStr(i['lastseen'])
            else:
                i['lastseen'] = 'No last Activity'
            devices.append(i)
        return devices

class Dashboard:
    collection = mongo.db.dashboards

    choices = [('var1', 'Phase 1 power (BEE62D)'), ('var1', 'Phase 3 power (BEE62D)')]

    def __init__(self, dash_name, user_id):
        self.dash_name = dash_name
        self.user_id = user_id

    @classmethod
    def register(cls, dash_name, user_id):
        new_dash = cls(dash_name, user_id)
        new_dash.add_dashboard()
        return True
    
    def jsonify(self):
        return {
            "name" : self.dash_name,
            "user_id" : self.user_id
        }

    def add_dashboard(self):
        self.collection.insert_one(self.jsonify())
    
    @staticmethod
    def get_by_id(_id):
        dashboard = dashboard.collection.find_one({ '_id' : ObjectId(_id) })
        return dashboard

    @staticmethod
    def get_cursor_by_uid(uid):
        return Dashboard.collection.find({ 'user_id' : str(uid) })

class Variable:
    collection = mongo.db.variables

    aggregation = [('none', 'None'), ('avg', 'Average'), ('min', 'Minimum'), ('max', 'Maximum'), ('sum', 'Sum'), ('count', 'Count')]
    expression = [('times', 'times'), ('div', 'divide'), ('add', 'add'), ('sub', 'subtract')]

    def __init__(self, var_name, dev_id):
        self.var_name = var_name
        self.dev_id = dev_id

    @classmethod
    def register(cls, var_name, dev_id):
        variable = cls(var_name, dev_id)
        variable.add_variable()
        return True

    def add_variable(self):
        self.collection.insert_one(self.jsonify())

    @staticmethod
    def delete_variable(_id):
        Variable.collection.delete_one({ '_id' : ObjectId(_id) })

    @staticmethod
    def delete_variables_by_id(id):
        Variable.collection.delete_many({ 'dev_id' : id })

    @staticmethod
    def get_by_id(_id):
        variable = Variable.collection.find_one({ '_id' : ObjectId(_id) })
        return variable

    @staticmethod
    def get_cursor_by_oid(oid):
        return Variable.collection.find({ 'dev_id' : str(oid) })

    @staticmethod
    def get_list_by_oid(oid):
        curs = Variable.get_cursor_by_oid(oid)
        variables = [i for i in curs]
        return variables   

    def jsonify(self):
        return {
            "var_name" : self.var_name,
            "dev_id" : self.dev_id
        }

class Message:
    collection = mongo.db.messages

    def __init__(self, content, **kwargs):
        self.content = content

    @classmethod
    def register(cls, content):
        if 'dev_id' in content:
            sid = content['dev_id']
            device = Device.get_by_sid(sid)
            content['sigfox_id'] = str(sid)
            content['dev_id'] = str(device['_id'])
            if not 'time' in content:
                content['time'] = str(int(time()))
            new_message = cls(content)
            new_message.add_message()
            return True
        return False

    def add_message(self):
        self.collection.insert_one(self.content)

    @staticmethod
    def delete_message(_id):
        Message.collection.delete_one({ '_id' : ObjectId(_id) })

    @staticmethod
    def delete_messages_by_id(id):
        id = str(id)
        Message.collection.delete_many({ '$or': [ { 'sigfox_id' : id }, { 'dev_id' : id } ] })

    @staticmethod
    def get_cursor_by_id(id):
        id = str(id)
        return Message.collection.find({ '$or': [ { 'sigfox_id' : id }, { 'dev_id' : id } ] })

    @staticmethod
    def get_list_by_id(id):
        id = str(id)
        curs = Message.get_cursor_by_id(id)
        messages = []
        for i in curs:
            i['time'] = timeToStr(i['time'])
            messages.append(i)
        return messages

    # find fields from newest message
    @staticmethod
    def get_fields(id):
        id = str(id)
        message = Message.collection.find_one({ '$or': [ { 'sigfox_id' : id }, { 'dev_id' : id } ] }, sort=[("time", -1)],  projection={'_id': False, 'sigfox_id': False, 'dev_id': False})
        if message:
            return list(message.keys())

    
