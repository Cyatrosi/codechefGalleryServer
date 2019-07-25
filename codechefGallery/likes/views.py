from django.shortcuts import render
from django.utils.html import escape
from django.http import HttpResponse, JsonResponse
import os
import sys
import json
from datetime import datetime, date
from bson import ObjectId
from codechefGallery.model.photos import photos
from codechefGallery.model.album import album

photosModel = photos()
albumModel = album()

# ====== Util Functions =====

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

def filterParams(request):
    body = {}
    if request.method == 'POST':
        ReqBody = request.body.decode('utf-8')
        if ReqBody:
            body = json.loads(ReqBody)
        else:
            body = {}
    elif request.method == 'GET':
       body = dict(request.GET.dict()) 
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

# ====== API ENDPOINTS ======

def index(request):
    return HttpResponse("Hello")

def photo(request):
    if request.method == 'GET':
        return hasLikedPhoto(request)
    elif request.method == 'POST':
        return likePhoto(request)
    else:
        errorResp('Invalid request method')

def albums(request):
    if request.method == 'POST':
        return likeAlbum(request)
    elif request.method == 'GET':
        return hasLikedAlbum(request)
    else:
        errorResp('Invalid request method')

def likePhoto(request):
    body = filterParams(request)
    if 'photoId' not in body:
        return errorResp("photoId missing")
    if 'userId' not in body:
        return errorResp("userId missing")
    if 'type' not in body:
        return errorResp("type missing")
    userId = body['userId']
    POId, msg = ObId(body['photoId'])
    if not POId:
        return errorResp(msg)
    likes,msg = photosModel.getLikes(POId)
    if likes:
        likes = json.loads(likes)
        likes = likes['likes']
        if body['type'] == 'like':
            if userId not in likes:
                likes.append(userId)
        elif body['type'] == 'unlike':
            if userId in likes:
                likes.remove(userId)
        else:
            return errorResp("Invalid Type")    
        res,exmsg = photosModel.setLikes(POId,{'likes':likes})
        if res:
            return createResponse(200,'OK',[])
        return errorResp(exmsg)
    else:
        return errorResp(msg)

def likeAlbum(request):
    body = filterParams(request)
    if 'albumId' not in body:
        return errorResp("albumId missing")
    if 'userId' not in body:
        return errorResp("userId missing")
    if 'type' not in body:
        return errorResp("type missing")
    userId = body['userId']
    POId, msg = ObId(body['albumId'])
    if not POId:
        return errorResp(msg)
    likes,msg = albumModel.getLikes(POId)
    if likes:
        likes = json.loads(likes)
        likes = likes['likes']
        if body['type'] == 'like':
            if userId not in likes:
                likes.append(userId)
        elif body['type'] == 'unlike':
            if userId in likes:
                likes.remove(userId)
        else:
            return errorResp("Invalid Type")    
        res,exmsg = albumModel.setLikes(POId,{'likes':likes})
        if res:
            return createResponse(200,'OK',[])
        return errorResp(exmsg)
    else:
        return errorResp(msg)

def hasLikedPhoto(request):
    body = filterParams(request)
    if 'photoId' not in body:
        return errorResp("photoId missing")
    if 'userId' not in body:
        return errorResp("userId missing")
    userId = body['userId']
    POId, msg = ObId(body['photoId'])
    if not POId:
        return errorResp(msg)
    res,msg = photosModel.hasLike(POId,userId)
    if res:
        if res!='null':
            res = json.loads(res)
        else:
            res = {}
        return createResponse(200,'OK',{'likes':res})
    else:
        return errorResp(msg)

def hasLikedAlbum(request):
    body = filterParams(request)
    if 'albumId' not in body:
        return errorResp("photoId missing")
    if 'userId' not in body:
        return errorResp("userId missing")
    userId = body['userId']
    POId, msg = ObId(body['albumId'])
    if not POId:
        return errorResp(msg)
    res,msg = albumModel.hasLike(POId,userId)
    if res:
        if res!='null':
            res = json.loads(res)
        else:
            res = {}
        return createResponse(200,'OK',{'likes':res})
    else:
        return errorResp(msg)