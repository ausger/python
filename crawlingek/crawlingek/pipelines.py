# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import copy
import image
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.http import Request
from scrapy import signals
from crawlingek.exporter.csv_item_exporter import EkCsvItemExporter
import xlsxwriter


class EkImageDownloader(ImagesPipeline):
    # CONVERTED_ORIGINAL = re.compile('^/[0-9,a-f,_,-,/]+.jpg$')

    # name information coming from the spider, in each item
    # add this information to Requests() for individual images downloads
    # through "meta" dict

    # image_url = 'thumbnail_url'
    # image_name = 'thumbnail'
    image_url = 'image_url'
    image_name = 'image'

    def get_media_requests(self, item, info):
        return [Request(item.get(self.image_url), meta={'title': item[self.image_name]})]

    # this is where the image is extracted from the HTTP response
    def get_images(self, response, request, info):
        for key, v_image, buf, in super(EkImageDownloader, self).get_images(response, request, info):
            # if self.CONVERTED_ORIGINAL.match(key):
            key = self.change_filename(key, response)
            yield key, v_image, buf

    def change_filename(self, key, response):
        return response.meta['title']


class EkXslxExportPipeline(object):
    def __init__(self):
        self.workbook = {}
        self.worksheet = {}
        self.row_count = 0

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file_name = spider.CATALOG_ID.lower() + '-' + spider.SEARCH_STRING.lower()
        self.workbook = xlsxwriter.Workbook('%s.xlsx' % file_name)
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.set_default_row(spider.IMAGE_CELL_HEIGHT)
        self.output_header()

    def output_header(self):
        self.worksheet.write(self.row_count, 0, 'product_id')
        self.worksheet.write(self.row_count, 1, 'article_nr')
        self.worksheet.write(self.row_count, 2, 'sku')
        self.worksheet.write(self.row_count, 3, 'name')
        self.worksheet.write(self.row_count, 4, 'ek_price')
        self.worksheet.write(self.row_count, 5, 'top_price')
        self.worksheet.write(self.row_count, 6, 'vk_price')
        # self.worksheet.write(self.row_count, 7, 'short_description')
        self.worksheet.write(self.row_count, 7, 'thumbnail')
        self.row_count += 1

    def spider_closed(self, spider):
        self.workbook.close()

    def process_item(self, item, spider):
        print('item[%s] to be processed:' % (item['name']))
        # write 'sku','name','image','image_label','price','miscellaneous' to xlsx
        self.worksheet.write(self.row_count, 0, item['product_id'])
        self.worksheet.write(self.row_count, 1, item['article_nr'])
        self.worksheet.write(self.row_count, 2, item['sku'])
        self.worksheet.write(self.row_count, 3, item['name'])
        self.worksheet.write(self.row_count, 4, item['ek_price'])
        self.worksheet.write(self.row_count, 5, item['top_price'])
        self.worksheet.write(self.row_count, 6, item['vk_price'])
        # self.worksheet.write(self.row_count, 7, item['short_description'])
        self.worksheet.insert_image(self.row_count, 7, spider.IMAGE_FOLDER + item['thumbnail'],
                                    {'x_scale': spider.IMAGE_X_SCALE, 'y_scale': spider.IMAGE_Y_SCALE})
        self.row_count += 1
        return item


class EkCsvExportPipeline(object):

    def __init__(self):
        self.files = {}

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file_name = spider.CATALOG_ID.lower() + '-' + spider.SEARCH_STRING.lower()
        file = open('%s_products.csv' % file_name, 'w+b')
        self.files[spider] = file
        self.exporter = EkCsvItemExporter(file)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        file = self.files.pop(spider)
        file.close()

    def process_item(self, item, spider):
        if item['image'] == 'image_':
            print('product[%s] has no image, so not to csv' % item['name'])
        else:
            self.exporter.export_item(item)
        return item
