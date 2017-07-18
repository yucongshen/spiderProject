# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DianpingscrapyItem(scrapy.Item):
    shop_id = scrapy.Field()
    # primary_category = scrapy.Field()
    # secondary_category = scrapy.Field()
    # region = scrapy.Field()
    # sub_region = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    avg_price = scrapy.Field()
    taste_score = scrapy.Field()
    environment_score = scrapy.Field()
    service_score = scrapy.Field()
    rank_stars = scrapy.Field()
    # lat = scrapy.Field()
    # lon = scrapy.Field()
    # detail_url = scrapy.Field()
