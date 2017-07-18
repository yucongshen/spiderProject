# !/usr/python/bin
# -*- coding: UTF-8 -*-
import cookielib
import urllib
import urllib2
def urlopen():
    url="http://blog.kamidox.com/no-exit"
    try:
        source=urllib2.urlopen(url, timeout=3)
    except urllib2.HTTPError, e:
        print e
    else:
        print source.read(100)
        source.close()

def request():
    #定制HTTP头
    headers = {'User-Agent': 'Mozilla/5.0', 'x-my-header': 'my value'}
    req=urllib2.Request("http://blog.kamidox.com", headers=headers)
    #urlopen不仅能接受url还能接受一个request对象
    source=urllib2.urlopen(req)
    print source.read(100)
    print req.headers
    source.close()

#使用这种方式可以将交互的信息打印出来，方便debug
def request_post_debug():
    # POST
    data = {'username': 'kamidox', 'password': 'xxxxxxxx'}
    # headers = {'User-Agent': 'Mozilla/5.0', 'Content-Type': 'plain/text'}
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request('http://www.douban.com', data=urllib.urlencode(data), headers=headers)
    opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1))
    s = opener.open(req)
    print(s.read(100))
    s.close()

def install_debug_handler():
    opener = urllib2.build_opener(urllib2.HTTPHandler(debuglevel=1),
                                  urllib2.HTTPSHandler(debuglevel=1))
    urllib2.install_opener(opener)

def handle_cookie():
    cookiejar = cookielib.CookieJar()
    handler = urllib2.HTTPCookieProcessor(cookiejar=cookiejar)
    opener = urllib2.build_opener(handler, urllib2.HTTPHandler(debuglevel=1))
    s = opener.open('http://www.douban.com')
    print(s.read(100))
    s.close()

    print('=' * 80)
    print(cookiejar._cookies)
    print('=' * 80)
    #上面保存的cookie，会在下一次发请求的时候，发给下一个请求
    s = opener.open('http://www.douban.com')
    s.close()

if __name__ == '__main__':
    # install_debug_handler()
    # request()
    handle_cookie()