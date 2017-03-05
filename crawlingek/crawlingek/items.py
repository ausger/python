# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# prevent csv convert the field type to date
def serialize_delivery_time(value):
    return "=\"" + value + "\""


class EkItem(scrapy.Item):
    # define the fields for your item here like:
    index = scrapy.Field()
    sku = scrapy.Field()
    brand = scrapy.Field()
    article_nr = scrapy.Field()
    product_id = scrapy.Field()
    log_id = scrapy.Field()
    name = scrapy.Field()
    image = scrapy.Field()
    image_url = scrapy.Field()
    small_image = scrapy.Field()
    small_image_url = scrapy.Field()
    thumbnail = scrapy.Field()
    thumbnail_url = scrapy.Field()
    simples_skus = scrapy.Field()
    model = scrapy.Field()
    # image_label = scrapy.Field()
    description = scrapy.Field()
    short_description = scrapy.Field()
    ek_price = scrapy.Field()
    top_price = scrapy.Field()
    vk_price = scrapy.Field()
    # csv fields
    store = scrapy.Field()
    websites = scrapy.Field()
    attribute_set = scrapy.Field()
    type = scrapy.Field()
    categories = scrapy.Field()
    url_key = scrapy.Field()
    url_path = scrapy.Field()
    image_label = scrapy.Field()
    small_image_label = scrapy.Field()
    thumbnail_label = scrapy.Field()
    media_gallery = scrapy.Field()
    country_of_manufacture = scrapy.Field()
    status = scrapy.Field()
    visibility = scrapy.Field()
    tax_class_id = scrapy.Field()
    price = scrapy.Field()
    weight = scrapy.Field()
    age_range = scrapy.Field()
    color = scrapy.Field()
    qty = scrapy.Field()
    is_in_stock = scrapy.Field()
    use_config_min_sale_qty = scrapy.Field()
    min_sale_qty = scrapy.Field()
    manage_stock = scrapy.Field()
    featured = scrapy.Field()
    delivery_time = scrapy.Field(serializer=serialize_delivery_time)
    free_shipping = scrapy.Field()
    meta_title = scrapy.Field()
    meta_description = scrapy.Field()
    meta_keywords = scrapy.Field()
    size = scrapy.Field()
