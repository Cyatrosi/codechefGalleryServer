from codechefGallery.model.mongo import mongo

class photos(mongo):
    def __init__(self):
        self.collection = 'photos'
        super().__init__('127.0.0.1',27017)
    
    def insertPhoto(self, doc):
        return super().insertDoc(self.collection, doc)

    def getAllPics(self,start,limit):
        query = {"access":"public"}
        projection = {"access":1,"url":1,"albumId":1,"desc":1,"datetime":1,"owner":1,"location":1,"likes": { '$cond': { 'if': { '$isArray': "$likes" }, 'then': { '$size': "$likes" }, 'else': "0"} }}
        return super().getDocsAggregate(self.collection,query,projection,None,start,limit)
    
    def getPic(self,userId):
        query = {'_id':userId}
        projection = {"access":1,"url":1,"albumId":1,"desc":1,"datetime":1,"owner":1,"location":1,"likes": { '$cond': { 'if': { '$isArray': "$likes" }, 'then': { '$size': "$likes" }, 'else': "0"} }}
        return super().getDocAggregate(self.collection,query,projection)
    
    def getMyPics(self,userId,start,limit):
        query = {'owner':userId}
        projection = {"access":1,"url":1,"albumId":1,"desc":1,"datetime":1,"owner":1,"location":1,"likes": { '$cond': { 'if': { '$isArray': "$likes" }, 'then': { '$size': "$likes" }, 'else': "0"} }}
        return super().getDocsAggregate(self.collection,query,projection,None,start,limit)

    def getAlbumPics(self,albumId,start,limit):
        query = {'albumId':albumId}
        projection = {"access":1,"url":1,"albumId":1,"desc":1,"datetime":1,"owner":1,"location":1,"likes": { '$cond': { 'if': { '$isArray': "$likes" }, 'then': { '$size': "$likes" }, 'else': "0"} }}
        return super().getDocsAggregate(self.collection,query,projection,None,start,limit)

    def deletePhoto(self,id):
        query = {'_id':id}
        return super().deleteDoc(self.collection,query)
    
    def deleteAlbumPhoto(self,albumId):
        query = {'albumId':albumId}
        return super().deleteDocs(self.collection,query)

    ## ========== Like function =============

    def getLikes(self,photoId):
        query = {'_id':photoId}
        projection = {'likes':1}
        return super().getDocAggregate(self.collection,query,projection)

    def setLikes(self,photoId,newLikes):
        query = dict(_id=photoId)
        newValues = {'$set': newLikes}
        return super().updateDoc(self.collection,query,newValues)
    
    def hasLike(self,photoId,userId):
        query = {'_id':photoId,'likes':{'$all':[userId]}}
        projection = {'_id':1}
        return super().getDoc(self.collection,query,projection)