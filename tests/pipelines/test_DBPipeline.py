import unittest2 as unittest
import mock
from scrapy.exceptions import DropItem
from pymongo.errors import DuplicateKeyError
from jobot.pipelines import DBPipeline

class TestDBPipeline(unittest.TestCase):

    def setUp(self):
        self.item = {'company': 'RedHat', 'link': 'some link', 'title': 'Python dev'}
        self.spider = mock.MagicMock()
        self.spider.name = "TestSpider"
        self.mongo_uri = "mongodb://test.com"
        self.mongo_db = "jobs"
        self.collection_name = "jobs"
        self.pipeline = DBPipeline(self.mongo_uri, self.mongo_db, self.collection_name)

    def test_process_existing_item(self):
        mock_mongodb= mock.MagicMock()
        mock_mongodb[self.collection_name].find_one.return_value = self.item
        self.pipeline.db = mock_mongodb
        with self.assertRaises(DropItem):
            self.pipeline.process_item(self.item, self.spider)

    def test_process_unique_item(self):
        mock_mongodb = mock.MagicMock()
        self.pipeline.db = mock_mongodb
        self.pipeline.get_item = mock.Mock(return_value=None)
        self.pipeline.process_item(self.item, self.spider)
        mock_mongodb[self.collection_name].insert_one.assert_called_once_with(self.item)

    def test_process_failed_insert(self):
        mock_mongodb = mock.MagicMock()
        mock_mongodb[self.collection_name].insert_one.side_effect = DuplicateKeyError("")
        self.pipeline.db = mock_mongodb
        self.pipeline.get_item = mock.Mock(return_value=None)
        with self.assertRaises(DropItem):
            self.pipeline.process_item(self.item, self.spider)

if __name__ == '__main__':
    unittest.main()
