# !/usr/python/bin
# -*- coding: UTF-8 -*-
import scrapy

class HeartsongSpider(scrapy.spiders.Spider):
    name = "heartsong"  # 爬虫的名字，执行时使用
    allowed_domains = ["heartsong.top"]  # 允许爬取的域名，非此域名的网页不会爬取
    start_urls = [
        "http://www.heartsong.top"  # 起始url，此例只爬这一个页面
    ]

    def parse(self, response):  # 真正的爬虫方法
        html = response.body  # response是获取到的来自网站的返回
        # 以下四行将html存入文件
        filename = "index.html"
        file = open(filename, "w")
        file.write(html)
        file.close()