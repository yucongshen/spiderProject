# !/usr/python/bin
# -*- coding: UTF-8 -*-
from webclient import WebBrowser
from headers import headers
def test_api(url):
    try:
        browser = WebBrowser(debug=False)
        content, rep_header = browser._request(url)
        print content

    except:
        print "request error....."




if __name__ == "__main__":
    url="http://api.map.baidu.com/place/v2/detail?uid=5a8fb739999a70a54207c130&output=json&scope=2&ak=zyELMPpA4hZ7Gh7974FuWxnAh4tphVgZ"
    test_api(url)