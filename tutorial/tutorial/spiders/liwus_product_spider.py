# -*- coding: utf-8 -*-
import scrapy
import csv
import sys
import re

from tutorial.items import LiwusItem
# import logging
from scrapy.http.request import Request
from scrapy.contrib.spiders import Rule

reload(sys)
sys.setdefaultencoding('utf8')


class LiwusProductSpider(scrapy.Spider):
    # Scrapy is single-threaded, except the interactive shell and some tests, see source.
    # Scrapy does most of it's work synchronously. However, the handling of requests is done asynchronously.
    name = "liwus-product"
    allowed_domains = ["www.liwus.de"]

    category = "[Chinese Category]/休闲旅游"
    export_file_name = "magmi_rimowa.csv"
    image_folder_prefix = "/rimowa/"
    brand_name = 'RIMOWA'
    attribute_set= 'Luggage'
    product_short_description= "RIMOWA高级旅行箱品牌是德国为数不多的旅行箱生产商之一，也是行业内仅有的承袭百年传统的生产商之一。产品采用了以坚固、耐用、轻巧著称的铝镁合金及高科技聚碳酸酯两种材料制作而成，集优质素材、卓越科技、独特设计及超凡手艺于一身，成为“德国制造”的又一传奇。"

    STORE= 'base'
    AGE= ''
    COUNTRY_OF_MANU= 'Germany'
    FEATURED= 'No'
    UTF_8_ENCODING='utf-8'
    PRODUCT_TYPE= 'simple'
    PRODUCT_WEBSITES= 'base'
    image=''
    image_label=''
    small_image=''
    small_image_label=''
    thumbnail=''
    thumbnail_label=''
    MEDIA_IMAGE= ''
    MEDIA_GALLERY= ''
    meta_description=''
    meta_title=''
    image_title=''
    url_key=''
    meta_keywords=''
    SPECIAL_PRICE= ''
    VISIBILITY= '4'
    WEIGHT= '1'
    QUANTITY= '10'
    IS_IN_STOCK= '1'
    TAX_CLASS_ID='2'
    STATUS='1'
    USE_CONFIG='Use config'
    SIZE= ''
    PRODUCT_INFO_COLUMN='Product Info Column'

    outputted_products = []
    failed_products = []

    product_csv_file = open(export_file_name, 'wt')
    writer = csv.writer(product_csv_file)

    ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/suitcases-and-luggage.html"

    ZH_PRODUCT_DETAILS_LINK = "//div[@class='category-products']/descendant::" \
                              "ul[contains(@class,'products-grid')]/descendant::a[@class='product-image']/@href"

    PROD_LANDING_IMG_SRC = "//img[@id='image']/@src"

    PROD_LANDING_IMG_TITLE = "//form[@id='product_addtocart_form']/div[@class='product-shop']" \
                             "/div[@class='product-name']/h1/text()"

    PRODUCT_SKU_LOC = "//table[@id='product-attribute-specs-table']/descendant::td[contains(@class,'data')]/text()"

    PRODUCT_PRICE_LOC = "//form[@id='product_addtocart_form']/descendant::div[@class='price-box']/descendant::span[@class='price']/text()"

    ADD_TO_CART_BUTTON = "//button[@id='product-addtocart-button']/descendant::span/text()"

    PRODUCT_DESCRIPTION_LOC = "//div[@id='product_tabs_description_contents']/div[@class='std']/text()"

    item_count = 0
    start_urls = [ZH_PRODUCT_LISTING_LINK]

    # start_urls = [amazon_cn_search_result_link + "%s" % n for n in product_ids]

    def parse(self, response):
        # print response.request.headers['User-Agent']
        # print response.request.headers.get('Referrer', None)
        items = response.xpath(self.ZH_PRODUCT_DETAILS_LINK).extract()
        print len(items)
        self.item_count = len(items)
        for index, item in enumerate(items):
            print 'crawling %d. element: ' % index + item
            request = Request(item, callback=self.parse_product_zh_details, meta={'item_index': index})
            yield request

    def parse_product_zh_details(self, response):
        item_index = response.meta["item_index"]
        product_images = response.xpath(self.PROD_LANDING_IMG_SRC).extract()
        product_title_holder = response.xpath(self.PROD_LANDING_IMG_TITLE).extract()
        add_tocartbutton_holder = response.xpath(self.ADD_TO_CART_BUTTON).extract()
        prod_sku_holder = response.xpath(self.PRODUCT_SKU_LOC).extract()
        prod_description_holder = response.xpath(self.PRODUCT_DESCRIPTION_LOC).extract()
        prod_price_holder = response.xpath(self.PRODUCT_PRICE_LOC).extract()

        if len(product_title_holder) > 0:
            self.meta_title = product_title_holder[0] + ' - AUSGER「德藝緻」德國精品百貨'
            self.meta_keywords = product_title_holder[0]
            self.meta_description = product_title_holder[0]
            self.url_key = product_title_holder[0].decode('unicode_escape').encode('ascii','ignore')
            # or name.encode('ascii',errors='ignore')
            product_title = self.process_product_title(product_title_holder)

        if len(product_images) > 0 and len(product_images[0].strip()) > 0:
            self.image_title = self.generate_image_name(product_title, product_images)

        liwus_item = LiwusItem()

        liwus_item['age']= self.AGE
        liwus_item['attribute_set']= self.attribute_set
        liwus_item['brand']= self.brand_name
        liwus_item['category']= self.category

        if len(prod_description_holder) > 0:
            liwus_item['description']= prod_description_holder[0]

        liwus_item['img']= self.image_folder_prefix + self.image_title
        liwus_item['meta_title']= self.meta_title
        liwus_item['meta_keywords']= self.meta_keywords
        liwus_item['meta_description']= self.meta_description
        liwus_item['name']= product_title

        if len(prod_price_holder) > 0:
            liwus_item['price']= prod_price_holder[0]
        else:
            print "!!!! %s price is null!!!!" % product_title
            self.failed_products.append(item_index)
            return

        liwus_item['product_id']= item_index
        liwus_item['short_description']= self.product_short_description

        if len(prod_sku_holder) > 0:
            liwus_item['sku'] = prod_sku_holder[0]
            print 'sku is ' + liwus_item['sku']
        else:
            print 'sku is null'

        liwus_item['url_key'] = self.url_key

        if len(add_tocartbutton_holder) > 0 and add_tocartbutton_holder[0] == 'Add to Cart':
            # output this product!
            self.write_to_product_csv(liwus_item)

    def process_product_title(self, product_title_holder):
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

    def generate_image_name(self, image_title, product_images):
        # product_images[0] is like http://www.liwus.de/media/catalog/product/cache/1/
        # image/9df78eab33525d08d6e5fb8d27136e95/N/U/NUK_10176092.jpg
        prod_image_tmp = product_images[0].split('/')

        # image_name is the last part in the product_images[0], i.e. NUK_10176092.jpg
        image_name = prod_image_tmp[-1]

        # remove the suffix, we need only the name without the suffix .jpg
        image_name_tmp = image_name.split(".")
        image_name = image_name_tmp[0]

        # image name is equal to <product title>-<image name>
        image_title = image_title + '-' + image_name + '.jpg'
        image_title = image_title.lower()
        return image_title

    def write_to_product_csv(self, item):

        a_row = item['name'] + "," + item['description'] +\
                "," + item["price"] + "," + item["sku"] + "," + item["url_key"] + ',' + \
                ',' + item['age'] + ',' + item['category']
        print "row is " + a_row

        try:
            if len(self.outputted_products) == 0:
                print "output header fields into file"
                self.writer.writerow(('sku', '_store', '_attribute_set','_type','categories','_product_websites','age_range','aptamil_code','bottle_volume',
                             'brand','carseat_color','cartoon_figures','color','cost','country_of_manufacture','created_at','custom_design',
                             'custom_design_from','custom_design_to','custom_layout_update','description','featured','gallery',
                             'gift_message_available','has_options','image','image_label','manufacturer','material','media_gallery',
                             'meta_description','meta_keyword','meta_title','minimal_price','msrp','msrp_display_actual_price_type',
                             'msrp_enabled','name','news_from_date','news_to_date','options_container','page_layout','price',
                             'required_options','short_description','sigg_figure','size','small_image','small_image_label','special_from_date',
                             'special_price','special_to_date','status','tax_class_id','thumbnail','thumbnail_label','updated_at','url_key',
                             'url_path','visibility','weight','qty','min_qty','use_config_min_qty','is_qty_decimal','backorders',
                             'use_config_backorders','min_sale_qty','use_config_min_sale_qty','max_sale_qty','use_config_max_sale_qty',
                             'is_in_stock','notify_stock_qty','use_config_notify_stock_qty','manage_stock','use_config_manage_stock',
                             'stock_status_changed_auto','use_config_qty_increments','qty_increments','use_config_enable_qty_inc',
                             'enable_qty_increments','is_decimal_divided','_links_related_sku','_links_related_position','_links_crosssell_sku',
                             '_links_crosssell_position','_links_upsell_sku','_links_upsell_position','_associated_sku',
                             '_associated_default_qty','_associated_position','_tier_price_website','_tier_price_customer_group','_tier_price_qty',
                             '_tier_price_price','_group_price_website','_group_price_customer_group','_group_price_price','_media_attribute_id',
                             '_media_image','_media_lable','_media_position','_media_is_disabled'))

            self.writer.writerow((item['sku'], self.STORE, item['attribute_set'], self.PRODUCT_TYPE, item['category'], self.PRODUCT_WEBSITES, item['age'], '', '',
                                  item['brand'], '', '', '', '', self.COUNTRY_OF_MANU, '', '',
                                  '', '', '', item['description'], self.FEATURED, '',
                                  '', '0', item['img'], self.image_label, '', '', self.MEDIA_GALLERY,
                                  item['meta_description'], item['meta_keywords'], item['meta_title'], '', '', self.USE_CONFIG,
                                  self.USE_CONFIG, item['name'], '', '', self.PRODUCT_INFO_COLUMN, '', item["price"],
                                  '0', item['short_description'], '', self.SIZE, item['img'], self.small_image_label, '',
                                  self.SPECIAL_PRICE, '', self.STATUS, self.TAX_CLASS_ID, item['img'], self.thumbnail_label, '', item['url_key'],
                                  item['url_key'] +'.html', self.VISIBILITY, self.WEIGHT, self.QUANTITY, '0', '1', '0', '0',
                                  '1', '1', '1', '0', '1',
                                  self.IS_IN_STOCK, '', '1', '0', '1',
                                  '0', '1', '0', '1',
                                  '0', '0', '', '', '',
                                  '', '', '', '',
                                  '', '', '', '', '',
                                  '', '', '', '', '',
                                  self.MEDIA_IMAGE, '', '1', '0'))
            print ((item["sku"], self.STORE, item['attribute_set'], self.PRODUCT_TYPE, item['category'], self.PRODUCT_WEBSITES, item['age'], '', '',
                    item['brand'], '', '', '', '', self.COUNTRY_OF_MANU, '', '',
                    '', '', '', item['description'], self.FEATURED, '',
                    '', '0', item['img'], self.image_label, '', '', self.MEDIA_GALLERY,
                    item['meta_description'], item['meta_keywords'], item['meta_title'], '', '', self.USE_CONFIG,
                    self.USE_CONFIG, item['name'], '', '', self.PRODUCT_INFO_COLUMN, '', item["price"],
                    '0', item['short_description'], '', self.SIZE, item['img'], self.small_image_label, '',
                    self.SPECIAL_PRICE, '', self.STATUS, self.TAX_CLASS_ID, item['img'], self.thumbnail_label, '', item["url_key"],
                    item["url_key"] +'.html', self.VISIBILITY, self.WEIGHT, self.QUANTITY, '0', '1', '0', '0',
                    '1', '1', '1', '0', '1',
                    self.IS_IN_STOCK, '', '1', '0', '1',
                    '0', '1', '0', '1',
                    '0', '0', '', '', '',
                    '', '', '', '',
                    '', '', '', '', '',
                    '', '', '', '', '',
                    self.MEDIA_IMAGE, '', '1', '0'))
            self.outputted_products.append(item['product_id'])

        finally:
            print "failed product %d, outputted product %d, product list size %d" \
                  % (len(self.failed_products), len(self.outputted_products), self.item_count)
            if len(self.failed_products) + len(self.outputted_products) == self.item_count:
                print "failed product: " + ','.join(self.failed_products)
                self.product_csv_file.close()
