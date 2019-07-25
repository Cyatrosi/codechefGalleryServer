from codechefGallery.model.mongo import mongo

class album(mongo):
    def __init__(self):
        self.collection = 'album'
        super().__init__('127.0.0.1',27017)
    
    def getMyAlbums(self,userId,start,limit):
        query = {'owner':userId}
        projection = {"access":1,"url":1,"name":1,"desc":1,"datetime":1,"owner":1,"location":1,"likes": { '$cond': { 'if': { '$isArray': "$likes" }, 'then': { '$size': "$likes" }, 'else': "0"} }}
        return super().getDocsAggregate(self.collection,query,projection,None,start,limit)

    def insertAlbum(self, doc):
        return super().insertDoc(self.collection, doc)

    def getAllAlbums(self,start,limit):
        query = {}
        projection = {"access":1,"url":1,"name":1,"desc":1,"datetime":1,"owner":1,"location":1,"likes": { '$cond': { 'if': { '$isArray': "$likes" }, 'then': { '$size': "$likes" }, 'else': "0"} }}
        return super().getDocsAggregate(self.collection,query,projection,None,start,limit)
    
    def getAlbum(self,userId):
        query = {'_id':userId}
        projection = {"access":1,"url":1,"name":1,"desc":1,"datetime":1,"owner":1,"location":1,"likes": { '$cond': { 'if': { '$isArray': "$likes" }, 'then': { '$size': "$likes" }, 'else': "0"} }}
        return super().getDocAggregate(self.collection,query,projection)
    
    def deleteUser(self,userId):
        query = dict(_id=userId)
        return super().deleteDoc(self.collection,query)
    
    def updateAlbum(self,userId,newValues):
        query = dict(_id=userId)
        newValues = {'$set': newValues}
        return super().updateDoc(self.collection,query,newValues)