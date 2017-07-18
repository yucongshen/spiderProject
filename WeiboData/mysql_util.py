# !/usr/python/bin
# -*- coding: UTF-8 -*-
import MySQLdb
from weibo_util import get_client


def get_connect():
    HOST_NAME = "192.168.1.10"
    USERNAME = "root"
    PASSWORD = "123456"
    DB_NAME = "spider"
    PORT = 3306
    conn = MySQLdb.connect(host=HOST_NAME, user=USERNAME, passwd=PASSWORD, db=DB_NAME, port=PORT, charset="utf8")
    return conn

def insert_data(features):
    conn = get_connect()
    cursor = conn.cursor()
    sql = "INSERT INTO weibo (idstr, screen_name, province, city, location, profile_image_url, gender, followers_count, friends_count, statuses_count, created_at, status_created_at, status_idstr, status_text, status_geo_longitude, status_geo_latitude) VALUES('{0}', '{1}', {2}, {3}, '{4}', '{5}', '{6}', {7}, {8}, {9}, '{10}', '{11}', '{12}', '{13}', '{14}', '{15}' )".format(features["idstr"], features["screen_name"], features["province"], features["city"], features["location"], features["profile_image_url"], features["gender"], features["followers_count"], features["friends_count"], features["statuses_count"], features["created_at"], features["status"]["created_at"], features["status"]["idstr"], features["status"]["text"], features["status_geo_longitude"], features["status_geo_latitude"])
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        print "sql insert fail"
        conn.rollback()
    conn.close()