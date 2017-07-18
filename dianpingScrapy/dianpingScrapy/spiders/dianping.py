# -*- coding: utf-8 -*-
import scrapy
from dianpingScrapy.items import DianpingscrapyItem
from headers import pc_headers

class DianpingSpider(scrapy.Spider):
    name = 'dianping'
    allowed_domains = ['dianping.com']
    start_urls = ['https://www.dianping.com/shop/77298586']

    def start_requests(self):
        request = scrapy.Request("https://www.dianping.com/shop/77298586", headers=pc_headers)
        yield request

    def parse(self, response):
        url=response.url
        item = DianpingscrapyItem()
        index=url.index("shop")
        url=url[index+len("/shop"):]
        item["shop_id"] = url
        basic_info=response.xpath('//div[@id="basic-info"]')
        brief_info=basic_info.xpath('div[contains(@class, "brief-info")]')
        item["title"] = basic_info.xpath('h1/text()')[0].extract().replace("\n", "")
        item["rank_stars"] = brief_info.xpath('span[contains(@class, "mid-rank-stars")]/@title')[0].extract()
        item["avg_price"] = brief_info.xpath('span[contains(@id, "avgPriceTitle")]/text()')[0].extract()
        item["taste_score"] = brief_info.xpath('span[@id="comment_score"]/span[1]/text()')[0].extract()
        item["environment_score"] = brief_info.xpath('span[@id="comment_score"]/span[2]/text()')[0].extract()
        item["service_score"] = brief_info.xpath('span[@id="comment_score"]/span[3]/text()')[0].extract()
        item["address"] = basic_info.xpath('div[contains(@class, "expand-info address")]/span[contains(@class, "item")]/text()')[0].extract().replace(" ", "")
        yield item
        # script=response.xpath('//script').extract()
        # for s in script:
        #     if "shopGlng" in str:
        #         script_arrs = s.split("\n")
        #         for script_arr in script_arrs:
        #             if "shopGlat" in script_arr:
        #                 item["lat"] = script_arr.replace(" ", "").replace(",", "").replace("\"", "")[9:]
        #             if "shopGlng" in script_arr:
        #                 item["lon"] = script_arr.replace(" ", "").replace(",", "").replace("\"", "")[9:]
        #         break
