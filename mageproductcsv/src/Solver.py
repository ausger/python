# -*- coding: utf-8 -*-
import sys
import csv
import codecs

_author_ = 'leoshang'


class Solver:
    CSV_OUTPUT_FILE_NAME = "wmf_standmixer_complete.csv"
    CSV_INPUT_FILE_NAME = "/Users/leishang/helenstreet/python/mageproductcsv/resources/wmf-standmixer.csv"
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

    def unicode_read(self):
        # the first row of the csv input file must be the csv head name
        # filename = sys.argv[1]
        # print "file name " + filename

        outputfile = file(self.CSV_OUTPUT_FILE_NAME, 'w')
        writer = csv.writer(outputfile)

        # outputfile = open("test.csv", 'w')
        # outputfile.write(codecs.BOM_UTF8)

        with open(self.CSV_INPUT_FILE_NAME, 'rU') as csvfile:
            data_reader = csv.reader(csvfile)
            try:
                for index, row in enumerate(data_reader):
                    print "%d. row has %d elements" % (index, len(row))
                    print(row[0], row[1], row[2], row[3], row[4], row[5],
                          row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15])
                    if index == 0:
                        # write column name into the csv output file.
                        writer.writerow(('sku', '_store', '_attribute_set','_type','categories','_product_websites','age_range','aptamil_code','bottle_volume',
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
                    else:
                        writer.writerow((row[0], self.store, row[15], self.product_type, row[1], self.product_websites, row[13],'','',
                            row[14],'','','','',self.country_of_manu,'','',
                            '','','',row[2],self.featured,'',
                            '','0',row[10],self.image_label,'','',self.media_gallery,
                            row[8],row[7],row[6],'','',self.USE_CONFIG,
                            self.USE_CONFIG,row[4],'','',self.PRODUCT_INFO_COLUMN,'',row[3],
                            '0',row[9],'',self.size,row[11],self.small_image_label,'',
                            self.special_price,'',self.STATUS,self.TAX_CLASS_ID,row[12],self.thumbnail_label,'',row[5],
                            row[5]+'.html',self.visibility,self.weight,self.quantity,'0','1','0','0',
                            '1','1','1','0','1',
                            self.is_in_stock,'','1','0','1',
                            '0','1','0','1',
                            '0','0','','','',
                            '','','','',
                            '','','','','',
                            '','','','','',
                            self.media_image,'','1','0'))

                        #  0      1         2        3     4     5        6           7              8                  9          10    11        12      13  14       15
                        # sku,category,description,price,name,url_key,meta_title,meta_keywords,meta_description,short_description,img,small_img,thumbnail,age,brand,attribute_set
                        # writer.writerow(row[0], row[1], row[2], row[3], row[4], row[5],
                        #                row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15])

            except csv.Error as e:
                sys.exit('file %s, line %d: %s' % (filename, data_reader.line_num, e))

Solver().unicode_read()
