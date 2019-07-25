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
