import confuse
import pandas as pd
from pymongo import MongoClient
from backend.utils.logs import CustomLogger

# LOAD CONFIG FROM YAML FILE
config = confuse.Configuration('FUNTER', __name__)
config.set_file('config/config.yaml')

APPVER = config['app']['version'].get()

DB_HOST = config['database']['connection']['host'].get()
DB_PORT = config['database']['connection']['port'].get()
DB_USERNAME = config['database']['connection']['user'].get()
DB_PASSWORD = config['database']['connection']['pass'].get()
DB_NAME = config['database']['connection']['dbname'].get()

# Logging configuration
logger = CustomLogger('test')

class MongoDBManager:
    def __init__(self, host=DB_HOST, port=DB_PORT, db_name=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.user = user
        self.password = password
        self.client = None
        self.db = None

    def connect(self):
        self.client = MongoClient(self.host, port=int(self.port), username=self.user, password=self.password)
        self.db = self.client[self.db_name]

    def insert_data(self, data_object):
        collection_name = data_object.__class__.__name__.lower()
        collection = self.db[collection_name]
        data_dict = data_object.to_mongo().to_dict()
        existing_document = collection.find_one(data_dict)
        if existing_document is None:
            collection.insert_one(data_dict)

    def get_collections_to_df(self, collection_name):
        collection = self.db[collection_name]

        # Retrieve all documents from the collection
        documents = list(collection.find())

        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(documents)

        return df

    def drop_db(self):
        try:
            self.client.drop_database(DB_NAME)
            logger.info("|+| Database reset")
        except AttributeError as AE:
            logger.error("|-| Error resetting database")

    def close(self):
        if self.client:
            self.client.close()