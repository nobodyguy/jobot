import unittest2 as unittest
import mock
from scrapy.exceptions import DropItem
from jobot.pipelines import ItemValidationPipeline

class TestItemValidationPipeline(unittest.TestCase):

    def setUp(self):
        self.item = {'company': 'RedHat', 'link': 'some link', 'title': 'Python dev'}
        self.spider = mock.MagicMock()
        self.spider.name = "TestSpider"
        self.pipeline = ItemValidationPipeline()

    def test_process_complete_item(self):
        self.assertEquals(self.pipeline.process_item(self.item, self.spider), self.item)

    def test_process_incomplete_item(self):
        del self.item['company']
        with self.assertRaises(DropItem):
            self.pipeline.process_item(self.item, self.spider)

    def test_process_empty_item(self):
        item = {}
        with self.assertRaises(DropItem):
            self.pipeline.process_item(item, self.spider)

    def test_process_extended_item(self):
        self.item["content"] = "Test content"
        self.item["location"] = "Brno"
        self.assertEquals(self.pipeline.process_item(self.item, self.spider ), self.item)


if __name__ == '__main__':
    unittest.main()