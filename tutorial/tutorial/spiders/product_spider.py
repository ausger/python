# -*- coding: utf-8 -*-
import scrapy
import csv
import sys
from deepdiff import DeepDiff

from tutorial.items import LegoItem
# import logging
from scrapy.http.request import Request
from scrapy.contrib.spiders import Rule

reload(sys)
sys.setdefaultencoding('utf8')


class ProductSpider(scrapy.Spider):
    # Scrapy is single-threaded, except the interactive shell and some tests, see source.
    # Scrapy does most of it's work synchronously. However, the handling of requests is done asynchronously.
    name = "product"
    allowed_domains = ["www.amazon.cn", "www.amazon.de"]

    # duplo & juniors
    # export_file_name = "ausger_magmi_duplo.csv"
    # product_ids = ['10587', '10590', '10594', '10595', '10596', '10600', '10615', '10616', '10617',
    #                '10618', '10674', '10682']
    # product_id_mapping = {'10587': '52,2-5岁,duplo', '10590': '29,2-5岁,duplo', '10594': '38,2-5岁,duplo',
    #                       '10595': '87,2-5岁,duplo', '10596': '63,2-5岁,duplo', '10600': '29,2-5岁,duplo',
    #                       '10615': '12,1.5-5岁,duplo', '10616': '25,1.5-5岁,duplo', '10617': '26,1.5-5岁,duplo',
    #                       '10618': '70,1.5-5岁,duplo', '10674': '306,4-7岁,juniors', '10682': '1000,4岁以上,classic'}

    # classic
    # export_file_name = "ausger_magmi_classic.csv"
    #
    # product_ids = ['10692', '10693', '10694', '10696', '10699', '10700', '10701']
    #
    # product_id_mapping = {'10692': '22,4岁以上,classic', '10693': '303,4岁以上,classic', '10694': '303,4岁以上,classic',
    #
    #                       '10696': '484,4岁以上,classic', '10699': '1,4岁以上,classic', '10700': '1,4岁以上,classic',
    #                       '10701': '1,4岁以上,classic'}

    # export_file_name = "ausger_magmi_creator.csv"
    # product_ids = ['31003', '31010', '31022', '31023', '31026', '31027', '31028', '31029', '31030',
    #                '31031', '31032', '31033', '31034', '31035', '31036']
    # product_id_mapping = {'31003': '145,6-12岁,creator',
    #                       '31010': '356,7-12岁,creator',
    #                       '31022': '186,7-12岁,creator',
    #                       '31023': '328,7-12岁,creator',
    #                       '31026': '1023,6岁以上,creator',
    #                       '31027': '67,6-12岁,creator',
    #                       '31028': '53,6-12岁,creator',
    #                       '31029': '132,6-12岁,creator',
    #                       '31030': '106,6-12岁,creator',
    #                       '31031': '215,6-12岁,creator',
    #                       '31032': '221,6-12岁,creator',
    #                       '31033': '264,6-12岁,creator',
    #                       '31034': '237,6-12岁,creator',
    #                       '31035': '286,7-12岁,creator',
    #     #                   '31036': '466,7-12岁,creator'}

    # export_file_name = "ausger_magmi_friends.csv"
    # product_ids = ['3933', '3935', '41005', '41015', '41035', '41037', '41038', '41039', '41056',
    #                '41057', '41058', '41059', '41091', '41093', '41094', '41095', '41097']
    # product_id_mapping = {'3933': '81,5-12岁,friends',
    #                       '3935': '73,5-12岁,friends',
    #                       '41005': '487,6-12岁,friends',
    #                       '41015': '612,7-12岁,friends',
    #                       '41035': '277,6-12岁,friends',
    #                       '41037': '369,6-12岁,friends',
    #                       '41038': '473,7-12岁,friends',
    #                       '41039': '721,6-12岁,friends',
    #                       '41056': '278,6-12岁,friends',
    #                       '41057': '355,6-12岁,friends',
    #                       '41058': '1120,7-12岁,friends',
    #                       '41059': '320,7-12岁,friends',
    #                       '41091': '187,5-12岁,friends',
    #                       '41093': '119,6-12岁,friends',
    #                       '41094': '476,6-12岁,friends',
    #                       '41095': '706,6-12岁,friends',
    #                       '41097': '254,6-12岁,friends'}

    # export_file_name = "ausger_magmi_technic_hero_city.csv"
    # product_ids = ['42009', '42025', '44003', '44029', '60004', '60047', '60048', '60050', '60055',
    #                '60057', '60060', '60069', '60085', '60086', '60088', '6176']
    # product_id_mapping = {'42009': '2606,11-16岁,technic',
    #                       '42025': '1297,10-16岁,technic',
    #                       '44003': '46,6-12岁,hero',
    #                       '44029': '218,8-14岁,hero',
    #                       '60004': '752,6-12岁,city',
    #                       '60047': '854,6-12岁,city',
    #                       '60048': '249,5-12岁,city',
    #                       '60050': '423,6-12岁,city',
    #                       '60055': '78,5-12岁,city',
    #                       '60057': '195,5-12岁,city',
    #                       '60060': '350,5-12岁,city',
    #                       '60069': '707,6-12岁,city',
    #                       '60085': '301,5-12岁,city',
    #                       '60086': '242,5-12岁,city',
    #                       '60088': '92,5-12岁,city',
    #                       '6176': '80,1-5岁,city'}

    # product_ids = ['41097']
    # product_id_mapping = {'41097': '254,6-12岁,friends'}

    # export_file_name = "ausger_magmi_chima_ninja.csv"
    # product_ids = ['70144', '70145', '70146', '70228', '70745', '70746', '70748', '70749', '70750',
    #                '70753', '70754', '70755', '70756']
    # product_id_mapping = {'70144': '450,8-14岁,chima',
    #                       '70145': '604,8-14岁,chima',
    #                       '70146': '1301,9-14岁,chima',
    #                       '70228': '480,8-14岁,chima',
    #                       '70745': '219,7-14岁,ninjago',
    #                       '70746': '311,7-14岁,ninjago',
    #                       '70748': '360,7-14岁,ninjago',
    #                       '70749': '219,7-14岁,ninjago',
    #                       '70750': '756,7-14岁,ninjago',
    #                       '70753': '94,7-14岁,ninjago',
    #                       '70754': '153,7-14岁,ninjago',
    #                       '70755': '188,7-14岁,ninjago',
    #                       '70756': '215,7-14岁,ninjago'}

    # export_file_name = "ausger_magmi_bionicle_starwars.csv"
    # product_ids = ['70784', '75038', '75040', '75076', '75077', '75078', '75079', '75080', '75081',
    #                '75085', '75089', '75090']
    # product_id_mapping = {'70784': '685,7-14岁,bionicle',
    #                       '75038': '223,8岁,starwars',
    #                       '75040': '261,7-12岁,starwars',
    #                       '75076': '105,6-12岁,starwars',
    #                       '75077': '102,6-12岁,starwars',
    #                       '75078': '141,6-12岁,starwars',
    #                       '75079': '95,6-12岁,starwars',
    #                       '75080': '251,7-12岁,starwars',
    #                       '75081': '247,7-12岁,starwars',
    #                       '75085': '163,7-12岁,starwars',
    #                       '75089': '105,6-12岁,starwars',
    #                       '75090': '253,7-12岁,starwars'}

    categories = {'duplo': '[Chinese Category]/益智玩具/乐高/Duplo 得宝',
                  'juniors': '[Chinese Category]/益智玩具/乐高/Junior 小拼砌师',
                  'classic': '[Chinese Category]/益智玩具/乐高/Classic 经典创意',
                  'creator': '[Chinese Category]/益智玩具/乐高/Creator 创意百变',
                  'friends': '[Chinese Category]/益智玩具/乐高/Friends 好朋友',
                  'technic': '[Chinese Category]/益智玩具/乐高/Technic 机械模型',
                  'hero': '[Chinese Category]/益智玩具/乐高/Hero Factory 英雄工厂',
                  'city': '[Chinese Category]/益智玩具/乐高/City 城市',
                  'chima': '[Chinese Category]/益智玩具/乐高/Chima 气功传奇',
                  'ninjago': '[Chinese Category]/益智玩具/乐高/Ninjago 幻影忍者',
                  'bionicle': '[Chinese Category]/益智玩具/乐高/Bionicle 生化战士',
                  'starwars': '[Chinese Category]/益智玩具/乐高/Star Wars 星球大战',
                  }
    store='base'
    brand_name = 'lego'
    country_of_manu='Germany'
    featured='No'
    UTF_8_ENCODING='utf-8'
    attribute_set='Toys'
    product_type='simple'
    product_websites='base'
    image=''
    image_label=''
    small_image=''
    small_image_label=''
    thumbnail=''
    thumbnail_label=''
    media_image=''
    media_gallery=''
    meta_description=''
    meta_title=''
    meta_keywords=''
    special_price=''
    visibility='4'
    weight='1'
    quantity='50'
    is_in_stock='1'
    TAX_CLASS_ID='2'
    STATUS='1'
    USE_CONFIG='Use config'

    PRODUCT_INFO_COLUMN='Product Info Column'
    PRODUCT_SHORT_DESCRIPTION="半个多世纪前，具有搭扣和连接功能的乐高颗粒获得专利。LEGO来自丹麦语“LEG GODT”，原意为“尽情地玩”。大小颜色不一的乐高颗粒，却能制造出无限的创意和梦想，让人惊叹！乐高集团怀着热情、决心和梦想，制造最优质的玩具；50多年以来，乐高玩具已经成为最知名的拼插类玩具，并两度被誉为“世纪玩具”。欢迎进入乐高玩具的创意世界！乐高玩具为孩子们带来比以往更多的选择，让他们更容易进入充满想象力的创意世界;乐高玩具总能激发孩子们的创造力和热情，陪伴他们度过充满欢乐的童年！"
    size=''

    outputted_products = []
    failed_products = []

    product_csv_file = open(export_file_name, 'wt')
    writer = csv.writer(product_csv_file)


    amazon_cn_search_result_link = "http://www.amazon.cn/s/ref=nb_sb_noss?__mk_zh_CN=" \
                                   "%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99&url=" \
                                   "search-alias%3Daps&field-keywords=%E4%B9%90%E9%AB%98+"

    amazon_de_search_result_link = "http://www.amazon.de/s/ref=nb_sb_noss_1?__mk_de_DE=" \
                                   "%C3%85M%C3%85%C5%BD%C3%95%C3%91" \
                                   "&url=search-alias%3Daps&field-keywords=lego+{0}&rh=i%3Aaps%2Ck%3A" + \
                                   brand_name + "+"

    zh_prod_details_link = "//li[@id='result_0']/descendant::a[contains(@class,'a-link-normal')]/@href"
    de_prod_details_link = "//li[@id='result_0']/descendant::a[contains(@class,'a-link-normal')]/@href"
    zh_search_result_prod_title = "//li[@id='result_0']/descendant::h2[contains(@class,'s-access-title')]/text()"
    zh_prod_title_loc = "//span[@id='productTitle']/text()"
    de_prod_title_loc = "//span[@id='productTitle']/text()"
    zh_prod_des_img = "//div[@id='productDescription']/div[@class='aplus']/img"
    de_prod_price_id = "//span[@id='priceblock_ourprice']"

    start_urls = [amazon_cn_search_result_link + "%s" % n for n in product_ids]

    # log.start(logfile="log.txt", loglevel="DEBUG", logstdout=None)

    #rules = (
    #    Rule(SgmlLinkExtractor(allow_domains=('example.com'),allow=('12\.html'),unique=True),callback='parsecatpage'),)

    def parse(self, response):
        url_parts = response.url.split("%20")
        print 'last part of URL: ' + url_parts[-1]

        # current_product_id = response.meta["product_id"]
        current_product_id = url_parts[-1]
        print "search result - current product_id: " + current_product_id
        # Get the real product details page link from the search result page
        request = self.crawler_zh_product_details(self.zh_prod_details_link, response, current_product_id)
        yield request

    def parse_product_zh_search_result(self, response):

        url_parts = response.url.split("%")
        print 'last part of URL: ' + url_parts[-1].strip()

        # current_product_id = response.meta["product_id"]
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

    def crawler_de_product_details(self, prod_details_link, response):

        ref_link = response.xpath(prod_details_link).extract()
        print 'german product details page is: ' + ref_link[0]
        # need to crawl the product details page.
        request = Request(ref_link[0], callback=self.parse_product_de_details)
        return request

    def parse_product_zh_details(self, response):
        product_name = response.xpath(self.zh_prod_title_loc).extract()
        print 'product chinese name is ' + product_name[0]

        product_description_holder = response.xpath(self.zh_prod_des_img).extract()
        if len(product_description_holder) > 0:
            product_description = product_description_holder[0].strip()
            print "product chinese description is " + product_description
        else:
            product_description = self.PRODUCT_SHORT_DESCRIPTION

        current_product_id = response.meta["product_id"]
        print "parse details - current product_id: " + current_product_id

        pieces_age = self.product_id_mapping[current_product_id].split(",")
        # crawler the search result page from amazon.de
        lego_item = LegoItem()
        lego_item['product_id'] = current_product_id
        lego_item['name'] = product_name[0] + " " + pieces_age[0] + " 颗粒"
        print 'item name ' + lego_item['name']
        lego_item['description'] = product_description
        lego_item['pieces'] = pieces_age[0]
        print 'item pieces ' + lego_item['pieces']
        lego_item['age'] = pieces_age[1]
        print 'item age ' + lego_item['age']
        print 'item category ' + pieces_age[2]
        lego_item['category'] = self.categories[pieces_age[2]]
        yield lego_item
        search_result_url = self.amazon_de_search_result_link.replace("{0}", current_product_id) + current_product_id
        print 'going to crawl ' + search_result_url
        request = Request(search_result_url, callback=self.crawler_product_de_details,
                          meta={'item': lego_item})
        yield request

    def crawler_product_de_details(self, response):
        # get item from response
        item = LegoItem(response.meta["item"])
        print 'lego item name ' + item['name']
        # retrieve the product details link from the response and
        # crawl the product details page and parse the required information such as price, name.
        ref_link = response.xpath(self.de_prod_details_link).extract()
        print 'german product details link ' + ref_link[0]
        request = Request(ref_link[0], callback=self.parse_product_de_details, meta={'item': item})
        yield request

    def parse_product_de_details(self, response):
        product_name_holder = response.xpath(self.de_prod_title_loc).extract()

        product_name = product_name_holder[0].lower().replace("-", "")
        product_name = product_name.replace(",", " ")
        sku = "-".join(product_name.split(" "))
        print 'product german name is ' + sku

        prod_price_holder = response.xpath(self.de_prod_price_id + "/text()").extract()
        if len(prod_price_holder) == 0 :
            prod_price_holder = response.xpath("//div[@id='olp_feature_div']/descendant::span[@class='a-color-price']" + "/text()").extract()

        product_price = prod_price_holder[0].split(" ")
        product_price = product_price[-1].replace(',', '.')
        print 'product german price is ' + product_price

        item = LegoItem(response.meta["item"])
        print 'lego item name ' + item['name']
        print 'lego item description ' + item['description']
        item2 = LegoItem()
        item2['product_id'] = item['product_id']
        item2['name'] = item['name']
        item2['description'] = item['description']
        item2['price'] = product_price
        item2['sku'] = sku
        item2['url_key'] = sku
        item2['pieces'] = item['pieces']
        item2['age'] = item['age']
        item2['category'] = item['category']

        yield item2
        self.write_to_product_csv(item2)

    def write_to_product_csv(self, item):

        a_row = item['name'] + "," + item['description'] +\
                "," + item["price"] + "," + item["sku"] + "," + item["url_key"] + ',' + \
                item['pieces'] + ',' + item['age'] + ',' + item['category']
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

            self.writer.writerow((item["sku"], self.store, self.attribute_set, self.product_type, item['category'], self.product_websites, item['age'],'','',
                            self.brand_name,'','','','',self.country_of_manu,'','',
                            '','','',item['description'],self.featured,'',
                            '','0',self.image,self.image_label,'','',self.media_gallery,
                            self.meta_description,self.meta_keywords,self.meta_title,'','',self.USE_CONFIG,
                            self.USE_CONFIG,item['name'],'','',self.PRODUCT_INFO_COLUMN,'',item["price"],
                            '0',self.PRODUCT_SHORT_DESCRIPTION,'',self.size,self.small_image,self.small_image_label,'',
                            self.special_price,'',self.STATUS,self.TAX_CLASS_ID,self.thumbnail,self.thumbnail_label,'',item["url_key"],
                            item["url_key"]+'.html',self.visibility,self.weight,self.quantity,'0','1','0','0',
                            '1','1','1','0','1',
                            self.is_in_stock,'','1','0','1',
                            '0','1','0','1',
                            '0','0','','','',
                            '','','','',
                            '','','','','',
                            '','','','','',
                            self.media_image,'','1','0'))
            print ((item["sku"], self.store, self.attribute_set, self.product_type, item['category'], self.product_websites, item['age'],'','',
                            self.brand_name,'','','','',self.country_of_manu,'','',
                            '','','',item['description'],self.featured,'',
                            '','0',self.image,self.image_label,'','',self.media_gallery,
                            self.meta_description,self.meta_keywords,self.meta_title,'','',self.USE_CONFIG,
                            self.USE_CONFIG,item['name'],'','',self.PRODUCT_INFO_COLUMN,'',item["price"],
                            '0',self.PRODUCT_SHORT_DESCRIPTION,'',self.size,self.small_image,self.small_image_label,'',
                            self.special_price,'',self.STATUS,self.TAX_CLASS_ID,self.thumbnail,self.thumbnail_label,'',item["url_key"],
                            item["url_key"]+'.html',self.visibility,self.weight,self.quantity,'0','1','0','0',
                            '1','1','1','0','1',
                            self.is_in_stock,'','1','0','1',
                            '0','1','0','1',
                            '0','0','','','',
                            '','','','',
                            '','','','','',
                            '','','','','',
                            self.media_image,'','1','0'))
            self.outputted_products.append(item['product_id'])

        finally:
            print "failed product %d, outputted product %d, product list size %d" \
                  % (len(self.failed_products), len(self.outputted_products), len(self.product_ids))
            if len(self.failed_products) + len(self.outputted_products) == len(self.product_ids):
                print "failed product: " + ','.join(self.failed_products)
                self.product_csv_file.close()
