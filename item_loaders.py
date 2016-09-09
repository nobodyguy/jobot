from urlparse import urljoin
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose


def construct_full_url(url, loader_context):
    base_url = loader_context.get('base_url')
    return urljoin(base_url, url)

def clean_newlines(text):
    return text.replace('\n', '').replace('\r', '')

def join_multiple_items(text):
    return ", ".join(text.split())

class StartupJobsItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    location_in = MapCompose(clean_newlines, join_multiple_items)
    title_in = MapCompose(unicode.strip)
    link_in = MapCompose(construct_full_url)

class JobsCZItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    location_in = MapCompose(unicode.strip)
    company_in = MapCompose(unicode.strip)
    link_in = MapCompose(construct_full_url)

class PraceCZItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    location_in = MapCompose(unicode.strip)
    company_in = MapCompose(unicode.strip)