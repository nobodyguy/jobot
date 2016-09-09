import pymongo
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import jobot.production_settings as production_settings

def run_spiders():
    settings = get_project_settings()

    # merge of general project settings + production settings
    settings.setmodule(production_settings)
    crawler_process = CrawlerProcess(settings)

    for spider_name in crawler_process.spider_loader.list():
        print "Starting spider " + spider_name
        spider_cls = crawler_process.spider_loader.load(spider_name)
        crawler_process.crawl(spider_cls)
    crawler_process.start()

run_spiders()
print "All spiders were finished"
print "Starting processing of new job offers"
client = pymongo.MongoClient(production_settings.MONGO_URI)
db = client[production_settings.MONGO_DATABASE]
collection = db[production_settings.MONGO_COLLECTION_NAME]
for row in collection.find():
    print row
print "Processing was finished."
client.close()
