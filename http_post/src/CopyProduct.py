# -*- coding: utf-8 -*-
import sys
import requests
import ConfigParser

_author_ = 'leoshang'

PY3 = sys.version_info[0] > 2


class CopyProduct:

    modman_location_config = ConfigParser.ConfigParser()
    modman_location_config.read("/Users/leishang/helenstreet/python/http_post/resources/product_skus.ini")
    #url = 'http://ausger.dev:8888/copyscript/copy.php'

    @staticmethod
    def config_section_map(section):
        dict1 = {}
        options = CopyProduct.modman_location_config.options(section)
        for option in options:
            try:
                dict1[option] = CopyProduct.modman_location_config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    def __init__(self):
        CopyProduct.all_sku = CopyProduct.config_section_map('PRODUCT')['sku_ids']
        CopyProduct.categories = CopyProduct.config_section_map('PRODUCT')['category_ids']
        CopyProduct.tools_session = CopyProduct.config_section_map('COOKIE')['tools_session']
        CopyProduct.store = CopyProduct.config_section_map('COOKIE')['store']
        CopyProduct.atuvc = CopyProduct.config_section_map('COOKIE')['atuvc']
        CopyProduct.compliancecookie = CopyProduct.config_section_map('COOKIE')['compliancecookie']
        CopyProduct.adminhtml = CopyProduct.config_section_map('COOKIE')['adminhtml']
        CopyProduct.url = CopyProduct.config_section_map('COOKIE')['url']
        CopyProduct.cookie = {'tools_session': CopyProduct.tools_session,
              'store': CopyProduct.store,
              '__atuvc': CopyProduct.atuvc,
              'complianceCookie': CopyProduct.compliancecookie,
              'adminhtml': CopyProduct.adminhtml
              }

    @staticmethod
    def doPost():
        sku_list = CopyProduct.all_sku.split(",")
        for sku in sku_list:
            data = {
                'store': '2',
                'SKU': sku,
                'CATEGORIES': CopyProduct.categories,
                'button': 'Copy+Product'
            }
            print 'handling sku %s' % sku
            r = requests.post(CopyProduct.url, data=data, cookies=CopyProduct.cookie)
            # print r.text
            if 'FINISHED: Product Copied' in r.text:
                print '[%s] Finished Successfully' % sku
            else:
                print 'Error during copying product[%s]' % sku
                print r.text
                break

CopyProduct().doPost()
