from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from datetime import datetime, date
import base64

def encodeSessionToken(sessionId,username):
    code = str(sessionId)+":"+username
    code = code.encode()
    code = base64.b64encode(code)
    return code.decode()

def decodeSessionToken(token):
    token = base64.b64decode(token)
    data = token.spllit(':')
    _sessionId = data[0]
    _userId = data[1]
    return data

def openSession(userId,username,email=None):
    u = User.objects.create_user(username=userId,email=email)
    return encodeSessionToken(u ,username)

def checkSession(userId):
    try:
        u = User.objects.get(username=userId)
        return u
    except Exception as e:
        print(" !!!! ERROR !!!!!\n",str(e))
        return False

def closeSession(username):
    return "OK" 
