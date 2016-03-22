# -*- coding: utf-8 -*-
import sys
import requests
import ConfigParser

_author_ = 'leoshang'

PY3 = sys.version_info[0] > 2


class PostForm:

    modman_location_config = ConfigParser.ConfigParser()
    modman_location_config.read("/Users/leishang/helenstreet/python/http_post/resources/product_skus.ini")
    url = 'http://ausger.dev:8888/copyscript/copy.php'

    @staticmethod
    def config_section_map(section):
        dict1 = {}
        options = PostForm.modman_location_config.options(section)
        for option in options:
            try:
                dict1[option] = PostForm.modman_location_config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    def __init__(self):
        PostForm.all_sku = PostForm.config_section_map('PRODUCT')['sku_ids']
        PostForm.categories = PostForm.config_section_map('PRODUCT')['category_ids']
        PostForm.tools_session = PostForm.config_section_map('COOKIE')['tools_session']
        PostForm.store = PostForm.config_section_map('COOKIE')['store']
        PostForm.atuvc = PostForm.config_section_map('COOKIE')['atuvc']
        PostForm.compliancecookie = PostForm.config_section_map('COOKIE')['compliancecookie']
        PostForm.adminhtml = PostForm.config_section_map('COOKIE')['adminhtml']
        PostForm.phpsessionid = PostForm.config_section_map('COOKIE')['phpsessionid']
        PostForm.cookie = {'tools_session': PostForm.tools_session,
              'store': PostForm.store,
              '__atuvc': PostForm.atuvc,
              'complianceCookie': PostForm.compliancecookie,
              'adminhtml': PostForm.adminhtml,
              'PHPSESSID': PostForm.phpsessionid
              }

    @staticmethod
    def doPost():
        sku_list = PostForm.all_sku.split(",")
        for sku in sku_list:
            data = {
                'store': '2',
                'SKU': sku,
                'CATEGORIES': PostForm.categories,
                'button': 'Copy+Product'
            }

            r = requests.post(PostForm.url, data=data, cookies=PostForm.cookie)
            if 'FINISHED: Product Copied' in r.text:
                print '[%s] Finished Successfully' % sku
            else:
                print 'Error during copying product[%s]' % sku
                print r.text
                break

PostForm().doPost()
