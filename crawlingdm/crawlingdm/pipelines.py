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
import xlsxwriter


class DmImageDownloader(ImagesPipeline):
    # CONVERTED_ORIGINAL = re.compile('^/[0-9,a-f,_,-,/]+.jpg$')

    # name information coming from the spider, in each item
    # add this information to Requests() for individual images downloads
    # through "meta" dict
    def get_media_requests(self, item, info):
        return [Request(item.get('image_urls'), meta={'title': item["image"]})]

    # this is where the image is extracted from the HTTP response
    def get_images(self, response, request, info):
        for key, image, buf, in super(DmImageDownloader, self).get_images(response, request, info):
            # if self.CONVERTED_ORIGINAL.match(key):
            key = self.change_filename(key, response)
            yield key, image, buf

    def change_filename(self, key, response):
        return response.meta['title']


class DmXslxExportPipeline(object):
    def __init__(self):
        self.workbook = {}
        self.worksheet = {}
        self.row_count = 0
        # self.image_folder = '../output/image_download'
        self.image_folder = 'E:/python/crawlingdm/output/image_download/'
        self.cell_height = 180
        self.image_x_scale = 0.5
        self.image_y_scale = 0.5

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        file_full_path = spider.html_file.split('/')
        file_full_name = file_full_path[-1]
        file_full_name_splitted = file_full_name.split('.')
        file_name = file_full_name_splitted[0]
        self.workbook = xlsxwriter.Workbook('%s.xlsx' % file_name)
        self.worksheet = self.workbook.add_worksheet()
        self.worksheet.set_default_row(self.cell_height)
        self.output_header()

    def output_header(self):
        self.worksheet.write(self.row_count, 0, 'sku')
        self.worksheet.write(self.row_count, 1, 'name')
        self.worksheet.write(self.row_count, 2, 'price')
        self.worksheet.write(self.row_count, 3, 'miscellaneous')
        self.worksheet.write(self.row_count, 4, 'image')
        self.row_count += 1

    def spider_closed(self, spider):
        self.workbook.close()

    def process_item(self, item, spider):
        print('item[%s] to be processed:' % (item['name']))
        # write 'sku','name','image','image_label','price','miscellaneous' to xlsx
        self.worksheet.write(self.row_count, 0, item['sku'])
        self.worksheet.write(self.row_count, 1, item['name'])
        self.worksheet.write(self.row_count, 2, item['price'])
        self.worksheet.write(self.row_count, 3, item['miscellaneous'])
        self.worksheet.insert_image(self.row_count, 4, self.image_folder + item['image'],
                                    {'x_scale': self.image_x_scale, 'y_scale': self.image_y_scale})
        self.row_count += 1
        return item
