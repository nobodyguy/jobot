# -*- coding: utf-8 -*-
import scrapy
from scrapy.utils.response import get_base_url
from jobot.items import JobItem
from jobot.item_loaders import JobsCZItemLoader


class JobsczSpider(scrapy.Spider):
    name = "JobsCZ"
    allowed_domains = ["jobs.cz"]
    start_urls = (
        'http://www.jobs.cz/prace/brno/?q[]=python&q[]=test&q[]=automation&locality[radius]=10',
    )

    def parse(self, response):
        jobs = response.xpath(
            '//div[@class="grid__item"]//div[@class="standalone search-list__item"]/div[@class="grid"]')
        for job in jobs:
            yield self.parse_job(response, job)

        next_page = response.xpath('//a[contains(@class,"pager__next")]/@href')
        if next_page:
            url = response.urljoin(next_page.extract_first())
            yield scrapy.Request(url, callback=self.parse)

    def parse_job(self, response, job):
        loader = JobsCZItemLoader(JobItem(), selector=job, base_url=get_base_url(response))
        loader.add_xpath('title', './/a[@class="search-list__main-info__title__link"]/text()')
        loader.add_xpath('location', './/div[@class="search-list__main-info__address"]//span[2]/text()')
        loader.add_xpath('company',
                         './/*[@class="search-list__main-info__company" or @class="search-list__main-info__company__link"]/text()')
        loader.add_xpath('link', './/a[@class="search-list__main-info__title__link"]/@href')
        return loader.load_item()
