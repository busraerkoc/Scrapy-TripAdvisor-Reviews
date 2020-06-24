# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    country = scrapy.Field()
    city = scrapy.Field()
    titleHotel = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    rating = scrapy.Field()
