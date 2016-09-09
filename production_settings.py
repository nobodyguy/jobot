from datetime import datetime

LOG_LEVEL = 'WARNING'
FEED_URI = '..\\results\items_%(name)s_%(time)s.json'
FEED_FORMAT = 'json'
LOG_FILE = "..\logs\scrapy_%s.log" % datetime.now().strftime('%H_%M_%d_%m_%Y')

MONGO_URI = 'mongodb://localhost:27017/'
MONGO_DATABASE = 'jobs'
MONGO_COLLECTION_NAME = 'jobs'