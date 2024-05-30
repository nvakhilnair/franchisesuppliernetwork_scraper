# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ReferencesStats(scrapy.Item):
    page = scrapy.Field()
    text_extracted = scrapy.Field()
    resources_refereced = scrapy.Field()
