#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4:et
import sys
import csv
import os
import shutil
import re
import ConfigParser
from collections import defaultdict
from collections import deque

PY3 = sys.version_info[0] > 2


class ProductCSVTransformer:

    CATEGORY_NAME = None
    DELIVERY_TIME = None
    BRAND = None
    COUNTRY_OF_MANU = None
    TAX_CLASS = None
    CSV_OUTPUT_FILE_NAME = None
    CSV_INPUT_FILE_NAME = None
    SKU_COLUMN = None
    NAME_COLUMN = None
    IMAGE_COLUMN = None
    MOG_COLUMN = None
    AGE_COLUMN = None
    VOLUME_COLUMN = None
    APTAMIL_COLUMN = None
    DELIVERY_T_COLUMN = None
    FREE_SHIP_COLUMN = None
    WEIGHT_COLUMN = None
    SKIP_PRODUCT_NAME = None
    OUTPUT_HEADER = None

    def config_section_map(self, section):
        dict1 = {}
        options = self.test_config.options(section)
        for option in options:
            try:
                dict1[option] = self.test_config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    def __init__(self):
        self.test_config = ConfigParser.ConfigParser()
        self.test_config.read("/Users/leishang/helenstreet/python/mageproductcsv/resources/productcsv-transformer.ini")
        print self.test_config.sections()

        self.CATEGORY_NAME = self.config_section_map('InputParameter')['CATEGORY_NAME'.lower()]
        self.DELIVERY_TIME = self.config_section_map('InputParameter')['DELIVERY_TIME'.lower()]
        self.BRAND = self.config_section_map('InputParameter')['BRAND'.lower()]
        self.COUNTRY_OF_MANU = self.config_section_map('ConstantParameter')['COUNTRY_OF_MANU'.lower()]
        self.TAX_CLASS = self.config_section_map('InputParameter')['TAX_CLASS'.lower()]
        self.CSV_INPUT_FILE_NAME = self.config_section_map('InputParameter')['CSV_INPUT_FILE_NAME'.lower()]
        self.CSV_OUTPUT_FILE_NAME = self.config_section_map('InputParameter')['CSV_OUTPUT_FILE_NAME'.lower()]
        self.IMAGE_SOURCE_FOLDER = self.config_section_map('ConstantParameter')['IMAGE_SOURCE_FOLDER'.lower()]
        self.IMAGE_TARGET_FOLDER = self.config_section_map('ConstantParameter')['IMAGE_TARGET_FOLDER'.lower()]
        self.SKU_COLUMN = self.config_section_map('ColumnOfInterest')['SKU_COLUMN'.lower()]
        self.NAME_COLUMN = self.config_section_map('ColumnOfInterest')['NAME_COLUMN'.lower()]
        self.IMAGE_COLUMN = self.config_section_map('ColumnOfInterest')['IMAGE_COLUMN'.lower()]
        self.MOG_COLUMN = self.config_section_map('ColumnOfInterest')['MOG_COLUMN'.lower()]
        self.AGE_COLUMN = self.config_section_map('ColumnOfInterest')['AGE_COLUMN'.lower()]
        self.VOLUME_COLUMN = self.config_section_map('ColumnOfInterest')['VOLUME_COLUMN'.lower()]
        self.APTAMIL_COLUMN = self.config_section_map('ColumnOfInterest')['APTAMIL_COLUMN'.lower()]
        self.DELIVERY_T_COLUMN = self.config_section_map('ColumnOfInterest')['DELIVERY_T_COLUMN'.lower()]
        self.FREE_SHIP_COLUMN = self.config_section_map('ColumnOfInterest')['FREE_SHIP_COLUMN'.lower()]
        self.WEIGHT_COLUMN = self.config_section_map('ColumnOfInterest')['WEIGHT_COLUMN'.lower()]
        self.SKIP_PRODUCT_NAME = self.config_section_map('SkipProductNamePattern')['SKIP_PRODUCT_NAME'.lower()]
        self.OUTPUT_HEADER = self.config_section_map('Csv_Header')['OUTPUT_HEADER'.lower()]
        self.ROW_RANGE = self.config_section_map('InputParameter')['ROW_RANGE'.lower()]
        self.columns = defaultdict(list)
        self.name_var = ''
        self.meta_title_var = ''
        self.meta_description_var = ''
        self.image_var = ''
        self.small_image_var = ''
        self.thumbnail_var = ''
        self.brand_var = ''
        self.url_key_var = ''
        self.url_path_var = ''
        self.image_label_var = ''
        self.small_image_label_var = ''
        self.thumbnail_label_var = ''
        self.status_var = ''
        self.visibility_var = ''
        self.color_var = ''
        self.price_var = ''
        self.weight_var = ''
        self.description_var = ''
        self.short_description_var = ''
        self.meta_keyword_var = ''
        self.qty_var = ''
        self.is_in_stock_var = ''
        self.manage_stock_var = ''
        self.media_gallery_var = ''
        self.age_range_var = ''
        self.bottle_volume_var = ''
        self.featured_var = ''
        self.aptamil_code_var = ''
        self.size_var = ''
        self.free_shipping_var = ''
        self.use_config_min_sale_qty = 1
        self.min_sale_qty = 1

    def getlastrow(self):
        with open(self.CSV_INPUT_FILE_NAME, 'r') as f:
            try:
                last_row = deque(csv.reader(f), 1)[0]
            except IndexError:  # empty file
                last_row = None
            return last_row

    def output(self):

        outputfile = file(self.CSV_OUTPUT_FILE_NAME, 'w')
        header = self.OUTPUT_HEADER.split(',')
        skupattern = re.compile(self.SKIP_PRODUCT_NAME)
        writer = csv.writer(outputfile)

        with open(self.CSV_INPUT_FILE_NAME) as input_file:
            reader = csv.DictReader(input_file)
            current_sku = None
            for index, row in enumerate(reader):
                print index
                if index == 0:
                    writer.writerow(header)
                output_product_row = []
                if skupattern.match(row[self.SKU_COLUMN]):
                    print 'Sku [' + row[self.SKU_COLUMN] + '] contains group or configurable, ' \
                                                           'which would not be processed.'
                    continue
                if current_sku:
                    if row[self.SKU_COLUMN] == current_sku:
                        # keep processing the next row for the same sku
                        if row[self.NAME_COLUMN]:
                            print '[ERROR:--]duplicated row with sku,name ' + current_sku
                        else:
                            media_gallery_var += ";" + row[self.MOG_COLUMN]
                            # if this is the last row, output the final product row to csv
                            if index + 2 == int(self.ROW_RANGE):
                                print 'last row reached. Sku is [' + current_sku + '].'
                                self.build_product_row(current_sku, media_gallery_var, output_product_row)
                                writer.writerow(output_product_row)

                    else:
                        # the current_sku has been completely processed, compose the final product output content,
                        # and then update the current_sku and media_gallery_var
                        self.build_product_row(current_sku, media_gallery_var, output_product_row)
                        writer.writerow(output_product_row)
                        previous_sku = current_sku
                        current_sku = row[self.SKU_COLUMN]
                        media_gallery_var = row[self.IMAGE_COLUMN]
                        # cache the current row but it will only be output when all rows of this sku has been gathered.
                        self.caching_fields(row)
                        if index + 2 == int(self.ROW_RANGE):
                            print 'last row reached. current sku is [' \
                                  + previous_sku + ']; last row sku is [' + current_sku + '].'
                            # clean up cache for the last row.
                            output_product_row = []
                            self.build_product_row(current_sku, media_gallery_var, output_product_row)
                            writer.writerow(output_product_row)
                        print 'processing sku:  ' + current_sku

                else:
                    # current_sku is empty, which means it must be the first row with a valid sku.
                    if row[self.NAME_COLUMN]:
                        # name column is not null
                        current_sku = row[self.SKU_COLUMN]
                        media_gallery_var = row[self.IMAGE_COLUMN]
                        self.caching_fields(row)
                        print 'first sku is ' + current_sku
                        if index + 2 == int(self.ROW_RANGE):
                            print 'last row reached. Only one row with sku[ ' + current_sku + '] ' \
                                                                                              'found in the input csv.'
                            self.build_product_row(current_sku, media_gallery_var, output_product_row)
                            writer.writerow(output_product_row)

                    else:
                        # name column should not be null for first row.
                        print '[ERROR:--] name is empty for the first row with a valid sku'
                        exit(2)

                for(k, v) in row.items():
                    if v not in self.columns[k]:
                        if k != 'media_gallery':
                            self.columns[k].append(v)
        print('sku have been processed ' + str(self.columns['sku']))
        print('media_gallery column: ' + str(self.columns['media_gallery']))
        print 'copy images ...'
        self.copyMediaGallery()

    def copyMediaGallery(self):
        for image_cell in self.columns['media_gallery']:
            print 'image cell ' + image_cell
            images = image_cell.split(';')
            for image_short_name in images:
                print 'image name ' + image_short_name
                src_image = self.IMAGE_SOURCE_FOLDER + image_short_name
                tgt_image = self.IMAGE_TARGET_FOLDER + image_short_name
                # create the target path
                if not os.path.exists(os.path.dirname(tgt_image)):
                    print 'creating path ' + tgt_image
                    try:
                        os.makedirs(os.path.dirname(tgt_image))
                    except OSError as exc:
                        print exc.message
                # do copy
                print 'copy from ' + src_image + ' to ' + tgt_image
                shutil.copy(src_image, tgt_image)

    def build_product_row(self, current_sku, media_gallery_var, output_product_row):
            output_product_row.append('default')
            output_product_row.append('base')
            output_product_row.append('Default')
            output_product_row.append('simple')
            output_product_row.append(self.CATEGORY_NAME)
            output_product_row.append(current_sku)
            output_product_row.append(self.name_var)
            output_product_row.append(self.meta_title_var)
            output_product_row.append(self.meta_description_var)
            output_product_row.append(self.image_var)
            output_product_row.append(self.small_image_var)
            output_product_row.append(self.thumbnail_var)
            output_product_row.append(self.url_key_var)
            output_product_row.append(self.url_path_var)
            output_product_row.append(self.image_label_var)
            output_product_row.append(self.small_image_label_var)
            output_product_row.append(self.thumbnail_label_var)
            output_product_row.append(self.COUNTRY_OF_MANU)
            output_product_row.append(self.status_var)
            output_product_row.append(self.visibility_var)
            output_product_row.append(self.TAX_CLASS)
            output_product_row.append(self.color_var)
            output_product_row.append(self.price_var)
            output_product_row.append(self.min_sale_qty)
            output_product_row.append(self.use_config_min_sale_qty)
            output_product_row.append(self.weight_var)
            output_product_row.append(self.description_var)
            output_product_row.append(self.short_description_var)
            output_product_row.append(self.meta_keyword_var)
            output_product_row.append(self.qty_var)
            output_product_row.append(self.is_in_stock_var)
            output_product_row.append(self.manage_stock_var)
            output_product_row.append(media_gallery_var)
            self.columns['media_gallery'].append(media_gallery_var)
            if self.brand_var:
                output_product_row.append(self.brand_var)
            else:
                output_product_row.append(self.BRAND)
            output_product_row.append(self.age_range_var)
            output_product_row.append(self.bottle_volume_var)
            output_product_row.append(self.featured_var)
            output_product_row.append(self.aptamil_code_var)
            output_product_row.append(self.size_var)
            output_product_row.append(self.DELIVERY_TIME)
            output_product_row.append(self.free_shipping_var)

    def reset_fields(self):
        self.name_var = ''
        self.meta_title_var = ''
        self.meta_description_var = ''
        self.image_var = ''
        self.small_image_var = ''
        self.thumbnail_var = ''
        self.url_key_var = ''
        self.url_path_var = ''
        self.image_label_var = ''
        self.small_image_label_var = ''
        self.thumbnail_label_var = ''
        self.status_var = ''
        self.visibility_var = ''
        self.color_var = ''
        self.price_var = ''
        self.weight_var = ''
        self.description_var = ''
        self.short_description_var = ''
        self.meta_keyword_var = ''
        self.qty_var = ''
        self.is_in_stock_var = ''
        self.manage_stock_var = ''
        self.age_range_var = ''
        self.bottle_volume_var = ''
        self.featured_var = ''
        self.aptamil_code_var = ''
        self.size_var = ''
        self.free_shipping_var = ''

    def caching_fields(self, row):
        self.name_var = row['name']
        self.meta_title_var = row['meta_title']
        self.meta_description_var = row['meta_description']
        self.image_var = row['image']
        self.small_image_var = row['small_image']
        self.thumbnail_var = row['thumbnail']
        self.brand_var = row['brand']
        self.url_key_var = row['url_key']
        self.url_path_var = row['url_path']
        self.image_label_var = row['image_label']
        self.small_image_label_var = row['small_image_label']
        self.thumbnail_label_var = row['thumbnail_label']
        self.status_var = row['status']
        self.visibility_var = row['visibility']
        self.color_var = row['color']
        self.price_var = row['price']
        self.weight_var = row['weight']
        self.description_var = row['description']
        self.short_description_var = row['short_description']
        self.meta_keyword_var = row['meta_keyword']
        self.qty_var = row['qty']
        self.is_in_stock_var = row['is_in_stock']
        self.manage_stock_var = row['manage_stock']
        self.age_range_var = row['age_range']
        self.bottle_volume_var = row['bottle_volume']
        self.featured_var = row['featured']
        self.aptamil_code_var = row['aptamil_code']
        self.size_var = row['size']
        self.free_shipping_var = row['free_shipping']


t = ProductCSVTransformer()
t.output()
