from datetime import datetime, date
from bson import ObjectId
from django.http import HttpResponse, JsonResponse
import json

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

def getContext(data,err):
    return {
        'data':data,
        'err':err
    }

def createResponse(statusCode, msg, data):
    return JsonResponse(dict(status=statusCode, message=msg, data=data))

def errorResp(msg):
    return JsonResponse(dict(status=400, message=msg, data=[]))

def ObId(id):
    try:
        return ObjectId(id), "OK"
    except Exception as e:
        return None, "Invalid Id"