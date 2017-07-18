# !/usr/python/bin
# -*- coding: UTF-8 -*-
import urllib

#按字节读取
def read():
    source=urllib.urlopen("http://blog.kamidox.com")
    content=source.read(100)
    print content

def readline():
    source=urllib.urlopen("http://blog.kamidox.com")
    for i in range(10):
        print ('line: %d: %s' %(i+1,source.readline()))

#这种方式输出的格式不太好
def readlines():
    source = urllib.urlopen("http://blog.kamidox.com")
    print print_list(source.readlines())

#返回http状态码(200代表请求成功)
def getcode():
    source=urllib.urlopen("http://blog.kamidox.com")
    print source.getcode()

#返回httpMessage
def info():
    source=urllib.urlopen("http://blog.kamidox.com")
    msg=source.info()
    print_list(msg.headers)
    print_list(msg.items())#返回一个解析过的元组
    print msg.getheader('Content-Type')

def dir_demo():
    source=urllib.urlopen("http://blog.kamidox.com")
    msg=source.info()
    print_list(dir(msg))#将msg中的方法全部打印出来


def print_list(list):
    for i in list:
        print i

if __name__ == '__main__':
    dir_demo()