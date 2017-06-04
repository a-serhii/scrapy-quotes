# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request
from scrapy_quotes.items import ScrapyQuotesItem


class QuotesSpider(Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for block_quote in response.xpath("//*[@class='quote']"):
            item = ScrapyQuotesItem()
            request = Request(response.urljoin(block_quote.xpath(
                ".//span/a/@href").extract_first()),
                callback=self.parse_author_page)
            item["tags"] = block_quote.xpath(
                ".//*[@class='tag']/text()").extract()
            item["text"] = block_quote.xpath(
                ".//*[@class='text']/text()").extract_first()
            item["author"] = block_quote.xpath(
                ".//*[@class='author']/text()").extract_first()
            yield item, request
            # yield {
            #     "tags": block_quote.xpath(
            #         ".//*[@class='tag']/text()").extract(),
            #     "text": block_quote.xpath(
            #         ".//*[@class='text']/text()").extract_first(),
            #     "author": block_quote.xpath(
            #         ".//*[@class='author']/text()").extract_first(),
            #     "born": data,
            #     "description": "pass",
            # }
        next_page = response.urljoin(response.xpath(
            "//*[@class='next']/a/@href").extract_first())
        yield Request(next_page)

    def parse_author_page(self, response):
        item = ScrapyQuotesItem()
        item["born"] = ' '.join(response.xpath(
            "//*[@class='author-born-date' or @class='author-born-location']//text()").extract())
        yield item
