# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb

class DianpingscrapyPipeline(object):
    def process_item(self, item, spider):
        DBKWARGS = spider.settings.get('DBKWARGS')
        con = MySQLdb.connect(**DBKWARGS)
        cur = con.cursor()
        # sql = ("insert into dianping(shop_id, primary_category, secondary_category, region, sub_region, title, address, avg_price, taste_score, environment_score, service_score, rank_stars, lat, lon, detail_url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        sql = ("insert into dianping(shop_id, title, address, avg_price, rank_stars, taste_score, environment_score, service_score, lat, lon) values(%s, %s, %s, %s, %s, %s, %s, %s)")
        # lis = (item['shop_id'], item['primary_category'], item['secondary_category'], item['region'], item['sub_region'],
        #        item['title'], item['address'], item['avg_price'], item['taste_score'], item['environment_score']
        #        , item['service_score'], item['rank_stars'], item['lat'], item['lon'], item['detail_url'])
        lis = (item["shop_id"], item["title"], item["address"], item["avg_price"], item["rank_stars"], item["taste_score"], item['environment_score'], item['service_score'])
        try:
            cur.execute(sql, lis)
        except Exception, e:
            print "Insert error:", e
            con.rollback()
        else:
            con.commit()
        cur.close()
        con.close()
        return item
