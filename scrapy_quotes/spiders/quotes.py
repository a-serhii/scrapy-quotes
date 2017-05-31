# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
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
