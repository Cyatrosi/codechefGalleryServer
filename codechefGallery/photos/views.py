from django.shortcuts import render
from django.utils.html import escape
from django.http import HttpResponse, JsonResponse
import os
import sys
import json
from datetime import datetime, date
from bson import ObjectId
from codechefGallery import upload
from codechefGallery.model.photos import photos
from django import forms
from django.core.files.storage import FileSystemStorage

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
            return getPhoto(request, userId)
        elif request.method == 'DELETE':
            return deletePhoto(request, userId)
        else:
            return errorResp('Invalid request method')
    else:
        if request.method == 'GET':
            return getAllPhotos(request)
        elif request.method == 'POST':
            return uploadPhoto(request)
        else:
            return errorResp('Invalid request method')


def filterParams(request):
    body = {}
    if request.method == 'GET':
        body = dict(request.GET.dict())
    elif request.method == 'POST' and 'file' in request.FILES and request.FILES['file']:
        body = {}
        userId = request.POST['userId']
        albumId = request.POST['albumId']
        desc = request.POST['desc']
        access = request.POST['access']
        myfile = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        body = {
            "userId": userId,
            "albumId": albumId,
            "desc": desc,
            "file": uploaded_file_url,
            "access": access
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


def getAllPhotos(request):
    params = filterParams(request)
    start = 0
    limit = 50
    if 'start' in params:
        start = int(params['start'])
    if 'limit' in params:
        limit = int(params['limit'])
    res, msg = photosModel.getAllPics(start, limit)
    if res:
        res = json.loads(res)
        for pic in res:
            pic['pid'] = pic['_id']
        context = {
            'data': res
        }
        return render(request, 'dash.html', context)
        # return createResponse(200,'OK',res)
    return errorResp(msg)


def getPhoto(request, userId):
    OId, msg = ObId(userId)
    if not OId:
        return errorResp(msg)
    res, msg = photosModel.getPic(OId)
    if res:
        res = json.loads(res)
        res['imageId'] = res['_id']
        context = {
            'data': res
        }
        return render(request, 'photo.html', context)
        # return createResponse(200,'OK',res)
    return errorResp(msg)


def uploadPhoto(request):
    body = filterParams(request)
    if 'userId' not in body:
        return errorResp("UserId Missing")
    if 'albumId' not in body:
        return errorResp("albumId Missing")
    if 'desc' not in body:
        return errorResp("Description Missing")
    if 'access' not in body:
        return errorResp("Access Missing")
    if 'file' not in body:
        return errorResp("File Missing")
    userId = body['userId']
    filePath = body['file']
    objUrl, ermsg = upload.uploadPhoto(userId, filePath)
    if objUrl:
        location = None
        if 'location' in body:
            location = body['location']
        doc = {"access": body['access'], "likes": [], "url": objUrl, "albumId": body['albumId'],
               "desc": body['desc'], "datetime": datetime.now(), "location": location, "owner": userId}
        res, msg = photosModel.insertPhoto(doc)
        return createResponse(200, 'Image Uploaded', [ObjectIdToStr(res)])
    else:
        return errorResp(ermsg)


def deletePhoto(request, photoId):
    OId, ermsg = ObId(photoId)
    if not OId:
        return errorResp(ermsg)
    res, msg = photosModel.deletePhoto(OId)
    if res:
        return createResponse(200, 'Photo Deleted', {"deleted_cnt": res})
    elif res == 0:
        return createResponse(200, 'No such Image exists', [])
    else:
        return errorResp(msg)

# ====== API ENDPOINTS ======


def index(request):
    return scanRequest(request)


def photo(request, userId):
    return scanRequest(request, userId)


def my(request):
    params = filterParams(request)
    start = 0
    limit = 50
    if 'start' in params:
        start = int(params['start'])
    if 'limit' in params:
        limit = int(params['limit'])
    res, msg = photosModel.getMyPics(params['userId'], start, limit)
    res = json.loads(res)
    if res:
        return createResponse(200, 'OK', res)
    return errorResp(msg)


def albumPics(request, albumId):
    params = filterParams(request)
    start = 0
    limit = 50
    if 'start' in params:
        start = int(params['start'])
    if 'limit' in params:
        limit = int(params['limit'])
    res, msg = photosModel.getAlbumPics(albumId, start, limit)
    if res:
        res = json.loads(res)
        return createResponse(200, 'OK', res)
    return errorResp(msg)
