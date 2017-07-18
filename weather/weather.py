# !/usr/python/bin
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
from webclient import WebBrowser
def setupSoup(url):
    browser = WebBrowser(debug = False)
    content, rep_header = browser._request(url)
    soup=BeautifulSoup(content, 'html.parser', from_encoding = 'utf-8')
    return soup
def get_feautres(url):
    # 解析一下当前页面是不是出现了验证码，如果出现了验证码，输出请输入验证码的提示信息
    soup = setupSoup(url)
    features = set_blank_features()
    table_tag = soup.find("table")
    if table_tag == None:
        print "no table"
    else:
        tr_tags= table_tag.find_all("tr")
        print len(tr_tags)
        for tr_tag in tr_tags[1:]:
            td_tags = tr_tag.find_all("td")
            features["date"] = td_tags[0].string.replace(" ", "")
            write_to_file(features)
            # print date
    return soup

#设置一个空的features
def set_blank_features():
    features = {}
    features["date"] = ""
    return features

def write_to_file(features):
    filename = "weather.csv"
    file = open(filename, "a")
    file.write(features["date"])

if  __name__ == "__main__":
    url = "http://www.tianqihoubao.com/aqi/beijing-201603.html"
    get_feautres(url)