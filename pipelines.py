# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from txmongo.connection import MongoConnection


class ItemValidationPipeline(object):

    def process_item(self, item, spider):
        # or use JobItem.fields.keys()
        required_fields = ['company', 'link', 'title']
        if set(required_fields).issubset(item):
            return item
        else:
            raise DropItem(
                "Validation of item failed in spider %s because of missing mandatory field(s) for item %s" % (spider.name, item))


class DBPipeline(object):

    def __init__(self, mongo_uri, mongo_db, collection_name):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection_name = collection_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items'),
            collection_name=crawler.settings.get('MONGO_COLLECTION_NAME')
        )

    def open_spider(self, spider):
        self.client = MongoConnection(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if self.get_item({"company": item["company"], "title": item["title"]}) is None:
            self.insert_item(item)
        else:
            raise DropItem(u'Existing item with same company and title found, skipping.')

    def get_item(self, item):
        return self.db[self.collection_name].find_one(item)

    def insert_item(self, item):
        try:
            self.db[self.collection_name].insert_one(dict(item))
            return item
        except Exception as e:
            raise DropItem(u'Inserting of item into database failed with error: %s' % str(e))