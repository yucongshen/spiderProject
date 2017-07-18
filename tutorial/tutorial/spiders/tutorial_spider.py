# !/usr/python/bin
# -*- coding: UTF-8 -*-
import scrapy
from tutorial.items import TutorialItem
class DmozSpider(scrapy.Spider):
    name = "dianping"
    allowed_domains = ["dianping.com"]
    start_urls = [
        "https://www.dianping.com/search/category/2/10/g110"
    ]
    def parse(self, response):
        url_list = response.xpath("//ul/li/div[@class='pic']/a/@href").extract()
        dianping_item=TutorialItem()
        for url in url_list:
            dianping_item["url"]=url
            yield dianping_item


