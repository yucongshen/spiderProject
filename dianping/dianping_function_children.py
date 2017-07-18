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

def get_children_features(url, retry = 0):
    features=set_blank_features()
    soup=setupSoup(url)
    #解析标题
    title_tag=soup.find("h1", class_ = 'shop-title')
    if title_tag == None:
        print "there is no title_div_class tag in get_children_features"
        if retry <= 2:
            retry += 1
            features = get_children_features(url, retry)
    else:
        title_str=title_tag.string
        if title_str != None:
            features["title"]=title_str.replace("\n", "").replace(" ", "")
    #解析评分和星级
    comment_rst=soup.find_all("div", class_="comment-rst")
    if len(comment_rst) == 0:
        print "there is no comment_rst in get_children_features"
    else:
        comment_rst=comment_rst[0]
        #解析星级
        star_span=comment_rst.find_all("meta")
        if len(star_span) == 0:
            print "there is no star_span in get children features"
        else:
            star_span=star_span[0]
            star_str=star_span.string
            if star_str != None:
                features["rank_stars"]=star_str.replace(" ", "").replace("\n", "")
    avg_price=soup.find_all("strong", class_="stress")
    if len(avg_price) == 0:
        avg_price=soup.find_all(class_="Price")
        if len(avg_price) == 0:
            avg_price=soup.find_all("em", class_="average")
            if len(avg_price) == 0:
                print "there is no avg_price in get children features"
            else:
                avg_price=avg_price[0]
                price_str=avg_price.string
                if price_str != None:
                    features["avg_price"]=price_str.replace(" ", "").replace("\n", "")
        else:
            avg_price=avg_price[0]
            avg_price=avg_price.parent
            if avg_price == None:
                print "there is no price parent in get children features"
            else:
                price=avg_price.contents[1]
                if price == None:
                    print "the price string is none"
                else:
                    features["avg_price"] =price
    else:
        avg_price=avg_price[0]
        price=avg_price.string
        if price != None:
            features["avg_price"]=price
    #解析地址
    address_div=soup.find_all("div", class_="shop-addr")
    if len(address_div) == 0:
        address_div=soup.find_all(itemprop="street-address")
        if len(address_div) == 0:
            print "there is no address in get children features"
        else:
            address_div=address_div[0]
            address_str=address_div.string
            if address_str != None:
                features["address"]=address_str
    else:
        address_div=address_div[0]
        address=address_div.find_all("span")
        if len(address) == 0:
            print "there is no address span"
        else:
            address=address[0]
            address_str=address.contents[2]
            if address_str != None:
                features["address"]=address_str.replace(" ", "").replace("\n", "")
    #解析id
    features["id"] = url[url.index("shop/") + len("shop/"):]
    if "?" in features["id"]:
        features["id"] = features["id"][:features["id"].index("?")]
    return features


#得到朝阳区，海淀区等分区
def get_children_all_region_url_list(url):
    region_list = []
    soup = setupSoup(url)
    region_box_tag=soup.find_all(class_="t-item-box t-district J_li")
    if len(region_box_tag) == 0:
        print "there is no region box tag in get children features"
    else:
        region_box_tag=region_box_tag[0]
        ul_region_tag = region_box_tag.find_all("ul")
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
                    region_url=region.get("href")
                    region_name=region.string
                    if region_url != None:
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
def get_children_all_sub_region_url_list(url):
    sub_region_url_list=get_children_all_region_url_list(url)
    return sub_region_url_list


#得到某一页所有url列表
def get_children_detail_url_list(url):
    detail_url_list=[]
    soup=setupSoup(url)
    shop_list=soup.find_all("ul", class_="shop-list")
    if len(shop_list) == 0:
        print "there is no class_pic tag"
    else:
        shop_list=shop_list[0]
        shop_name_tag=shop_list.find_all(class_="shopname")
        if len(shop_name_tag) == 0:
            print "there is no shop name tag in get children detail url list"
        else:
            for detail_tag in shop_name_tag:
                href=detail_tag.get("href")
                if href != None:
                    href="https://www.dianping.com"+href
                    detail_url_list.append(href)
    return detail_url_list


#得到下一页的url
def get_next_page_url(url):
    next_page_url=""
    soup = setupSoup(url)
    next_tag = soup.find_all(class_="NextPage")
    if len(next_tag) > 0:
        next_tag=next_tag[0]
        next_page_url="https://www.dianping.com"+next_tag.get("href")
    return next_page_url

#只得到当前传入url的后面的页数，因此传参要传入第一页url
def get_children_all_page_url(url):
    all_page_url_list=[]
    all_page_url_list.append(url)
    next_url=get_next_page_url(url)
    while len(next_url) != 0:
        all_page_url_list.append(next_url)
        next_url=get_next_page_url(next_url)
    return all_page_url_list

#传入一个url，得到这个url的所有页，和所有详情,并写入文件
def get_children_all_pages_features(url, filename):
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
    all_page_url_list = get_children_all_page_url(url)
    if len(all_page_url_list) > 0:
        for one_page_url in all_page_url_list:
            print "one_page_url...", one_page_url
            detail_list = get_children_detail_url_list(one_page_url)
            if len(detail_list) > 0:
                for features_url in detail_list:
                    print "detail_url...", features_url
                    features = get_children_features(features_url)
                    features["primary_category"]=primary_category_name
                    features["secondary_category"]=secondary_category_name
                    features["region"]=region_name
                    features["sub_region"]=sub_region_name
                    features["detail_url"]=features_url
                    write_features_to_file(features,new_filename)
                print "\n"

# 得到某一个分类的全部features
def get_children_all_category_features(url, filename):
    new_filename=filename
    all_region_list = get_children_all_region_url_list(url)
    if len(all_region_list) > 0:
        for region in all_region_list:
            print "one_region_url...", region["name"],":", region["href"]
            all_sub_region_list = get_children_all_sub_region_url_list(region["href"])
            if len(all_sub_region_list) > 0:
                for sub_region in all_sub_region_list:
                    print "one_sub_region_url...", sub_region["name"], ":", sub_region["href"]
                    filename=new_filename+"-"+region["name"]+"-"+sub_region["name"]+".txt"
                    get_children_all_pages_features(sub_region["href"], filename)

# 得到某一个二级分类的全部url
def get_children_all_category_url(url, filename, r):
    new_filename = filename
    all_region_list = get_children_all_region_url_list(url)
    if len(all_region_list) > 0:
        for region in all_region_list:
            print "one_region_url...", region["name"], ":", region["href"]
            all_sub_region_list = get_children_all_sub_region_url_list(region["href"])
            if len(all_sub_region_list) > 0:
                for sub_region in all_sub_region_list:
                    print "one_sub_region_url...", sub_region["name"], ":", sub_region["href"]
                    filename = new_filename + "-" + region["name"] + "-" + sub_region["name"]
                    all_page_url_list = get_children_all_page_url(sub_region["href"])
                    if len(all_page_url_list) > 0:
                        for one_page_url in all_page_url_list:
                            print "one_page_url...", one_page_url
                            detail_list = get_children_detail_url_list(one_page_url)
                            if len(detail_list) > 0:
                                for features_url in detail_list:
                                    print "detail_url...", features_url
                                    result_url=filename+"**"+features_url
                                    r.lpush("dian_ping", result_url)
                                print "\n"

if __name__ == "__main__":
    url_test_get_children_features="http://www.dianping.com/shop/2484394"
    url_test_get_children_features1="http://www.dianping.com/shop/3657541"
    url_test_get_children_features2="http://www.dianping.com/shop/8352286"
    url_test_get_children_all_region_url_list="http://www.dianping.com/search/category/2/70/g193"
    url_test_get_children_all_region_url_list2="https://www.dianping.com/search/category/2/70/g27762"
    url_test_sub_region="https://www.dianping.com/search/category/2/70/g27762r14"
    # get_children_features(url_test_get_children_features2)
    # list=get_children_all_region_url_list(url_test_get_children_all_region_url_list)
    # get_children_detail_url_list(url_test_sub_region)

    # list=get_children_all_page_url("http://www.dianping.com/search/category/2/70/r1466")
    # for url in list:
    #     print url

    # get_children_features("https://www.dianping.com/shop/6146895")
    get_children_features("https://www.dianping.com/shop/20890100")