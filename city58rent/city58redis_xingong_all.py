# !/usr/bin/python
# -*- coding:UTF-8 -*-
import redis
import time
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
        url_xingong = "http://bj.58.com/zufang/sub/l573045/s573046/j2/?pagetype=ditie&PGTID=0d300008-0000-1295-9fb4-55ecef83ba4e&ClickID=2"
        self.get_all_urls(url_xingong, r)
    def get_all_urls(self, url, r):
        all_pages_url_list = get_all_page_url_list(url)
        for one_page_url in all_pages_url_list:
            print "one_page_url_list....", one_page_url
            detail_url_list = get_detail_url_list(one_page_url)
            time.sleep(3)
            for detail_url in detail_url_list:
                print "detail_url......", detail_url
                r.lpush("xingongall", detail_url)

class Consumer(Thread):
    def run(self):
        while True:
            createRedisPool=CreateRedisPool()
            r=createRedisPool.connect()
            url=r.brpop("xingongall")
            url=url[1]
            print "********Consumer......:" +url
            self.consumer_write_features(url)


    def consumer_write_features(self, url):
        filename = "data/redis-daxing-xingong-all.txt"
        features = get_features(url)
        time.sleep(3)
        write_feautres_to_file(features, filename)

if __name__ == "__main__":
    # p = Producer()
    # p.start()
    c = Consumer()
    c.start()