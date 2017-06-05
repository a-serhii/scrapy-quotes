# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.http import Request


class QuotesSpider(Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for block_quote in response.xpath("//*[@class='quote']"):
            url_author_page = response.urljoin(block_quote.xpath(
                ".//span/a/@href").extract_first())
            tags = block_quote.xpath(
                ".//*[@class='tag']/text()").extract()
            text = block_quote.xpath(
                ".//*[@class='text']/text()").extract_first()
            author = block_quote.xpath(
                ".//*[@class='author']/text()").extract_first()
            yield Request(url=url_author_page,
                          meta={'tags': tags,
                                'text': text,
                                "author": author},
                          callback=self.parse_author_page)
        next_page = response.urljoin(response.xpath(
            "//*[@class='next']/a/@href").extract_first())
        yield Request(next_page)

    def parse_author_page(self, response):
        born = ' '.join(response.xpath(
            "//*[@class='author-born-date' or @class='author-born-location']//text()").extract())
        description = response.xpath(
            "//*[@class='author-description']//text()").extract_first().strip()
        yield{
            'tags': response.meta['tags'],
            'text': response.meta['text'],
            'author': response.meta['author'],
            'born': born,
            "description": description
        }
