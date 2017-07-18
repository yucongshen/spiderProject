# !/usr/python/bin
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
import urllib2

def nowplaying_movies(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.73 Safari/537.36'}
    req=urllib2.Request(url, headers=headers)
    source=urllib2.urlopen(req)
    soup=BeautifulSoup(source)
    # tagName=soup.li.name
    tagList= soup.find_all("li", attrs={"data-category": "nowplaying"})
    print len(tagList)
    for i in tagList:
        print i.get("data-title")

def print_list(list):
    for i in list:
        print i

if __name__ == '__main__':
    url = "https://movie.douban.com/nowplaying/xiamen/"
    nowplaying_movies(url)
