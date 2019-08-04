from django.shortcuts import render, redirect
from django.utils.html import escape
import os
import sys
import json
from codechefGallery import upload
from codechefGallery import sessions as sessions
from codechefGallery.model.users import users
import codechefGallery.utils as utils
from django import forms
from django.core.files.storage import FileSystemStorage
import base64
from django.contrib import messages
from codechefGallery import macros as macros

usersModel = users()
# ===== Forms ======


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=10000000)
    password = forms.CharField(label='password', max_length=10000000)

# ====== Util Functions =====


def scanRequest(request, userId=None):
    if userId:
        if request.method == 'PUT':
            return updateUser(request, userId)
        elif request.method == 'DELETE':
            return deleteUser(request, userId)
        else:
            return utils.errorResp('Invalid request method')
    else:
        if request.method == 'POST':
            return createUser(request)
        elif request.method == 'GET':
            return allUsers(request)
        else:
            return utils.errorResp('Invalid request method')


def filterParams(request):
    if request.method == 'GET':
        body = dict(request.GET.dict())
    elif request.method == 'POST' and 'file' in request.FILES and request.FILES['file']:
        body = {}
        username = request.POST['username']
        gender = request.POST['gender']
        firstName = request.POST['first_name']
        lastName = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        body = {
            'username': username,
            'gender': gender,
            'first_name': firstName,
            'last_name': lastName,
            'email': email,
            'password': password,
            'dp': uploaded_file_url
        }
        return body
    elif request.method in ['POST', 'PUT', 'DELETE']:
        ReqBody = request.body.decode('utf-8')
        if ReqBody:
            body = json.loads(ReqBody)
        else:
            body = {}
    else:
        body = {}
    return body

# ====== Main Functions =====


def createUser(request):
    body = filterParams(request)
    userName = body['username']
    filePath = body['dp']
    objUrl, ermsg = upload.uploadPhoto(userName, filePath)
    if objUrl:
        body['dp'] = objUrl
        res, msg = usersModel.insertUser(body)
        if res:
            return utils.createResponse(200, 'User Registered Successfully', [])
        return utils.errorResp(msg)
    else:
        return utils.errorResp(ermsg)


def allUsers(request):
    params = filterParams(request)
    start = 0
    limit = 10
    if 'start' in params:
        start = int(params['start'])
    if 'limit' in params:
        limit = int(params['limit'])
    res, msg = usersModel.getUsersList(start, limit)
    res = json.loads(res)
    if res:
        return utils.createResponse(200, 'Users List', res)
    return utils.errorResp(msg)


def updateUser(request, userId):
    body = filterParams(request)
    OId, msg = utils.ObId(userId)
    if not OId:
        return utils.errorResp(msg)
    res, msg = usersModel.updateUser(OId, body)
    if res:
        return utils.createResponse(200, 'User Updated', [])
    return utils.errorResp(msg)

def deleteUser(request, userId):
    OId, msg = utils.ObId(userId)
    if not OId:
        return utils.errorResp(msg)
    res, msg = usersModel.deleteUser(OId)
    if res:
        return utils.createResponse(200, 'User Deleted', res)
    elif res == 0:
        return utils.createResponse(200, 'User not found', [])
    return utils.errorResp(msg)

# ====== API ENDPOINTS ======


def index(request):
    if 'userId' not in request.session:
        return redirect(macros.HOME,error="Session Logged Out")
    userId = request.session['userId']
    OId, msg = utils.ObId(userId)
    if not OId:
        return utils.errorResp(msg)
    res, msg = usersModel.getUserInfo(OId)
    res = json.loads(res)
    if res:
        context = {
            'data': res
        }
        return render(request, 'me.html', context)
    return utils.errorResp(msg)
    return scanRequest(request)


def user(request, userId):
    return scanRequest(request, userId)


def login(request):
    if request.method == 'POST':
        MyLoginForm = LoginForm(request.POST)
        if MyLoginForm.is_valid():
            username = MyLoginForm.cleaned_data['username']
            password = MyLoginForm.cleaned_data['password']
            res, msg = usersModel.validateUser(username, password)
            if res == 'null':
                return redirect(macros.HOME,error="No such user exists")
            if res:
                res = json.loads(res)
                userSession = "23" #sessions.openSession(res['_id'], res['username'])
                print("UserId:",res)
                request.session['username'] = username
                request.session['userId'] = res['_id']
                request.session['sessionToken'] = userSession
                return redirect(macros.DASH)
            return redirect(macros.HOME,error=msg)
        else:
            MyLoginForm = LoginForm()
            return redirect(macros.HOME,error="Invalid Form")
    else:
        return redirect(macros.HOME,error="Invalid request method")

def logout(request):
    try:
        if 'username' in request.session:
            del request.session['username']
        if 'userId' in request.session:
            del request.session['userId']
        if 'sessionToken' in request.session:
            del request.session['sessionToken']
        #del request.session
        return redirect(macros.HOME,msg="Logged out!!")
    except Exception as e:
        print("Error:",str(e))
        return redirect(macros.USER,error=str(e))
