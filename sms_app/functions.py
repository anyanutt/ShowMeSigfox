import secrets
import datetime

def createToken():
    return secrets.token_urlsafe(32)

def timeToStr(time):
    return datetime.datetime.fromtimestamp(int(time)).strftime('%Y-%m-%d %H:%M:%S')

def sortTimeKey(e):
    return e['time']

def sortTimeAsc(list):
    return sorted(list, key=sortTimeKey)

def sortTimeDec(list):
    return sorted(list, reverse=True, key=sortTimeKey)