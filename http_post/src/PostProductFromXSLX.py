# -*- coding: utf-8 -*-
import sys
import csv
import codecs
import openpyxl as px
#import xlrd
import requests
import ConfigParser
_author_ = 'leoshang'


class PostProductFromXSLX:

    XLS_INPUT_FILE_NAME = "/Users/leishang/helenstreet/python/http_post/resources/carseat.xlsx"
    XLS_SHEET_NAME = "Sheet1"
    store='base'
    country_of_manu='Germany'
    featured='No'
    UTF_8_ENCODING='utf-8'
    product_type='simple'
    product_websites='base'
    image_label=''
    small_image_label=''
    thumbnail_label=''
    media_image=''
    media_gallery=''
    special_price=''
    visibility='4'
    weight='1'
    quantity='10'
    is_in_stock='1'
    TAX_CLASS_ID='2'
    STATUS='1'
    USE_CONFIG='Use config'
    PRODUCT_INFO_COLUMN='Product Info Column'
    size=''

    modman_location_config = ConfigParser.ConfigParser()
    modman_location_config.read("/Users/leishang/helenstreet/python/http_post/resources/product_skus.ini")

    @staticmethod
    def config_section_map(section):
        dict1 = {}
        options = PostProductFromXSLX.modman_location_config.options(section)
        for option in options:
            try:
                dict1[option] = PostProductFromXSLX.modman_location_config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    def __init__(self):
        PostProductFromXSLX.all_sku = PostProductFromXSLX.config_section_map('PRODUCT')['sku_ids']
        PostProductFromXSLX.categories = PostProductFromXSLX.config_section_map('PRODUCT')['category_ids']
        PostProductFromXSLX.tools_session = PostProductFromXSLX.config_section_map('COOKIE')['tools_session']
        PostProductFromXSLX.store = PostProductFromXSLX.config_section_map('COOKIE')['store']
        PostProductFromXSLX.atuvc = PostProductFromXSLX.config_section_map('COOKIE')['atuvc']
        PostProductFromXSLX.compliancecookie = PostProductFromXSLX.config_section_map('COOKIE')['compliancecookie']
        PostProductFromXSLX.adminhtml = PostProductFromXSLX.config_section_map('COOKIE')['adminhtml']
        PostProductFromXSLX.url = PostProductFromXSLX.config_section_map('COOKIE')['url']
        PostProductFromXSLX.cookie = {'tools_session': PostProductFromXSLX.tools_session,
              'store': PostProductFromXSLX.store,
              '__atuvc': PostProductFromXSLX.atuvc,
              'complianceCookie': PostProductFromXSLX.compliancecookie,
              'adminhtml': PostProductFromXSLX.adminhtml
              }

    @staticmethod
    def generate():
        # the first row of the csv input file must be the csv head name
        # filename = sys.argv[1]
        # print "file name " + filename

        workbook = px.load_workbook(PostProductFromXSLX.XLS_INPUT_FILE_NAME, use_iterators=True)
        worksheet = workbook.get_sheet_by_name(PostProductFromXSLX.XLS_SHEET_NAME)

        for row in worksheet.iter_rows(row_offset=1):
            sku_value = ''
            a = []
            is_empty_row = 1
            # check out the last row
            for index, cell in enumerate(row):
                if cell.value is not None:
                    a.append(cell.value)
                    is_empty_row = 0
                    if index == 4:
                        sku_value = cell.value
                else:
                    a.append('')

            if is_empty_row == 0:
                test = '|'.join(u''.join(x).encode('utf-8').strip() for x in a)
                #print test
                #print '--------------------------------------------------------'
            else:
                print '********empty************'
                continue
            data = {
                'store': '2',
                'SKU': test,
                'CATEGORIES': PostProductFromXSLX.categories,
                'button': 'Copy+Product'
            }
            print 'handling sku %s' % sku_value
            r = requests.post(PostProductFromXSLX.url, data=data, cookies=PostProductFromXSLX.cookie)
            # print r.text
            if 'FINISHED: Product Copied' in r.text:
                print '[%s] Finished Successfully' % sku_value
            else:
                print 'Error during copying product[%s]' % sku_value
                print r.text
                break

PostProductFromXSLX().generate()
