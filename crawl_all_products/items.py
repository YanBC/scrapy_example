# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Product(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    name = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    price = scrapy.Field()
    upc = scrapy.Field()
    pass
