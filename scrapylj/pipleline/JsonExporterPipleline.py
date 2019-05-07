#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@author:xiaozhun
@file: JsonExporterPipleline.py
@time: 2019/05/05
"""
import json
class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open('items.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item
