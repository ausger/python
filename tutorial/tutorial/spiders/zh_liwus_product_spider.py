# -*- coding: utf-8 -*-
import scrapy
import csv
import sys
import re

from tutorial.items import LiwusItem
# import logging
import ConfigParser
from scrapy.http.request import Request
from scrapy.contrib.spiders import Rule

reload(sys)
sys.setdefaultencoding('utf8')


class ZhLiwusProductSpider(scrapy.Spider):
    # Scrapy is single-threaded, except the interactive shell and some tests, see source.
    # Scrapy does most of it's work synchronously. However, the handling of requests is done asynchronously.
    name = "zh-liwus-product"
    allowed_domains = ["www.liwus.de"]
    data_feed_config = ConfigParser.ConfigParser()
    data_feed_config.read('/Users/leishang/helenstreet/python/tutorial/tutorial/spiders/datafeed-config.ini')

    # it needs to changed according to the product to be crawled.
    current_section = 'nuk_zh'
    brand_de = 'NUK'
    brand_zh = ''

    @staticmethod
    def config_section_map(section):
        dict1 = {}
        options = ZhLiwusProductSpider.data_feed_config.options(section)
        for option in options:
            try:
                dict1[option] = ZhLiwusProductSpider.data_feed_config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        print dict1
        return dict1

    def __init__(self, *a, **kw):
        print "***************** here ********************"
        print ZhLiwusProductSpider.data_feed_config.sections()
        super(ZhLiwusProductSpider, self).__init__(*a, **kw)
        self.category = ZhLiwusProductSpider.config_section_map(ZhLiwusProductSpider.current_section)['category']
        self.export_file_name = ZhLiwusProductSpider.config_section_map(ZhLiwusProductSpider.current_section)['export_file_name']
        self.image_folder_prefix = ZhLiwusProductSpider.config_section_map(ZhLiwusProductSpider.current_section)['image_folder_prefix']
        self.brand_name = ZhLiwusProductSpider.config_section_map(ZhLiwusProductSpider.current_section)['brand_name']
        self.attribute_set = ZhLiwusProductSpider.config_section_map(ZhLiwusProductSpider.current_section)['attribute_set']
        self.product_short_description = ZhLiwusProductSpider.config_section_map(ZhLiwusProductSpider.current_section)['product_short_description']
        self.product_description_images = ZhLiwusProductSpider.config_section_map(ZhLiwusProductSpider.current_section)['product_description_images']
        tmp = ZhLiwusProductSpider.config_section_map(ZhLiwusProductSpider.current_section)['start_urls']
        self.start_urls = tmp.split(",")
        print self.start_urls
        product_csv_file = open(self.export_file_name, 'wt')
        ZhLiwusProductSpider.writer = csv.writer(product_csv_file)


    #start_urls = ["http://www.liwus.de/suitcases-and-luggage.html"]
    BESTECK_PATTERN = "(.)*((餐具(.)*件套)|糖罐|调料罐|盐罐套装)(.)*"
    KITCHEN_HELPER_PATTERN = "(.)*((蒸笼)|((油|烧烤)刷)|((漏|炒菜|翻|翻炒)勺)|((压蒜|开罐|削皮|搅拌|去核|土豆泥|刨丝|打蛋)器)|面捞|水壶|锅铲|锅垫|配件|磨刀|核桃夹|切蛋)(.)*"
    KITCHEN_HELPER_PATTERN_2 = "(.)*(pinzette-abgewinkelt-mattiert|schal|teigschaber|wender|topfuntersetzer|multitool-clever|schraubdeckelzange)(.)*"
    KITCHEN_HELPER_PATTERN_3 = "(.)*(reparaturstein|pizza-steakm-set|schleifhilfe|schubladeneinsatz|wetzstahl|bbq-set)(.)*"
    KITCHEN_ORGANIZER_PATTERN = "(.)*(厨房置物架)(.)*"
    KITCHEN_BLATTER_PATTERN = "(.)*((砧|案|刀)板)(.)*"
    KITCHEN_PAN_PATTERN = "(.)*(奶|煎|炖|汤|高压|平底|炖肉|蒸)锅(.)*[^件套]*"
    KITCHEN_PAN_SET_PATTERN = "(.)*(奶|煎|炖|汤|高压|平底|炖肉|蒸)锅(.)*件套(.)*"
    KITCHEN_KNIFE_PATTERN = "[^(刮|军)]*刀[^(套装|件套|石|器|叉)]"
    KITCHEN_KNIFE_SET_PATTERN = "(.)*(刀[^叉]*(套装|件套))(.)*"
    KITCHEN_SCISSOR_PATTERN = "(.)*(剪(.)*)(.)*"
    KITCHEN_COOK_POT = "(.)*(kessel|glas|karaffe|tasse|becher|auflaufform|kanne|schussel|schale|teller|烤盘|水杯|杯子|烧水壶)(.)*"
    MANICURE = "(.)*(眉毛|美甲)(.)*"
    BAR_WEIN = "(.)*(启瓶器|开瓶器|bar|loft|shaker|flachmann|korkenzieher|clip-weinthermometer|topfring|flaschenverschlus|weinpumpe)(.)*"
    KAFFE = "(.)*(latte-macchiato|咖啡杯|茶壶)(.)*"
    SWISS = "(.)*((瑞士)军刀)(.)*"
    TABLE_WARE = "(.)*(糖罐|调料罐|盐罐套装|汤勺|拌色拉碗|奶油刮刀|面包刀|儿童煮蛋器|取食勺|餐盘|小吃碗|汤碗|盏|勺|果酱罐|胡椒罐|盐罐)(.)*"

    product_category = {BESTECK_PATTERN : '[Chinese Category]/厨房用具/餐具器皿',
                        KITCHEN_HELPER_PATTERN: '[Chinese Category]/厨房用具/厨房小工具',
                        KITCHEN_ORGANIZER_PATTERN: '[Chinese Category]/厨房用具/厨房收纳',
                        KITCHEN_BLATTER_PATTERN:'[Chinese Category]/厨房用具/砧板',
                        KITCHEN_PAN_SET_PATTERN:'[Chinese Category]/厨房用具/德国锅具/德国锅具套装',
                        KITCHEN_PAN_PATTERN:'[Chinese Category]/厨房用具/德国锅具',
                        KITCHEN_KNIFE_SET_PATTERN:'[Chinese Category]/厨房用具/德国刀具/德国刀具套装',
                        KITCHEN_KNIFE_PATTERN:'[Chinese Category]/厨房用具/德国刀具',
                        KITCHEN_SCISSOR_PATTERN:'[Chinese Category]/厨房用具/厨房专用剪刀',
                        KITCHEN_COOK_POT:'[Chinese Category]/厨房用具/杯壺烘焙',
                        MANICURE:'[Chinese Category]/美妆护肤/美妆工具',
                        BAR_WEIN:'[Chinese Category]/厨房用具/红酒器皿',
                        KAFFE:'[Chinese Category]/厨房用具/咖啡器皿',
                        SWISS:'[Chinese Category]/休闲旅游/瑞士军刀',
                        TABLE_WARE: '[Chinese Category]/厨房用具/餐桌用具'}

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


    ZH_PRODUCT_DETAILS_LINK = "//div[@class='category-products']/descendant::" \
                              "ul[contains(@class,'products-grid')]/descendant::a[@class='product-image']/@href"

    PROD_LANDING_IMG_SRC = "//img[@id='image']/@src"

    PROD_LANDING_IMG_TITLE = "//form[@id='product_addtocart_form']/div[@class='product-shop']" \
                             "/div[@class='product-name']/h1/text()"

    PRODUCT_SKU_LOC = "//table[@id='product-attribute-specs-table']/descendant::td[contains(@class,'data')]/text()"

    PRODUCT_PRICE_LOC = "//form[@id='product_addtocart_form']/descendant::div[@class='price-box']/descendant::span[@class='price']/text()"

    ADD_TO_CART_BUTTON = "//button[@id='product-addtocart-button']/descendant::span/text()"

    PRODUCT_DESCRIPTION_LOC = "//div[@id='product_tabs_description_contents']/div[@class='std']"

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
            self.image_title = self.generate_image_name(product_images)
            self.category = self.get_category_name(product_title)

        liwus_item = LiwusItem()

        liwus_item['age']= self.AGE
        liwus_item['attribute_set']= self.attribute_set
        liwus_item['brand']= self.brand_name
        liwus_item['category']= self.category

        if len(prod_description_holder) > 0:
            print 'description is: %s' % prod_description_holder[0]
            liwus_item['description']= prod_description_holder[0] + self.product_description_images
        else:
            print 'sku %s description is null' % prod_sku_holder[0]

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

        #if len(add_tocartbutton_holder) > 0 and add_tocartbutton_holder[0] == 'Add to Cart':
            # output this product!
        self.write_to_product_csv(liwus_item)
        #else:
        #    print "%s is only for pre order, no output"
        #    self.failed_products.append(item_index)

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

        prod_title = product_title_holder[0].strip()
        #print "original product title: " + prod_title
        if ZhLiwusProductSpider.brand_de.lower() not in prod_title.lower():
            prod_title = ZhLiwusProductSpider.brand_de + ' ' + prod_title
        if ZhLiwusProductSpider.brand_zh.lower() not in prod_title.lower():
            prod_title = ZhLiwusProductSpider.brand_zh + ' ' + prod_title
        #print 'now is: ' + prod_title
        return prod_title

    def generate_image_name(self, product_images):
        # product_images[0] is like http://www.liwus.de/media/catalog/product/cache/1/
        # image/9df78eab33525d08d6e5fb8d27136e95/N/U/NUK_10176092.jpg
        prod_image_tmp = product_images[0].split('/')

        # image_name is the last part in the product_images[0], i.e. NUK_10176092.jpg
        image_name = prod_image_tmp[-1]

        # remove the suffix, we need only the name without the suffix .jpg
        #image_name_tmp = image_name.split(".")
        #image_name = image_name_tmp[0]

        # image name is equal to <product title>-<image name>
        #image_title = image_title + '-' + image_name + '.jpg'
        #image_title = image_title.lower()
        return image_name.lower()

    def get_category_name(self, product_title_name):
        return self.category
        matched = 0
        for key, value in self.product_category.iteritems():
            print 'matching title %s against regex %s ' % (product_title_name, key)
            result = re.match(key.decode('utf-8'), product_title_name.decode('utf-8'))
            if result is None:
                continue
            matched += 1
            print product_title_name + " matches " + key + " and it's category is: " + value
            return value
        if matched == 0:
            print "[no matches!]:" + product_title_name + " no matches!"
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
                print "output header fields into file, remove image, small_image, thumnail"
                self.writer.writerow(('sku', '_store', '_attribute_set','_type','categories','name','_product_websites','age_range','aptamil_code','bottle_volume',
                             'brand','carseat_color','cartoon_figures','color','cost','country_of_manufacture','created_at','custom_design',
                             'custom_design_from','custom_design_to','custom_layout_update','description','featured','gallery',
                             'gift_message_available','has_options','image_label','manufacturer','material','media_gallery',
                             'meta_description','meta_keyword','meta_title','minimal_price','msrp','msrp_display_actual_price_type',
                             'msrp_enabled','news_from_date','news_to_date','options_container','page_layout','price',
                             'required_options','short_description','sigg_figure','size','small_image_label','special_from_date',
                             'special_price','special_to_date','status','tax_class_id','thumbnail_label','updated_at','url_key',
                             'url_path','visibility','weight','qty','min_qty','use_config_min_qty','is_qty_decimal','backorders',
                             'use_config_backorders','min_sale_qty','use_config_min_sale_qty','max_sale_qty','use_config_max_sale_qty',
                             'is_in_stock','notify_stock_qty','use_config_notify_stock_qty','manage_stock','use_config_manage_stock',
                             'stock_status_changed_auto','use_config_qty_increments','qty_increments','use_config_enable_qty_inc',
                             'enable_qty_increments','is_decimal_divided','_links_related_sku','_links_related_position','_links_crosssell_sku',
                             '_links_crosssell_position','_links_upsell_sku','_links_upsell_position','_associated_sku',
                             '_associated_default_qty','_associated_position','_tier_price_website','_tier_price_customer_group','_tier_price_qty',
                             '_tier_price_price','_group_price_website','_group_price_customer_group','_group_price_price','_media_attribute_id',
                             '_media_image','_media_lable','_media_position','_media_is_disabled'))

            self.writer.writerow((item['sku'], self.STORE, item['attribute_set'], self.PRODUCT_TYPE, item['category'], item['name'], self.PRODUCT_WEBSITES, item['age'], '', '',
                                  item['brand'], '', '', '', '', self.COUNTRY_OF_MANU, '', '',
                                  '', '', '', item['description'], self.FEATURED, '',
                                  '', '0', self.image_label, '', '', self.MEDIA_GALLERY,
                                  item['meta_description'], item['meta_keywords'], item['meta_title'], '', '', self.USE_CONFIG,
                                  self.USE_CONFIG, '', '', self.PRODUCT_INFO_COLUMN, '', item["price"],
                                  '0', item['short_description'], '', self.SIZE, self.small_image_label, '',
                                  self.SPECIAL_PRICE, '', self.STATUS, self.TAX_CLASS_ID, self.thumbnail_label, '', item['url_key'],
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


