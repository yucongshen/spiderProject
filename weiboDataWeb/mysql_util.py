# !/usr/python/bin
# -*- coding: UTF-8 -*-
import MySQLdb


def get_connect():
    HOST_NAME = "192.168.1.10"
    USERNAME = "root"
    PASSWORD = "123456"
    DB_NAME = "spider"
    PORT = 3306
    conn = MySQLdb.connect(host=HOST_NAME, user=USERNAME, passwd=PASSWORD, db=DB_NAME, port=PORT, charset="utf8")
    return conn

def insert_data(feature):
    conn = get_connect()
    cursor = conn.cursor()
    sql = "INSERT INTO weibodata (uid, user_name, user_url, device, time, content, thumbs, comments, forward) VALUES('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')".format(feature["uid"], feature["user_name"], feature["user_url"], feature["device"], feature["time"], feature["content"], feature["thumbs"], feature["comments"], feature["forward"])
    try:
        cursor.execute(sql)
        conn.commit()
    except:
        print "sql insert fail"
        conn.rollback()
    conn.close()

def insert_data1(feature):
    conn = get_connect()
    sql = "INSERT INTO weibodata (uid, user_name, user_url, device, time, content, thumbs, comments, forward) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
