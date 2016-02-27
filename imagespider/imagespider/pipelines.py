# -*- coding: utf-8 -*-

# from scrapy.contrib.pipeline.images import ImagesPipeline
# from scrapy.http import Request
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ImagespiderPipeline(object):
    def process_item(self, item, spider):
        return item


# class MyImagesPipeline(ImagesPipeline):
#     # Name download version
#     def file_path(self, request, response=None, info=None):
#         image_guid = request.meta['title'][0]
#         return 'full/%s' % image_guid
#
#     # Name thumbnail version
#     def thumb_path(self, request, thumb_id, response=None, info=None):
#         image_guid = thumb_id + request.url.split('/')[-1]
#         return 'thumbs/%s/%s.jpg' % (thumb_id, image_guid)
#
#     def get_media_requests(self, item, info):
#         yield Request(item['image_urls'][0], meta=item)
#