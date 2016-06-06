# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TruckProjectItem(scrapy.Item):
    # define the fields for your item here like:
    responsibility = scrapy.Field()
    number = scrapy.Field()
    stop_number = scrapy.Field()
    district = scrapy.Field()
    village = scrapy.Field()
    stop_location = scrapy.Field()
    stop_time = scrapy.Field()
    recycle = scrapy.Field()
    # pass
