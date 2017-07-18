# !/usr/bin/python
# -*- coding: UTF-8 -*-
from webclient import WebBrowser
from headers import fans_page_headers
from bs4 import BeautifulSoup
import json
from util import set_blank_feature
from mysql_util import insert_data
import urllib
import urlparse
from headers import fans_detail_headers

def get_feature_list_common(html_soup, url):
    feature_list = []
    tbinfo_tags = html_soup.find_all(class_="WB_cardwrap")
    if len(tbinfo_tags) == 0:
        print "there is no tbinfo tags in get features"
    else:
        for tbinfo in tbinfo_tags:
            feature = set_blank_feature()
            ul_tag = tbinfo.find("ul", class_="WB_row_line WB_row_r4 clearfix S_line2")
            if ul_tag != None:
                li_tags = ul_tag.find_all("li")
                if len(li_tags) >= 4:
                    zhuanfa_li = li_tags[1]
                    zhuanfa_em = zhuanfa_li.find_all("em")
                    if len(zhuanfa_em) >= 3:
                        zhuanfa_em = zhuanfa_em[1]
                        zhuanfa = zhuanfa_em.string
                        if zhuanfa != None:
                            if zhuanfa == "转发":
                                zhuanfa = 0
                            feature["forward"] = zhuanfa
                            # print feature["forward"]
                    comments_li = li_tags[2]
                    comments_em = comments_li.find_all("em")
                    if len(comments_em) >= 3:
                        comments_em = comments_em[1]
                        comments = comments_em.string
                        if comments != None:
                            if comments == "评论":
                                comments = 0
                            feature["comments"] = comments
                            # print feature["comments"]
                    zan_li = li_tags[3]
                    zan_em = zan_li.find_all("em")
                    if len(zan_em) >= 3:
                        zan_em = zan_em[1]
                        zan = zan_em.string
                        if zan != None:
                            if zan == "赞":
                                zan = 0
                            feature["thumbs"] = zan
                            # print feature["thumbs"]
            content_tag = tbinfo.find("div", class_="WB_text W_f14")
            if content_tag != None:
                content_tag_string = content_tag.get_text()
                if content_tag_string != None:
                    feature["content"] = content_tag_string.replace(" ", "").replace("\n", "")
                place_a_tag = content_tag.find_all("a", target="_blank")
                if len(place_a_tag) != 0:
                    place_a_tag = place_a_tag[-1]
                    place_id = place_a_tag.get("suda-uatrack")
                    if place_id != None:
                        if "place" in place_id:
                            index = place_id.index("place")
                            result_id = place_id[index + len("place:1022%3A"):]
                            print result_id
            time_device_info = tbinfo.find("div", class_="WB_from S_txt2")
            if time_device_info != None:
                time_device = time_device_info.find_all("a")
                if len(time_device) >= 1:
                    time_a = time_device[0]
                    time_a_title = time_a.string
                    if time_a_title != None:
                        feature["time"] = time_a_title
                if len(time_device) >=2:
                    device_a = time_device[1]
                    device_a_string = device_a.string
                    if device_a_string != None:
                        feature["device"] = device_a_string
                        # print feature["device"]
            web_info = tbinfo.find("div", class_="WB_info")
            if web_info != None:
                title_tag = web_info.find("a")
                if title_tag != None:
                    feature["user_url"] = url
                    dic = get_oid_and_pageid(url)
                    if dic["oid"] != "":
                        feature["uid"] = dic["oid"]
                    # print feature["user_url"]
                    title_name = title_tag.string
                    if title_name != None:
                        feature["user_name"] = title_name
                        # print feature["user_name"]
            if not ((feature["uid"] == "") and (feature["user_name"] == "") and (feature["user_url"] == "") and (
                        feature["device"] == "") and (feature["time"] == "") and (feature["content"] == "") and (
                        feature["thumbs"] == "") and (feature["forward"] == "") and (feature["comments"] == "")):
                feature_list.append(feature)
    return feature_list

def get_feature_list_front(url):
    feature_list = []
    content = get_response(url, fans_page_headers)
    content = BeautifulSoup(content, "html.parser", from_encoding="utf-8")
    script_tags = content.find_all("script")
    if len(script_tags) == 0:
        print "there is no script tags in get features front"
    else:
        for tag in script_tags:
            str = tag.string
            if (str != None) and "feedtop" in str:
                str_replace = str.replace("FM.view(", "")[:-1]
                str_json = json.loads(str_replace)
                html = str_json["html"]
                html_soup = BeautifulSoup(html, 'html.parser')
                feature_list = get_feature_list_common(html_soup, url)
    return feature_list

def get_feature_list_behind(url):
    content = get_response(url, fans_page_headers)
    content = json.loads(content)
    html = content["data"]
    html_soup = BeautifulSoup(html, 'html.parser')
    feature_list = get_feature_list_common(html_soup, url)
    return feature_list

def get_response(url, header):
    browser = WebBrowser(debug = False)
    content, rep_header = browser._request(url, headers = header)
    return content

def insert_feature_list_to_database(feature_list):
    for feature in feature_list:
        insert_data(feature)


def get_oid_and_pageid(url):
    dic = {}
    dic["oid"] = ""
    dic["page_id"] = ""
    content = get_response(url, fans_page_headers)
    if "mbloglist" in url:
        arrays_url = url.split("&")
        for a in arrays_url:
            if "script_uri" in a:
                dic["oid"] = a[a.index("script_uri=%2Fu%2F")+len("script_uri=%2Fu%2F"):]
                break
    else:
        content = BeautifulSoup(content, "html.parser", from_encoding="utf-8")
        script_tags = content.find_all("script")
        if len(script_tags) == 0:
            print "there is no script tags in get oid and page_id"
        else:
            for tag in script_tags:
                str = tag.string
                if "$CONFIG" in str:
                    arrays = str.split(";")
                    for a in arrays:
                        if "$CONFIG['oid']" in a:
                            oid_index = a.index("$CONFIG['oid']='")
                            dic["oid"] = a[oid_index + len("$CONFIG['oid']='"):-1]
                        if "$CONFIG['page_id']" in a:
                            page_id_index = a.index("$CONFIG['page_id']='")
                            dic["page_id"] = a[page_id_index + len("$CONFIG['page_id']='"):-1]
                        if (dic["oid"] != "") and (dic["page_id"] != ""):
                            break
                    break
    return dic


def get_middle_behind_url(url, num):
    middle_behind_url_dic = {}
    middle_behind_url_dic["url_middle"] = ""
    middle_behind_url_dic["url_behind"] = ""
    oid_and_pageid = get_oid_and_pageid(url)
    page_id = oid_and_pageid["page_id"]
    oid = oid_and_pageid["oid"]
    url_base = "http://weibo.com/p/aj/v6/mblog/mbloglist?"
    param_dic = {}
    param_dic["domain"] = "100505"
    param_dic["pre_page"] = num
    param_dic["page"] = num
    param_dic["script_uri"] = "/u/%s" % (oid)
    param_dic["pagebar"] = "0"
    param_dic["id"] = page_id
    param_str = urllib.urlencode(param_dic)
    url_middle = "%s%s" % (url_base, param_str)
    middle_behind_url_dic["url_middle"] = url_middle
    param_dic["pagebar"] = "1"
    param_str = urllib.urlencode(param_dic)
    url_behind = "%s%s" % (url_base, param_str)
    middle_behind_url_dic["url_behind"] = url_behind
    return middle_behind_url_dic

def get_total_page_num(url_behind):
    total_page_num = 0
    content = get_response(url_behind, fans_page_headers)
    content_json = json.loads(content)
    html = content_json["data"]
    html_soup = BeautifulSoup(html, "html.parser")
    page_tag = html_soup.find("div", class_ = "layer_menu_list W_scroll")
    if page_tag != None:
        page_a = page_tag.find("a")
        if page_a != None:
            str = page_a.string
            if str != None:
                total_page_num = str.replace("第", "").replace("页", "")
                total_page_num = total_page_num[1:-1]
                total_page_num = int(total_page_num)
    return total_page_num

# 传入主页第一页的url http://weibo.com/u/5391323887
# 并且返回第一页的第三段内容的url
def get_all_page_features(url):
    init_url_base = url.split("?")
    init_url_base = "%s?" %(init_url_base[0])
    list_init = get_feature_list_front(url)
    insert_feature_list_to_database(list_init)
    print "one......%s" %(url)
    middle_behind_url_dic = get_middle_behind_url(url, "1")
    url_middle = middle_behind_url_dic["url_middle"]
    if url_middle != "":
        list_middle = get_feature_list_behind(url_middle)
        insert_feature_list_to_database(list_middle)
        print "two......%s" %(url_middle)
    url_behind = middle_behind_url_dic["url_behind"]
    if url_behind != "":
        list_behind = get_feature_list_behind(url_behind)
        insert_feature_list_to_database(list_behind)
        print "three......%s\n" %(url_behind)
        page_num = get_total_page_num(url_behind)
        for num in range(2, page_num+1):
            num = str(num)
            init_param = urlparse.parse_qs(urlparse.urlparse(url).query)
            init_param["page"] = num
            init_param_str = urllib.urlencode(init_param)
            init_url = "%s%s" %(init_url_base, init_param_str)
            init_list = get_feature_list_front(init_url)
            insert_feature_list_to_database(init_list)
            print "one......%s" % (init_url)
            middle_behind_dic = get_middle_behind_url(init_url, num)
            middle_url = middle_behind_dic["url_middle"]
            if middle_url != "":
                middle_list = get_feature_list_behind(middle_url)
                insert_feature_list_to_database(middle_list)
                print "two......%s" % (middle_url)
            behind_url = middle_behind_dic["url_behind"]
            if behind_url != "":
                behind_list = get_feature_list_behind(behind_url)
                insert_feature_list_to_database(behind_list)
                print "three......%s\n" % (behind_url)


    # 将url转化为字典形式
    # url_middle = "http://weibo.com/p/aj/v6/mblog/mbloglist?domain=100505&pagebar=0&id=1005055391323887&script_uri=/u/5391323887&page=1&pre_page=1"
    # param_str = urlparse.urlparse(url_middle).query
    # param_dic = urlparse.parse_qs(param_str)
    # print param_dic


def get_userid_list_from_fans_page(url):
    fans_url_list = []
    if url == "":
        print "fans page url is blank in get userid list from fans page"
    else:
        response = get_response(url, fans_detail_headers)
        soup = BeautifulSoup(response, "html.parser", from_encoding="utf-8")
        script_follow = soup.find_all("script")
        for script_i in script_follow:
            script_i_string = script_i.string
            if script_i_string != None:
                if "follow_list" in script_i_string:
                    follow_content = script_i_string
                    follow_str = follow_content.replace("FM.view(", "")[:-1]
                    follow_json = json.loads(follow_str)
                    follow_content = follow_json["html"]
                    follow_soup = BeautifulSoup(follow_content, 'html.parser')
                    fans_ul = follow_soup.find("ul", class_="follow_list")
                    if fans_ul == None:
                        print "there is no fans ul tag"
                    else:
                        fans_li_list = fans_ul.find_all("li", class_="follow_item S_line2")
                        if len(fans_li_list) == 0:
                            print "there is no fans_li_list......"
                        else:
                            for li in fans_li_list:
                                fans_li_a = li.find("a", target="_blank")
                                if fans_li_a == None:
                                    print "there is no fans li a"
                                else:
                                    fans_id = fans_li_a.get("href")
                                    if fans_id == None:
                                        print "fans id is none"
                                    else:
                                        fans_id_array = fans_id.split("?")
                                        for a in fans_id_array:
                                            if "/u/" in a:
                                                index = a.index("/u/")
                                                id = a[index+len("/u/"):]
                                                fans_url = "http://weibo.com/u/%s?page=1" %(id)
                                                fans_url_list.append(fans_url)
                                                break
                    break
    return fans_url_list

# 传入粉丝列表页的第一页的url,得到所有页的粉丝列表
def get_all_fans_pages_url(url):
    all_fans_page_url_list = []
    all_fans_page_url_list.append(url)
    param_dic = urlparse.parse_qs(urlparse.urlparse(url).query)
    index = 2
    url_array = url.split("?")
    url_base = "%s?" %(url_array[0])
    while True:
        param_dic["page"] = index
        next_param_str = urllib.urlencode(param_dic)
        next_url = "%s%s" %(url_base, next_param_str)
        response = get_response(next_url, fans_detail_headers)
        if "下一页" not in response:
            break
        else:
            all_fans_page_url_list.append(next_url)
            index = index+1
    return all_fans_page_url_list

# 传入某用户的url主页，得到主页上的粉丝链接
def get_fans_link(url):
    fans_page_url = ""
    dic = get_oid_and_pageid(url)
    page_id = dic["page_id"]
    if page_id != "":
        fans_page_url = "http://weibo.com/p/%s/follow?relate=fans&page=1" %(page_id)
    return fans_page_url

# 传入某用户的主页url，得到全部页的粉丝url
def get_all_fans_url_list(url):
    user_url_list = []
    fans_page_url = get_fans_link(url)
    all_fans_page_url = get_all_fans_pages_url(fans_page_url)
    for page_url in all_fans_page_url:
        print page_url
        detail_user_url_list = get_userid_list_from_fans_page(page_url)
        for user_url in detail_user_url_list:
            user_url_list.append(user_url)
            print user_url
    return user_url_list
# 迭代得到用户的url

user_url_set = set("user_url_set")
user_url_set.clear()
def user_url_iterator(url, iter_num = 1):
    if iter_num <=1:
        list = get_all_fans_url_list(url)
        for user_url in list:
            user_url_set.add(user_url)
            user_url_iterator(user_url, iter_num+1)



def url_set():
    user_set = set("user_url")
    user_set.clear()
    user_url_set.add("http://weibo.com/u/5391323887?page=1")
    if user_url_set.__contains__("http://weibo.com/u/5391323887?page=1"):
        print "already....."



if __name__ == "__main__":
    qiexiang_1 = "http://weibo.com/u/5391323887?page=1"
    qiexiang_2 = "http://weibo.com/p/aj/v6/mblog/mbloglist?domain=100505&pagebar=0&id=1005055391323887&script_uri=/u/5391323887&page=1&pre_page=1"
    qiexiang_3 = "http://weibo.com/p/aj/v6/mblog/mbloglist?domain=100505&pagebar=1&id=1005055391323887&script_uri=/u/5391323887&page=1&pre_page=1"

    yinjiaoshou_1 = "http://weibo.com/u/234535428?page=1"
    shenyucong = "http://weibo.com/u/3006812112?page=1"
    yinjiaoshoufans_url = "http://weibo.com/p/1035051098618600/follow?relate=fans"
    fans = "http://weibo.com/p/1035051098618600/follow?relate=fans&page=1"
    url_juxiezuo = "http://weibo.com/u/1949171560?page=1"
    list = get_feature_list_front(yinjiaoshou_1)
    # for i in list:
    #     print "content......", i["content"]
    # url_set()

    # user_url_iterator(yinjiaoshou_1)
    # print len(user_url_set)
    # for i in user_url_set:
    #     print i
    # url_set()
    # get_all_fans_url_list(yinjiaoshou_1)

    # list = get_userid_list_from_fans_page(fans)
    # print len(list)
    # print get_oid_and_pageid(yinjiaoshou_1)
    # print get_fans_link(shenyucong)
    # get_all_page_features(shenyucong)

    # 插入企鹅乡的第一页的前半部分
    # list = get_feature_list_front(qiexiang_1)
    # insert_feature_list_to_database(list)


    # list = get_feature_list_behind(qiexiang_2)
    # insert_feature_list_to_database(list)

    # list = get_feature_list_behind(qiexiang_3)
    # insert_feature_list_to_database(list)



    # get_feature_list_front("http://weibo.com/u/3006812112?is_all=1")
    # get_feature_list_front("http://weibo.com/u/2390934947?is_all=1&stat_date=201610#feedtop")