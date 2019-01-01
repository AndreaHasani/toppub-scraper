import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess
import requests
import re
import MySQLdb
import os
from lxml import html
from w3lib.html import remove_tags, remove_tags_with_content
import time
from functions import writeCsv



class MySpider(scrapy.Spider):
    name = "toppub"
    site = "https://toppub.xyz/publications"

    custom_settings = {
        'LOG_LEVEL': 'INFO',
        # 'LOG_ENABLED': 'False',
        'CONCURRENT_REQUESTS': '64',
        'CONCURRENT_REQUESTS_PER_DOMAIN': '64',
    }

    def __init__(self):
        self.data = []

    def start_requests(self):
        yield scrapy.Request(url=self.site, callback=self.parse_items)

    def parse_items(self, response):
        urls = response.xpath("//table//tr/td[1]/a/@href").extract()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_item)

        try:
            nextUrl = response.xpath(
                "//ul[@class='pagination']//a[@rel='next']/@href").extract()
            yield scrapy.Request(url=nextUrl[0], callback=self.parse_items)
        except Exception as e:
            print("End reached")

    def parse_item(self, response):
        # Info scraped
        title = response.xpath(
            "//div[@class='media-body']/h2/text()").extract() or ['empty']

        tags = response.xpath(
            "//div[@class='media-body']/div[@class='pb-4']/a/span/text()").extract() or ['empty']

        desc = response.xpath(
            "//div[@class='media']/div[@class='media-body']/p[1]/text()").extract() or ['empty']

        social = response.xpath(
            "//div[@class='media-body']/div[@class='mt-3']/a/@href").extract() or ['empty']

        followers = response.xpath(
            "//span[contains(text(), 'Followers')]/../span[1]/text()").extract() or ['empty']

        reviews = response.xpath(
            "//span[contains(text(), 'Followers')]/..//div[@class='mt-3']/a/text()").extract() or ['empty']

        # Editors
        editorsHub = response.xpath(
            "//div[@class='card-deck']/div//div[@class='media-body']")

        editors = []

        for editor in editorsHub:
            editor_link = editor.xpath("a/@href").extract() or ['empty']
            editor_name = editor.xpath("a/h5/text()").extract() or ['empty']
            editor_desc = editor.xpath("p/text()").extract() or ['empty']

            editors.append([editor_name, editor_link, editor_desc])

        editors = [[x[0], y[0], z[0]] for x, y, z in editors]
        self.data.append([title, tags, desc, social,
                          followers, reviews, editors])

    def closed(self, reason):
        writeCsv('output', self.data)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
})

process.crawl(MySpider)
process.start()
