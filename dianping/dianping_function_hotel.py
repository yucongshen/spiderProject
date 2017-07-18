# !/usr/bin/python
# -*- coding: UTF-8 -*-
from util import setupSoup
from util import set_blank_features
from util import delete_file
from util import write_features_to_file
# 返回值是一个二维的字典数组，每一行代表一个大分类
# 输入的参数url是一个城市的url
# url_beijing = "https://www.dianping.com/beijing"

def get_hotel_features(url, retry = 0):
    features=set_blank_features()
    soup=setupSoup(url)
    #解析标题
    title_tag=soup.find("h1")
    if title_tag == None:
        print "there is no title_div_class tag in get_hotel_features"
        if retry <= 2:
            retry += 1
            features = get_hotel_features(url, retry)
    else:
        if title_tag.string != None:
            features["title"]=title_tag.string.replace("\n", "").replace(" ", "")
    #解析地址
    address_tag=soup.find_all(class_="hotel-address")
    if len(address_tag) == 0:
        print "there is no hotel-address in get_hotel_features"
    else:
        address_tag=address_tag[0]
        if address_tag.string != None:
            features["address"] = address_tag.string
    #解析评分和星级
    start_tag=soup.find_all(class_="score")
    if len(start_tag) == 0:
        print "there is no score class in get_hotel_features"
    else:
       start_tag=start_tag[0]
       if start_tag.string != None:
           features["rank_stars"]=start_tag.string
    #解析id
    url_array=url.split("/")
    features["id"]=url_array[-1]
    #解析经纬度
    script_tags=soup.find_all("script")
    if len(script_tags) == 0:
        print "there is no script in get_features"
    else:
        for script in script_tags:
            script_str = script.string
            if script_str !=None:
                if "basicInfo" in script_str:
                    script_arrs=script_str.split(",")
                    for script_arr in script_arrs:
                        if "\"lat\"" in script_arr:
                            lat_arr=script_arr.split(":")
                            if len(lat_arr) == 2:
                                features["lat"]=lat_arr[1]
                        if "\"lng\"" in script_arr:
                            lng_arr=script_arr.split(":")
                            if len(lng_arr) == 2:
                                features["lon"]=lng_arr[1]
                    break
    return features


#得到朝阳区，海淀区等分区
def get_hotel_all_region_url_list(url):
    region_url_list=[]
    soup=setupSoup(url)
    region_tag=soup.find_all(class_="nav-2nd J_choice-trigger-wrap-downtown")
    if len(region_tag) == 0:
        print "there is no id=region_nav tag in get_hotel_region_url_list"
    else:
        region_tag=region_tag[0]
        regions=region_tag.find_all("a")
        if len(regions) == 0:
            print "there is no regions tag"
        else:
            for region in regions:
                region_dic={}
                region_name=region.string
                region_url=region.get("href")
                if region_name != None:
                    region_dic["name"]=region_name
                if region_url != None:
                    region_dic["href"]="https://www.dianping.com"+region_url
                region_url_list.append(region_dic)
    return region_url_list

#得到朝阳区等区的分区
def get_hotel_all_sub_region_url_list(url):
    sub_region_url_list=[]
    soup=setupSoup(url)
    region_nav_sub=soup.find_all(class_="recom J_choice-content-2nd ")
    if len(region_nav_sub) == 0:
        print "there is no region_nav_sub in get_hotel_all_sub_region_url_list"
    else:
        region_nav_sub=region_nav_sub[0]
        sub_regions=region_nav_sub.find_all("a")
        if len(sub_regions) == 0:
            print "there is no sub_regions_a_tag"
        else:
            for i in range(1,len(sub_regions)):
                sub_region_dic={}
                sub_region_dic["name"]=sub_regions[i].string
                sub_region_dic["href"]="https://www.dianping.com"+sub_regions[i].get("href")
                sub_region_url_list.append(sub_region_dic)
    return sub_region_url_list


#得到某一页所有url列表
def get_hotel_detail_url_list(url):
    detail_url_list=[]
    soup=setupSoup(url)
    class_hotel=soup.find_all("h2", class_="hotel-name")
    if len(class_hotel) == 0:
        print "there is no class_pic tag in hotel features"
    else:
        for pic in class_hotel:
            a_tag=pic.find_all("a")
            if len(a_tag) == 0:
                print "there is no a_tag find in pic class"
            else:
                a_tag=a_tag[0]
                href=a_tag.get("href")
                if href != None:
                    href="https://www.dianping.com"+href
                    detail_url_list.append(href)
    return detail_url_list


#得到下一页的url
def get_hotel_next_page_url(url):
    next_page_url=""
    soup = setupSoup(url)
    next_tag = soup.find_all(class_="next")
    if len(next_tag) > 0:
        next_tag=next_tag[0]
        href=next_tag.get("href")
        if href != None:
            next_page_url="https://www.dianping.com"+href
    return next_page_url

#只得到当前传入url的后面的页数，因此传参要传入第一页url
def get_hotel_all_page_url(url):
    all_page_url_list=[]
    all_page_url_list.append(url)
    next_url=get_hotel_next_page_url(url)
    while len(next_url) != 0:
        all_page_url_list.append(next_url)
        next_url=get_hotel_next_page_url(next_url)
    return all_page_url_list

#传入一个url，得到这个url的所有页，和所有详情,并写入文件
def get_hotel_all_pages_features(url, filename):
    new_filename=filename.replace("/", "&")
    print new_filename
    primary_category_name=""
    secondary_category_name=""
    region_name=""
    sub_region_name=""
    category_and_region=filename.split("-")
    if len(category_and_region) == 4:
        primary_category_name=category_and_region[0]
        secondary_category_name=category_and_region[1]
        region_name=category_and_region[2]
        sub_region_name=category_and_region[3][:-4]
    else:
        print "filename error....."
    delete_file(new_filename)
    all_page_url_list = get_hotel_all_page_url(url)
    if len(all_page_url_list) > 0:
        for one_page_url in all_page_url_list:
            print "one_page_url...", one_page_url
            detail_list = get_hotel_detail_url_list(one_page_url)
            if len(detail_list) > 0:
                for features_url in detail_list:
                    print "detail_url...", features_url
                    features = get_hotel_features(features_url)
                    features["primary_category"]=primary_category_name
                    features["secondary_category"]=secondary_category_name
                    features["region"]=region_name
                    features["sub_region"]=sub_region_name
                    features["detail_url"]=features_url
                    write_features_to_file(features,new_filename)
                print "\n"

# 得到某一个分类的全部features
def get_hotel_all_category_features(url, filename):
    new_filename=filename
    all_region_list = get_hotel_all_region_url_list(url)
    if len(all_region_list) > 0:
        for region in all_region_list:
            print "one_region_url...", region["name"],":", region["href"]
            all_sub_region_list = get_hotel_all_sub_region_url_list(region["href"])
            if len(all_sub_region_list) > 0:
                for sub_region in all_sub_region_list:
                    print "one_sub_region_url...", sub_region["name"], ":", sub_region["href"]
                    filename=new_filename+"-"+region["name"]+"-"+sub_region["name"]+".txt"
                    get_hotel_all_pages_features(sub_region["href"], filename)

# 得到某一个二级分类的全部url
def get_hotel_all_category_url(url, filename, r):
    new_filename = filename
    all_region_list = get_hotel_all_region_url_list(url)
    if len(all_region_list) > 0:
        for region in all_region_list:
            print "one_region_url...", region["name"], ":", region["href"]
            all_sub_region_list = get_hotel_all_sub_region_url_list(region["href"])
            if len(all_sub_region_list) > 0:
                for sub_region in all_sub_region_list:
                    print "one_sub_region_url...", sub_region["name"], ":", sub_region["href"]
                    filename = new_filename + "-" + region["name"] + "-" + sub_region["name"]
                    all_page_url_list = get_hotel_all_page_url(sub_region["href"])
                    if len(all_page_url_list) > 0:
                        for one_page_url in all_page_url_list:
                            print "one_page_url...", one_page_url
                            detail_list = get_hotel_detail_url_list(one_page_url)
                            if len(detail_list) > 0:
                                for features_url in detail_list:
                                    print "detail_url...", features_url
                                    result_url = filename + "**" + features_url
                                    r.lpush("dian_ping", result_url)
                                print "\n"



if __name__ == "__main__":
    url_hotel_features="https://www.dianping.com/newhotel/2534212"
    url_hotel_features2="https://www.dianping.com/newhotel/8916000"
    url_one_category="https://www.dianping.com/beijing/hotel/"
    url_test_sub_region_chaoyang="https://www.dianping.com/beijing/hotel/r14c226"
    url_test_sub_region_miyunqu="https://www.dianping.com/beijing/hotel/c6946r0"
    url_test_get_detail_url_list="https://www.dianping.com/beijing/hotel/c6946r0"
    url_test_get_hotel_all_category_features="https://www.dianping.com/beijing/hotel/g3024n10"
    # get_hotel_features(url_hotel_features2)
    # get_hotel_all_region_url_list(url_one_category)
    # get_hotel_all_sub_region_url_list(url_test_sub_region_chaoyang)
    # get_hotel_detail_url_list(url_test_get_detail_url_list)
    # get_hotel_all_page_url(url_test_get_detail_url_list)
    # get_hotel_all_category_features(url_test_get_hotel_all_category_features, "酒店频道-三星级&舒适型")
    features=get_hotel_features("https://www.dianping.com/newhotel/2900890")
    print features["title"]
    print features["id"]
    print features["rank_stars"]
    print features["address"]
    print features["lat"]
    print features["lon"]