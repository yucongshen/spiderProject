# !/usr/bin/python
# -*- coding: UTF-8 -*-
import json
from bs4 import BeautifulSoup
from util import setupSoup
from headers import fans_page_headers
from headers import fans_detail_headers
from util import set_blank_feature
from mysql_util import insert_data
from webclient import WebBrowser

# from util import setCookie
import spynner
from lxml import etree
def get_feautres_list(url):
    soup = setupSoup(url, fans_page_headers)
    feature_list = []
    script_tags = soup.find_all("script")
    if len(script_tags) == 0:
        print "there is no script tags"
    else:
        for script_i in script_tags:
            script_i_string = script_i.string
            if script_i_string == None:
                print "the script i string is none in get features"
            else:
                if "WB_text W_f14" in script_i_string:
                    weibo_content = script_i_string
                    weibo_content = weibo_content.replace("FM.view(", "")[:-1]
                    weibo_json = json.loads(weibo_content)
                    weibo_content = weibo_json["html"]
                    weibo_soup = BeautifulSoup(weibo_content, "html.parser")
                    tbinfo_tags = weibo_soup.find_all(class_ = "WB_cardwrap")
                    if len(tbinfo_tags) == 0:
                        print "there is no tbinfo tags in get features"
                    else:
                        for tbinfo in tbinfo_tags:
                            feature = set_blank_feature()
                            ul_tag = tbinfo.find("ul", class_ = "WB_row_line WB_row_r4 clearfix S_line2")
                            if ul_tag == None:
                                print "there is no ul tag in get features"
                            else:
                                li_tags = ul_tag.find_all("li")
                                if len(li_tags) < 4:
                                    print "there is no li tags in ul in get features"
                                else:
                                    zhuanfa_li = li_tags[1]
                                    zhuanfa_em = zhuanfa_li.find_all("em")
                                    if len(zhuanfa_em) < 3:
                                        print "there is no zhuanfa em in get features"
                                    else:
                                        zhuanfa_em = zhuanfa_em[1]
                                        zhuanfa = zhuanfa_em.string
                                        if zhuanfa == None:
                                            print "the zhuan fa is none"
                                        else:
                                            if zhuanfa == "转发":
                                                zhuanfa = 0
                                            feature["forward"] = zhuanfa
                                            # print feature["forward"]
                                    comments_li = li_tags[2]
                                    comments_em = comments_li.find_all("em")
                                    if len(comments_em) < 3:
                                        print "there is no comments em in get features"
                                    else:
                                        comments_em = comments_em[1]
                                        comments = comments_em.string
                                        if comments == None:
                                            print "the comments is none in get features"
                                        else:
                                            if comments == "评论":
                                                comments = 0
                                            feature["comments"] = comments
                                            # print feature["comments"]
                                    zan_li = li_tags[3]
                                    zan_em = zan_li.find_all("em")
                                    if len(zan_em) < 3:
                                        print "there is no zan em in get features"
                                    else:
                                        zan_em = zan_em[1]
                                        zan = zan_em.string
                                        if zan == None:
                                            print "the zan is none in get features"
                                        else:
                                            if zan == "赞":
                                                zan = 0
                                            feature["thumbs"] = zan
                                            # print feature["thumbs"]
                            content_tag = tbinfo.find("div", class_ = "WB_text W_f14")
                            if content_tag == None:
                                print "there is no content tag in get features"
                            else:
                                content_tag_string = content_tag.contents[0]
                                if content_tag_string == None:
                                    print "there is no content tag string int get features"
                                else:
                                    feature["content"] = content_tag_string.replace(" ", "").replace("\n", "")
                                    # print feature["content"]
                            time_device_info = tbinfo.find("div", class_ = "WB_from S_txt2")
                            if time_device_info == None:
                                print "there is no time info in get features"
                            else:
                                time_device = time_device_info.find_all("a")
                                if len(time_device) < 2:
                                    print "there is no time a in get features"
                                else:
                                    time_a = time_device[0]
                                    time_a_title = time_a.get("title")
                                    if time_a_title == None:
                                        print "the time a title is none"
                                    else:
                                        feature["time"] = time_a_title
                                        # print feature["time"]
                                    device_a = time_device[1]
                                    device_a_string = device_a.string
                                    if device_a_string == None:
                                        print "there is no device a string in get features"
                                    else:
                                        feature["device"] = device_a_string
                                        # print feature["device"]
                            web_info = tbinfo.find("div", class_ = "WB_info")
                            if web_info == None:
                                print "there is no web info in get features"
                            else:
                                title_tag = web_info.find("a")
                                if title_tag == None:
                                    print "there is no title tag a in get features"
                                else:
                                    feature["user_url"] = url
                                    if "?refer_flag" in url:
                                        if "/u/" in url:
                                            feature["uid"] = url[len("http://weibo.com/u/"):url.index("?refer_flag")]
                                        else:
                                            feature["uid"] = url[len("http://weibo.com/"):url.index("?refer_flag")]
                                    else:
                                        if "/u/" in url:
                                            feature["uid"] = url[len("http://weibo.com/u/"):]
                                        else:
                                            feature["uid"] = url[len("http://weibo.com/"):]
                                    # print feature["user_url"]
                                    title_name = title_tag.string
                                    if title_name == None:
                                        print "there is no title name in get features"
                                    else:
                                        feature["user_name"] = title_name
                                        # print feature["user_name"]
                            if (feature["uid"] == "") and (feature["user_name"] == "") and (feature["user_url"] == "") and (feature["device"] == "") and (feature["time"] == "") and (feature["content"] == "") and (feature["thumbs"] == "") and (feature["forward"] == "") and (feature["comments"] == ""):
                                pass
                            else:
                                feature_list.append(feature)
                    break
    return feature_list

def get_fans_page_url(url):
    fans_page_url = ""
    soup = setupSoup(url, fans_detail_headers)
    script_tag = soup.find_all("script")
    if len(script_tag) == 0:
        print "there is no script_tag in soup"
    else:
        for script_i in script_tag:
            script_i_string = script_i.string
            # print script_i_string
            if "粉丝" in script_i_string and "微博" in script_i_string and "关注" in script_i_string:
                script_fans = script_i
                fans_content = script_fans.string
                if fans_content == None:
                    print "fans content is none......"
                else:
                    fans_str = fans_content.replace("FM.view(", "")[:-1]
                    fans_json = json.loads(fans_str)
                    fans_content = fans_json["html"]
                    fans_soup = BeautifulSoup(fans_content, 'html.parser')
                    fans_a = fans_soup.find_all("a")
                    if len(fans_a) < 2:
                        print "there is no fans a in"
                    else:
                        fans_a = fans_a[1]
                        fans_page_url = fans_a.get("href")
                        if fans_page_url == None:
                            fans_page_url = ""
                            print "there is no fans page url"
                        else:
                            if "http" not in fans_page_url:
                                if "weibo.com" in fans_page_url:
                                    fans_page_url = "http:" + fans_page_url
                                else:
                                    fans_page_url = "http://weibo.com" + fans_page_url
                break
    return fans_page_url

def get_fans_detail_url_list(fans_page_url):
    fans_url_list = []
    if fans_page_url == "":
        print "fans page url is blank"
    else:
        soup = setupSoup(fans_page_url, fans_detail_headers)
        print soup
        script_follow = soup.find_all("script")
        for script_i in script_follow:
            script_i_string = script_i.string
            if script_i_string == None:
                print "there is no script_i_string......"
            else:
                if "follow_list" in script_i_string:
                    follow_content = script_i_string
                    follow_str = follow_content.replace("FM.view(", "")[:-1]
                    follow_json = json.loads(follow_str)
                    follow_content = follow_json["html"]
                    follow_soup = BeautifulSoup(follow_content, 'html.parser')
                    fans_ul = follow_soup.find("ul", class_ = "follow_list")
                    if fans_ul == None:
                        print "there is no fans ul tag"
                    else:
                        fans_li_list = fans_ul.find_all("li", class_ = "follow_item S_line2")
                        if len(fans_li_list) == 0:
                            print "there is no fans_li_list......"
                        else:
                            for li in fans_li_list:
                                fans_li_a = li.find("a" , target = "_blank")
                                if fans_li_a == None:
                                    print "there is no fans li a"
                                else:
                                    fans_url = fans_li_a.get("href")
                                    if fans_ul == None:
                                        print "fans url is none"
                                    else:
                                        fans_url = "http://weibo.com" + fans_url
                                        fans_url_list.append(fans_url)
                    break
    return fans_url_list


# def iterator(personal_url, num = 0):
#     feature_list = get_feautres_list(personal_url)
#     insert_feature_to_database(feature_list)
#     fans_page_url = get_fans_page_url(personal_url)
#     print "fans page url...", fans_page_url
#     fans_url_list = get_fans_detail_url_list(fans_page_url)
#     for url in fans_url_list:
#         print url
#         if num <= 10:
#             num += 1
#             iterator(url, num)

def get_qian(url):
    soup = setupSoup(url, fans_page_headers)
    print soup

def get_next_weibo_page_url(url):
    next_weibo_page_url = ""
    if url == "":
        print "the weibo next url is blank in get all pages url"
    else:
        browser = WebBrowser(debug=False)
        content, rep_header = browser._request(url, headers=fans_page_headers)
        content_json = json.loads(content)
        print content_json["data"]
        # script_tags = soup.find_all("script")
        # script_page = script_tags[-1].string.replace("FM.view(", "")[:-1]
        # page_json = json.loads(script_page)
        # print page_json["html"]
    return next_weibo_page_url

def get_next_pages_url(url):
    next_page_url = ""
    if url == "":
        print "the url is blank in get all pages url"
    else:
        soup = setupSoup(url, fans_detail_headers)
        script_tags = soup.find_all("script")
        for script_i in script_tags:
            script_i_string = script_i.string
            if script_i_string == None:
                print "there is no script i string in get all pages url"
            else:
                if "下一页" in script_i_string:
                    page_content = script_i_string
                    page_str = page_content.replace("FM.view(", "")[:-1]
                    page_json = json.loads(page_str)
                    page_content = page_json["html"]
                    page_soup = BeautifulSoup(page_content, 'html.parser')
                    page_tag = page_soup.find("a", class_ = "page next S_txt1 S_line1")
                    if page_tag == None:
                        print "there is no page tag in get all pages......"
                    else:
                        next_page_url = page_tag.get("href")
                        if next_page_url == None:
                            next_page_url = ""
                            print "there is no next page url"
                        else:
                            next_page_url = "http://weibo.com" + next_page_url
                    break
    return next_page_url

def get_all_pages_url(url):
    all_page_url_list = []
    all_page_url_list.append(url)
    next_page_url = get_next_pages_url(url)
    while next_page_url != "":
        all_page_url_list.append(next_page_url)
        next_page_url = get_next_pages_url(next_page_url)
    return all_page_url_list[:-1]





if __name__ == "__main__":
    url = "http://weibo.com/u/6026653677?refer_flag=1005050005_"
    url_all_pages = "http://weibo.com/p/1005055923855286/follow?relate=fans&from=100505&wvr=6&mod=headfans&current=fans#place"
    url_yinjiaoshou = "http://weibo.com/234535428?refer_flag=1005055013_&is_all=1"
    url_shenyucong = "http://weibo.com/3006812112"
    url_yinjiaoshou3 = "http://weibo.com/234535428?is_search=0&visible=0&is_all=1&is_tag=0&profile_ftype=1&page=3#feedtop"
    url_yinjiaoshou_all = "http://weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=103505&from=myfollow_all&is_all=1&pagebar=1&pl_name=Pl_Official_MyProfileFeed__23&id=1035051098618600&script_uri=/234535428&feed_type=0&page=1&pre_page=1&domain_op=103505&__rnd=1499754639479"
    qiexiang_page2_qian = "http://weibo.com/u/5391323887"
    qiexiang_page2_zhong = ""
    qiexiang_page2_hou = ""
    get_qian(qiexiang_page2_qian)
    # get_next_weibo_page_url(qiexiang_page2_qian)


    # get_feautres_list(url_shenyucong)
    # iterator(url_shenyucong)
    # feature_list = get_feautres_list(url_yinjiaoshou3)
    # insert_feature_to_database(feature_list)
    # print get_next_pages_url(url_yinjiaoshou)

    # feature_list = get_feautres_list(url_yinjiaoshou)
    # for i in feature_list:
    #     print i["uid"]


    # all_pages_url_list = get_all_pages_url(url_all_pages)
    # for url in all_pages_url_list:
    #     print url

    # iterator(url)

    # url = "http://weibo.com/u/3006812112"
    # fans_page_url = get_fans_page_url(url)
    # print fans_page_url

    url_cong = "http://weibo.com/u/3006812112"
    fans_page_url = get_fans_page_url(url_cong)
    fans_url_list = get_fans_detail_url_list(fans_page_url)
    for url in fans_url_list:
        print url
    #     fans_page_url2 = get_fans_page_url(url)
    #     print "fans_page_url2...",fans_page_url2
    #     fans_url_list2 = get_fans_detail_url_list(fans_page_url2)
    #     for url2 in fans_url_list2:
    #         print url2

    # iterator(url_cong)