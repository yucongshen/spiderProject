# !/usr/bin/python
# -*- coding:UTF-8 -*-
import os
from bs4 import BeautifulSoup
from webclient import WebBrowser
import spynner
from headers import pc_headers
import time
import sys
def get_cookie(browser):
    phoenixid=""
    jsessionid=""
    hcv=""
    for cookie in browser.cookiesjar.allCookies():
        if cookie.name() == 'PHOENIX_ID':
            phoenixid = 'PHOENIX_ID=' + cookie.value()
        elif cookie.name() == '_hc.v':
            hcv = '_hc.v=' + cookie.value()
        elif cookie.name() == 'JSESSIONID':
            jsessionid = 'JSESSIONID=' + cookie.value()
    cookies=phoenixid + ";" + jsessionid + ";" +hcv
    return cookies

def setupSoup(url):
    browser = WebBrowser(debug = False)
    content, rep_header = browser._request(url, headers = pc_headers)
    soup=BeautifulSoup(content, 'html.parser', from_encoding = 'utf-8')
    # 解析一下当前页面是不是出现了验证码，如果出现了验证码，输出请输入验证码的提示信息
    verify_title=soup.find_all("title")
    if len(verify_title) == 0:
        print "there is no verify_title in setSoup"
    else:
        verify_title=verify_title[0]
        if verify_title.string == "提示_大众点评网":
            print "请输入验证码"
            phone_url = 'http://m.dianping.com'
            browser_spy = spynner.Browser()
            browser_spy.hide()
            browser_spy.load(phone_url, load_timeout=10, tries=2)
            cookies=get_cookie(browser_spy)
            pc_headers["Cookie"]=cookies
            print pc_headers["Cookie"]
            pc_content, pc_rep_header = browser._request(url, headers=pc_headers)
            soup = BeautifulSoup(pc_content, 'html.parser', from_encoding='utf-8')
    return soup

#设置一个空的features
def set_blank_features():
    features = {}
    features["primary_category"] = ""
    features["secondary_category"] = ""
    features["region"] = ""
    features["sub_region"] = ""
    features["id"] = ""
    features["title"] = ""
    features["address"] = ""
    features["avg_price"] = ""
    features["taste_score"] = ""
    features["environment_score"] = ""
    features["service_score"] = ""
    features["rank_stars"] = ""
    features["lat"] = ""
    features["lon"] = ""
    features["detail_url"]=""
    return features

#输出list
def print_list(list):
    for i in list:
        print i

def print_dic(features):
    print features["primary_category"]
    print features["secondary_category"]
    print features["region"]
    print features["sub_region"]
    print features["id"]
    print features["title"]
    print features["address"]
    print features["avg_price"]
    print features["taste_score"]
    print features["environment_score"]
    print features["service_score"]
    print features["rank_stars"]
    print features["lat"]
    print features["lon"]
    print features["detail_url"]

#如果文件存在，删除文件
def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

#将list写入文件
def write_features_to_file(features, filename):
    #加上时间戳，防止写操作混乱
    date=time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
    # filename=filename.replace("/", "&")
    filename="dianping_data"+"-"+date+".txt"
    path="data_category_region/"+filename
    fl = open(path.decode('utf-8'), "a")
    if features["primary_category"] == None:
        fl.write("")
    else:
        fl.write(features["primary_category"])
    fl.write(";")

    if features["secondary_category"] == None:
        fl.write("")
    else:
        fl.write(features["secondary_category"])
    fl.write(";")

    if features["region"] == None:
        fl.write("")
    else:
        fl.write(features["region"])
    fl.write(";")

    if features["sub_region"] == None:
        fl.write("")
    else:
        fl.write(features["sub_region"])
    fl.write(";")

    if features["id"] == None:
        fl.write("")
    else:
        fl.write(features["id"])
    fl.write(";")
    if features["title"] == None:
        fl.write("")
    else:
        fl.write(features["title"])
    fl.write(";")
    if features["avg_price"] == None:
        fl.write("")
    else:
        fl.write(features["avg_price"])
    fl.write(";")
    if features["taste_score"] == None:
        fl.write("")
    else:
        fl.write(features["taste_score"])
    fl.write(";")
    if features["environment_score"] == None:
        fl.write("")
    else:
        fl.write(features["environment_score"])
    fl.write(";")
    if features["service_score"] ==None:
        fl.write("")
    else:
        fl.write(features["service_score"])
    fl.write(";")
    if features["rank_stars"] == None:
        fl.write("")
    else:
        fl.write(features["rank_stars"])
    fl.write(";")
    if features["address"] == None:
        fl.write("")
    else:
        fl.write(features["address"])
    fl.write(";")
    if features["lon"] == None:
        fl.write("")
    else:
        fl.write(features["lon"])
    fl.write(";")
    if features["lat"] == None:
        fl.write("")
    else:
        fl.write(features["lat"])
    fl.write(";")
    if features["detail_url"] == None:
        fl.write("")
    else:
        fl.write(features["detail_url"])
    fl.write("\n")
    fl.close()

def combine_region(dic_list1, dic_list2):
    new_dic_list = dic_list1
    list1_names = []
    print_list(list1_names)
    for dic1 in dic_list1:
        list1_names.append(dic1["name"])
    for dic in dic_list2:
        if dic["name"] not in list1_names:
            new_dic_list.append(dic)
    return new_dic_list

if __name__ == "__main__":
    # print time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
    phone_url = 'http://m.dianping.com'
    browser_spy = spynner.Browser()
    browser_spy.hide()
    browser_spy.load(phone_url, load_timeout=10, tries=2)
    cookies = get_cookie(browser_spy)
    pc_headers["Cookie"] = cookies
    print pc_headers["Cookie"]