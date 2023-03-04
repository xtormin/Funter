
import scrapy
import scrapy_splash

from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_project.scrapy_project.items import *
from backend.db.models import *
from backend.db.db import db_drop_all, create_collection_ifnoexists_input, create_collection
from backend.db.MongoAPI import *

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

class LinkScraper(CrawlSpider):
    name = "linksscraper"

    def __init__(self, urls, **kwargs):
        self.start_urls = urls
        super().__init__(**kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy_splash.SplashRequest(url, callback=self.parse)


    def parse(self, response):
        
        # print("###########")
        # links = response.xpath('//a/@href').extract()
        
        forms = response.xpath('//form').extract()
        for f in forms:
            inputs = Selector(text=f).xpath('//input').extract()
            for i in inputs:
                form = Form()

                form_url = response.url
                if form_url: form['url_name'] = form_url

                form_action = Selector(text=f).xpath('//@action').extract()
                if form_action: form['action'] = form_action[0]

                form_method = Selector(text=f).xpath('//@method').extract()
                if form_method: form['method'] = form_method[0]

                input_name = Selector(text=i).xpath('//@name').extract()
                if input_name: form['input_name'] = input_name[0]

                input_type = Selector(text=i).xpath('//@type').extract()
                if input_type and len(input_type)>0: form['type'] = input_type[0]

                input_value = Selector(text=i).xpath('//@value').extract()
                if input_value: form['value'] = input_value[0]

                input_options = Selector(text=i).xpath('//@options').extract()
                if input_options: form['options'] = input_options[0]

                create_collection_ifnoexists_input(form)

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)