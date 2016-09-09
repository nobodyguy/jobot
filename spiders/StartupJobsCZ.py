# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import get_base_url
from jobot.items import JobItem
from jobot.item_loaders import StartupJobsItemLoader


class StartupjobsczSpider(scrapy.Spider):
    name = "StartupJobsCZ"
    allowed_domains = ["startupjobs.cz"]
    start_urls = (
        'https://www.startupjobs.cz/nabidky?key=test&locality=Brno',
        'https://www.startupjobs.cz/nabidky?key=python&locality=Brno',
    )

    def parse(self, response):
        jobs = response.xpath('//div[@id="offer-list"]//table//tr')
        for job in jobs:
            yield self.parse_job(response, job)

        next_page = response.xpath(u'//p[@class="paginator"]/a[contains(text(), "Další")]/@href')
        if next_page:
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url, callback=self.parse)

    def parse_job(self, response, job):
        loader = StartupJobsItemLoader(JobItem(), selector=job, base_url=get_base_url(response))
        loader.add_xpath('title', './/td[@class="positionCol"]//a/text()')
        loader.add_xpath('location', './/td[@class="cityCol"]/text()')
        loader.add_xpath('company', './/td[@class="positionCol"]//span/text()')
        loader.add_xpath('link', './/td[@class="positionCol"]//a/@href')
        return loader.load_item()