# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Form(scrapy.Item):
    # define the fields for your item here like:
    url_name = scrapy.Field()
    form_name = scrapy.Field()
    action = scrapy.Field()
    method = scrapy.Field()
    input_name = scrapy.Field()
    type = scrapy.Field()
    value = scrapy.Field()
    options = scrapy.Field()
