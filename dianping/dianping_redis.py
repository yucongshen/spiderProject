# !usr/python/bin
# -*- coding: UTF-8 -*-
import redis
from threading import Thread
import time
from util import set_blank_features
from dianping_function_common import get_features
from dianping_function_wedding import get_wedding_features
from dianping_function_hotel import get_hotel_features
from dianping_function_decoration import get_decoration_features
from dianping_function_banquet import get_banquet_features
from dianping_function_children import get_children_features
from dianping_function_common import get_all_category_url
from dianping_function_wedding import get_wedding_all_category_url
from dianping_function_hotel import get_hotel_all_category_url
from dianping_function_decoration import get_decoration_all_category_url
from dianping_function_banquet import get_banquet_all_category_url
from dianping_function_children import get_children_all_category_url
from util import write_features_to_file
from dianping_main import get_category

class CreateRedisPool:
    def connect(self):
        pool = redis.ConnectionPool(host="192.168.1.10", port=6379)
        r = redis.Redis(connection_pool=pool)
        return r

class Producer(Thread):
    def run(self):
        createRedisPool=CreateRedisPool()
        r=createRedisPool.connect()
        url_beijing = "https://www.dianping.com/beijing"
        self.get_all_one_city_features(url_beijing, r)

    # 得到全北京的url
    def get_all_one_city_features(self, url, r):
        all_category_list = get_category(url)
        for dic_list in all_category_list:
            primary_category_name = dic_list[0]["name"]
            print "primary_category_name....", primary_category_name
            for dic_index in range(1, len(dic_list)):
                secondary_category_url = dic_list[dic_index]["href"]
                secondary_category_name = dic_list[dic_index]["name"]
                print "secondary_category_url....", secondary_category_name, secondary_category_url
                filename = primary_category_name + "-" + secondary_category_name
                if primary_category_name == "结婚频道":
                    get_wedding_all_category_url(secondary_category_url, filename, r)
                elif primary_category_name == "酒店频道":
                    get_hotel_all_category_url(secondary_category_url, filename, r)
                elif primary_category_name == "亲子频道":
                    get_children_all_category_url(secondary_category_url, filename, r)
                elif primary_category_name == "家装频道":
                    get_decoration_all_category_url(secondary_category_url, filename, r)
                elif primary_category_name == "宴会频道":
                    get_banquet_all_category_url(secondary_category_url, filename, r)
                else:
                    get_all_category_url(secondary_category_url, filename, r)


class Consumer(Thread):
    def run(self):
        while True:
            createRedisPool=CreateRedisPool()
            r=createRedisPool.connect()
            url=r.brpop("dian_ping")
            url=url[1]
            print "********Consumer......:" +url
            self.consumer_write_features(url)


    def consumer_write_features(self, url):
        url_array = url.split("**")
        category_and_region = url_array[0]
        detail_url = url_array[-1]
        primary_category_name = ""
        secondary_category_name = ""
        region_name = ""
        sub_region_name = ""
        arrays = category_and_region.split("-")
        if len(arrays) == 3:
            primary_category_name = arrays[0]
            secondary_category_name = arrays[1]
            region_name = arrays[2]
        elif len(arrays) == 4:
            primary_category_name = arrays[0]
            secondary_category_name = arrays[1]
            region_name = arrays[2]
            sub_region_name = arrays[3]
        else:
            print "filename error in consumer"
        if primary_category_name == "结婚频道":
            features = get_wedding_features(detail_url)
        elif primary_category_name == "酒店频道":
            features = get_hotel_features(detail_url)
        elif primary_category_name == "亲子频道":
            features = get_children_features(detail_url)
        elif primary_category_name == "家装频道":
            features = get_decoration_features(detail_url)
        elif primary_category_name == "宴会频道":
            features = get_banquet_features(detail_url)
        else:
            features = get_features(detail_url)
        features["primary_category"] = primary_category_name
        features["secondary_category"] = secondary_category_name
        features["region"] = region_name
        features["sub_region"] = sub_region_name
        features["detail_url"] = detail_url
        filename = category_and_region + ".txt"
        write_features_to_file(features, filename)



if __name__ == "__main__":
    p = Producer()
    p.start()
    # c = Consumer()
    # c.start()


    # pool = redis.ConnectionPool(host="192.168.1.10", port=6379)
    # r = redis.Redis(connection_pool=pool)
    # r.lpush("dian_ping",666)
    # res=r.lrange("dian_ping", 0, -1)
    # print res




# pool=redis.ConnectionPool(host="192.168.1.10", port=6379)
# r=redis.Redis(connection_pool=pool)
# res=r.lrange("syctopic",0,-1)
# print res
# # r.lpush("syctopic", "shen")
# r.rpop("syctopic")
# res=r.lrange("syctopic",0,-1)
# print(res)

