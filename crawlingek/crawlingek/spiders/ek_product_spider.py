# -*- coding: utf-8 -*-
import scrapy
import configparser
import re
import copy
from crawlingek.items import EkItem
from lxml import etree
import requests
from io import StringIO


class EkProductCrawler(scrapy.Spider):
    # Scrapy is single-threaded, except the interactive shell and some tests, see source.
    # Scrapy does most of it's work synchronously. However, the handling of requests is done asynchronously.
    name = "ek"
    allowed_domains = ["www.ek-online.de"]
    data_feed_config = configparser.ConfigParser()
    data_feed_config.read('/Users/leishang/helenstreet/python/crawlingek/crawlingek/spiders/ek-config.ini')
    # data_feed_config.read('E:/python/crawlingek/crawlingek/spiders/ek-config.ini')
    BASE_URL = 'https://www.ek-online.de'
    LOGIN_URL = BASE_URL + '/ekcontent/control/landingpage'
    LOGOUT_URL = BASE_URL + '/ekcontent/control/logout'
    SEARCH_URL = BASE_URL + '/ekcontent/control/keywordsearch'
    PAGE_NO = 1
    SEARCH_RESULT_PAGING_URL = SEARCH_URL + "?VIEW_SIZE=32&VIEW_INDEX="
    # SEARCH_RESULT_PAGING = [SEARCH_URL + '?VIEW_SIZE=32&VIEW_INDEX=2', SEARCH_URL + '?VIEW_SIZE=32&VIEW_INDEX=3']
    CATALOG_ID = 'EK_Gesamtkatalog'
    IMAGE_CELL_HEIGHT = 150
    IMAGE_X_SCALE = 1
    IMAGE_Y_SCALE = 1
    paging_urls = []

    @staticmethod
    def config_section_map(section):
        dict1 = {}
        options = EkProductCrawler.data_feed_config.options(section)
        for option in options:
            try:
                dict1[option] = EkProductCrawler.data_feed_config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        # print(dict1)
        return dict1

    def __init__(self, *a, **kw):
        super(EkProductCrawler, self).__init__(*a, **kw)
        # fields for csv export starts
        self.categories = EkProductCrawler.config_section_map('DataField')['categories']
        self.store = EkProductCrawler.config_section_map('DataField')['store']
        self.websites = EkProductCrawler.config_section_map('DataField')['websites']
        self.attribute_set = EkProductCrawler.config_section_map('DataField')['attribute_set']
        self.type = EkProductCrawler.config_section_map('DataField')['type']
        self.country_of_manufacture = EkProductCrawler.config_section_map('DataField')['country_of_manufacture']
        self.status = EkProductCrawler.config_section_map('DataField')['status']
        self.visibility = EkProductCrawler.config_section_map('DataField')['visibility']
        self.tax_class_id = EkProductCrawler.config_section_map('DataField')['tax_class_id']
        self.qty = EkProductCrawler.config_section_map('DataField')['qty']
        self.is_in_stock = EkProductCrawler.config_section_map('DataField')['is_in_stock']
        self.use_config_min_sale_qty = EkProductCrawler.config_section_map('DataField')['use_config_min_sale_qty']
        self.min_sale_qty = EkProductCrawler.config_section_map('DataField')['min_sale_qty']
        self.manage_stock = EkProductCrawler.config_section_map('DataField')['manage_stock']
        self.featured = EkProductCrawler.config_section_map('DataField')['featured']
        self.delivery_time = EkProductCrawler.config_section_map('DataField')['delivery_time']
        self.free_shipping = EkProductCrawler.config_section_map('DataField')['free_shipping']
        self.search_keyword = EkProductCrawler.config_section_map('General')['search_keyword']
        self.image_folder = EkProductCrawler.config_section_map('General')['image_folder']
        # fields for csv export ends
        # generate paging url
        self.build_paging_urls()
        start_url = EkProductCrawler.config_section_map('General')['start_urls']
        self.start_urls = start_url.split(",")
        print(self.start_urls)

    def build_paging_urls(self):
        if self.PAGE_NO > 1:
            for i in range(2, self.PAGE_NO + 1):
                self.paging_urls.append(self.SEARCH_RESULT_PAGING_URL + str(i))

    PRODUCT_DETAILS_XPATH = "//div[@class='productdetails']"

    PRODUCT_LOG_ID = ".//div[@class='productdescription']/div[@class='head3']"
    BRAND_PATH = ".//div[@class='productdescription']/div[@class='head2']"
    SHORT_DESCRIPTION_PATH = ".//div[@class='productdescription']"

    MULTIPLE_SKUS = ".//div[@class='producttable']/descendant::tr[contains(normalize-space(@id), 'tr')]"
    NAME_PATH = "./td[3]/text()"
    EK_PRICE_PATH = "./td[4]/text()"
    TOP_PRICE_PATH = "./td[@class='price']/descendant::a"
    VK_PRICE_PATH = "./td[6]/text()"
    EK_ARTICLE_PATH = "./td/table/tr/td/text()"
    EK_PRODUCT_ID_PATH = "./td/descendant::form/descendant::input[@name='product_id']/@value"

    THUMB_IMG_URL = ".//div[@class='productimage']/descendant::img/@src"
    IMG_URL = ".//div[@class='productimage']/a/@href"

    DESCRIPTION_PATH_1 = ".//div[@id='detailPopup_"
    DESCRIPTION_PATH_2 = "']"

    # @TODO
    AMOUNT_PATH = ".//div[@class='amountdisplay']/a[0]/text()"
    ORDERING_WARE_PATH = ".//div[@class='productimage']//img[@class='zrproductdetail']/@src"
    SALES_AGREEMENT_WARE_PATH = ".//div[@class='productimage']//img[@class='mayorderdetail']/@src"

    item_count = 0

    # start_urls = [amazon_cn_search_result_link + "%s" % n for n in product_ids]

    def parse(self, response):
        print('start parsing')
        login_credential = {'USERNAME': 'ekm45161-29957', 'PASSWORD': 'fei250811', 'Login': 'Login'}
        with requests.session() as a_session:
            # initially get a page
            a_session.get(self.LOGIN_URL)
            login_response = a_session.post(self.LOGIN_URL, data=login_credential)
            print(login_response.text)
            # search product
            search_payload = {'CATALOG_ID': self.CATALOG_ID, 'CLEAR_SEARCH': 'Y', 'CAT_FACET': '',
                              'QUERY_TYPE': '',
                              'SEARCH_STRING': self.search_keyword, 'SORT': '', 'x': '0', 'y': '0'}
            search_result = a_session.post(self.SEARCH_URL, search_payload)
            yield from self.handle_search_response(search_result)
            # paging using get, while search using post
            for page in self.paging_urls:
                search_result = a_session.get(page)
                yield from self.handle_search_response(search_result)

            a_session.get(self.LOGOUT_URL)

    def handle_search_response(self, search_result):
        product_elements = search_result.content.decode('utf-8')
        string_ioed_products = StringIO(product_elements)
        doc_tree = etree.parse(string_ioed_products, etree.HTMLParser())
        # result = etree.tostring(doc_tree.getroot(), pretty_print=True, method="html")
        # print(result)
        items = doc_tree.xpath(self.PRODUCT_DETAILS_XPATH)
        for index, doc_element in enumerate(items):
            yield from self.parse_element(index, doc_element)

    def parse_element(self, index, doc_element):
        ek_item = EkItem()
        ek_item['index'] = index
        # SKU, BRAND, NAME, IMG_SRC, IMG_URL, THUMB_IMG_SRC, THUMB_IMG_URL,
        # DESCRIPTION, SHORT_DESCRIPTION, PRICE, DISCOUNT_PRICE

        # handle common properties of a product
        self.handle_brand(doc_element, ek_item)

        # @TODO parse B, V mark, which indicates not available.

        self.handle_short_desc(doc_element, ek_item)
        self.handle_images(doc_element, ek_item)
        self.populate_static_data(ek_item)

        multiple_skus_holder = doc_element.xpath(self.MULTIPLE_SKUS)
        if len(multiple_skus_holder) > 1:
            print('its a product of [%d] sku' % len(multiple_skus_holder))
            # below can be multiple SKUs for a single product
            yield from self.handle_multiple_skus_product(ek_item, multiple_skus_holder)
        else:
            self.handle_singlesku_product(ek_item, multiple_skus_holder)
        self.handle_description(doc_element, ek_item)
        self.handle_color(doc_element, ek_item)
        self.handle_weight(doc_element, ek_item)
        # below handle extra fields for csv export
        self.handle_url_info(ek_item)
        yield ek_item

    def handle_multiple_skus_product(self, ek_item, multiple_skus_holder):
        for idx, sku_holder in enumerate(multiple_skus_holder):
            # replicate a new ek_item
            a_sku_item = copy.deepcopy(ek_item)
            a_sku_item['model'] = ''
            a_sku_item['simples_skus'] = ''
            self.handle_product_name(sku_holder, a_sku_item)
            self.handle_article_nr(sku_holder, a_sku_item)
            self.handle_product_id(sku_holder, a_sku_item)
            self.handle_sku(a_sku_item)
            self.handle_price(multiple_skus_holder[0], a_sku_item)
            if idx == 0:
                ek_item['model'] = a_sku_item['name']
                ek_item['simples_skus'] = a_sku_item['sku']
            else:
                ek_item['model'] += ',' + a_sku_item['name']
                ek_item['simples_skus'] += ',' + a_sku_item['sku']
            self.handle_price(sku_holder, a_sku_item)
            # below handle extra fields for csv export
            self.handle_url_info(a_sku_item)
            # 1 = Not Visible Individually, 2 = Catalog, 3 = Search, 4 = Catalog, Search
            a_sku_item['visibility'] = 1
            ek_item['price'] = a_sku_item['price']
            yield a_sku_item
        # name should be parsed from h3 of short description. Sku needs to be ...
        ek_item['name'] = ek_item['log_id']
        ek_item['sku'] = '-'.join(ek_item['simples_skus'].split(','))
        ek_item['type'] = 'configurable'
        ek_item['product_id'] = 'configurable_product_id'

    def handle_singlesku_product(self, ek_item, multiple_skus_holder):
        self.handle_product_name(multiple_skus_holder[0], ek_item)
        self.handle_article_nr(multiple_skus_holder[0], ek_item)
        self.handle_product_id(multiple_skus_holder[0], ek_item)
        self.handle_sku(ek_item)
        self.handle_price(multiple_skus_holder[0], ek_item)

    def handle_description(self, doc_element, ek_item):
        desc_part = self.DESCRIPTION_PATH_1 + ek_item['product_id'] + self.DESCRIPTION_PATH_2
        desc_holder = doc_element.xpath(desc_part)
        if len(desc_holder):
            description = str(etree.tostring(desc_holder[0]))
            idx = description.find('</div>')
            r_idx = description.rfind('</div>')
            tmp = description[(idx + len('</div>')): r_idx]
            # &#13; is "\r"
            ek_item['description'] = tmp.replace(r"&#13;\n", r"")

    def find_property_from_description_block(self, doc_element, ek_item, tag):
        desc_part = self.DESCRIPTION_PATH_1 + ek_item['product_id'] + self.DESCRIPTION_PATH_2
        desc_holder = doc_element.xpath(desc_part)
        if len(desc_holder):
            description = str(etree.tostring(desc_holder[0]))
            idx = description.find(tag)
            if idx > 0:
                property_section = description[(idx + len(tag)):]
                t_index = property_section.index('</td>')
                p_value = property_section[:t_index]
                print('property section ' + p_value)
                t_index = p_value.index('<td>')
                p_value = p_value[(t_index + len('<td>')):]
                return p_value

    def handle_color(self, doc_element, ek_item):
        color_tag = "use-Farben</td>"
        ek_item['color'] = self.find_property_from_description_block(doc_element, ek_item, color_tag)

    def handle_weight(self, doc_element, ek_item):
        weight_tag = '<td>Gewicht</td>'
        ek_item['weight'] = self.find_property_from_description_block(doc_element, ek_item, weight_tag)

    def handle_short_desc(self, doc_element, ek_item):
        short_desc_holder = doc_element.xpath(self.SHORT_DESCRIPTION_PATH)
        if len(short_desc_holder) > 0:
            short_desc = str(etree.tostring(short_desc_holder[0]))
            # for m in re.finditer(r"</div>", short_desc):
            #     m.start()
            # find the second </div> within short_desc
            # http://stackoverflow.com/questions/1883980/find-the-nth-occurrence-of-substring-in-a-string
            second_div_index = short_desc.replace('</div>', 'XXXXXX', 1).find('</div>')
            last_div_index = short_desc.rfind('</div>')
            tmp = short_desc[second_div_index + len('</div>') : last_div_index]
            # &#13; is "\r"
            ek_item['short_description'] = tmp.replace(r"&#13;\n", r"")

    # log_id and brand are located within the same div.
    # log_id can be found from the tag h3, but brand is sometimes wrapped with h2 and sometimes with h3.
    def handle_brand(self, doc_element, ek_item):
        brand_holder = doc_element.xpath(self.BRAND_PATH)
        log_id_holder = doc_element.xpath(self.PRODUCT_LOG_ID)
        if len(brand_holder) > 0 and len(log_id_holder) > 0:
            ek_item['brand'] = brand_holder[0].text
            ek_item['log_id'] = log_id_holder[0].text
        elif len(brand_holder) == 0 and len(log_id_holder) == 2:
            ek_item['brand'] = log_id_holder[0].text
            ek_item['log_id'] = log_id_holder[1].text
        elif len(brand_holder) == 0 and len(log_id_holder) == 1:
            ek_item['brand'] = 'NOT FOUND'
            ek_item['log_id'] = log_id_holder[0].text
        else:
            ek_item['brand'] = 'NOT FOUND'
            ek_item['log_id'] = 'NOT FOUND'
            print('It seems more than three h3 tags in the div. Cannot decide the brand and log_id of '
                  'the %sth product %s' % ek_item['index'])

    def handle_images(self, doc_element, ek_item):
        thumbnail_holder = doc_element.xpath(self.THUMB_IMG_URL)
        image_holder = doc_element.xpath(self.IMG_URL)
        images = {'thumbnail': thumbnail_holder, 'image': image_holder}
        for key, value in images.items():
            if len(value) > 0:
                image_url = str(value[0])
                ek_item[key] = self.generate_image_name(key, image_url)
                ek_item[key + '_url'] = self.BASE_URL + image_url
            else:
                print('cannot find the %s of the product %s' % (key, ek_item['log_id']))
        ek_item['small_image'] = ek_item['image']
        ek_item['media_gallery'] = ek_item['image'] + ";" + ek_item['small_image'] + ";" + ek_item['thumbnail']

    def handle_price(self, doc_element, ek_item):
        ek_price_holder = doc_element.xpath(self.EK_PRICE_PATH)
        top_price_holder = doc_element.xpath(self.TOP_PRICE_PATH)
        vk_price_holder = doc_element.xpath(self.VK_PRICE_PATH)
        price_list = {'ek_price': ek_price_holder, 'top_price': top_price_holder, 'vk_price': vk_price_holder}
        for key, value in price_list.items():
            if len(value) > 0:
                if key == 'top_price':
                    ek_item[key] = value[0].text
                else:
                    ek_item[key] = str(value[0])
                print("%s was %s" % (key, ek_item[key]))
                tmp = re.sub('((\s)*€(\s)*)', '', ek_item[key])
                ek_item[key] = tmp.strip()
                print("now %s is %s" % (key, ek_item[key]))
            else:
                ek_item[key] = '---'
                print('cannot find the %s of the product %s' % (key, ek_item['log_id']))
        ek_item['price'] = ek_item['vk_price']

    def handle_product_id(self, doc_element, ek_item):
        product_id_holder = doc_element.xpath(self.EK_PRODUCT_ID_PATH)
        if len(product_id_holder) > 0:
            ek_item['product_id'] = str(product_id_holder[0])
        else:
            # npi for no product id
            ek_item['product_id'] = 'npi'
            print('cannot find the product_id of the product %s' % ek_item['log_id'])

    def handle_article_nr(self, doc_element, ek_item):
        article_nr_holder = doc_element.xpath(self.EK_ARTICLE_PATH)
        if len(article_nr_holder) > 0:
            ek_item['article_nr'] = str(article_nr_holder[0]).strip()
        else:
            print('cannot find the article nr of the product %s' % ek_item['log_id'])

    def handle_product_name(self, doc_element, ek_item):
        product_name_holder = doc_element.xpath(self.NAME_PATH)
        if len(product_name_holder) > 0:
            name_tmp = str(product_name_holder[0])
            ek_item['name'] = name_tmp
        else:
            print('cannot find the name of the product %s' % ek_item['log_id'])

    def populate_static_data(self, ek_item):
        ek_item['store'] = self.store
        ek_item['websites'] = self.websites
        ek_item['attribute_set'] = self.attribute_set
        ek_item['categories'] = self.categories
        ek_item['type'] = self.type
        ek_item['country_of_manufacture'] = self.country_of_manufacture
        ek_item['status'] = self.status
        ek_item['visibility'] = self.visibility
        ek_item['tax_class_id'] = self.tax_class_id
        ek_item['qty'] = self.qty
        ek_item['size'] = ''
        ek_item['is_in_stock'] = self.is_in_stock
        ek_item['use_config_min_sale_qty'] = self.use_config_min_sale_qty
        ek_item['min_sale_qty'] = self.min_sale_qty
        ek_item['manage_stock'] = self.manage_stock
        ek_item['featured'] = self.featured
        ek_item['delivery_time'] = self.delivery_time
        ek_item['free_shipping'] = self.free_shipping

    def handle_url_info(self, ek_item):
        tmp = self.build_url_info(ek_item['name'])
        ek_item['url_key'] = tmp + '-' + ek_item['sku']
        ek_item['url_path'] = tmp + '-' + ek_item['sku']

    def build_url_info(self, name_tmp):
        # replace comma & space with -
        # str.replace() does not recognize regular expressions, to perform a substitution using
        # regular expressions use re.sub().
        # print("original product title: %s" % name_tmp)
        name_tmp = name_tmp.strip()
        tmp = re.sub('((\s)*,(\s)*)', '', name_tmp)
        tmp = re.sub('((\s)+)', '-', tmp)
        tmp = tmp.replace("/", "-")
        tmp = tmp.replace(".", "")
        tmp = tmp.replace("+", "-")
        tmp = tmp.replace('"', "")
        tmp = re.sub('((-)+)', '-', tmp)
        # replace german umlaut
        tmp = tmp.replace('ä', 'a')
        tmp = tmp.replace('Ä', 'a')
        tmp = tmp.replace('ö', 'o')
        tmp = tmp.replace('Ö', 'o')
        tmp = tmp.replace('ü', 'u')
        tmp = tmp.replace('Ü', 'u')
        tmp = tmp.replace('ß', 'ss')
        # print('dashed title %s ' % tmp)
        return tmp.lower()

    def generate_image_name(self, prefix, image_url):
        # product_images is like http://www.liwus.de/media/catalog/product/cache/1/
        # image/9df78eab33525d08d6e5fb8d27136e95/N/U/NUK_10176092.jpg
        image_tmp = image_url.split('/')
        image_name = prefix + '_' + image_tmp[-1]
        return image_name.lower()

    def handle_sku(self, ek_item):
        tmp = ek_item['product_id'].lower() + '-' + ek_item['article_nr'].lower()
        ek_item['sku'] = re.sub('((\s)+)', '', tmp)

