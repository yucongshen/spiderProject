# !/usr/python/bin
# -*- coding: UTF-8 -*-
from weibopack.weibo import APIClient
import webbrowser  # python内置的包
APP_KEY = '285146347'  # 你的app_key
APP_SECRET = '03def7d938166850d05127dfe27eeeea'  # 你的app_secret
# CALLBACK_URL = 'https://api.weibo.com/oauth2/default.html'  # 网站回调地址
CALLBACK_URL = "http://blog.csdn.net/u014152701"
# 在网站设置"使用微博账号登陆"的链接，当用户点击链接后，引导用户跳转至如下地址
# 利用官方微博ADK
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
# 得到授权页面的url，利用webbrowser打开这个url
url = client.get_authorize_url()
print url
webbrowser.open_new(url)  # 打开了一个网址，网址后面附带了你需要的code
# 用户授权后，将跳转至网站回调地址，并附加参数code=abcd1234

# 获取URL参数code：
print "输入url中code后面的内容后按回车键："
code = raw_input()  # 人工输入网址后面的code内容

r = client.request_access_token(code)  # 获得用户授权

# 保存access_token, expires_in
access_token = r.access_token  # 新浪返回的token，类似abc123xyz456
print access_token
expires_in = r.expires_in
# 设置得到的access_token，client可以直接调用API了
client.set_access_token(access_token, expires_in)

print client.friendships.friends.bilateral.ids.get(uid = 12345678)

# r = client.place__nearby_timeline(lat = 10, long = 10)
# print r

# r = client.statuses__friends_timeline()
# print r

# print client.statuses__public_timeline()
# statuses = client.statuses__public_timeline()['statuses']

# https://api.weibo.com/2/place/nearby_timeline.json?access_token=2.00YLRURD0da8S_418ea4c9c7K4D8TD&lat=39.932311&long=116.450692
# r = client.place.nearby_timeline
# print r.get(lat = 10, long = 10)


# r = client.place.poi_timeline.get(poiid = 1)
# print r


# https://api.weibo.com/2/statuses/home_timeline.json?access_token=2.00YLRURDEZemSE2d8af63abfGT8u_D&count=20
# r = client.statuses.home_timeline.get(count = 20)
# print r

#高级接口
# r = client.search.topics.get(q = "鹿晗")
# print r

# r = client.statuses.repost_timeline.get(id = 3006812112)
# print r

# r = client.account.get_uid.get()
# print r

# r = client.statuses.home_timeline.get(count=50, page=1)
# print r

# statuses = client.place__nearby_timeline()['statuses']
# length = len(statuses)
# print length
# 输出了部分信息
# for i in range(0, length):
#     print u"微博创建时间:" + statuses[i]['created_at']
#     print u'昵称:' + statuses[i]['user']['screen_name']
#     print u'简介:' + statuses[i]['user']['description']
#     print u'位置:' + statuses[i]['user']['location']
#     print u'微博:' + statuses[i]['text']