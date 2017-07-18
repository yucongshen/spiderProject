# !/usr/python/bin
# -*- coding: UTF-8 -*-
from weibo_user import APIClient
import webbrowser
APP_KEY = '285146347' # app key
APP_SECRET = '03def7d938166850d05127dfe27eeeea' # app secret
CALLBACK_URL = 'http://blog.csdn.net/u014152701' # callback url
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
url = client.get_authorize_url()
# 获取URL参数code:
webbrowser.open_new(url)  # 打开了一个网址，网址后面附带了你需要的code

print "输入url中code后面的内容后按回车键："
code = raw_input()  # 人工输入网址后面的code内容
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
r = client.request_access_token(code)
access_token = r.access_token # 新浪返回的token，类似abc123xyz456
print access_token
expires_in = r.expires_in # token过期的UNIX时间：http://zh.wikipedia.org/wiki/UNIX%E6%97%B6%E9%97%B4

client.set_access_token(access_token, expires_in)
# print client.place.nearby_timeline.get(lat=10, long=10, starttime=1497318472, endtime=1497318498, count=30, range=3000, page=1)
information = client.users.show.get(uid = 3006812112)
print information