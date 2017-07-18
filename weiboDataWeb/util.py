# !/urs/bin/python
# -*- coding: UTF-8 -*-
import cookielib
import urllib2
import spynner
from webclient import WebBrowser
from headers import fans_page_headers
from urllib2 import Request, urlopen
from bs4 import BeautifulSoup

def setCookie():
    cookie = {}
    # cookie['SINAGLOBAL'] = '8006445736573.964.1498791175491'
    # cookie['TC-Ugrow-G0'] = '370f21725a3b0b57d0baaf8dd6f16a18'
    # cookie['SSOLoginState'] = '1499305985'
    # cookie['TC-V5-G0'] = 'ac3bb62966dad84dafa780689a4f7fc3'
    # cookie['TC-Page-G0'] = '0dba63c42a7d74c1129019fa3e7e6e7c'
    # cookie['_s_tentry'] = '-'
    # cookie['Apache'] = '21442175893.713333.1499305990255'
    # cookie['ULV'] = '1499305990295:4:3:3:21442175893.713333.1499305990255:1499161331836'
    # cookie['WBtopGlobal_register_version'] = '85d55bc0e4930702'
    # cookie['login_sid_t'] = 'ae9e9c10cd3528ae8bc5c12b81b5b0c3'
    # cookie['SUBP'] = '0033WrSXqPxfM725Ws9jqgMF55529P9D9WFhYHom8_HluTXmuk_ahodT5JpX5KMhUgL.Foe7ehqReKzpeKz2dJLoI7D0IsHVwPHodc4r'
    # cookie['UOR'] = 'www.liaoxuefeng.com,widget.weibo.com,www.baidu.com'
    # cookie['YF-Page-G0'] = '00acf392ca0910c1098d285f7eb74a11'
    # cookie['YF-V5-G0'] = 'f59276155f879836eb028d7dcd01d03c'
    # cookie['SCF'] = 'ArWvED6VZA7JGWL9d4BT1uYR3nYlqw13uXV7zMrlWorOULbvaAQWbieXf3b29aZPGUfp5Y88gNkySNC4x4sv_d0.'
    cookie['SUB'] = '_2A250Zq-2DeRhGeVO61QZ8SzNyj6IHXVXFYZ-rDV8PUNbmtAKLUHCkW8xyPFucRqgoo6Hj9KxJPD5Q0W4Dg..'
    # cookie['SUHB'] = '0QS5yuGIT7lRju'
    # cookie['ALF'] = '1531188069'
    # cookie['wvr'] = '6'
    cookie_str = ""
    for k in cookie:
        cookie_str = cookie_str + "%s=%s; " %(k, cookie[k])
    cookie_str = cookie_str[:-2]
    return cookie_str



def get_cookie(browser):
    cookie = browser.cookiesjar.allCookies()[0]
    return "%s = %s" %(cookie.name(), cookie.value())



def cookies_to_file():
    # 设置保存cookie的文件，同级目录下的cookie.txt
    filename = 'data/cookie.txt'
    # 声明一个MozillaCookieJar对象实例来保存cookie，之后写入文件
    cookie = cookielib.MozillaCookieJar(filename)
    # 利用urllib2库的HTTPCookieProcessor对象来创建cookie处理器
    handler = urllib2.HTTPCookieProcessor(cookie)
    # 通过handler来构建opener
    opener = urllib2.build_opener(handler)
    # 创建一个请求，原理同urllib2的urlopen
    opener.open("http://weibo.com/3006812112")
    # 保存cookie到文件
    cookie.save(ignore_discard=True, ignore_expires=True)

def get_cookies():
    # 创建MozillaCookieJar实例对象
    cookie = cookielib.MozillaCookieJar()
    # 从文件中读取cookie内容到变量
    cookie.load('data/cookie.txt', ignore_discard=True, ignore_expires=True)
    # 创建请求的request
    req = urllib2.Request("http://weibo.com/3006812112")
    # 利用urllib2的build_opener方法创建一个opener
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
    response = opener.open(req)
    print response.info()



def set_blank_feature():
    feature = {}
    feature["uid"] = ""
    feature["user_url"] = ""
    feature["user_name"] = ""
    feature["device"] = ""
    feature["time"] = ""
    feature["content"] = ""
    feature["thumbs"] = ""
    feature["comments"] = ""
    feature["forward"] = ""
    return feature

def setupSoup(url, headers):
    browser = WebBrowser(debug = False)
    content, rep_header = browser._request(url, headers = headers)
    soup = BeautifulSoup(content, 'html.parser', from_encoding = 'utf-8')
    if "ERROR 404 HTTP Error 404: Not Found" in soup:
        browser_spy = spynner.Browser()
        browser_spy.hide()
        browser_spy.load(url, load_timeout=10, tries=2)
        cookie = get_cookie(browser_spy)
        fans_page_headers["Cookie"] = cookie
        browser = WebBrowser(debug=False)
        content, rep_header = browser._request(url, headers=fans_page_headers)
        soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    return soup

if __name__ == "__main__":
    setCookie()
    # url = "http://weibo.com/3006812112"
    # browser_spy = spynner.Browser()
    # browser_spy.hide()
    # browser_spy.load(url, load_timeout=10, tries=2)
    # print get_cookie(browser_spy)