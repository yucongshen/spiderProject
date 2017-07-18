# !/usr/bin/python
# -*- coding: UTF-8 -*-
import redis
from threading import Thread
from weibo_main import get_all_fans_url_list
import threading
from weibo_main import get_feature_list_front
from weibo_main import get_feature_list_behind
from weibo_main import insert_feature_list_to_database
from weibo_main import get_middle_behind_url
import urllib
import urlparse
from weibo_main import get_total_page_num

class CreateRedisPool:
    def connect(self):
        pool = redis.ConnectionPool(host="192.168.1.10", port=6379)
        r = redis.Redis(connection_pool=pool)
        return r


class Producer(Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.user_url_set = set("user_url_set")
        self.user_url_set.clear()
    def run(self):
        createRedisPool=CreateRedisPool()
        r=createRedisPool.connect()
        yinjiaoshou_1 = "http://weibo.com/u/234535428?page=1"
        self.user_url_iterator(yinjiaoshou_1, r)

    def user_url_iterator(self, url, r, iter_num=1):
        if iter_num <= 6:
            list = get_all_fans_url_list(url)
            for user_url in list:
                if not self.user_url_set.__contains__(user_url):
                    r.lpush("weibo_users_url", user_url)
                    self.user_url_set.add(user_url)
                    self.user_url_iterator(user_url, r, iter_num + 1)

class Consumer(Thread):
    def run(self):
        while True:
            createRedisPool=CreateRedisPool()
            r=createRedisPool.connect()
            url=r.brpop("weibo_users_url")
            url=url[1]
            print "********Consumer......:" +url
            self.get_all_page_features(url)

    def get_all_page_features(self, url):
        init_url_base = url.split("?")
        init_url_base = "%s?" % (init_url_base[0])
        list_init = get_feature_list_front(url)
        insert_feature_list_to_database(list_init)
        print "one......%s" % (url)
        middle_behind_url_dic = get_middle_behind_url(url, "1")
        url_middle = middle_behind_url_dic["url_middle"]
        if url_middle != "":
            list_middle = get_feature_list_behind(url_middle)
            insert_feature_list_to_database(list_middle)
            print "two......%s" % (url_middle)
        url_behind = middle_behind_url_dic["url_behind"]
        if url_behind != "":
            list_behind = get_feature_list_behind(url_behind)
            insert_feature_list_to_database(list_behind)
            print "three......%s\n" % (url_behind)
            page_num = get_total_page_num(url_behind)
            for num in range(2, page_num + 1):
                num = str(num)
                init_param = urlparse.parse_qs(urlparse.urlparse(url).query)
                init_param["page"] = num
                init_param_str = urllib.urlencode(init_param)
                init_url = "%s%s" % (init_url_base, init_param_str)
                init_list = get_feature_list_front(init_url)
                insert_feature_list_to_database(init_list)
                print "one......%s" % (init_url)
                middle_behind_dic = get_middle_behind_url(init_url, num)
                middle_url = middle_behind_dic["url_middle"]
                if middle_url != "":
                    middle_list = get_feature_list_behind(middle_url)
                    insert_feature_list_to_database(middle_list)
                    print "two......%s" % (middle_url)
                behind_url =middle_behind_dic["url_behind"]
                if behind_url != "":
                    behind_list = get_feature_list_behind(behind_url)
                    insert_feature_list_to_database(behind_list)
                    print "three......%s\n" % (behind_url)

if __name__ == "__main__":
    # producer = Producer()
    # producer.start()
    consumer = Consumer()
    consumer.start()