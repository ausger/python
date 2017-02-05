# -*- coding: utf-8 -*-

# Scrapy settings for crawlingdm project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'google_dm'

SPIDER_MODULES = ['crawlingdm.spiders']
NEWSPIDER_MODULE = 'crawlingdm.spiders'


# Obey robots.txt rules
ROBOTSTXT_OBEY = True

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
IMAGES_STORE = "E:/python/crawlingdm/output/image_download/"

ITEM_PIPELINES = {
    'crawlingdm.pipelines.DmImageDownloader': 600,
    'crawlingdm.pipelines.DmXslxExportPipeline': 800,
}
