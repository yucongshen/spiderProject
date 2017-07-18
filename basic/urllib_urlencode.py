# !/usr/python/bin
# -*- coding: UTF-8 -*-
import urllib
import urlparse
#把字典数据(要传的参数)转化为url编码，对url参数进行编码，对post上去的form数据进行编码
def urlenconde_demo():
    params = {'score': 100, 'name': '爬虫基础', 'comment': 'very good'}
    qs = urllib.urlencode(params)#此时的qs为url编码
    print qs
    print urlparse.parse_qs(qs)

#把url编码转化为字典数据
def parse_qs_demo():
    url = 'https://www.baidu.com/s?wd=url%20%E7%BC%96%E7%A0%81%E8%A7%84%E5%88%99&rsv_spt=1&rsv_iqid=0x928cf1380000a436&issp=1&f=8&rsv_bp=0&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=1&rsv_sug3=16&rsv_sug1=15&rsv_t=1699JwFmhB8a5kfErU33lHHt8KRbsMzqMwqlJ00%2F9fusUM%2Bmx3gc8GLs5In0kVh7s3zU&rsv_sug2=0&inputT=5565&rsv_sug4=6174'
    result=urlparse.urlparse(url)
    print result   #result中有一个query属性，是这个要执行的程序的url（如上url的query是从wd开始的那段）
    #将result中的query指的是要传的那些参数，下面将这些参数解析一下
    print_dict(urlparse.parse_qs(result.query))


def print_dict(d):
    for k, v in d.items():
        print('%s: %s' % (k, v))

if __name__ == '__main__':
    urlenconde_demo()
    parse_qs_demo()