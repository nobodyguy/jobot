# -*- coding: utf-8 -*-
import urlparse
import scrapy
from jobot.items import JobItem
from jobot.item_loaders import PraceCZItemLoader


class PraceczSpider(scrapy.Spider):
    name = "PraceCZ"
    allowed_domains = ["prace.cz"]
    start_urls = (
        'http://www.prace.cz/hledat?searchForm[locality_codes]=D265746&searchForm[profs]=Informatika&searchForm[other]=python;test;automation&searchForm[employment_type_codes][]=201300001&searchForm[minimal_salary]=&searchForm[education]=&searchForm[suitable_for]=&searchForm[search]=',
    )

    def parse(self, response):
        jobs = response.xpath('//ul[@class="search-result"]/li/div[contains(@class, "grid--rev")]')
        for job in jobs:
            yield self.parse_job(response, job)

        next_page = response.xpath('//div[contains(@class,"pager")]/span[@class="page" or @class="pager__next"]/a/@href')
        if next_page:
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url, callback=self.parse)

    def parse_job(self, response, job):
        loader = PraceCZItemLoader(JobItem(), selector=job)
        loader.add_xpath('title', './/h3[@class="half-standalone"]//strong/text()')
        loader.add_xpath('location', '..//div[contains(@class,"search-result__advert__box__item--location")]//strong/text()')
        loader.add_xpath('company',
                         '..//div[contains(@class,"search-result__advert__box__item--company")]/text()|..//div[contains(@class,"search-result__advert__box__item--company")]/a/text()')
        loader.add_xpath('link', './/h3[@class="half-standalone"]/a/@href')
        return loader.load_item()