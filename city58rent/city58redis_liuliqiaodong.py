# !/usr/bin/python
# -*- coding:UTF-8 -*-
import redis
from threading import Thread
from liuliqiaodong import get_all_page_url_list
from liuliqiaodong import get_detail_url_list
from util import write_feautres_to_file
from liuliqiaodong import get_features
class CreateRedisPool:
    def connect(self):
        pool = redis.ConnectionPool(host="192.168.1.10", port=6379)
        r = redis.Redis(connection_pool=pool)
        return r
class Producer(Thread):
    def run(self):
        createRedisPool=CreateRedisPool()
        r=createRedisPool.connect()
        url_liuliqiaodong = "http://bj.58.com/zufang/sub/l634618/s634626/0/j2/?pagetype=ditie&PGTID=0d300008-0000-19ce-2a15-bcac6237bb50&ClickID=2"
        self.get_all_urls(url_liuliqiaodong, r)
    def get_all_urls(self, url, r):
        all_pages_url_list = get_all_page_url_list(url)
        for one_page_url in all_pages_url_list:
            print "one_page_url_list....", one_page_url
            detail_url_list = get_detail_url_list(one_page_url)
            for detail_url in detail_url_list:
                print "detail_url......", detail_url
                r.lpush("liuliqiaodong", detail_url)

class Consumer(Thread):
    def run(self):
        while True:
            createRedisPool=CreateRedisPool()
            r=createRedisPool.connect()
            url=r.brpop("liuliqiaodong")
            url=url[1]
            print "********Consumer......:" +url
            self.consumer_write_features(url)


    def consumer_write_features(self, url):
        filename = "data/redis-9-liuliqiaodong-geren.txt"
        features = get_features(url)
        write_feautres_to_file(features, filename)

if __name__ == "__main__":
    p = Producer()
    p.start()
    # c = Consumer()
    # c.start()