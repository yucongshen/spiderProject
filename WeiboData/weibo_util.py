# !/usr/python/bin
# -*- coding: UTF-8 -*-
from weibo import APIClient
import webbrowser

def get_user_ids(initial_uid):
    all_ids = []
    friends = get_friends(initial_uid)
    friends_ids = friends["ids"]
    for id in friends_ids:
        all_ids.append(id)
    return all_ids


def get_followers(uid):
    client = get_client()
    followers = client.friendships.followers.ids.get(uid = uid)
    return followers

def get_friends(uid):
    client = get_client()
    friends = client.friendships.friends.ids.get(uid = uid)
    return friends

def get_information(uid):
    client = get_client()
    try:
        information = client.users.show.get(uid = uid)
        if information["idstr"] == None:
            information["idstr"] = ""
        if information["screen_name"] == None:
            information["screen_name"] = ""
        if information["province"] == None:
            information["province"] = ""
        if information["city"] == None:
            information["city"] = ""
        if information["location"] == None:
            information["location"] = ""
        if information["profile_image_url"] == None:
            information["profile_image_url"] = ""
        if information["gender"] == None:
            information["gender"] = ""
        if information["followers_count"] == None:
            information["followers_count"] = ""
        if information["friends_count"] == None:
            information["friends_count"] = ""
        if information["statuses_count"] == None:
            information["statuses_count"] = ""
        if information["created_at"] == None:
            information["created_at"] = ""
        if len(information["status"]) == 0:
            information["status"]["created_at"] = ""
            information["status"]["idstr"] = ""
            information["status"]["text"] = ""
            information["status_geo_longitude"] = ""
            information["status_geo_latitude"] = ""
        elif information["status"]["geo"]== None:
            information["status_geo_longitude"] = ""
            information["status_geo_latitude"] = ""
        else:
            information["status_geo_longitude"] = information["status"]["geo"]["longitude"]
            information["status_geo_latitude"] = information["status"]["geo"]["latitude"]
        return information
    except:
        print "get information fail"
        return None


def get_client():
    APP_KEY = '285146347' # app key
    APP_SECRET = '03def7d938166850d05127dfe27eeeea' # app secret
    CALLBACK_URL = 'http://blog.csdn.net/u014152701' # callback url
    client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    url = client.get_authorize_url()
    # 获取URL参数code:
    webbrowser.open_new(url)  # 打开了一个网址，网址后面附带了你需要的code
    access_token = "2.00YLRURD0da8S_418ea4c9c7K4D8TD"
    expires_in = 1655797996
    client.set_access_token(access_token, expires_in)
    return client
    # print "输入url中code后面的内容后按回车键："
    # code = raw_input()  # 人工输入网址后面的code内容
    # client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
    # r = client.request_access_token(code)
    # access_token = r.access_token # 新浪返回的token，类似abc123xyz456
    # print access_token
    # expires_in = r.expires_in # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4
    # print expires_in
    # client.set_access_token(access_token, expires_in)
    # information = client.users.show.get(uid = 3006812112)
    # print information["status"]["text"]

