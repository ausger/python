#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vi:ts=4:et
import sys
import pycurl
from lxml import etree

PY3 = sys.version_info[0] > 2


class Test:
    def __init__(self):
        self.contents = ''
        if PY3:
            self.contents = self.contents.encode('ascii')

    def body_callback(self, buf):
        self.contents = self.contents + buf


sys.stderr.write("Testing %s\n" % pycurl.version)

t = Test()
c = pycurl.Curl()
c.setopt(c.URL, 'http://www.liwus.de/xlx-a-lxx.html/')
c.setopt(c.WRITEFUNCTION, t.body_callback)
c.perform()
c.close()

print(t.contents)

tree = etree.HTML(t.contents)
r = tree.xpath("//span[@id='product-price-10352']")
print len(r)
