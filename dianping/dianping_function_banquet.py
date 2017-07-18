# !/usr/bin/python
# -*- coding: UTF-8 -*-
from util import setupSoup
from util import set_blank_features
from util import delete_file
from util import write_features_to_file
# 返回值是一个二维的字典数组，每一行代表一个大分类
# 输入的参数url是一个城市的url
# url_beijing = "https://www.dianping.com/beijing"

def get_banquet_features(url, retry = 0):
    features=set_blank_features()
    soup=setupSoup(url)
    #解析标题
    title_tag=soup.find("h1")
    if title_tag == None:
        title_tag=soup.find("h2")
        if title_tag == None:
            print "there is no title_div_class tag in get_banquet_features"
            if retry <= 2:
                retry += 1
                features = get_banquet_features(url, retry)
        else:
            str=title_tag.string
            if str != None:
                features["title"] = str.replace("\n", "").replace(" ", "")
    else:
        if title_tag.string != None:
            features["title"]=title_tag.string.replace("\n", "").replace(" ", "")
    #解析地址
    address_tag=soup.find_all("span", class_="info-name")
    if len(address_tag) == 0:
        address_tag=soup.find_all("span", class_="info-con detail-info mr15")
        if len(address_tag) == 0:
            print "there is no hotel-address in get_banquet_features"
        else:
            address_tag=address_tag[0]
            if address_tag.string != None:
                features["address"] = address_tag.string.replace(" ", "").replace("\n", "")
    else:
        address_tag=address_tag[0]
        if address_tag.string != None:
            features["address"] = address_tag.string.replace(" ", "").replace("\n", "")
    #解析评分和星级
    start_tag=soup.find_all("span", class_="mid-rank-stars")
    if len(start_tag) == 0:
        start_tag=soup.find_all(class_="big-star")
        if len(start_tag) == 0:
            print "there is no start class in get_banquet_features"
        else:
            start_tag=start_tag[0]
            star_str = start_tag.get("title")
            if star_str != None:
                features["rank_stars"] = star_str
    else:
       start_tag=start_tag[0]
       star_str=start_tag.get("title")
       if star_str != None:
           features["rank_stars"]=star_str
    #解析id
    url_array=url.split("/")[-1].split("?")
    features["id"]=url_array[0]
    return features


#得到朝阳区，海淀区等分区
def get_banquet_all_region_url_list(url):
    region_url_list = []
    region_dic = {}
    region_dic["name"] = "朝阳区"
    region_dic["href"] = "https://www.dianping.com/search/category/2/40?regionId=14"
    region_url_list.append(region_dic)
    region_dic = {}
    region_dic["name"] = "东城区"
    region_dic["href"] = "https://www.dianping.com/search/category/2/40?regionId=15"
    region_url_list.append(region_dic)
    region_dic = {}
    region_dic["name"] = "西城区"
    region_dic["href"] = "https://www.dianping.com/search/category/2/40?regionId=16"
    region_url_list.append(region_dic)
    region_dic = {}
    region_dic["name"] = "海淀区"
    region_dic["href"] = "https://www.dianping.com/search/category/2/40?regionId=17"
    region_url_list.append(region_dic)
    region_dic = {}
    region_dic["name"] = "丰台区"
    region_dic["href"] = "https://www.dianping.com/search/category/2/40?regionId=20"
    region_url_list.append(region_dic)
    region_dic = {}
    region_dic["name"] = "石景山区"
    region_dic["href"] = "https://www.dianping.com/search/category/2/40?regionId=328"
    region_url_list.append(region_dic)
    region_dic = {}
    region_dic["name"] = "昌平区"
    region_dic["href"] = "https://www.dianping.com/search/category/2/40?regionId=5950"
    region_url_list.append(region_dic)
    region_dic = {}
    region_dic["name"] = "通州区"
    region_dic["href"] = "https://www.dianping.com/search/category/2/40?regionId=5951"
    region_url_list.append(region_dic)
    region_dic = {}
    region_dic["name"] = "大兴区"
    region_dic["href"] = "https://www.dianping.com/search/category/2/40?regionId=5952"
    region_url_list.append(region_dic)
    region_dic = {}
    region_dic["name"] = "房山区"
    region_dic["href"] = "https://www.dianping.com/search/category/2/40?regionId=9157"
    region_url_list.append(region_dic)
    region_dic = {}
    region_dic["name"] = "顺义区"
    region_dic["href"] = "https://www.dianping.com/search/category/2/40?regionId=9158"
    region_url_list.append(region_dic)
    region_dic = {}
    region_dic["name"] = "门头沟区"
    region_dic["href"] = "https://www.dianping.com/search/category/2/40?regionId=27614"
    region_url_list.append(region_dic)
    region_dic = {}
    region_dic["name"] = "怀柔区"
    region_dic["href"] = "https://www.dianping.com/search/category/2/40?regionId=27615"
    region_url_list.append(region_dic)
    region_dic = {}
    region_dic["name"] = "平谷区"
    region_dic["href"] = "https://www.dianping.com/search/category/2/40?regionId=27616"
    region_url_list.append(region_dic)
    return region_url_list


#得到某一页所有url列表
def get_banquet_detail_url_list(url):
    detail_url_list=[]
    soup=setupSoup(url)
    class_shop=soup.find_all("a", class_="shop-link clearfix")
    if len(class_shop) == 0:
        print "there is no class_pic tag in get banquet detail url list"
    else:
        for a_tag in class_shop:
            href=a_tag.get("href")
            if href != None:
                href="https://www.dianping.com"+href
                detail_url_list.append(href)
    return detail_url_list


#得到下一页的url
def get_banquet_next_page_url(url):
    next_page_url=""
    soup = setupSoup(url)
    next_tag = soup.find_all(class_="pages-link")
    if len(next_tag) > 0:
        next_tag=next_tag[-1]
        href=next_tag.get("href")
        if href != None:
            try:
                index=href.index("/search")
                href=href[index:]
                next_page_url="https://www.dianping.com"+href
            except:
                next_page_url=""
    return next_page_url

#只得到当前传入url的后面的页数，因此传参要传入第一页url
def get_banquet_all_page_url(url):
    all_page_url_list=[]
    all_page_url_list.append(url)
    next_url=get_banquet_next_page_url(url)
    while len(next_url) != 0:
        all_page_url_list.append(next_url)
        next_url=get_banquet_next_page_url(next_url)
    return all_page_url_list

#传入一个url，得到这个url的所有页，和所有详情,并写入文件
def get_banquet_all_pages_features(url, filename):
    new_filename=filename.replace("/", "&")
    print new_filename
    primary_category_name=""
    secondary_category_name=""
    region_name=""
    category_and_region=filename.split("-")
    if len(category_and_region) == 3:
        primary_category_name=category_and_region[0]
        secondary_category_name=category_and_region[1]
        region_name=category_and_region[2][:-4]
    else:
        print "filename error....."
    delete_file(new_filename)
    all_page_url_list = get_banquet_all_page_url(url)
    if len(all_page_url_list) > 0:
        for one_page_url in all_page_url_list:
            print "one_page_url...", one_page_url
            detail_list = get_banquet_detail_url_list(one_page_url)
            if len(detail_list) > 0:
                for features_url in detail_list:
                    print "detail_url...", features_url
                    features = get_banquet_features(features_url)
                    features["primary_category"]=primary_category_name
                    features["secondary_category"]=secondary_category_name
                    features["region"]=region_name
                    features["detail_url"]=features_url
                    write_features_to_file(features,new_filename)
                print "\n"

# 得到某一个分类的全部features
def get_banquet_all_category_features(url, filename):
    new_filename=filename
    all_region_list = get_banquet_all_region_url_list(url)
    if len(all_region_list) > 0:
        for region in all_region_list:
            print "one_region_url...", region["name"], ":", region["href"]
            filename=new_filename+"-"+region["name"]+".txt"
            get_banquet_all_pages_features(region["href"], filename)

# 得到某一个二级分类的全部url
def get_banquet_all_category_url(url, filename, r):
    new_filename = filename
    all_region_list = get_banquet_all_region_url_list(url)
    if len(all_region_list) > 0:
        for region in all_region_list:
            print "one_region_url...", region["name"], ":", region["href"]
            filename = new_filename + "-" + region["name"]
            all_page_url_list = get_banquet_all_page_url(region["href"])
            if len(all_page_url_list) > 0:
                for one_page_url in all_page_url_list:
                    print "one_page_url...", one_page_url
                    detail_list = get_banquet_detail_url_list(one_page_url)
                    if len(detail_list) > 0:
                        for features_url in detail_list:
                            print "detail_url...", features_url
                            result_url=filename + "**" + features_url
                            r.lpush("dian_ping", result_url)
                        print "\n"


if __name__ == "__main__":
    url_hotel_features="https://www.dianping.com/newhotel/2534212"
    url_hotel_features2="https://www.dianping.com/newhotel/8916000"
    url_one_category="https://www.dianping.com/beijing/hotel/"
    url_test_get_detail_url_list="https://www.dianping.com/beijing/hotel/c6946r0"
    url_test_get_hotel_all_category_features="https://www.dianping.com/beijing/hotel/g3024n10"

    list=get_banquet_all_region_url_list("http://www.dianping.com/search/category/2/40")
    for i in list:
        print i
    # get_banquet_all_page_url("https://www.dianping.com/search/category/2/40/g3014?regionId=14")

    # get_banquet_all_region_url_list("https://www.dianping.com/search/category/2/40")
    # get_banquet_detail_url_list("https://www.dianping.com/search/category/2/40/g3014?regionId=14")

    # features=get_banquet_features("https://www.dianping.com/shop/22152524?siteuse=0")
    # print features["title"]
    # print features["id"]
    # print features["rank_stars"]
    # print features["address"]