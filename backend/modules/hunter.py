import confuse
from backend.utils import cli, banner
from backend.utils import update
from scrapy_project.scrapy_project.spiders.linksscraper import LinkScraper
from backend.utils.functions import *
from requests_html import HTMLSession
from scrapy.crawler import CrawlerProcess
from backend.db.models import *
from backend.utils.logs import CustomLogger
from backend.db.MongoDBManager import MongoDBManager

# Logging configuration
logger = CustomLogger('test')

# ENVIRONMENT VARIABLES
dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

# LOAD CONFIG FROM YAML FILE
config = confuse.Configuration('FUNTER', __name__)
config.set_file('config/config.yaml')

APPVER = config['app']['version'].get()

# GLOBAL VARIABLES
PROJECT_NAME = "formshunter"
SCOPE_NAME = "default"
CRAWLER_SETTINGS = {'LOG_ENABLED': False}
ARGS = cli.get()

# SESSIONS
session = HTMLSession()

# DB CONNECTION
try:
    db = MongoDBManager()
    db.connect()
except Exception as e:
    logger.error('|-| [ERROR] Error connecting to database...')
    logger.error(e)

def run():
    try:
        banner.main()

        # Update tool
        update.update_program()

        output_filename = ARGS.outputfile

        # Read scope urls
        urls = []
        if ARGS.url:
            urls.append(ARGS.url[0])
        elif ARGS.urlslist:
            urls.extend(read_from_file(ARGS.urlslist[0]))

        # Reset data if enabled
        if ARGS.resetdata:
            db.drop_db()

        # Create project and scope
        id_project = db.insert_data(Project(name=PROJECT_NAME))
        id_scope = db.insert_data(Scope(name=SCOPE_NAME, id_project=id_project))

        # Scrape URLs to hunt forms
        process = CrawlerProcess(settings=CRAWLER_SETTINGS)
        process.crawl(LinkScraper, urls=urls)
        process.start()

        # Create CSV if output file is specified
        if output_filename:
            df = db.get_collections_to_df('form')
            df.to_csv(output_filename, ";", index=False)

            if ARGS.verbose:
                logger.info(df)

        # Close DB collection
        db.close()

    except KeyboardInterrupt:
        programInterruption()