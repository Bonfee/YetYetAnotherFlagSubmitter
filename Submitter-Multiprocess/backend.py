from pymongo import *
from config import Config

mongo = MongoClient(Config.Backend.Mongo.ip, Config.Backend.Mongo.port)
flagcollection = mongo.submitter_db.flags
