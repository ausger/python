# -*- coding: utf-8 -*-
import scrapy
import sys
import re

from imagespider.items import LegoImageItem
# import logging
from scrapy.http.request import Request

reload(sys)
sys.setdefaultencoding('utf8')


class LegoImageSpider(scrapy.Spider):
    # Scrapy is single-threaded, except the interactive shell and some tests, see source.
    # Scrapy does most of it's work synchronously. However, the handling of requests is done asynchronously.
    name = "image"
    allowed_domains = ["www.amazon.cn"]

    # product_ids = ['10596']
    # duplo & juniors
    # product_ids = ['10587', '10590', '10594', '10595', '10596', '10600', '10615', '10616', '10617',
    #                '10618', '10674', '10682']

    # product_ids = ['10692', '10693', '10694', '10696', '10699', '10700', '10701', '31003', '31010', '31022', '31023', '31026', '31027', '31028', '31029', '31030',
    #                '31031', '31032', '31033', '31034', '31035', '31036', '3933', '3935', '41005', '41015', '41035', '41037', '41038', '41039', '41056',
    #                '41057', '41058', '41059', '41091', '41093', '41094', '41095', '41097']

    # classic
    # product_ids = ['10692', '10693', '10694', '10696', '10699', '10700', '10701']

    # product_ids = ['31003', '31010', '31022', '31023', '31026', '31027', '31028', '31029', '31030',
    #                '31031', '31032', '31033', '31034', '31035', '31036']

    # product_ids = ['3933', '3935', '41005', '41015', '41035', '41037', '41038', '41039', '41056',
    #                '41057', '41058', '41059', '41091', '41093', '41094', '41095', '41097']

    product_ids = ['42009', '42025', '44003', '44029', '60004', '60047', '60048', '60050', '60055',
                     '60057', '60060', '60069', '60085', '60086', '60088', '6176', '70144', '70145',
                     '70146', '70228', '70745', '70746', '70748', '70749', '70750', '70753', '70754',
                     '70755', '70756', '70784', '75038', '75040', '75076', '75077', '75078', '75079', '75080', '75081',
                     '75085', '75089', '75090']

    # product_ids = ['42009', '42025', '44003', '44029', '60004', '60047', '60048', '60050', '60055',
    #                '60057', '60060', '60069', '60085', '60086', '60088', '6176']

    # product_ids = ['70144', '70145', '70146', '70228', '70745', '70746', '70748', '70749', '70750',
    #                '70753', '70754', '70755', '70756']

    # product_ids = ['70784', '75038', '75040', '75076', '75077', '75078', '75079', '75080', '75081',
    #                '75085', '75089', '75090']

    amazon_cn_search_result_link = "http://www.amazon.cn/s/ref=nb_sb_noss?__mk_zh_CN=" \
                                   "%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=" \
                                   "search-alias%3Daps&field-keywords=%E4%B9%90%E9%AB%98+"

    zh_prod_details_link = "//li[@id='result_0']/descendant::a[contains(@class,'a-link-normal')]/@href"
    zh_search_result_prod_title = "//li[@id='result_0']/descendant::h2[contains(@class,'s-access-title')]/text()"

    # DON'T use /@src
    prod_landing_img_src = "//img[@id='landingImage']/@data-old-hires"
    # If @data-old-hires is emtpy, use data-a-dynamic-image
    prod_dynamic_img_loc = "//img[@id='landingImage']/@data-a-dynamic-image"
    prod_landing_img_title = "//img[@id='landingImage']/@alt"

    start_urls = [amazon_cn_search_result_link + "%s" % n for n in product_ids]

    def parse(self, response):
        url_parts = response.url.split("%20")
        print 'last part of URL: ' + url_parts[-1]
        current_product_id = url_parts[-1]
        print "search result - current product_id: " + current_product_id
        # Get the real product details page link from the search result page
        request = self.crawler_zh_product_details(self.zh_prod_details_link, response, current_product_id)
        yield request

    def parse_product_zh_search_result(self, response):

        url_parts = response.url.split("%")
        print 'last part of URL: ' + url_parts[-1].strip()

        current_product_id = url_parts[-1].strip()
        print "search result - current product_id: " + current_product_id
        # Get the real product details page link from the search result page
        request = self.crawler_zh_product_details(self.zh_prod_details_link, response, current_product_id)
        yield request

    def crawler_zh_product_details(self, prod_details_link, response, current_product_id):

        ref_link = response.xpath(prod_details_link).extract()
        if len(ref_link) == 0:
            self.failed_products.append(current_product_id)
            print '****** CANNOT find the product: ' + current_product_id
            return
        print 'chinese product details page is: ' + ref_link[0]#

        prod_title_found = response.xpath(self.zh_search_result_prod_title).extract()
        print 'product title in the search result is ' + prod_title_found[0]

        if "乐高" in prod_title_found[0] and current_product_id in prod_title_found[0]:
            print "Lego product " + current_product_id + " found in the search result"
            # need to crawl the product details page. it seems here change to another thread to handle next product
            request = Request(ref_link[0], callback=self.parse_product_zh_details, meta={'product_id': current_product_id})
            return request
        else:
            self.failed_products.append(current_product_id)
            print "****** Lego product " + current_product_id + " NOT FOUND in the search result"
            return

    def parse_product_zh_details(self, response):
        current_product_id = response.meta["product_id"]
        print "parse details - current product_id: " + current_product_id
        product_images = response.xpath(self.prod_landing_img_src).extract()
        product_title = response.xpath(self.prod_landing_img_title).extract()
        if len(product_images[0].strip()) == 0:
            # dyn_images = response.xpath(self.prod_dynamic_img_loc).extract()
            print "data-old-hires is empty"
            dyn_images_holder = response.xpath(self.prod_dynamic_img_loc).extract()
            print "dyn images " + dyn_images_holder[0]
            tmp = re.sub('(:\[\d+,\d+\]|\{|\}|\")', "", dyn_images_holder[0])
            # tmp = tmp.replace("{", "")
            print "after cleanup: " + tmp
            tmp = tmp.split(",")
            product_images = [tmp[-1]]
        print "image title " + product_title[0]
        print "product image url: " + product_images[0]
        yield LegoImageItem(title=product_title[0], file_urls=product_images)
