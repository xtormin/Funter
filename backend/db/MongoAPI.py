# https://ishmeet1995.medium.com/how-to-create-restful-crud-api-with-python-flask-mongodb-and-docker-8f6ccb73c5bc

import os
from pathlib import Path
from dotenv import load_dotenv
from pymongo import MongoClient
from mongoengine import connect


dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

DATABASE_ADDRESS = os.getenv('DATABASE_ADDRESS')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_DB_NAME = os.getenv('DATABASE_DB_NAME')

class MongoAPI():
    def __init__(self):
        self.client = MongoClient(DATABASE_ADDRESS, port=int(DATABASE_PORT), username=DATABASE_USERNAME, password=DATABASE_PASSWORD)
        self.db = self.client[DATABASE_DB_NAME]

    def read(self, collection = None):
        self.collection = self.db[collection]
        documents = self.collection.find()
        output = [{item: data[item] for item in data if item != '_id'} for data in documents]
        return output

    def conn(self):
        return connect(DATABASE_DB_NAME, host='mongodb://' + DATABASE_USERNAME + ':' + DATABASE_PASSWORD + '@' + DATABASE_ADDRESS + ':' + str(DATABASE_PORT) + '/?authSource=admin', alias='default')