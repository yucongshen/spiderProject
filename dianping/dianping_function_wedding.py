# !/usr/bin/python
# -*- coding: UTF-8 -*-
from util import print_list
from util import setupSoup
from util import set_blank_features
from util import write_features_to_file
from util import delete_file
# 返回值是一个二维的字典数组，每一行代表一个大分类
# 输入的参数url是一个城市的url
# url_beijing = "https://www.dianping.com/beijing"

#得到详情页面的各个poi特征
def get_wedding_features(url, retry = 0):
    features=set_blank_features()
    soup=setupSoup(url)
    #解析标题
    title_tag=soup.find_all("h1", class_ = "shop-title")
    if len(title_tag) == 0:
        print "there is no title_div_class tag in get_features"
        if retry <= 2:
            retry += 1
            features = get_wedding_features(url, retry)
    else:
        title_tag=title_tag[0]
        features["title"]=title_tag.string.replace("\n", "").replace(" ", "")

    #解析星级
    star_span=soup.find_all(class_="item-rank-rst")
    if len(star_span) == 0:
        print "there is no star_span in get_features"
    else:
        star_span=star_span[0]
        features["rank_stars"]=star_span.get("title").replace("\n", "").replace(" ", "")
    avg_price=soup.find_all(class_="average")
    if len(avg_price) == 0:
        avg_price_div=soup.find_all(class_="comment-rst")
        if len(avg_price_div) == 0:
            print "there is no comment-rst in get_features"
        else:
            avg_price_div=avg_price_div[0]
            avg_price=avg_price_div.find_all("dd")
            if len(avg_price) ==0:
                print "there is no avg_price in get_features"
            else:
                avg_price=avg_price[0]
                # if isinstance(avg_price.contents[1], str):
                features["avg_price"] =avg_price.contents[1].string
                # else:
                #     features["avg_price"]=""
    else:
        avg_price=avg_price[0]
        features["avg_price"]=avg_price.string
    #解析地址
    address_tag=soup.find_all(class_="fl road-addr")
    if len(address_tag) == 0:
        address_tag=soup.find_all(itemprop="street-address")
        if len(address_tag) == 0:
            print "there is no address_tag in get_wedding_features"
        else:
            address_tag=address_tag[0]
            address_str=address_tag.string
            if address_str != None:
                features["address"]=address_str.replace(" ", "").replace("\n", "")
    else:
        address_tag=address_tag[0]
        address=address_tag.contents[2]
        if address == None:
            address=""
        features["address"]=address.replace(" ", "").replace("\n", "")
    #解析id,没有经纬度
    features["id"]=url[url.index("shop/")+len("shop/"):]
    if "?" in features["id"]:
        features["id"]=features["id"][:features["id"].index("?")]
    return features

#得到朝阳区，海淀区等分区
def get_wedding_all_region_url_list(url):
    region_list=[]
    soup=setupSoup(url)
    class_t_list_tag=soup.find_all(class_="t-list")
    if len(class_t_list_tag) == 0:
        print "there is no class_=t-list tag in get_wedding_region_url_list"
    else:
        if len(class_t_list_tag) >= 2:
            class_t_list_tag=class_t_list_tag[1]
        else:
            class_t_list_tag=class_t_list_tag[0]

        ul_region_tag=class_t_list_tag.find_all("ul")
        if len(ul_region_tag) == 0:
            print "there is no ul region tag in get_wedding_region_url_list"
        else:
            ul_region_tag=ul_region_tag[0]
            a_region_tag=ul_region_tag.find_all("a")
            if len(a_region_tag) == 0:
                print "there is no a_region_tag"
            else:
                for region in a_region_tag:
                    region_dic={}
                    region_dic["name"]=""
                    region_dic["href"]=""
                    if len(region.contents) >= 3:
                        region_name=region.contents[2]
                    else:
                        region_name=region.contents[0]
                    # print region_name
                    region_url="https://www.dianping.com"+region.get("href")
                    if region_name == None:
                        print "region_name is none"
                        region_dic["name"]=""
                    else:
                        region_dic["name"] = region_name.replace("\n", "").replace(" ", "")
                        arrays = region_dic["name"].split("区")
                        region_dic["name"] = arrays[0] + "区"
                    if region_url == None:
                        region_dic["href"]=""
                    else:
                        region_dic["href"]=region_url
                    region_list.append(region_dic)
    return region_list

#得到朝阳区等区的分区
def get_wedding_all_sub_region_url_list(url):
    sub_region_list = []
    soup = setupSoup(url)
    class_t_list_tag = soup.find_all(class_="t-list")
    if len(class_t_list_tag) == 0:
        print "there is no class_=t-list tag in get_wedding_region_url_list"
    else:
        if len(class_t_list_tag) == 2:
            class_t_list_tag = class_t_list_tag[1]
        else:
            class_t_list_tag = class_t_list_tag[0]

        ul_region_tag = class_t_list_tag.find_all("ul")
        if len(ul_region_tag) == 0:
            print "there is no ul region tag in get_wedding_region_url_list"
        else:
            ul_region_tag = ul_region_tag[0]
            a_region_tag = ul_region_tag.find_all("a")
            if len(a_region_tag) == 0:
                print "there is no a_region_tag"
            else:
                for region in a_region_tag:
                    region_dic = {}
                    region_dic["name"] = ""
                    region_dic["href"] = ""
                    region_name = region.contents[0]
                    # print region_name
                    region_url = "https://www.dianping.com" + region.get("href")
                    if region_name == None:
                        region_dic["name"] = ""
                    else:
                        region_dic["name"] = region_name.replace("\n", "").replace(" ", "")
                    if region_url == None:
                        region_dic["href"] = ""
                    else:
                        region_dic["href"] = region_url
                        sub_region_list.append(region_dic)
    return sub_region_list

#得到某一页所有url列表
def get_wedding_detail_url_list(url):
    detail_url_list=[]
    soup=setupSoup(url)
    ul_shop_list=soup.find_all("ul", class_="shop-list")
    if len(ul_shop_list) == 0:
        print "there is no ul_shop_list tag in get_wedding_detail_url_list"
    else:
        ul_shop_list=ul_shop_list[0]
        li_shop_name=ul_shop_list.find_all("li")
        if len(li_shop_name) == 0:
            print "there is no li_shop_name in get_wedding_detail_url_list"
        else:
            for li in li_shop_name:
                a_tag=li.find("a")
                if a_tag == None:
                    print "there is no a_tag in get_wedding_detail_url_list"
                else:
                    detail_url=a_tag.get("href")
                    if detail_url != None:
                        detail_url="https://www.dianping.com"+detail_url
                        detail_url_list.append(detail_url)
    return detail_url_list

#得到下一页的url
def get_wedding_next_page_url(url):
    next_page_url=""
    soup = setupSoup(url)
    next_tag = soup.find_all(class_="NextPage")
    if len(next_tag) > 0:
        next_tag=next_tag[0]
        next_page_url="https://www.dianping.com"+next_tag.get("href")
    return next_page_url

#只得到当前传入url的后面的页数，因此传参要传入第一页url
def get_wedding_all_page_url(url):
    all_page_url_list=[]
    all_page_url_list.append(url)
    next_url=get_wedding_next_page_url(url)
    while len(next_url) != 0:
        all_page_url_list.append(next_url)
        next_url=get_wedding_next_page_url(next_url)
    return all_page_url_list

#传入一个url，得到这个url的所有页，和所有详情,并写入文件
def get_wedding_all_pages_features(url, filename):
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
    all_page_url_list = get_wedding_all_page_url(url)
    if len(all_page_url_list) > 0:
        for one_page_url in all_page_url_list:
            print "one_page_url...", one_page_url
            detail_list = get_wedding_detail_url_list(one_page_url)
            if len(detail_list) > 0:
                for features_url in detail_list:
                    print "detail_url...", features_url
                    features = get_wedding_features(features_url)
                    features["primary_category"]=primary_category_name
                    features["secondary_category"]=secondary_category_name
                    features["region"]=region_name
                    features["sub_region"]=sub_region_name
                    features["detail_url"]=features_url
                    write_features_to_file(features,new_filename)
                print "\n"

# 得到某一个分类的全部features
def get_wedding_category_features(url, filename):
    new_filename=filename
    all_region_list = get_wedding_all_region_url_list(url)
    if len(all_region_list) > 0:
        for region in all_region_list:
            print ("one_region_url..."+region["name"]+":"+ region["href"])
            all_sub_region_list = get_wedding_all_sub_region_url_list(region["href"])
            if len(all_sub_region_list) > 0:
                for sub_region in all_sub_region_list:
                    print "one_sub_region_url...", sub_region["name"], ":", sub_region["href"]
                    filename=new_filename+"-"+ region["name"]+"-"+sub_region["name"]+".txt"
                    get_wedding_all_pages_features(sub_region["href"], filename)

# 得到某一个二级分类的全部url
def get_wedding_all_category_url(url, filename, r):
    new_filename = filename
    all_region_list = get_wedding_all_region_url_list(url)
    if len(all_region_list) > 0:
        for region in all_region_list:
            print "one_region_url...", region["name"], ":", region["href"]
            all_sub_region_list = get_wedding_all_sub_region_url_list(region["href"])
            if len(all_sub_region_list) > 0:
                for sub_region in all_sub_region_list:
                    print "one_sub_region_url...", sub_region["name"], ":", sub_region["href"]
                    filename = new_filename + "-" + region["name"] + "-" + sub_region["name"]
                    all_page_url_list = get_wedding_all_page_url(sub_region["href"])
                    if len(all_page_url_list) > 0:
                        for one_page_url in all_page_url_list:
                            print "one_page_url...", one_page_url
                            detail_list = get_wedding_detail_url_list(one_page_url)
                            if len(detail_list) > 0:
                                for features_url in detail_list:
                                    print "detail_url...", features_url
                                    result_url = filename + "**" + features_url
                                    r.lpush("dian_ping", result_url)
                                print "\n"


if __name__ == "__main__":
    url_features="https://www.dianping.com/shop/4194652"
    url_get_wedding_region_url_list="https://www.dianping.com/search/category/2/55/g192"
    url_get_wedding_sub_region_url_list="https://www.dianping.com/search/category/2/55/g164r16"
    url_get_wedding_detail_url_list="https://www.dianping.com/search/category/2/55/g163"
    url_wedding="https://www.dianping.com/search/category/2/55/g163"
    # get_wedding_features("https://www.dianping.com/shop/83108582")
    # get_wedding_all_region_url_list("http://www.dianping.com/wedding/hunyan?cityId=2")
    # get_wedding_all_sub_region_url_list(url_get_wedding_sub_region_url_list)
    # get_wedding_all_region_url_list(url_get_wedding_region_url_list)
    # get_wedding_detail_url_list(url_get_wedding_detail_url_list)
    # get_wedding_next_page_url(url_get_wedding_detail_url_list)
    # get_wedding_all_page_url(url_get_wedding_detail_url_list)

    # features=get_wedding_features("https://www.dianping.com/shop/14887470")
    # features = get_wedding_features("https://www.dianping.com/shop/6184158")
    # print features["avg_price"]
    # print features["title"]


    filename="结婚频道-婚纱摄影"
    get_wedding_category_features("https://www.dianping.com/search/category/2/55/g163", filename)