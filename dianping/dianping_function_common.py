# !/usr/bin/python
# -*- coding: UTF-8 -*-
from util import print_list
from util import setupSoup
from util import set_blank_features
from util import combine_region
from util import delete_file
from util import write_features_to_file
# 返回值是一个二维的字典数组，每一行代表一个大分类
# 输入的参数url是一个城市的url
# url_beijing = "https://www.dianping.com/beijing"

def get_features(url, retry = 0):
    features=set_blank_features()
    soup=setupSoup(url)
    #解析标题
    title_tag=soup.find("h1", class_ = 'shop-name')
    if title_tag == None:
        print "there is no title_div_class tag in get_features"
        if retry <= 2:
            retry += 1
            features = get_features(url, retry)
    else:
        features["title"]=title_tag.contents[0].replace("\n", "").replace(" ", "")
    #解析评分和星级
    brief_info=soup.find_all(class_="brief-info")
    if len(brief_info) == 0:
        print "there is no brief-info in get_features"
    else:
        brief_info=brief_info[0]
        #解析星级
        star_span=brief_info.find_all(class_="mid-rank-stars")
        if len(star_span) == 0:
            print "there is no star_span in get_features"
        else:
            star_span=star_span[0]
            features["rank_stars"]=star_span.get("title")
        avg_price=brief_info.find_all(id="avgPriceTitle")
        if len(avg_price) == 0:
            print "there is no avg_price in get_features"
        else:
            avg_price=avg_price[0]
            features["avg_price"]=avg_price.string
        #解析评分
        comment_score=brief_info.find_all(id="comment_score")
        if len(comment_score) == 0:
            print "there is no comment_score in get_features"
        else:
            comment_score=comment_score[0]
            scores_tags=comment_score.find_all("span")
            if len(scores_tags) == 0:
                print "there is no scores_tags in get_features"
            else:
                for span in scores_tags:
                    str=span.string
                    print str
                    if "口味" in str:
                        features["taste_score"]=str
                    if "环境" in str:
                        features["environment_score"]=str
                    if "服务" in str:
                        features["service_score"]=str
    #解析地址
    address_div=soup.find_all(class_="expand-info address")
    if len(address_div) == 0:
        print "there is no address_div in get_features"
    else:
        address_div=address_div[0]
        address=address_div.find_all(class_="item")
        if len(address) == 0:
            print "there is no address span"
        else:
            address=address[0]
            features["address"]=address.string.replace(" ", "").replace("\n", "")
    #解析id和经纬度
    script_tags=soup.find_all("script")
    if len(script_tags) == 0:
        print "there is no script in get_features"
    else:
        for script in script_tags:
            script_str = script.string
            if script_str !=None:
                if "shopGlat" in script_str:
                    script_arrs=script_str.split("\n")
                    for script_arr in script_arrs:
                        if "shopId" in script_arr:
                            features["id"]=script_arr.replace(" ", "").replace(",", "").replace("\"", "")[7:]
                        if "shopGlat" in script_arr:
                            features["lat"]=script_arr.replace(" ", "").replace(",", "").replace("\"", "")[9:]
                        if "shopGlng" in script_arr:
                            features["lon"]=script_arr.replace(" ", "").replace(",", "").replace("\"", "")[9:]
                    break
    return features


#得到朝阳区，海淀区等分区
def get_region_url_list(url):
    region_url_list=[]
    soup=setupSoup(url)
    region_tag=soup.find_all(id="region-nav")
    if len(region_tag) == 0:
        print "there is no id=region_nav tag"
    else:
        region_tag=region_tag[0]
        regions=region_tag.find_all("a")
        if len(regions) == 0:
            print "there is no regions tag"
        else:
            for region in regions:
                region_dic={}
                region_dic["name"]=region.string
                region_dic["href"]="https://www.dianping.com"+region.get("href")
                region_url_list.append(region_dic)
    return region_url_list

# “不限”页面得到的大分区不完整，下面把所有的url打开一边，重新计算大分区
# 参数传入不限的url
def get_all_region_url_list(url):
    region_url_list=get_region_url_list(url)
    all_region_url_list=region_url_list
    for current_url in region_url_list:
        current_url_list=get_region_url_list(current_url["href"])
        # all_region_url_list=list(set(all_region_url_list+current_url_list))
        all_region_url_list=combine_region(all_region_url_list, current_url_list)
    return all_region_url_list





#得到朝阳区等区的分区
def get_sub_region_url_list(url):
    sub_region_url_list=[]
    soup=setupSoup(url)
    region_nav_sub=soup.find_all(id="region-nav-sub")
    if len(region_nav_sub) == 0:
        print "there is no region_nav_sub"
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

# “不限”页面得到的小分区不完整，下面把所有的url打开一边，重新计算小分区
# 参数传入不限区的大分区url
def get_all_sub_region_url_list(url):
    sub_region_url_list = get_sub_region_url_list(url)
    all_sub_region_url_list = sub_region_url_list
    for current_sub_url in sub_region_url_list:
        current_sub_url_list = get_sub_region_url_list(current_sub_url["href"])
        all_sub_region_url_list = combine_region(all_sub_region_url_list, current_sub_url_list)
    return all_sub_region_url_list

#得到某一页所有url列表
def get_detail_url_list(url):
    detail_url_list=[]
    soup=setupSoup(url)
    class_pic=soup.find_all(class_="pic")
    if len(class_pic) == 0:
        print "there is no class_pic tag"
    else:
        for pic in class_pic:
            a_tag=pic.find_all("a")
            if len(a_tag) == 0:
                print "there is no a_tag find in pic class"
            else:
                a_tag=a_tag[0]
                detail_url_list.append("https://www.dianping.com"+a_tag.get("href"))
    return detail_url_list

#得到总页数
def get_total_page_num(url):
    page_num=1
    soup=setupSoup(url)
    page_tag=soup.find_all(class_="page")
    if len(page_tag) == 0:
        print "there is no class next in get_all_pages"
    else:
        page_tag=page_tag[0]
        pages=page_tag.find_all("a")
        if len(pages) <2 :
            print "there is no pages in get_all_pages"
        else:
            page_num=pages[-2].string
    return int(page_num)

#得到下一页的url
def get_next_page_url(url):
    next_page_url=""
    soup = setupSoup(url)
    next_tag = soup.find_all(class_="next")
    if len(next_tag) > 0:
        next_tag=next_tag[0]
        next_page_url="https://www.dianping.com"+next_tag.get("href")
    return next_page_url

#只得到当前传入url的后面的页数，因此传参要传入第一页url
def get_all_page_url(url):
    all_page_url_list=[]
    all_page_url_list.append(url)
    next_url=get_next_page_url(url)
    while len(next_url) != 0:
        all_page_url_list.append(next_url)
        next_url=get_next_page_url(next_url)
    return all_page_url_list


#传入一个url，得到这个url的所有页，和所有详情,并写入文件
def get_all_pages_features(url, filename):
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
    all_page_url_list = get_all_page_url(url)
    if len(all_page_url_list) > 0:
        for one_page_url in all_page_url_list:
            print "one_page_url...", one_page_url
            detail_list = get_detail_url_list(one_page_url)
            if len(detail_list) > 0:
                for features_url in detail_list:
                    print "detail_url...", features_url
                    features = get_features(features_url)
                    features["primary_category"]=primary_category_name
                    features["secondary_category"]=secondary_category_name
                    features["region"]=region_name
                    features["sub_region"]=sub_region_name
                    features["detail_url"]=features_url
                    write_features_to_file(features,new_filename)
                print "\n"


# 得到某一个分类的全部features
def get_all_category_features(url, filename):
    new_filename=filename
    all_region_list = get_all_region_url_list(url)
    if len(all_region_list) > 0:
        for region in all_region_list:
            print "one_region_url...", region["name"],":", region["href"]
            all_sub_region_list = get_all_sub_region_url_list(region["href"])
            if len(all_sub_region_list) > 0:
                for sub_region in all_sub_region_list:
                    print "one_sub_region_url...", sub_region["name"], ":", sub_region["href"]
                    filename=new_filename+"-"+region["name"]+"-"+sub_region["name"]+".txt"
                    get_all_pages_features(sub_region["href"], filename)

# 得到某一个二级分类的全部url
def get_all_category_url(url, filename, r):
    new_filename = filename
    all_region_list = get_all_region_url_list(url)
    if len(all_region_list) > 0:
        for region in all_region_list:
            print "one_region_url...", region["name"], ":", region["href"]
            all_sub_region_list = get_all_sub_region_url_list(region["href"])
            if len(all_sub_region_list) > 0:
                for sub_region in all_sub_region_list:
                    print "one_sub_region_url...", sub_region["name"], ":", sub_region["href"]
                    filename = new_filename + "-" + region["name"] + "-" + sub_region["name"]
                    all_page_url_list = get_all_page_url(sub_region["href"])
                    if len(all_page_url_list) > 0:
                        for one_page_url in all_page_url_list:
                            print "one_page_url...", one_page_url
                            detail_list = get_detail_url_list(one_page_url)
                            if len(detail_list) > 0:
                                for features_url in detail_list:
                                    print "detail_url...", features_url
                                    result_url = filename + "**" + features_url
                                    r.lpush("dian_ping", result_url)
                                print "\n"



if __name__ == "__main__":
    get_features("https://www.dianping.com/shop/6232395")