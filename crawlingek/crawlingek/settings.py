# -*- coding: utf-8 -*-

# Scrapy settings for crawlingek project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'crawlingek'

SPIDER_MODULES = ['crawlingek.spiders']
NEWSPIDER_MODULE = 'crawlingek.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'crawlingek (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:44.0) Gecko/20100101 Firefox/44.0"

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    # 'crawlingdm.middlewares.CrawlingdmSpiderMiddleware': 543,
    'scrapy.spidermiddlewares.referer.RefererMiddleware': True,
}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'crawlingdm.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
}

# FILES_STORE = "E:/python/crawlingdm/output/csv/"
IMAGES_STORE = "/Users/leishang/helenstreet/python/crawlingek/output/image_download/"
# IMAGES_STORE = "E:/python/crawlingek/output/image_download/"

ITEM_PIPELINES = {
    'crawlingek.pipelines.EkImageDownloader': 600,
    # 'crawlingek.pipelines.EkXslxExportPipeline': 800,
    'crawlingek.pipelines.EkCsvExportPipeline': 800,
}

# below configuration is only for csv export.
FEED_EXPORTERS = {
    'csv': 'crawlingek.exporter.csv_item_exporter.EkCsvItemExporter',
}

FIELDS_TO_EXPORT = [
    'store',
    'websites',
    'attribute_set',
    'type',
    'categories',
    'sku',
    'simples_skus',
    'name',
    'url_key',
    'url_path',
    'image',
    'image_label',
    'small_image',
    'small_image_label',
    'thumbnail',
    'thumbnail_label',
    'media_gallery',
    'country_of_manufacture',
    'status',
    'visibility',
    'tax_class_id',
    'price',
    'weight',
    'brand',
    'age_range',
    'size',
    'model',
    'color',
    'description',
    'short_description',
    'qty',
    'is_in_stock',
    'use_config_min_sale_qty',
    'min_sale_qty',
    'manage_stock',
    'featured',
    'delivery_time',
    'free_shipping',
    'meta_title',
    'meta_description',
    'meta_keyword'
]
