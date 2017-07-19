from pymongo import MongoClient

class MongoDBRepo:
    db = None

    def __init__(self):
        #MongoClient('localhost', 27017) - Maybe use that in the Linux implementation. Don't know. w/e
        self.db = MongoClient().test_database

    def getTemperature(self):
        return 30.0

    def getUPSStatus(self):
        return True

    def getInternetStatus(self):
        return True

    def updateUPSStatus(self, data):
        return self.db.ups.insert_one(data).inserted_id

    def updateInternetStatus(self, data):
        return self.db.internetStatus.insert_one(data).inserted_id

