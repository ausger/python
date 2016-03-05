# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LegoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    #short_description = scrapy.Field()
    sku = scrapy.Field()
    pieces = scrapy.Field()
    age = scrapy.Field()
    category = scrapy.Field()
    product_id = scrapy.Field()
    #store = scrapy.Field()
    #attribute_set = scrapy.Field()
    #type = scrapy.Field()
    #categories = scrapy.Field()
    #product_websites = scrapy.Field()
    #age_range = scrapy.Field()
    #brand = scrapy.Field()
    #country_manu = scrapy.Field()
    #created_at = scrapy.Field()
    description = scrapy.Field()
    #featured = scrapy.Field()
    #image = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    url_key = scrapy.Field()
    #visibility = scrapy.Field()
    #weight = scrapy.Field()
    #quantity = scrapy.Field()
    pass


class LiwusItem(scrapy.Item):
    # define the fields for your item here like
    age = scrapy.Field()
    attribute_set = scrapy.Field()
    brand = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    img = scrapy.Field()
    meta_title = scrapy.Field()
    meta_keywords = scrapy.Field()
    meta_description = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    product_id = scrapy.Field()
    short_description = scrapy.Field()
    sku = scrapy.Field()
    url_key = scrapy.Field()

    pass