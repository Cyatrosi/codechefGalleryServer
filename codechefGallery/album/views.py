from django.shortcuts import render
from django.utils.html import escape
from django.http import HttpResponse, JsonResponse
import os
import sys
import json
from datetime import datetime, date
from bson import ObjectId
from codechefGallery import upload
from codechefGallery.model.album import album
from codechefGallery.model.photos import photos
from django import forms
from django.core.files.storage import FileSystemStorage
from django.utils.safestring import mark_safe
from django.template import Context

albumModel = album()
photosModel = photos()
# ====== Util Functions =====


class NameForm(forms.Form):
    file = forms.CharField(label='file', max_length=10000000)


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
        res = res.replace("\"", "")
        res = res.replace("\\", "")
    else:
        res = None
    return res


def scanRequest(request, userId=None):
    if userId:
        if request.method == 'GET':
            return getAlbum(request, userId)
        elif request.method == 'POST':
            return updateAlbum(request, userId)
        elif request.method == 'POST':
            return updateAlbum(request, userId)
        elif request.method == 'DELETE':
            return deleteAlbum(request, userId)
        else:
            return errorResp('Invalid request method')
    else:
        if request.method == 'GET':
            return getAllAblums(request)
        elif request.method == 'POST':
            return createAlbum(request)
        else:
            return errorResp('Invalid request method')


def filterParams(request, isNew=True):
    if isNew:
        body = {}
        if request.method == 'GET':
            body = dict(request.GET.dict())
        elif request.method == 'POST':
            body = {}
            if 'userId' in request.POST:
                body['userId'] = request.POST['userId']
            if 'name' in request.POST:
                body['name'] = request.POST['name']
            if 'desc' in request.POST:
                body['desc'] = request.POST['desc']
            if 'access' in request.POST:
                body['access'] = request.POST['access']
            if 'file' in request.FILES:
                myfile = request.FILES['file']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
                body['file'] = uploaded_file_url
        elif request.method == 'PUT':
            body = {}
            print("Body:", request.POST)
            if 'name' in request.POST:
                body['name'] = request.POST['name']
            if 'desc' in request.POST:
                body['desc'] = request.POST['desc']
            if 'access' in request.POST:
                body['access'] = request.POST['access']
            if 'file' in request.FILES:
                myfile = request.FILES['file']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
                body['file'] = uploaded_file_url
        elif request.method == 'DELETE':
            ReqBody = request.body.decode('utf-8')
            if ReqBody:
                body = json.loads(ReqBody)
            else:
                body = {}
        else:
            body = {}
    else:
        if request.method == 'POST':
            body = {}
            print("Body:", request.POST)
            if 'name' in request.POST:
                body['name'] = request.POST['name']
            if 'desc' in request.POST:
                body['desc'] = request.POST['desc']
            if 'access' in request.POST:
                body['access'] = request.POST['access']
            if 'file' in request.FILES:
                myfile = request.FILES['file']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
                body['url'] = uploaded_file_url
    return body


def createResponse(statusCode, msg, data):
    return JsonResponse(dict(status=statusCode, message=msg, data=data))


def errorResp(msg):
    return JsonResponse(dict(status=400, message=msg, data=[]))


def ObId(id):
    try:
        return ObjectId(id), "OK"
    except Exception as e:
        return None, "Invalid Id"

# ====== Main Functions =====


def getAllAblums(request):
    params = filterParams(request)
    start = 0
    limit = 50
    if 'start' in params:
        start = int(params['start'])
    if 'limit' in params:
        limit = int(params['limit'])
    res, msg = albumModel.getAllAlbums(start, limit)
    res = json.loads(res)
    if res:
        '''
        context = {
            'data':res
        }
        return render(request,'dash.html',context)
        '''
        return createResponse(200, 'OK', res)
    return errorResp(msg)


def getAlbum(request, userId):
    OId, msg = ObId(userId)
    if not OId:
        return errorResp(msg)
    res, msg = albumModel.getAlbum(OId)
    if res: 
        res = json.loads(res)
        res['albumId']=res['_id']
        context = dict({'data': res, "albumId": res['_id']})
        return render(request, 'album.html', context)
        # return createResponse(200,'OK',res)
    return errorResp(msg)


def updateAlbum(request, albumId):
    body = filterParams(request, False)
    if 'owner' in body or 'datetime' in body:
        return errorResp("forbidden values sent")
    OId, msg = ObId(albumId)
    if not OId:
        return errorResp(msg)
    if 'url' in body:
        filePath = body['url']
        objUrl, ermsg = upload.uploadPhoto(albumId, filePath)
    else:
        objUrl=True
    if objUrl:
        if 'url' in body:
            body['url']=objUrl
        res, msg = albumModel.updateAlbum(OId, body)
        if res:
            return createResponse(200, 'Album Updated', [])
        return errorResp(msg)
    return errorResp(ermsg)


def createAlbum(request):
    body = filterParams(request)
    if 'userId' not in body:
        return errorResp("User ID Missing")
    if 'name' not in body:
        return errorResp("Name Missing")
    if 'access' not in body:
        return errorResp("access Missing")
    if 'desc' not in body:
        return errorResp("Description Missing")
    if 'file' not in body:
        return errorResp("Cover Photo Missing")
    userId = body['userId']
    filePath = body['file']
    objUrl, ermsg = upload.uploadPhoto(userId, filePath)
    if objUrl:
        location = None
        if 'location' in body:
            location = body['location']
        doc = {"name": body['name'], "access": "public", "likes": [], "url": objUrl,
               "desc": body['desc'], "datetime": datetime.now(), "location": location, "owner": userId}
        res, msg = albumModel.insertAlbum(doc)
        return createResponse(200, 'Ablum Created', [ObjectIdToStr(res)])
    else:
        return errorResp(ermsg)

def deleteAlbum(request,albumId):
    OId, ermsg = ObId(albumId)
    if not OId:
        return errorResp(ermsg)
    res, msg = albumModel.deleteAlbum(OId)
    if res:
        res2,msg2 = photosModel.deleteAlbumPhoto(albumId)
        print("RES:",res,msg2)
        if res2 or res==0:
            return createResponse(200, 'Album Deleted with all photos', {"deleted_cnt":res})
        return createResponse(200, 'Album Deleted without all photos', {"deleted_cnt":res})
    elif res == 0:
        return createResponse(200, 'No such Album exists', [])
    else:
        return errorResp(msg)

# ====== API ENDPOINTS ======


def index(request):
    return scanRequest(request)

def albums(request, userId):
    return scanRequest(request, userId)

def my(request):
    params = filterParams(request)
    start = 0
    limit = 50
    if 'start' in params:
        start = int(params['start'])
    if 'limit' in params:
        limit = int(params['limit'])
    res, msg = albumModel.getMyAlbums(params['userId'], start, limit)
    res = json.loads(res)
    if res or res == {} or res == []:
        return createResponse(200, 'OK', res)
    return errorResp(msg)
