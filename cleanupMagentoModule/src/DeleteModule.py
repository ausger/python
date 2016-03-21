# -*- coding: utf-8 -*-
import sys
import csv
import os
import shutil
import ConfigParser

_author_ = 'leoshang'

PY3 = sys.version_info[0] > 2


class ModuleRemover:

    CURRENT_SECTION = 'main'
    MODMAN = 'modman'
    modman_location_config = ConfigParser.ConfigParser()
    modman_location_config.read("/Users/leishang/helenstreet/python/cleanupMagentoModule/resources/modman-location.ini")

    def __init__(self):
        ModuleRemover.magento_project_base = ModuleRemover.config_section_map(ModuleRemover.CURRENT_SECTION)['magento_project_base']
        ModuleRemover.vendor_base = ModuleRemover.config_section_map(ModuleRemover.CURRENT_SECTION)['vendor_base']
        print '[Magento project base]: ' + ModuleRemover.magento_project_base
        print '[Module Vendor base]: ' + ModuleRemover.vendor_base

    @staticmethod
    def config_section_map(section):
        dict1 = {}
        options = ModuleRemover.modman_location_config.options(section)
        for option in options:
            try:
                dict1[option] = ModuleRemover.modman_location_config.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1

    @staticmethod
    def find(file_name, directory_path):
        for root, dirs, files in os.walk(directory_path):
            if file_name in files:
                target = os.path.join(root, file_name)
                print target
                return target

    @staticmethod
    def delete(module_name):
        # module name convert to lower case
        # some module don't have modman file, it is only contained in vendor folder.
        if module_name == 'all':
            modules = ModuleRemover.config_section_map(ModuleRemover.CURRENT_SECTION)['modules_installed']
            print "[All modules installed]: " + modules
            mod_array = modules.split(",")
            for modman_name in mod_array:
                ModuleRemover.get_modman_file(modman_name)
        else:
            ModuleRemover.get_modman_file(module_name)

    @staticmethod
    def rreplace(s, old, new, occurrence):
        li = s.rsplit(old, occurrence)
        return new.join(li)

    @staticmethod
    def get_modman_file(modman_name):
        modman_full_path = ModuleRemover.vendor_base + modman_name.lower() + '/' + ModuleRemover.MODMAN
        if os.path.isfile(modman_full_path):
            print "[reading modman file %s]: " % modman_full_path
            with open(modman_full_path, 'r') as module_modman_file:
                for line in module_modman_file:
                    if line.startswith("#"):
                        continue
                    if len(line.strip()) > 0:
                        #print line
                        line_parts = line.split()
                        mappedfile = line_parts[-1].strip()
                        if mappedfile.endswith("lib/") and modman_name == "colinmollenhour/cache-backend-redis":
                            mappedfile += "Credis"
                        elif mappedfile.endswith("modules/") and modman_name == "fbrnc/aoe_quotecleaner":
                            mappedfile += "Aoe_QuoteCleaner.xml"
                        elif (mappedfile.endswith("de_DE/") or mappedfile.endswith("de_AT/") or mappedfile.endswith("nl_NL/") ) and modman_name == "firegento/pdf":
                            mappedfile += "FireGento_Pdf.csv"
                        elif mappedfile.endswith("/"):
                            mappedfile = ModuleRemover.rreplace(mappedfile, '/', '', 1)
                        print "[Mapping file is:] %s" % mappedfile
                        print "------------------------------------------------------------------------------------------------------------------------------------------------"
                        file_to_delete = ModuleRemover.magento_project_base + mappedfile
                        if os.path.isdir(file_to_delete):
                            shutil.rmtree(file_to_delete)
                        elif os.path.isfile(file_to_delete):
                            os.remove(file_to_delete)
                        else:
                            print "%s not exist and cannot be deleted" %file_to_delete

        else:
            print "[File %s not exists]" % modman_full_path


ModuleRemover().delete('all')
