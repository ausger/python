#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4:et
import sys
import re
import ConfigParser

PY3 = sys.version_info[0] > 2


class Test:

    BESTECK_PATTERN = None
    KITCHEN_HELPER_PATTERN = None
    KITCHEN_HELPER_PATTERN_2 = None
    KITCHEN_HELPER_PATTERN_3 = None
    KITCHEN_ORGANIZER_PATTERN = None
    KITCHEN_BLATTER_PATTERN = None
    KITCHEN_PAN_PATTERN = None
    KITCHEN_PAN_SET_PATTERN = None
    KITCHEN_KNIFE_PATTERN = None
    KITCHEN_KNIFE_SET_PATTERN = None
    KITCHEN_SCISSOR_PATTERN = None
    KITCHEN_COOK_POT = None
    MANICURE = None

    #test_data = ['anreib-reparaturstein-j-80-wuesthof_4454','aufschnittmesser-wuesthof_4107','ausbeinmesser-wuesthof_4863','bbq-set-wuesthof_9883',
    #             'chin-kochmesser-wuesthof_4673/18','chinesisches-kochmesser-01_1382','chin-kochmesser-wuesthof_4891/20','chinesisches-kochmesser-01_1383',
    #             'chinesisches-kochmesser-01_1384','chinesisches-kochmesser-01_1385','classic-ikon-2tlg--wuesthof_9283',
    #             'classic-ikon-messerblock-esche-schwarz-wuesthof_9878','classic-messersatz-3tlg--wuesthof_9285','dosenoffner-wuesthof_3735',
    #             'filiermesser-wuesthof_4856','fischfiliermesser-wuesthof_4878/18','gemusemesser-grun-wuesthof_3013g','gemusemesser-grun-wuesthof_3043g',
    #             'gemusemesser-orange-wuesthof_3013o','gemusemesser-orange-wuesthof_3043o','gemusemesser-rot-wuesthof_3013r','gemusemesser-rot-wuesthof_3043r',
    #             'gemusemesser-set-2-tlg--wuesthof_9343','gemusemesser-set-2-tlg-rot-wuesthof_9343r','gemusemesser-set-3-tlg--wuesthof_9332',
    #             'gemusemesser-set-3-tlg-grun-wuesthof_9332g','gemusemesser-wuesthof_3013','gemusemesser-wuesthof_3043','gemussemessersatz-wuesthof_9352c',
    #             'gourmet-2tlg--wuesthof_9284','hackmesser-01_1379','hackmesser-01_1380','hackmesser-01_1381',
    #             'haushaltmesser-wave-wuesthof_4855','hautschere-wuesthof_5030','ikon-messersatz-3tlg--01_1406','kitchensurfer-wuesthof_4192',
    #             'knife-set-2tlg-silverpoint-wuesthof_9811','knoblauchpresse-wuesthof_3734','kochmesser-01_1374','kochmesser-01_1377','kochmesser-01_1386',
    #             'Konditormesser','kuchen-fischschere-wuesthof_5564','kuchenmesser-set-3-tlg--wuesthof_9333','kuchenschere-01_1392','messerblock-(beton)-wuesthof_7258',
    #             'messerblock-mit-5-teilen-„china-block“-wuesthof_9835-8','messersatz--01_1403','messerscharfer-01_1368','messerset-01_3083','nagelpflegeetui-8tlg--wuesthof_9174',
    #             'pizza-steakm-set-2-tlg--wuesthof_9341','santoku-01_1364','schal-gemusem-set-2-tlg--wuesthof_9313','schalmesser-grun-wuesthof_3033g','schalmesser-orange-wuesthof_3033o',
    #             'schleifhilfe-"slider"-wuesthof_4349','schneidbrett-300-x-400-x-50-mm-wuesthof_7288','schubladeneinsatz-fur-7-teile-wuesthof_7273','spickmesser-01_1360',
    #             'universalmesser-grun-wuesthof_3003g','wetzstahl-01_1369','yanagiba-geschenkset-wuesthof_9753']

    test_data = ['dara-wasserfilter-kartuschen-set3-01_1881','2er-set-wasserglas-0-25l-wmf_0950502040--1','bar-set-loft-bar-wmf_0686926030',
                 'boston-shaker-2tlg-loft-wmf_0613556030--1','champagnerkuhler-stratic-wmf_0636706040-1','clip-weinthermometer-clever-&-more-wmf_0658516030--2',
                 'eiszange-loft-bar-wmf_0600136030','latte-macchiato-longdrinkloffel-set-6-type-wmf_1289656046','kapselheber-loft-bar-14cm-01_2022',
                 'flachmann-manhatten-20cl-wmf_0603519990--2','multitool-clever-and-more-wmf_0640636030--3','schraubdeckelzange-profi-plus-wmf_1873556030--2',
                 'topfring-vino-wmf_0658247920--1','weinflaschenverschluss-clever-&-more-wmf_0640956030','weinpumpe-mit-2-verschlussen-vino-wmf_0640717920']

    def __init__(self):
        self.test_config = ConfigParser.ConfigParser()
        self.test_config.read("/Users/leishang/helenstreet/python/mageproductcsv/resources/data-config.ini")
        print self.test_config.sections()
        # key must be here little case!!!
        self.BESTECK_PATTERN = self.config_section_map('ImageNamePattern')['BESTECK_PATTERN'.lower()]
        self.KITCHEN_HELPER_PATTERN = self.config_section_map('ImageNamePattern')['KITCHEN_HELPER_PATTERN'.lower()]
        self.KITCHEN_HELPER_PATTERN_2 = self.config_section_map('ImageNamePattern')['KITCHEN_HELPER_PATTERN_2'.lower()]
        self.KITCHEN_HELPER_PATTERN_3 = self.config_section_map('ImageNamePattern')['KITCHEN_HELPER_PATTERN_3'.lower()]
        self.KITCHEN_ORGANIZER_PATTERN = self.config_section_map('ImageNamePattern')['KITCHEN_ORGANIZER_PATTERN'.lower()]
        self.KITCHEN_BLATTER_PATTERN = self.config_section_map('ImageNamePattern')['KITCHEN_BLATTER_PATTERN'.lower()]
        self.KITCHEN_PAN_PATTERN = self.config_section_map('ImageNamePattern')['KITCHEN_PAN_PATTERN'.lower()]
        self.KITCHEN_PAN_SET_PATTERN = self.config_section_map('ImageNamePattern')['KITCHEN_PAN_SET_PATTERN'.lower()]
        self.KITCHEN_KNIFE_PATTERN = self.config_section_map('ImageNamePattern')['KITCHEN_KNIFE_PATTERN'.lower()]
        self.KITCHEN_KNIFE_SET_PATTERN = self.config_section_map('ImageNamePattern')['KITCHEN_KNIFE_SET_PATTERN'.lower()]
        self.KITCHEN_SCISSOR_PATTERN = self.config_section_map('ImageNamePattern')['KITCHEN_SCISSOR_PATTERN'.lower()]
        self.KITCHEN_COOK_POT = self.config_section_map('ImageNamePattern')['KITCHEN_COOK_POT'.lower()]
        self.MANICURE = self.config_section_map('ImageNamePattern')['MANICURE'.lower()]
        self.BAR_WEIN = self.config_section_map('ImageNamePattern')['BAR_WEIN'.lower()]
        self.KAFFE = self.config_section_map('ImageNamePattern')['KAFFE'.lower()]

        self.product_category = {self.BESTECK_PATTERN : '[Chinese Category]/厨房用具/餐具器皿',
                                 self.KITCHEN_HELPER_PATTERN: '[Chinese Category]/厨房用具/厨房小工具',
                                 self.KITCHEN_HELPER_PATTERN_2: '[Chinese Category]/厨房用具/厨房小工具',
                                 self.KITCHEN_HELPER_PATTERN_3: '[Chinese Category]/厨房用具/厨房小工具',
                                 self.KITCHEN_ORGANIZER_PATTERN: '[Chinese Category]/厨房用具/厨房收纳',
                                 self.KITCHEN_BLATTER_PATTERN:'[Chinese Category]/厨房用具/砧板',
                                 self.KITCHEN_PAN_PATTERN:'[Chinese Category]/厨房用具/德国锅具',
                                 self.KITCHEN_PAN_SET_PATTERN:'[Chinese Category]/厨房用具/德国锅具/德国锅具套装',
                                 self.KITCHEN_KNIFE_PATTERN:'[Chinese Category]/厨房用具/德国刀具',
                                 self.KITCHEN_KNIFE_SET_PATTERN:'[Chinese Category]/厨房用具/德国刀具/德国刀具套装',
                                 self.KITCHEN_SCISSOR_PATTERN:'[Chinese Category]/厨房用具/厨房专用剪刀',
                                 self.KITCHEN_COOK_POT:'[Chinese Category]/厨房用具/杯壺烘焙',
                                 self.MANICURE:'[Chinese Category]/美妆护肤/美妆工具',
                                 self.BAR_WEIN:'[Chinese Category]/厨房用具/红酒器皿',
                                 self.KAFFE:'[Chinese Category]/厨房用具/咖啡器皿'}

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

    def test_re(self):
        for bt in self.test_data:
            matched = 0
            for key, value in self.product_category.iteritems():
                result = re.match(key, bt)
                if result is None:
                    continue
                matched += 1
                print bt + " matches " + key + " and it's category is: " + value
            if matched == 0:
                print "[no matches!]:" + bt + " no matches!"
            elif matched > 1:
                print "***" + bt + " is matched %d times.***" % matched
            else:
                print bt + " is matched once. OK"
t = Test()
t.test_re()
