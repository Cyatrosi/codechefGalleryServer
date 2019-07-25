from django.shortcuts import render
from django.utils.html import escape
from django.http import HttpResponse,JsonResponse
import os, sys, json
from datetime import datetime, date
from bson import ObjectId
from codechefGallery import upload
from codechefGallery.model.users import users
from django import forms
from django.core.files.storage import FileSystemStorage

usersModel = users()
## ====== Util Functions =====

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, (date, datetime)):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)

def ObjectIdToStr(id):
    if id:
        res = JSONEncoder().encode(id)
        res = res.replace("\"","")
        res = res.replace("\\","")
    else:
        res = None
    return res

def scanRequest(request,userId=None):
    if userId:
        if request.method == 'PUT':
            return updateUser(request,userId)
        elif request.method == 'GET':
            return userInfo(request,userId)
        elif request.method == 'DELETE':
            return deleteUser(request,userId)
        else:
            return errorResp('Invalid request method')
    else:
        if request.method == 'POST':
            return createUser(request)
        elif request.method == 'GET':
            return allUsers(request)
        else:
            return errorResp('Invalid request method')
    
def filterParams(request):
    if request.method == 'GET':
        body = dict(request.GET.dict())
    elif request.method == 'POST' and 'file' in request.FILES and request.FILES['file']:
        body={}
        username = request.POST['username']
        gender= request.POST['gender']
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
    elif request.method in ['POST','PUT','DELETE']:
        ReqBody = request.body.decode('utf-8')
        if ReqBody:
            body = json.loads(ReqBody)
        else:
            body = {}
    else:
        body = {}
    return body

def createResponse(statusCode,msg,data):
    return JsonResponse(dict(status=statusCode,message=msg,data=data))

def errorResp(msg):
    return JsonResponse(dict(status=400,message=msg,data=[]))

def ObId(id):
    try:
        return ObjectId(id),"OK"
    except Exception as e:
        return None,"Invalid Id"

## ====== Main Functions =====
def createUser(request):
    body = filterParams(request)
    userName = body['username']
    filePath = body['dp']
    objUrl,ermsg = upload.uploadPhoto(userName,filePath)
    if objUrl:  
        body['dp']=objUrl
        res,msg = usersModel.insertUser(body)
        if res:
            return createResponse(200,'User Registered Successfully',[])
        return errorResp(msg)
    else:
        return errorResp(ermsg)

def allUsers(request):
    params = filterParams(request)
    start = 0
    limit = 10
    if 'start' in params:
        start = int(params['start'])
    if 'limit' in params:
        limit = int(params['limit'])
    res,msg = usersModel.getUsersList(start,limit)
    res = json.loads(res)
    if res:
        return createResponse(200,'Users List',res)
    return errorResp(msg)

def updateUser(request,userId):
    body = filterParams(request)
    OId,msg = ObId(userId)
    if not OId:
        return errorResp(msg)
    res,msg = usersModel.updateUser(OId,body)
    if res:
        return createResponse(200,'User Updated',[])
    return errorResp(msg)

def userInfo(request,userId):
    OId,msg = ObId(userId)
    if not OId:
        return errorResp(msg)
    res,msg = usersModel.getUserInfo(OId)
    res = json.loads(res)
    if res:
        context = {
            'data':res
        }
        return render(request,'me.html',context)
        #return createResponse(200,'User Info',res)
    return errorResp(msg)

def deleteUser(request,userId):
    OId,msg = ObId(userId)
    if not OId:
        return errorResp(msg)
    res,msg = usersModel.deleteUser(OId)
    if res:
        return createResponse(200,'User Deleted',res)
    elif res == 0:
        return createResponse(200,'User not found',[])
    return errorResp(msg)

## ====== API ENDPOINTS ======

def index(request):
    return scanRequest(request)

def user(request,userId):
    return scanRequest(request,userId)

def login(request):
    body = filterParams(request)
    if 'username' not in body:
        return errorResp("username missing")
    if 'password' not in body:
        return errorResp("password missing")    
    res,msg = usersModel.validateUser(body['username'],body['password'])
    if res == 'null':
        return errorResp("No such user exists")    
    if res:
        res = json.loads(res)
        return createResponse(200,'User Login Successfully',res)
    return errorResp(msg)

