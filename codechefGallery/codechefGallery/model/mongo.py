from pymongo import MongoClient
from datetime import datetime
import os
import sys
import json
from datetime import datetime, date
from bson import ObjectId


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        if isinstance(o, (date, datetime)):
            return o.isoformat()
        return json.JSONEncoder.default(self, o)


class mongo():
    def __init__(self, host, port):
        self.db = 'gallery'
        self.mongoClient = MongoClient('mongodb://'+host, port)
        pass

    def insertDoc(self, collection, doc):
        try:
            mongoColl = self.mongoClient[self.db][collection]
            ret = mongoColl.insert_one(doc)
            return ret.inserted_id, "OK"
        except Exception as e:
            return None, str(e)

    def updateDoc(self, collection, query, newValues):
        try:
            mongoColl = self.mongoClient[self.db][collection]
            ret = mongoColl.update_one(query, newValues)
            return ret, "OK"
        except Exception as e:
            return None, str(e)

    def getDocs(self, collection, condition, projection=None, sortField=None, start=0, lim=None):
        mongoColl = self.mongoClient[self.db][collection]
        try:
            if projection:
                mongoCursor = mongoColl.find(condition, projection)
            else:
                mongoCursor = mongoColl.find(condition)
            if sortField is not None:
                mongoCursor = mongoCursor.sort(sortField)
            mongoCursor = mongoCursor.skip(start)
            if lim is not None:
                mongoCursor = mongoCursor.limit(lim)
            records = []
            for rec in mongoCursor:
                records.append(rec)
            return JSONEncoder().encode(records), "OK"
        except Exception as e:
            return None, str(e)

    def getDocsAggregate(self, collection, condition, projection, sortField=None, start=0, lim=None):
        mongoColl = self.mongoClient[self.db][collection]
        try:
            agrQuery = [{'$match': condition}, {'$project': projection}]
            if sortField is not None:
                mongoCursor = agrQuery.append({"$sort": sortField})
            agrQuery.append({"$skip": start})
            if lim is not None:
                agrQuery.append({"$limit": lim})
            mongoCursor = mongoColl.aggregate(agrQuery)
            records = []
            for rec in mongoCursor:
                records.append(rec)
            return JSONEncoder().encode(records), "OK"
        except Exception as e:
            return None, str(e)

    def getDoc(self, collection, condition, projection=None):
        mongoColl = self.mongoClient[self.db][collection]
        try:
            if projection:
                rec = mongoColl.find_one(condition, projection)
            else:
                rec = mongoColl.find_one(condition)
            return JSONEncoder().encode(rec), "OK"
        except Exception as e:
            return None, str(e)

    def getDocAggregate(self, collection, condition, projection):
        mongoColl = self.mongoClient[self.db][collection]
        try:
            records = mongoColl.aggregate(
                [{'$match': condition}, {'$project': projection}, {'$limit': 1}])
            rec = []
            for r in records:
                rec.append(r)
            return JSONEncoder().encode(rec[0]), "OK"
        except Exception as e:
            return None, str(e)

    def deleteDoc(self, collection, condition):
        mongoColl = self.mongoClient[self.db][collection]
        try:
            res = mongoColl.delete_one(condition)
            return res.deleted_count, "OK"
        except Exception as e:
            return None, str(e)
