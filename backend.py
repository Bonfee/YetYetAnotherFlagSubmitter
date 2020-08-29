from pymongo import *
from config import Config


# Initialize new mongo connection
class MongoConnection(object):

    def __init__(self):
        client = MongoClient(Config.Backend.Mongo.ip, Config.Backend.Mongo.port)
        self.db = client.submitter_db
