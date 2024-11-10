import os
from pymongo import MongoClient
import app.dataconn as dataconn


def get_mongo_client():
    mongo_url = dataconn.URI
    return MongoClient(mongo_url)