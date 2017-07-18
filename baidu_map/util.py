# !/usr/python/bin
# -*- coding: UTF-8 -*-
import urlparse
import urllib
import time
def set_blank_features():
    features={}
    features["id"]=""
    features["category"]=""
    features["name"]=""
    features["address"]=""
    features["point_x"]=""
    features["point_y"]=""
    return features

#传入url，返回参数字典
def url_parse(url):
    result=urlparse.urlparse(url)
    query_dict=urlparse.parse_qs(result.query)
    return query_dict


#传入参数字典，返回url
def url_encode(param_dic):
    qs = urllib.urlencode(param_dic)
    return qs

#输出字典
def print_dict(d):
    for k, v in d.items():
        print('%s: %s' % (k, v))

#通过第一页得到第二页
def init_page2(url):
    param_dic = url_parse(url)
    for k, v in param_dic.items():
        param_dic[k] = v[0]
    param_dic["src"] = "7"
    param_dic["qt"] = "con"
    param_dic["da_src"] = "pcmappg.poi.page"
    if param_dic.has_key("biz_forward"):
        param_dic.pop("biz_forward")
    param_dic["gr"] = "3"
    param_dic["pl_hotel_book_pc_section"] = "0,+"
    param_dic["pl_sort_rule"] = "0"
    param_dic["pl_ticket_book_flag_section"] = "0,+"
    param_dic["addr"] = "0"
    param_dic["pl_cater_book_pc_section"] = "0,+"
    param_dic["pl_movie_book_section"] = "0,+"
    param_dic["pl_data_type"] = "cater"
    param_dic["pl_price_section"] = "0,+"
    param_dic["db"] = "0"
    param_dic["pl_business_type"] = "cater"
    param_dic["pl_groupon_section"] = "0,+"
    param_dic["pl_sub_type"] = "%E9%A4%90%E9%A6%86"
    param_dic["pl_discount2_section"] = "0,+"
    param_dic["on_gel"] = "1"
    param_dic["pl_sort_type"] = "data_type"
    return param_dic

def write_features_to_file(features):
    # 加上时间戳，防止写操作混乱
    date = time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))
    # filename=filename.replace("/", "&")
    # filename = "baidu_map_data" + "-" + date + ".txt"
    filename = "baidu_map_data" + ".txt"
    path = "data/" + filename
    fl = open(path.decode('utf-8'), "a")
    fl.write(date)
    fl.write(";")
    if features["id"] == None:
        fl.write("")
    else:
        fl.write(features["id"])
    fl.write(";")
    if features["category"] == None:
        fl.write("")
    else:
        fl.write(features["category"])
    fl.write(";")
    if features["name"] == None:
        fl.write("")
    else:
        fl.write(features["name"])
    fl.write(";")
    if features["address"] == None:
        fl.write("")
    else:
        fl.write(features["address"])
    fl.write(";")
    if features["point_x"] == None:
        fl.write("")
    else:
        fl.write(str(features["point_x"]))
    fl.write(";")
    if features["point_y"] == None:
        fl.write("")
    else:
        fl.write(str(features["point_y"]))
    fl.write("\n")
    fl.close()

def print_features_list(features_list):
    for features in features_list:
        print features["id"]
        print features["category"]
        print features["name"]
        print features["address"]
        print features["point_x"]
        print features["point_y"]
        print "\n"

if __name__ == "__main__":
    url1="http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=baidu&pcevaname=pc4.1&qt=s&da_src=searchBox.button&wd=%E7%BE%8E%E9%A3%9F&c=131&src=0&wd2=&sug=0&l=8&b=(12927835,4509215;12997467,5149215)&from=webmap&biz_forward={%22scaler%22:1,%22styles%22:%22pl%22}&sug_forward=&tn=B_NORMAL_MAP&nn=0&u_loc=12952155,4832191&ie=utf-8&t=1495523334044"
    url2="http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=baidu&pcevaname=pc4.1&qt=con&from=webmap&c=131&wd=%E7%BE%8E%E9%A3%9F&wd2=&pn=1&nn=10&db=0&sug=0&addr=0&pl_data_type=cater&pl_sub_type=%E9%A4%90%E9%A6%86&pl_price_section=0%2C%2B&pl_sort_type=data_type&pl_sort_rule=0&pl_discount2_section=0%2C%2B&pl_groupon_section=0%2C%2B&pl_cater_book_pc_section=0%2C%2B&pl_hotel_book_pc_section=0%2C%2B&pl_ticket_book_flag_section=0%2C%2B&pl_movie_book_section=0%2C%2B&pl_business_type=cater&pl_business_id=&da_src=pcmappg.poi.page&on_gel=1&src=7&gr=3&l=8&tn=B_NORMAL_MAP&u_loc=12952155,4832191&ie=utf-8&b=(12927835,4508703;12997467,5148703)&t=1495523395106"
    url2_1="http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=baidu&pcevaname=pc4.1&qt=con&from=webmap&c=131&wd=%E7%BE%8E%E9%A3%9F&wd2=&pn=1&nn=10&db=0&sug=0&addr=0&pl_data_type=cater&pl_sub_type=%E9%A4%90%E9%A6%86&pl_price_section=0%2C%2B&pl_sort_type=data_type&pl_sort_rule=0&pl_discount2_section=0%2C%2B&pl_groupon_section=0%2C%2B&pl_cater_book_pc_section=0%2C%2B&pl_hotel_book_pc_section=0%2C%2B&pl_ticket_book_flag_section=0%2C%2B&pl_movie_book_section=0%2C%2B&pl_business_type=cater&pl_business_id=&da_src=pcmappg.poi.page&on_gel=1&src=7&gr=3&l=8&tn=B_NORMAL_MAP&u_loc=12952155,4832191&ie=utf-8&b=(12922715,4507679;12992347,5147679)&t=1495523856292"
    url3="http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=baidu&pcevaname=pc4.1&qt=con&from=webmap&c=131&wd=%E7%BE%8E%E9%A3%9F&wd2=&pn=2&nn=20&db=0&sug=0&addr=0&pl_data_type=cater&pl_sub_type=%E9%A4%90%E9%A6%86&pl_price_section=0%2C%2B&pl_sort_type=data_type&pl_sort_rule=0&pl_discount2_section=0%2C%2B&pl_groupon_section=0%2C%2B&pl_cater_book_pc_section=0%2C%2B&pl_hotel_book_pc_section=0%2C%2B&pl_ticket_book_flag_section=0%2C%2B&pl_movie_book_section=0%2C%2B&pl_business_type=cater&pl_business_id=&da_src=pcmappg.poi.page&on_gel=1&src=7&gr=3&l=8&tn=B_NORMAL_MAP&u_loc=12952155,4832191&ie=utf-8&b=(12927835,4504607;12997467,5144607)&t=1495524024985"
    url4="http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=baidu&pcevaname=pc4.1&qt=con&from=webmap&c=131&wd=%E7%BE%8E%E9%A3%9F&wd2=&pn=3&nn=30&db=0&sug=0&addr=0&pl_data_type=cater&pl_sub_type=%E9%A4%90%E9%A6%86&pl_price_section=0%2C%2B&pl_sort_type=data_type&pl_sort_rule=0&pl_discount2_section=0%2C%2B&pl_groupon_section=0%2C%2B&pl_cater_book_pc_section=0%2C%2B&pl_hotel_book_pc_section=0%2C%2B&pl_ticket_book_flag_section=0%2C%2B&pl_movie_book_section=0%2C%2B&pl_business_type=cater&pl_business_id=&da_src=pcmappg.poi.page&on_gel=1&src=7&gr=3&l=8&tn=B_NORMAL_MAP&u_loc=12952155,4832191&ie=utf-8&b=(12927835,4509727;12997467,5149727)&t=1495523540249"
    url6="http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=baidu&pcevaname=pc4.1&qt=con&from=webmap&c=131&wd=%E7%BE%8E%E9%A3%9F&wd2=&pn=5&nn=50&db=0&sug=0&addr=0&pl_data_type=cater&pl_sub_type=%E9%A4%90%E9%A6%86&pl_price_section=0%2C%2B&pl_sort_type=data_type&pl_sort_rule=0&pl_discount2_section=0%2C%2B&pl_groupon_section=0%2C%2B&pl_cater_book_pc_section=0%2C%2B&pl_hotel_book_pc_section=0%2C%2B&pl_ticket_book_flag_section=0%2C%2B&pl_movie_book_section=0%2C%2B&pl_business_type=cater&pl_business_id=&da_src=pcmappg.poi.page&on_gel=1&src=7&gr=3&l=8&tn=B_NORMAL_MAP&u_loc=12952155,4832191&ie=utf-8&b=(12928859,4507679;12998491,5147679)&t=1495523684101"
    # dic=url_parse(url6)
    # print_dict(dic)
    features={}
    features["id"]="28e700f163244d18095cb3d9"
    features["category"]="美食;中餐厅"
    features["name"]="金百万美食广场"
    features["point_x"]=str(1303820208)
    features["point_y"]=str(485955633)
    features["address"]="北京市平谷区府前街19号"
    write_features_to_file(features)




