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
                "tags": block_quote.xpath(
                    ".//*[@class='tag']/text()").extract(),
                "text": block_quote.xpath(
                    ".//*[@class='text']/text()").extract_first(),
                "author": block_quote.xpath(
                    ".//*[@class='author']/text()").extract_first(),
                "born": "pass",
                "description": "pass",
            }
        next_page = response.urljoin(response.xpath(
            "//*[@class='next']/a/@href").extract_first())
        yield Request(next_page)
# response.urljoin(block_quote.xpath(".//span/a/@href").extract_first())
