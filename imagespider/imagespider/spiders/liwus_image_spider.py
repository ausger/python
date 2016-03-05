# -*- coding: utf-8 -*-
import scrapy
import sys
import re

from imagespider.items import LegoImageItem
# import logging
from scrapy.http.request import Request

reload(sys)
sys.setdefaultencoding('utf8')


class LiwusImageSpider(scrapy.Spider):
    # Scrapy is single-threaded, except the interactive shell and some tests, see source.
    # Scrapy does most of it's work synchronously. However, the handling of requests is done asynchronously.
    name = "liwus-image"
    allowed_domains = ["www.liwus.de"]

    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/suitcases-and-luggage.html"

    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/alfi/isolierkanne.html?___store=en&dir=asc&limit=50&order=name"

    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/zwilling/zwilling-beauty.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&dir=desc&order=name"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/zwilling/zwilling-beauty.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&dir=desc&order=name&p=2"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/zwilling/zwilling-beauty.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&dir=desc&order=name&p=3"

    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/zwilling/zwilling-kuchen.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&dir=asc&order=name"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/zwilling/zwilling-kuchen.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&dir=asc&order=name&p=2"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/zwilling/zwilling-kuchen.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&dir=asc&order=name&p=3"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/zwilling/zwilling-kuchen.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&dir=asc&order=name&p=4"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/zwilling/zwilling-kuchen.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&dir=asc&order=name&p=5"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/zwilling/zwilling-kuchen.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&dir=asc&order=name&p=6"

    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/zielonka/zilopp.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&___store=en&dir=asc&limit=24&order=sku"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/zielonka/kuhlschrank-becher.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&___store=en&dir=asc&limit=24&order=sku"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/zielonka/classic-inkl-schale.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&___store=en&dir=asc&limit=24&order=sku"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/zielonka/auto-geruchskiller.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&___store=en&dir=asc&limit=24&order=sku"

    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/baby-s-products/avent.html?dir=asc&limit=50&order=sku"

    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/baby-s-products/nuk.html?dir=asc&limit=50&order=sku"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/baby-s-products/nuk.html?dir=asc&limit=50&order=sku&p=2"

    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/le-creuset/pottery.html?___store=en&dir=asc&limit=100&order=name"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/le-creuset/wasserkessel.html?___store=en&dir=asc&limit=100&order=name"
    #ZHPRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/le-creuset/gusseisen-signature.html?___store=en&dir=asc&limit=24&manufacturer=12&order=name"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/le-creuset/gusseisen-signature.html?___store=en&dir=asc&limit=24&manufacturer=12&order=name&p=2"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/le-creuset/gusseisen-signature.html?___store=en&dir=asc&limit=24&manufacturer=12&order=name&p=3"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/le-creuset/backen.html?___store=en&dir=asc&limit=100&order=price"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/victorinox/taschenmesser.html?___store=en&dir=asc&limit=24&order=name"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/victorinox/taschenmesser.html?___store=en&dir=asc&limit=24&order=name&p=2"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/victorinox/taschenmesser.html?___store=en&dir=asc&limit=24&order=name&p=3"
    #ZH_PRODUCT_LISTING_LINK = http://www.liwus.de/haushaltswaren/victorinox/taschenmesser.html?___store=en&dir=asc&limit=24&order=name&p=4"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/victorinox/taschenmesser.html?___store=en&dir=asc&limit=24&order=name&p=5"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/victorinox/taschenmesser.html?___store=en&dir=asc&limit=24&order=name&p=6"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/victorinox/taschenmesser.html?___store=en&dir=asc&limit=24&order=name&p=7"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/victorinox/sonstige.html?___store=en&dir=asc&order=name"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/victorinox/sonstige.html?___store=en&dir=asc&order=name&p=2"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/victorinox/sonstige.html?___store=en&dir=asc&order=name&p=3"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/victorinox/sonstige.html?___store=en&dir=asc&order=name&p=4"

    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/bar-wein.html?dir=desc&limit=24&mode=grid&order=position"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/bar-wein.html?dir=desc&limit=24&mode=grid&order=position&p=2"

    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/kochen.html?dir=desc&limit=24&mode=grid&order=position"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/kochen.html?dir=desc&limit=24&mode=grid&order=position&p=2"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/kochen.html?dir=desc&limit=24&mode=grid&order=position&p=3"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/kochen.html?dir=desc&limit=24&mode=grid&order=position&p=4"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/kochen.html?dir=desc&limit=24&mode=grid&order=position&p=5"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/kochen.html?dir=desc&limit=24&mode=grid&order=position&p=6"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/kochen.html?dir=desc&limit=24&mode=grid&order=position&p=7"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/kochen.html?dir=desc&limit=24&mode=grid&order=position&p=8"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/kochen.html?dir=desc&limit=24&mode=grid&order=position&p=9"

    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/wohnen.html?dir=desc&limit=24&mode=grid&order=position&p=1"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/wohnen.html?dir=desc&limit=24&mode=grid&order=position&p=2"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/wohnen.html?dir=desc&limit=24&mode=grid&order=position&p=3"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/wohnen.html?dir=desc&limit=24&mode=grid&order=position&p=4"

    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/bestecke.html?dir=desc&limit=24&mode=grid&order=position"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/bestecke.html?dir=desc&limit=24&mode=grid&order=position&p=2"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/bestecke.html?dir=desc&limit=24&mode=grid&order=position&p=3"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/bestecke.html?dir=desc&limit=24&mode=grid&order=position&p=4"

    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/skt.html?dir=desc&limit=24&mode=grid&order=position"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/skt.html?dir=desc&limit=24&mode=grid&order=position&p=2"

    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/kuchenhelfer.html?dir=desc&limit=24&mode=grid&order=position"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/kuchenhelfer.html?dir=desc&limit=24&mode=grid&order=position&p=2"

    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/pfanne.html?dir=desc&limit=24&mode=grid&order=position"

    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/kochtopfe.html?p=1"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/kochtopfe.html?p=2"

    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/kaffee-tee.html?p=1"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wmf/kaffee-tee.html?p=2"

    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wusthof.html?dir=desc&limit=24&mode=grid&order=position&p=1"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wusthof.html?dir=desc&limit=24&mode=grid&order=position&p=2"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wusthof.html?dir=desc&limit=24&mode=grid&order=position&p=3"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wusthof.html?dir=desc&limit=24&mode=grid&order=position&p=4"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wusthof.html?dir=desc&limit=24&mode=grid&order=position&p=5"
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/wusthof.html?dir=desc&limit=24&mode=grid&order=position&p=6"

    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/silit.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&___store=en&dir=desc&limit=24&order=name"

    ZH_PRODUCT_DETAILS_LINK = "//div[@class='category-products']/descendant::" \
                              "ul[contains(@class,'products-grid')]/descendant::a[@class='product-image']/@href"

    PROD_LANDING_IMG_SRC = "//img[@id='image']/@src"

    PROD_LANDING_IMG_TITLE = "//form[@id='product_addtocart_form']/div[@class='product-shop']" \
                             "/div[@class='product-name']/h1/text()"

    ADD_TO_CART_BUTTON = "//button[@id='product-addtocart-button']/descendant::span/text()"

    start_urls = [ZH_PRODUCT_LISTING_LINK]

    def parse(self, response):
        print response.request.headers['User-Agent']
        # print response.request.headers.get('Referrer', None)
        items = response.xpath(self.ZH_PRODUCT_DETAILS_LINK).extract()
        print len(items)
        for index, item in enumerate(items):
            print 'crawling %d. element: ' % index + item
            request = Request(item, callback=self.parse_product_zh_details, meta={'item_index': index})
            yield request

    def parse_product_zh_details(self, response):
        item_index = response.meta["item_index"]
        product_images = response.xpath(self.PROD_LANDING_IMG_SRC).extract()
        product_title_holder = response.xpath(self.PROD_LANDING_IMG_TITLE).extract()
        add_tocartbutton_holder = response.xpath(self.ADD_TO_CART_BUTTON).extract()

        if len(product_title_holder) > 0:
            product_title = self.processProductTitle(product_title_holder)
        else:
            product_title = 'empty'

        image_title = product_title

        if len(add_tocartbutton_holder) > 0:
            print add_tocartbutton_holder[0]

        if len(product_images) > 0 and len(product_images[0].strip()) > 0:
            image_title = self.generateImageName(image_title, product_images)
        else:
            print "***** %d. item's image src is empty****" % item_index
            product_images = ["http://www.liwus.de/skin/frontend/base/default/liwus_logo_200_80.png"]

        print "img src %s; img title %s " % (product_images[0], product_title[0])
        yield LegoImageItem(title=image_title, image_urls=product_images)

    def processProductTitle(self, product_title_holder):
        # replace comma & space with -
        # str.replace() does not recognize regular expressions, to perform a substitution using
        # regular expressions use re.sub().

        # product_title = product_title_holder[0].replace(', ', '-')
        # product_title = product_title.replace(',', '-')

        # product_title = product_title.replace(' ', '-')
        # # replace / with -
        # product_title = product_title.replace('/', '-')
        # product_title = product_title.lower()

        print "original product title: " + product_title_holder[0]
        tmp = re.sub('((\s)*,(\s)*)', '-', product_title_holder[0])
        print "all comma replaced, it becomes: " + tmp
        tmp = re.sub('((\s)+)', '-', tmp)
        print "all space replaced, it becomes: " + tmp
        tmp = tmp.replace("/", "-")
        tmp = tmp.replace(".", "-")
        tmp = tmp.replace("+", "-")
        print "all forward / replaced, it becomes: " + tmp
        tmp = re.sub('((-)+)', '-', tmp)
        print "multiple - - - replaced, it becomes: " + tmp
        # replace german umlaut
        tmp = tmp.replace('ä', 'a')
        tmp = tmp.replace('Ä', 'a')
        tmp = tmp.replace('ö', 'o')
        tmp = tmp.replace('Ö', 'o')
        tmp = tmp.replace('ü', 'u')
        tmp = tmp.replace('Ü', 'u')
        tmp = tmp.replace('ß', 'ss')

        print "umlaut replaced, it becomes: " + tmp

        return tmp

    def generateImageName(self, image_title, product_images):
        # product_images[0] is like http://www.liwus.de/media/catalog/product/cache/1/
        # image/9df78eab33525d08d6e5fb8d27136e95/N/U/NUK_10176092.jpg
        prod_image_tmp = product_images[0].split('/')

        # image_name is the last part in the product_images[0], i.e. NUK_10176092.jpg
        image_name = prod_image_tmp[-1]

        # remove the suffix, we need only the name without the suffix .jpg
        image_name_tmp = image_name.split(".")
        image_name = image_name_tmp[0]

        # image name is equal to <product title>-<image name>
        image_title = image_title + '-' + image_name
        image_title = image_title.lower()
        return image_title
