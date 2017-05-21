# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# encoding=utf-8
from pymongo import MongoClient
from items import WeibotopicspiderItem
from scrapy.conf import settings

# HOST = settings["MONGODB_SERVER"]
# PORT = settings["MONGODB_PORT"]
# DB = settings["MONGODB_DB"]
# TWEETS = settings["TWEETS"]

class WeibotopicspiderPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDBPipleline(object):
    # def __init__(self):
    #     connection = pymongo.Connection(
    #         HOST,
    #         PORT
    #    )
    # db = connection[DB]
    # self.tweets = db[TWEETS]
    def __init__(self):
        connection = MongoClient(
            host=settings['MONGODB_SERVER'],
            port=settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.tweets = db[settings['TWEETS']]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, WeibotopicspiderItem):
            try:
                self.tweets.insert(dict(item))
            except Exception:
                pass
        return item