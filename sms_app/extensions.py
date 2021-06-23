from flask_pymongo import PyMongo
import secrets
import datetime

mongo = PyMongo()

def createToken():
    return secrets.token_urlsafe(32)

def timeToStr(time):
    return datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')