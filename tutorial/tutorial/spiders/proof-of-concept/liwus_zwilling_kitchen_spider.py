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
    name = "liwus-zwilling-kitchen"
    allowed_domains = ["www.liwus.de"]

    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/suitcases-and-luggage.html"
    #category = "[Chinese Category]/休闲旅游/箱包"
    #export_file_name = "magmi_rimowa.csv"
    #image_folder_prefix = "/rimowa/"
    #brand_name = 'RIMOWA'
    #attribute_set= 'Luggage'
    #product_short_description= "RIMOWA高级旅行箱品牌是德国为数不多的旅行箱生产商之一，也是行业内仅有的承袭百年传统的生产商之一。产品采用了以坚固、耐用、轻巧著称的铝镁合金及高科技聚碳酸酯两种材料制作而成，集优质素材、卓越科技、独特设计及超凡手艺于一身，成为“德国制造”的又一传奇。"
    #product_description_images= "<img width='100%' src='https://img.alicdn.com/imgextra/i3/2037026074/TB2xVsxfXXXXXb4XpXXXXXXXXXX_!!2037026074.jpg'/><img width='100%' src='https://img.alicdn.com/imgextra/i1/2037026074/TB2kIMGfXXXXXbEXpXXXXXXXXXX_!!2037026074.jpg'/>"

    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/alfi/isolierkanne.html?___store=en&dir=asc&limit=50&order=name"
    #category = "[Chinese Category]/休闲旅游/保温壶"
    #export_file_name = "magmi_alfi.csv"
    #image_folder_prefix = "/alfi/Isolierkanne/"
    #brand_name = 'ALFI'
    #attribute_set= 'Alfi Drinkbottle'
    #product_short_description= "百年来每一只ALFI的产品都是拥有市场上的高品质的保证,资深熟练的工程设计师针对每道工序反复检验,确保产品100%符合保准,加上独特的抽真空双层玻璃内胆设计,经过1400摄氏度煅烧而成,保温保冷效力可以长时间维持. 采用高品质的材料及无毒可回收的环保材料是ALFI对消费者及环境的承诺."
    #product_description_images= "<img width='100%' src='https://img.alicdn.com/imgextra/i3/2663345110/TB2aqV_kXXXXXcBXpXXXXXXXXXX_!!2663345110.jpg'><img width='100%' src='https://img.alicdn.com/imgextra/i2/2663345110/TB2AmKMkXXXXXbwXXXXXXXXXXXX_!!2663345110.jpg'>"

    # 中文Zwilling美妆工具 https://list.tmall.com/search_shopitem.htm?user_id=2115745306&cat=2&spm=a1z10.5-b.a2227oh.d100&oq=zwilling%C3%C0%D7%B1%B9%A4%BE%DF%C6%EC%BD%A2%B5%EA&suggest=0_4&ds=1&stype=search
    #ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/zwilling/zwilling-beauty.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&dir=desc&order=name"
    #ZH_PRODUCT_LISTING_LINK_2 = "http://www.liwus.de/haushaltswaren/zwilling/zwilling-beauty.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&dir=desc&order=name&p=2"
    #ZH_PRODUCT_LISTING_LINK_3 = "http://www.liwus.de/haushaltswaren/zwilling/zwilling-beauty.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&dir=desc&order=name&p=3"

    ZH_PRODUCT_LISTING_LINK = "http://www.liwus.de/haushaltswaren/zwilling/zwilling-kuchen.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&dir=asc&order=name"
    ZH_PRODUCT_LISTING_LINK_2 = "http://www.liwus.de/haushaltswaren/zwilling/zwilling-kuchen.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&dir=asc&order=name&p=2"
    ZH_PRODUCT_LISTING_LINK_3 = "http://www.liwus.de/haushaltswaren/zwilling/zwilling-kuchen.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&dir=asc&order=name&p=3"
    ZH_PRODUCT_LISTING_LINK_4 = "http://www.liwus.de/haushaltswaren/zwilling/zwilling-kuchen.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&dir=asc&order=name&p=4"
    ZH_PRODUCT_LISTING_LINK_5 = "http://www.liwus.de/haushaltswaren/zwilling/zwilling-kuchen.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&dir=asc&order=name&p=5"
    ZH_PRODUCT_LISTING_LINK_6 = "http://www.liwus.de/haushaltswaren/zwilling/zwilling-kuchen.html?SID=kv6bt8uq0bi32oi7a2c94m0th3&dir=asc&order=name&p=6"

    start_urls = [ZH_PRODUCT_LISTING_LINK,ZH_PRODUCT_LISTING_LINK_2,ZH_PRODUCT_LISTING_LINK_3,ZH_PRODUCT_LISTING_LINK_4,ZH_PRODUCT_LISTING_LINK_5,ZH_PRODUCT_LISTING_LINK_6]

    category = "[Chinese Category]/厨房用具/"
    export_file_name = "magmi_zwilling_kitchen.csv"
    image_folder_prefix = "/zwilling/kitchen/"
    brand_name = 'Zwilling'
    attribute_set= 'Kitchen'
    product_short_description= "双立人品牌是Peter·Henckels（彼得·亨克斯先生）以双子座作为最初的构想，在德国美丽的莱茵河畔小镇索林根创立的品牌。同时也揭开了这一人类现存最古老商标之一不老传说的序幕。他的后代约翰·阿布雷汉姆·亨克斯将公司名称改成Zwilling J.A.Henckel.US。 双立人拥有超过2000种的不锈钢刀剪餐具、锅具、厨房炊具和个人护理用品，开创了摩登厨房理念，让烹饪成为一种享受，带给人们看得见的完美品质和生活情趣。"
    product_description_images= "<img width='80%' src='/media/wysiwyg/zwilling/zwilling-ny-fifth-ave-1907.jpg'>"

    BESTECK_PATTERN = "(.)*besteck(.)*"
    KITCHEN_HELPER_PATTERN = "(.)*(backpinsel|offner|knoblauchpresse|kuchenhelfer|messerscharfer|watzstahl|lo(e)*ffel|scheebesen)(.)*"
    KITCHEN_HELPER_PATTERN_2 = "(.)*(pinzette-abgewinkelt-mattiert|schalmesser|schaler|teigschaber|wender|topfuntersetzer)(.)*"
    KITCHEN_ORGANIZER_PATTERN = "(.)*tool-box-bambus(.)*"
    KITCHEN_BLATTER_PATTERN = "(.)*(brett|platillo-magnetis)(.)*"
    KITCHEN_PAN_PATTERN = "(.)*(pfanne-|topf-|dampfeinsatz|raucherset-|wok-)(.)*"
    KITCHEN_PAN_SET_PATTERN = '(.)*(koch(.)*set-|touristen-set-13tlg--zwilling)(.)*'
    KITCHEN_KNIFE_PATTERN = '(.)*(messer-)(.)*'
    KITCHEN_KNIFE_SET_PATTERN = '(.)*(block|style-2tlg--zwilling_32433-001-0)(.)*'
    KITCHEN_SCISSOR_PATTERN = '(.)*schere(.)*'
    KITCHEN_COOK_POT = '(.)*kessel(.)*'

    product_category = {BESTECK_PATTERN : '[Chinese Category]/厨房用具/餐具器皿',
                        KITCHEN_HELPER_PATTERN: '[Chinese Category]/厨房用具/厨房小工具',
                        KITCHEN_HELPER_PATTERN_2: '[Chinese Category]/厨房用具/厨房小工具',
                        KITCHEN_ORGANIZER_PATTERN: '[Chinese Category]/厨房用具/厨房收纳',
                        KITCHEN_BLATTER_PATTERN:'[Chinese Category]/厨房用具/砧板',
                        KITCHEN_PAN_PATTERN:'[Chinese Category]/厨房用具/德国锅具',
                        KITCHEN_PAN_SET_PATTERN:'[Chinese Category]/厨房用具/德国锅具/德国锅具套装',
                        KITCHEN_KNIFE_PATTERN:'[Chinese Category]/厨房用具/德国刀具',
                        KITCHEN_KNIFE_SET_PATTERN:'[Chinese Category]/厨房用具/德国刀具/德国刀具套装',
                        KITCHEN_SCISSOR_PATTERN:'[Chinese Category]/厨房用具/厨房专用剪刀',
                        KITCHEN_COOK_POT:'[Chinese Category]/厨房用具/杯壺烘焙'}

    #category = "[Chinese Category]/美妆护肤/美妆工具"
    #export_file_name = "magmi_zwilling_manicure.csv"
    #image_folder_prefix = "/zwilling/beauty/"
    #brand_name = 'Zwilling'
    #attribute_set= 'Manicure'
    #product_short_description= "双立人品牌是Peter·Henckels（彼得·亨克斯先生）以双子座作为最初的构想，在德国美丽的莱茵河畔小镇索林根创立的品牌。同时也揭开了这一人类现存最古老商标之一不老传说的序幕。他的后代约翰·阿布雷汉姆·亨克斯将公司名称改成Zwilling J.A.Henckel.US。 双立人拥有超过2000种的不锈钢刀剪餐具、锅具、厨房炊具和个人护理用品，开创了摩登厨房理念，让烹饪成为一种享受，带给人们看得见的完美品质和生活情趣。"
    #product_description_images= "<img width='100%' src='http://s2.sinaimg.cn/mw690/001Tjud7gy6EouKfjVve1&690'>"


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
            self.category = self.get_category_name(self.image_title)

        liwus_item = LiwusItem()

        liwus_item['age']= self.AGE
        liwus_item['attribute_set']= self.attribute_set
        liwus_item['brand']= self.brand_name
        liwus_item['category']= self.category

        if len(prod_description_holder) > 0:
            liwus_item['description']= prod_description_holder[0] + self.product_description_images

        liwus_item['img']= self.image_folder_prefix + self.image_title
        liwus_item['meta_title']= self.meta_title
        liwus_item['meta_keywords']= self.meta_keywords
        liwus_item['meta_description']= self.meta_description
        liwus_item['name']= product_title

        if len(prod_price_holder) > 0:
            self.get_price(liwus_item, prod_price_holder)
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
            self.failed_products.append(item_index)
            return

        liwus_item['url_key'] = self.url_key

        if len(add_tocartbutton_holder) > 0 and add_tocartbutton_holder[0] == 'Add to Cart':
            # output this product!
            self.write_to_product_csv(liwus_item)
        else:
            print "%s is only for pre order, no output"
            self.failed_products.append(item_index)

    def get_price(self, liwus_item, prod_price_holder):
        tmp = prod_price_holder[0]
        print "price was " + prod_price_holder[0]
        tmp = tmp.replace('€', '')
        liwus_item['price'] = tmp.strip()
        print "now price is " + liwus_item['price']

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

    def get_category_name(self, product_image_name):
        matched = 0
        for key, value in self.product_category.iteritems():
            result = re.match(key, product_image_name)
            if result is None:
                continue
            matched += 1
            print product_image_name + " matches " + key + " and it's category is: " + value
            return value
        if matched == 0:
            print "[no matches!]:" + product_image_name + " no matches!"
            return self.category
        # elif matched > 1:
        #     print "***" + product_image_name + " is matched %d times.***" % matched
        # else:
        #     print product_image_name + " is matched only once. OK"

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
            #if len(self.failed_products) + len(self.outputted_products) == self.item_count:
            #    print "failed product: " + ','.join(self.failed_products)
                # self.product_csv_file.close()
