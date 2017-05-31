# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request


class QuotesSpider(Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for block_quote in response.xpath("//*[@class='quote']"):
            yield {
                "text": block_quote.xpath(
                    ".//*[@class='text']/text()").extract_first(),
                "author": block_quote.xpath(
                    ".//*[@class='author']/text()").extract_first(),
                "tags": block_quote.xpath(
                    ".//*[@class='tag']/text()").extract(),
            }
        next_page = response.urljoin(response.xpath(
            "//*[@class='next']/a/@href").extract_first())
        yield Request(next_page)
