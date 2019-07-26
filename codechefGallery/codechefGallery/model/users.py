from codechefGallery.model.mongo import mongo


class users(mongo):
    def __init__(self):
        self.collection = 'users'
        super().__init__('127.0.0.1', 27017)

    def insertUser(self, doc):
        return super().insertDoc(self.collection, doc)

    def getUsersList(self, start, limit):
        query = {}
        projection = dict(name=1, username=1)
        return super().getDocs(self.collection, query, projection, None, start, limit)

    def getUserInfo(self, userId):
        query = dict(_id=userId)
        return super().getDoc(self.collection, query)

    def validateUser(self, userName, password):
        query = dict(username=userName, password=password)
        projection = dict(name=1, username=1)
        return super().getDoc(self.collection, query, projection)

    def deleteUser(self, userId):
        query = dict(_id=userId)
        return super().deleteDoc(self.collection, query)

    def updateUser(self, userId, newValues):
        query = dict(_id=userId)
        newValues = {'$set': newValues}
        return super().updateDoc(self.collection, query, newValues)
