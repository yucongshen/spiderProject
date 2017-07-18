# !/usr/bin/python
# -*- coding: UTF-8 -*-
from util import print_list
from util import setupSoup
from util import set_blank_features
from dianping_function_wedding import get_wedding_all_region_url_list
from util import delete_file
from util import write_features_to_file
# 返回值是一个二维的字典数组，每一行代表一个大分类
# 输入的参数url是一个城市的url
# url_beijing = "https://www.dianping.com/beijing"

def get_decoration_features(url, retry = 0):
    features=set_blank_features()
    soup=setupSoup(url)
    #解析标题
    title_tag=soup.find("h1", class_ = 'shop-title')
    if title_tag == None:
        print "there is no title_div_class tag in get_decoration_features"
        if retry <= 2:
            retry += 1
            features = get_decoration_features(url, retry)
    else:
        title_str=title_tag.string
        if title_str != None:
            features["title"]=title_str.replace("\n", "").replace(" ", "")
    #解析星级
    star_span=soup.find_all("span", class_="dp-star-md")
    if len(star_span) == 0:
        star_span=soup.find_all(class_="comment-rst")
        if len(star_span) == 0:
            print "there is no comment-rst in get decoration features"
        else:
            star_span=star_span[0]
            star_content=star_span.find_all(class_="item-rank-rst")
            if len(star_content) == 0:
                print "there is no star content in get decoration features"
            else:
                star_content=star_content[0]
                star_str=star_content.contents[1].string
                if star_str != None:
                    features["rank_stars"]=star_str.replace(" ", "").replace("\n", "")
    else:
        star_span=star_span[0]
        star_str=star_span.get("title")
        if star_str != None:
            features["rank_stars"]=star_str.replace(" ", "").replace("\n", "")
    #解析均价
    avg_price=soup.find_all("span", class_="avg-price")
    if len(avg_price) == 0:
        avg_price=soup.find_all(class_="Price")
        if len(avg_price) == 0:
            print "there is no price in get decoration features"
        else:
            avg_price=avg_price[0]
            dd=avg_price.parent
            if dd != None:
                str=dd.contents[1]
                if str != None:
                    features["avg_price"]=str
    else:
        avg_price=avg_price[0]
        price=avg_price.string
        if price != None:
            features["avg_price"]=price
    #解析地址
    address_div=soup.find_all("p", class_="shop-contact address")
    if len(address_div) == 0:
        address_div=soup.find_all(itemprop="street-address")
        if len(address_div) == 0:
            print "there is no street-address div in get decoration features"
        else:
            address_div=address_div[0]
            address_str=address_div.string
            if address_str != None:
                features["address"]=address_str
    else:
        address_div=address_div[0]
        address_str=address_div.contents[4]
        if address_str != None:
            try:
                features["address"]=address_str.replace(" ", "").replace("\n", "")
            except :
                address_str=address_div.contents[3]
                if address_str != None:
                    features["address"]=address_str.replace(" ", "").replace("\n", "")
    #解析id
    features["id"] = url[url.index("shop/") + len("shop/"):]
    if "?" in features["id"]:
        features["id"] = features["id"][:features["id"].index("?")]
    return features

#得到朝阳区，海淀区等分区
def get_decoration_all_region_url_list(url):
    region_list = []
    soup = setupSoup(url)
    region_box_tag=soup.find_all(class_="row")
    ul_region_tag=""
    if len(region_box_tag) == 0:
        region_box_tag = soup.find_all(class_="type")
        if len(region_box_tag) == 0:
            print "there is no class type in get decoration class"
        else:
            region_box_tag = region_box_tag[-1]
            ul_region_tag = region_box_tag.find_all("ul")
            if len(ul_region_tag) == 0:
                print "there is no ul find in type class"
    else:
        region_box_tag=region_box_tag[2]
        ul_region_tag = region_box_tag.find_all("ul")
        if len(ul_region_tag) == 0:
            region_box_tag=soup.find_all(class_="type")
            if len(region_box_tag) == 0  :
                print "there is no class type in get decoration class ul"
            else:
                region_box_tag=region_box_tag[-1]
                ul_region_tag = region_box_tag.find_all("ul")
                if len(ul_region_tag) == 0:
                    print "there is no ul find in type class"
    if len(ul_region_tag) >0 :
        ul_region_tag = ul_region_tag[0]
        a_region_tag = ul_region_tag.find_all("a")
        if len(a_region_tag) == 0:
            print "there is no a_region_tag"
        else:
            for region in a_region_tag:
                region_dic = {}
                region_dic["name"] = ""
                region_dic["href"] = ""
                region_url=region.get("href")
                region_name=region.string
                if region_url != None:
                    if "javascript" in region_url:
                        break
                    region_dic["href"]="https://www.dianping.com"+region_url
                if region_name != None:
                    region_dic["name"]=region_name.replace(" ", "").replace("\n", "")
                else:
                    region_name=region.contents[0]
                    if region_name != None:
                        region_dic["name"]=region_name.replace(" ", "").replace("\n", "")
                arrays = region_dic["name"].split("区")
                region_dic["name"] = arrays[0] + "区"
                region_list.append(region_dic)

    return region_list


#得到朝阳区等区的分区
def get_decoration_all_sub_region_url_list(url):
    sub_region_list = []
    soup = setupSoup(url)
    sub_content_tag = soup.find_all("ul", class_="sub-content")
    if len(sub_content_tag) == 0:
        region_box_tag = soup.find_all(class_="type")
        if len(region_box_tag) == 0:
            print "there is no class type in get decoration class"
        else:
            region_box_tag = region_box_tag[-1]
            ul_region_tag = region_box_tag.find_all("ul")
            if len(ul_region_tag) == 0:
                print "there is no ul find in type class in get sub region"
            else:
                ul_region_tag = ul_region_tag[0]
                a_region_tag = ul_region_tag.find_all("a")
                if len(a_region_tag) == 0:
                    print "there is no a_region_tag"
                else:
                    for region in a_region_tag[1:]:
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
                            if "javascript" in region_url:
                                break
                            region_dic["href"] = region_url
                            sub_region_list.append(region_dic)
    else:
        ul_region_tag = sub_content_tag[0]
        a_region_tag = ul_region_tag.find_all("a")
        if len(a_region_tag) == 0:
            print "there is no a_region_tag"
        else:
            for region in a_region_tag[1:]:
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
def get_decoration_detail_url_list(url):
    detail_url_list=[]
    soup=setupSoup(url)
    shop_list=soup.find_all(class_="shop-title")
    if len(shop_list) == 0:
        print "there is no shop-title tag"
    else:
        for detail_tag in shop_list:
            a_tag=detail_tag.find_all("a")
            if len(a_tag) == 0:
                print "there is no a tag in detail tag"
            else:
                a_tag=a_tag[0]
                href=a_tag.get("href")
                if href != None:
                    href="https://www.dianping.com"+href
                    detail_url_list.append(href)
    return detail_url_list


#得到下一页的url
def get_decoration_next_page_url(url):
    next_page_url=""
    soup = setupSoup(url)
    next_tag = soup.find_all(class_="nextPage")
    if len(next_tag) > 0:
        next_tag=next_tag[0]
        next_page_url="https://www.dianping.com"+next_tag.get("href")
    return next_page_url

#只得到当前传入url的后面的页数，因此传参要传入第一页url
def get_decoration_all_page_url(url):
    all_page_url_list=[]
    all_page_url_list.append(url)
    next_url=get_decoration_next_page_url(url)
    while len(next_url) != 0:
        all_page_url_list.append(next_url)
        next_url=get_decoration_next_page_url(next_url)
    return all_page_url_list

#传入一个url，得到这个url的所有页，和所有详情,并写入文件
def get_decoration_all_pages_features(url, filename):
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
    all_page_url_list = get_decoration_all_page_url(url)
    if len(all_page_url_list) > 0:
        for one_page_url in all_page_url_list:
            print "one_page_url...", one_page_url
            detail_list = get_decoration_detail_url_list(one_page_url)
            if len(detail_list) > 0:
                for features_url in detail_list:
                    print "detail_url...", features_url
                    features = get_decoration_features(features_url)
                    features["primary_category"]=primary_category_name
                    features["secondary_category"]=secondary_category_name
                    features["region"]=region_name
                    features["sub_region"]=sub_region_name
                    features["detail_url"]=features_url
                    write_features_to_file(features,new_filename)
                print "\n"

# 得到某一个分类的全部features
def get_decoration_all_category_features(url, filename):
    new_filename=filename
    all_region_list = get_decoration_all_region_url_list(url)
    if len(all_region_list) > 0:
        for region in all_region_list:
            print "one_region_url...", region["name"],":", region["href"]
            all_sub_region_list = get_decoration_all_sub_region_url_list(region["href"])
            if len(all_sub_region_list) > 0:
                for sub_region in all_sub_region_list:
                    print "one_sub_region_url...", sub_region["name"], ":", sub_region["href"]
                    filename=new_filename+"-"+region["name"]+"-"+sub_region["name"]+".txt"
                    get_decoration_all_pages_features(sub_region["href"], filename)

# 得到某一个二级分类的全部url
def get_decoration_all_category_url(url, filename, r):
    new_filename = filename
    all_region_list = get_decoration_all_region_url_list(url)
    if len(all_region_list) > 0:
        for region in all_region_list:
            print "one_region_url...", region["name"], ":", region["href"]
            all_sub_region_list = get_decoration_all_sub_region_url_list(region["href"])
            if len(all_sub_region_list) > 0:
                for sub_region in all_sub_region_list:
                    print "one_sub_region_url...", sub_region["name"], ":", sub_region["href"]
                    filename = new_filename + "-" + region["name"] + "-" + sub_region["name"]
                    all_page_url_list = get_decoration_all_page_url(sub_region["href"])
                    if len(all_page_url_list) > 0:
                        for one_page_url in all_page_url_list:
                            print "one_page_url...", one_page_url
                            detail_list = get_decoration_detail_url_list(one_page_url)
                            if len(detail_list) > 0:
                                for features_url in detail_list:
                                    print "detail_url...", features_url
                                    result_url = filename + "**" + features_url
                                    r.lpush("dian_ping", result_url)
                                print "\n"


if __name__ == "__main__":
    url_test_get_children_features="http://www.dianping.com/shop/2484394"
    url_test_get_children_features1="http://www.dianping.com/shop/3657541"
    url_test_get_children_features2="http://www.dianping.com/shop/8352286"
    url_test_get_children_all_region_url_list="http://www.dianping.com/search/category/2/70/g193"
    url_test_get_children_all_region_url_list2="https://www.dianping.com/search/category/2/70/g27762"
    url_test_sub_region="https://www.dianping.com/search/category/2/70/g27762r14"

    # get_decoration_detail_url_list("https://www.dianping.com/search/category/2/90/g6826r2877")

    # list=get_decoration_all_page_url("https://www.dianping.com/search/category/2/90/g6826r2877")
    # get_children_features(url_test_get_children_features2)
    # list=get_children_all_region_url_list(url_test_get_children_all_region_url_list)
    # get_children_detail_url_list(url_test_sub_region)

    # list=get_children_all_page_url("http://www.dianping.com/search/category/2/70/r1466")
    # for url in list:
    #     print url

    # get_children_features("https://www.dianping.com/shop/6146895")
    # get_decoration_features("https://www.dianping.com/shop/6003472")
    # get_decoration_all_region_url_list("https://www.dianping.com/search/category/2/90/g25475")
    # print "\n"
    # get_decoration_all_region_url_list("https://www.dianping.com/search/category/2/90/g6826")
    # print "\n"
    # get_decoration_all_region_url_list("https://www.dianping.com/search/category/2/90/g6828")
    # print "\n"
    # get_decoration_all_region_url_list("https://www.dianping.com/search/category/2/90/g32705")
    # print "\n"
    # get_decoration_all_region_url_list("https://www.dianping.com/search/category/2/90/g32702")
    # print "\n"
    # get_decoration_all_region_url_list("https://www.dianping.com/search/category/2/90/g32704")
    # get_decoration_all_sub_region_url_list("https://www.dianping.com/search/category/2/90/g25475r14")

    # get_decoration_all_sub_region_url_list("https://www.dianping.com/search/category/2/90/g25475r14")
    # print "\n"
    # get_decoration_all_sub_region_url_list("https://www.dianping.com/search/category/2/90/g6826r14")
    # print "\n"
    # get_decoration_all_sub_region_url_list("https://www.dianping.com/search/category/2/90/g6828r14")
    # print "\n"
    # get_decoration_all_sub_region_url_list("https://www.dianping.com/search/category/2/90/g32705r14")
    # print "\n"
    # get_decoration_all_sub_region_url_list("https://www.dianping.com/search/category/2/90/g32702r14")
    # print "\n"
    # get_decoration_all_sub_region_url_list("https://www.dianping.com/search/category/2/90/g32704r14")
    get_decoration_features("https://www.dianping.com/shop/1757146")