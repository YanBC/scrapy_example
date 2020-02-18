# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import os
import sqlite3
from scrapy.pipelines.images import ImagesPipeline


class sqlitePipeline(object):
    tableName = 'Products'

    def __init__(self, sqlite_uri):
        self.sqlite_uri = sqlite_uri     

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            sqlite_uri=crawler.settings.get('SQLITE_URI')
        )

    def open_spider(self, spider):
        self.conn = sqlite3.connect(self.sqlite_uri)
        self.c = self.conn.cursor()

        self.c.execute('''SELECT name FROM sqlite_master WHERE type="table" AND name=?''', (self.tableName,))
        if len(self.c.fetchall()) == 0:
            self.c.execute('''CREATE TABLE %s (name text, 
                                            price real,
                                            web_url text, 
                                            local_url text,
                                            checksum text)''' % (self.tableName,))


    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        product_name = item['name']
        product_price = float(item['price'][1:])
        web_url = item['images'][0]['url']
        local_url = item['images'][0]['path']
        checksum = item['images'][0]['checksum']

        self.c.execute('''INSERT INTO %s VALUES (?,?,?,?,?)''' % self.tableName, 
                                (product_name, product_price, web_url, local_url, checksum))
        self.conn.commit()

        return item