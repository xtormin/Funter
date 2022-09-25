from pymongo import *
from bson.objectid import ObjectId
from mongoengine import connect, disconnect
from pathlib import Path
from backend.db.models import *
from backend.db.MongoAPI import *

try:
    mongoengine = MongoAPI()
    client = mongoengine.client
    db = mongoengine.db
    conn = mongoengine.conn

except Exception as e:
    print('|-| [ERROR] Error connecting to database...')
    print(e)

# WEB 

def get_all_forms():
    dataJson = []

    for data in db['form'].find():
        data = Data(data['url_name'], 
                    data['action'], 
                    data['method'], 
                    data['input_name'],
                    data['type'],
                    data['value']).forms_json()
        dataJson.append(data)

    return dataJson

# DB 

def create_collection(col, cursor=None):
    try:
        col.save()
        return col.id
    except Exception as e:
        print(e)
        pass

def create_collection_ifnoexists_input(col):
    col_name = col.__tablename__
    data = {'url_name': col.url_name, 
                                'action':col.action, 
                                'method': col.method, 
                                'input_name': col.input_name, 
                                'type': col.type, 
                                'value': col.value}
    cursor = db[col_name].find(data)
    
    for i in cursor:
        if i:
            return str(i['_id'])

    return create_collection(col, cursor)

def db_drop_all():
    client.drop_database(DATABASE_DB_NAME)


