import os, sys
from pymongo import MongoClient
from bson.objectid import ObjectId
from mongoengine import connect, disconnect, DynamicDocument, StringField, ReferenceField
from pathlib import Path
from backend.db.MongoAPI import *
from dotenv import load_dotenv

try:
    mongoengine = MongoAPI()
    client = mongoengine.client
    db = mongoengine.db
    conn = mongoengine.conn

except Exception as e:
    print('|-| [ERROR] Error connecting to database...')
    print(e)

# DATABASE MODELS

class Project(DynamicDocument):
    __tablename__ = 'project'
    name = StringField(required=True, max_length=200, unique=True)

class Scope(DynamicDocument):
    __tablename__ = 'scope'
    name = StringField(required=True, max_length=200, unique=True)
    id_project = ReferenceField(Project)

# class Form(DynamicDocument):
#     __tablename__ = 'form'
#     url_name = StringField(max_length=200, default='None')
#     action = StringField(max_length=200, default='None')
#     method = StringField(max_length=200, default='None')
#     input_name = StringField(max_length=200, default='None')
#     type = StringField(max_length=200, default='None')
#     value = StringField(max_length=500, default='None')
#     options = StringField(max_length=200, default='None')
#     id_scope = ReferenceField(Scope)

class Form(DynamicDocument):
    __tablename__ = 'form'
    url_name = StringField(max_length=200, default='None')
    form_name = StringField(max_length=200, default='None')
    action = StringField(max_length=200, default='None')
    method = StringField(max_length=200, default='None')
    input_name = StringField(max_length=200, default='None')
    type = StringField(max_length=200, default='None')
    value = StringField(max_length=500, default='None')
    options = StringField(max_length=200, default='None')

# WEB OUTPUT MODELS
class Data(object):
    def __init__(self, url_name, action, method, input_name, type, value):
        self.url_name = str(url_name)
        self.action = str(action)
        self.method = str(method)
        self.input_name = str(input_name)
        self.type = str(type)
        self.value = str(value)

    def forms_json(self):
        return {
            "url_name": self.url_name, 
            "action": self.action, 
            "method": self.method,
            "input_name": self.input_name,
            "type": self.type,
            "value": self.value
        }