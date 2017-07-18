# !/usr/bin/python
# -*- coding: UTF-8 -*-
from util import setupSoup
from dianping_function_common import get_all_category_features
from dianping_function_wedding import get_wedding_category_features
from dianping_function_hotel import get_hotel_all_category_features
from dianping_function_children import get_children_all_category_features
from dianping_function_decoration import get_decoration_all_category_features
from dianping_function_banquet import get_banquet_all_category_features
#得到首页的全部分类信息
def get_category(url):
    all_category_list = []
    soup=setupSoup(url)
    primary_category_class=soup.find_all(class_="primary-category")
    if len(primary_category_class) == 0:
        print "there is no primary-category J-primary-category in get_category"
    else:
        for primary_tag in primary_category_class:
            sub_category_dic_list=[]
            secondary_a_tags=primary_tag.find_all("a")
            if len(secondary_a_tags) == 0:
                print "there is no secondary_a_tags in get_category"
            else:
                for a in secondary_a_tags[3:]:
                    sub_category_dic={}
                    # print a.string, " ", "https://www.dianping.com"+a.get("href")
                    sub_category_dic["name"] = a.string
                    sub_category_dic["href"]="https://www.dianping.com"+a.get("href")
                    sub_category_dic_list.append(sub_category_dic)
                all_category_list.append(sub_category_dic_list)
                # print "\n"
    #婚礼数组特殊处理，位于第三行的数据是婚礼
    all_category_list[2][0]["name"]="婚纱摄影"
    all_category_list[2][1]["name"]="婚纱礼服"
    all_category_list[2][2]["name"]="婚庆公司"
    all_category_list[2][3]["name"]="婚宴"
    wedding_dic={}
    wedding_dic["name"]="结婚频道"
    wedding_dic["href"]="https://www.dianping.com/beijing/wedding"
    all_category_list[2].insert(0, wedding_dic)
    return all_category_list


#得到全北京的features
def get_all_one_city_features(url):
    all_category_list=get_category(url)
    for dic_list in all_category_list:
        primary_category_name=dic_list[0]["name"]
        print "primary_category_name....", primary_category_name
        for dic_index in range(1, len(dic_list)):
            secondary_category_url=dic_list[dic_index]["href"]
            secondary_category_name=dic_list[dic_index]["name"]
            print "secondary_category_url....", secondary_category_name, secondary_category_url
            filename=primary_category_name+"-"+secondary_category_name
            if primary_category_name == "结婚频道":
                get_wedding_category_features(secondary_category_url, filename)
            elif primary_category_name == "酒店频道":
                get_hotel_all_category_features(secondary_category_url, filename)
            elif primary_category_name == "亲子频道":
                get_children_all_category_features(secondary_category_url, filename)
            elif primary_category_name == "家装频道":
                get_decoration_all_category_features(secondary_category_url, filename)
            elif primary_category_name == "宴会频道":
                get_banquet_all_category_features(secondary_category_url, filename)
            else:
                get_all_category_features(secondary_category_url, filename)

if __name__ == "__main__":
    url_beijing = "https://www.dianping.com/beijing"
    url_huoguo = "https://www.dianping.com/search/category/2/10/g110"
    url_chaoyang="https://www.dianping.com/search/category/2/10/g110r14"
    url_dongcheng="https://www.dianping.com/search/category/2/10/g110r15"
    url_features="https://www.dianping.com/shop/4017142"
    url_test_pages="https://www.dianping.com/search/category/2/10/g110r2580"
    url_test_get_all="https://www.dianping.com/search/category/2/10/g132r2583"
    url_hunchezulin="https://www.dianping.com/search/category/2/80/g181"

    # 得到全北京所有分类的features
    get_all_one_city_features(url_beijing)

    #得到所有婚车租赁的数据
    # get_all_one_category_features(url_hunchezulin)

    #得到首页的所有分类url列表
    # list=get_category(url_beijing)
    # for i in list:
    #     for ii in i:
    #         print ii["name"]
    #         print ii["href"]
    #     print "\n"
    # get_category(url_beijing)


    #得到火锅所有数据
    # get_all_one_category(url_huoguo)

    # print_dic(get_features("https://www.dianping.com/shop/6086612"))
    # print_dic(get_features("https://www.dianping.com/shop/63318931"))
    # print_dic(get_features("https://www.dianping.com/shop/24101239"))

    #得到一个url的所有数据
    # get_all_pages_features(url_test_get_all)


    # 得到火锅的所有大区域
    # print get_region_url_list(url_huoguo)
    # all_region_url_list=get_all_region_url_list(url_huoguo)
    # print_list(all_region_url_list)
    # print len(all_region_url_list)

    # 得到朝阳区所有的小分区
    # print len(get_sub_region_url_list(url_chaoyang))
    # all_sub_region_url_list=get_all_sub_region_url_list(url_chaoyang)
    # print_list(all_sub_region_url_list)
    # print len(all_sub_region_url_list)

    #测试combine_region函数
    # dic_list1=[{"name":"chaoyang1", "href":"http://chaoyang1"}, {"name":"chaoyang2", "href":"http://chaoyang2"}, {"name":"haidian1", "href":"http://haidian1"}]
    # dic_list2=[{"name":"haidian1", "href":"http://haidian1"}, {"name":"haidian2", "href":"http://haidian2"}]
    # print combine_region(dic_list1, dic_list2)
    # get_all_pages_features("https://www.dianping.com/search/category/2/35/g2926r1469", "周边游频道-展馆展览-朝阳区-亮马桥/三元桥.txt")
    # filename="周边游频道-展馆展览-朝阳区-三里屯.txt"
    # get_all_pages_features("https://www.dianping.com/search/category/2/35/g2926r2580", filename)

    # filename="data/test.txt"
    # fl = open(filename.decode('utf-8'), "a")
    # fl.write("alsdkjfal")

    # get_features("https://www.dianping.com/shop/37111438")

    # category_and_region="周边游频道-展馆展览-丰台区-草桥.txt".decode("utf-8").split("-")
    # primary_category_name = category_and_region[0]
    # secondary_category_name = category_and_region[1]
    # region_name = category_and_region[2]
    # sub_region_name = category_and_region[3][:-4]
    # print primary_category_name
    # print secondary_category_name
    # print region_name
    # print sub_region_name

