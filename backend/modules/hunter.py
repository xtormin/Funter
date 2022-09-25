from ast import arg
import datetime
import pandas as pd
from utils import cli, banner
from scrapy_project.scrapy_project.spiders.linksscraper import LinkScraper
from mongoengine import connect, disconnect
from utils.functions import *
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from bson.objectid import ObjectId
from pathlib import Path
from dotenv import load_dotenv
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from scrapy import signals
from scrapy.signalmanager import dispatcher
from backend.db.models import *
from backend.db.db import db_drop_all, create_collection_ifnoexists_input, create_collection, get_all_forms
from backend.db.MongoAPI import *

# ENVIRONMENT VARIABLES
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

DATABASE_ADDRESS = os.getenv('DATABASE_ADDRESS')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_DB_NAME = os.getenv('DATABASE_DB_NAME')

# ARGUMENTS
ARGS = cli.get()

# DB CONNECTION
try:
    mongoengine = MongoAPI()
    client = mongoengine.client
    db = mongoengine.db
    # conn = mongoengine.conn
    connect(DATABASE_DB_NAME, host='mongodb://' + DATABASE_USERNAME + ':' + DATABASE_PASSWORD + '@' + DATABASE_ADDRESS + ':' + str(DATABASE_PORT) + '/?authSource=admin', alias='default')

except Exception as e:
    print('|-| [ERROR] Error connecting to database...')
    print(e)

# SESSIONS
session = HTMLSession()

# LOGGING
logger = logging.getLogger()

logger.setLevel(logging.ERROR)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.disabled = True

if ARGS.verbose:
    logger.disabled = False

def create_project(PROJECT_NAME):
    return create_collection(Project(name=PROJECT_NAME))

def create_scope(id_project, SCOPE_NAME):
    return create_collection(Scope(name=SCOPE_NAME, id_project=id_project))

def run():
    try:
        banner.ascii()

        # Read scope urls
        urls = []
        if ARGS.url:
            urls.append(ARGS.url[0])
        if ARGS.urlslist:
            urlslist_arg = ARGS.urlslist[0]
            urls = urls + read_from_file(urlslist_arg)

        
        

        if ARGS.resetdata:
            logger.info("|+| Database reseted")
            db_drop_all()

        PROJECT_NAME = "formshunter"
        SCOPE_NAME = "default"

        # Create project and scope
        id_project = create_project(PROJECT_NAME)
        id_scope = create_scope(id_project, SCOPE_NAME)
        
        # Scrape URLs to hunt forms
        process = CrawlerProcess(settings={'LOG_ENABLED': False})
        process.crawl(LinkScraper, urls=urls)
        process.start()

        # Create CSV
        if ARGS.outputfile: 
            output_filename = ARGS.outputfile
            forms = get_all_forms()
            docs = pd.DataFrame(forms)
            docs.to_csv(output_filename, ";", index=False)
            
            if ARGS.verbose: print(docs)

    except KeyboardInterrupt:
        programInterruption()