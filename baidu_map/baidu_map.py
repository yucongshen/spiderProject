# !/usr/python/bin
# -*- coding: UTF-8 -*-
from webclient import WebBrowser
from headers import headers
from util import url_encode
import json
from util import init_page2
from util import set_blank_features
from util import write_features_to_file

def get_response_json(url):
    try:
        browser = WebBrowser(debug=False, proxy="http://112.91.135.115:8080")
        # browser = WebBrowser(debug = False, proxy="http://61.139.104.216:80")
        # browser=WebBrowser(debug= False)
        content, rep_header = browser._request(url, headers = headers)
        json_content=json.loads(content)
        return json_content
    except:
        print "get response json error...."

def get_all_features_num(url):
    json_content=get_response_json(url)
    return json_content["result"]["total"]

def get_all_url_list(url):
    all_url_list=[]
    all_url_list.append(url)
    param_dic=init_page2(url)
    all_features_num=get_all_features_num(url)
    json_content=get_response_json(url)
    if json_content != None:
        if json_content.has_key("content"):
            one_page_features_num = len(json_content["content"])
            total_page_num = all_features_num / one_page_features_num
            for i in range(1,total_page_num+1):
                param_dic["nn"] = i*10
                param_dic["pn"] = i
                url_param=url_encode(param_dic)
                result_url="http://map.baidu.com/?"+url_param
                response_content=get_response_json(result_url)
                if response_content.has_key("content"):
                    all_url_list.append(result_url)
                else:
                    break
        else:
            print "there is no key content in get all url list"
    return all_url_list

def get_all_pages_features(url):
    all_url_list=get_all_url_list(url)
    for one_url in all_url_list:
        print "one page url...:", one_url
        get_one_page_features(one_url)



def get_one_page_features(url):
    response=get_response_json(url)
    if response == None:
        print "get response json error....in get one page features"
    else:
        length=0
        if response.has_key("content"):
            length=len(response["content"])
        else:
            print "there is no key content in get one page features"
        for i in range(length):
            features = set_blank_features()
            features["id"]=response["content"][i]["uid"]
            features["category"]=response["content"][i]["std_tag"]
            features["name"]=response["content"][i]["name"]
            features["address"]=response["content"][i]["addr"]
            features["point_x"]=response["content"][i]["x"]
            features["point_y"]=response["content"][i]["y"]
            write_features_to_file(features)






if __name__ == "__main__":
    url = "http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s&da_src=searchBox.button&wd=%E7%BE%8E%E9%A3%9F&c=131&src=0&wd2=&sug=0&l=6&b=(12951110.56,3592451.4699999997;12996166.56,6058243.47)&from=webmap&biz_forward={%22scaler%22:2,%22styles%22:%22pl%22}&sug_forward=&tn=B_NORMAL_MAP&nn=0&u_loc=12952667,4832593&ie=utf-8&t=1495553688508"
    get_all_pages_features(url)

    # url="http://map.baidu.com/?gr=3&pl_hotel_book_pc_section=0%2C%2B&da_src=pcmappg.poi.page&pl_ticket_book_flag_section=0%2C%2B&ie=utf-8&sug=0&pl_cater_book_pc_section=0%2C%2B&from=webmap&addr=0&nn=530&tn=B_NORMAL_MAP&pn=53&pl_price_section=0%2C%2B&pl_sub_type=%25E9%25A4%2590%25E9%25A6%2586&pl_data_type=cater&wd=%E7%BE%8E%E9%A3%9F&pl_sort_rule=0&pl_movie_book_section=0%2C%2B&db=0&newmap=1&da_par=direct&pl_discount2_section=0%2C%2B&biz=1&pl_groupon_section=0%2C%2B&pcevaname=pc4.1&src=7&c=131&b=%2812951110.56%2C3592451.4699999997&qt=con&u_loc=12952667%2C4832593&reqflag=pcmap&l=6&t=1495553688508&pl_business_type=cater&on_gel=1&pl_sort_type=data_type"
    # print_dict(get_response_json(url))


    # get_all_features_num(url)
    # get_all_pages_features(url)
    # url="http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=baidu&pcevaname=pc4.1&qt=s&da_src=searchBox.button&wd=%E7%BE%8E%E9%A3%9F&c=131&src=0&wd2=&sug=0&l=12&b=(12933915,4839071;12995867,4852191)&from=webmap&biz_forward={%22scaler%22:1,%22styles%22:%22pl%22}&sug_forward=&tn=B_NORMAL_MAP&nn=0&u_loc=12952155,4832191&ie=utf-8&t=1495464405715"
    # url="http://ditu.amap.com/service/poiInfo?query_type=TQUERY&pagesize=%s&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=17&city=110000&geoobj=116.343134%7C40.029228%7C116.35264%7C40.031857&keywords=%E7%BE%8E%E9%A3%9F"
    # url_encode(url)
    # url = "http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s&da_src=searchBox.button&wd=%E7%BE%8E%E9%A3%9F&c=204&src=0&wd2=&sug=0&l=12&b=(12005833,2450878;12067785,2463998)&from=webmap&biz_forward={%22scaler%22:1,%22styles%22:%22pl%22}&sug_forward=&tn=B_NORMAL_MAP&nn=0&u_loc=12024073,2443998&ie=utf-8&t=1495505784302"
    # url="http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s&da_src=searchBox.button&wd=%E7%BE%8E%E9%A3%9F&c=204&src=0&wd2=&sug=0&l=13&b=(12011561,2457518;12042537,2464590)&from=webmap&biz_forward={%22scaler%22:1,%22styles%22:%22pl%22}&sug_forward=&tn=B_NORMAL_MAP&nn=0&u_loc=12024073,2443998&ie=utf-8&t=1495521863660"

    # url="http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=baidu&pcevaname=pc4.1&qt=s&da_src=searchBox.button&wd=%E7%BE%8E%E9%A3%9F&c=131&src=0&wd2=&sug=0&l=12&b=(12933915,4839071;12995867,4852191)&from=webmap&biz_forward={%22scaler%22:1,%22styles%22:%22pl%22}&sug_forward=&tn=B_NORMAL_MAP&nn=0&u_loc=12952155,4832191&ie=utf-8&t=1495464405715"
    # url="http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s&da_src=searchBox.button&wd=%E7%BE%8E%E9%A3%9F&c=131&src=0&wd2=&sug=0&l=11&b=(12910555,4796625;12911963,4873681)&from=webmap&biz_forward={%22scaler%22:2,%22styles%22:%22pl%22}&sug_forward=&tn=B_NORMAL_MAP&nn=0&u_loc=12952667,4832593&ie=utf-8&t=1495550953110"
    # url="http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s&da_src=searchBox.button&wd=%E7%BE%8E%E9%A3%9F&c=131&src=0&wd2=&sug=0&l=5&b=(12881755,2352977;12971867,7284561)&from=webmap&biz_forward={%22scaler%22:2,%22styles%22:%22pl%22}&sug_forward=&tn=B_NORMAL_MAP&nn=0&u_loc=12952667,4832593&ie=utf-8&t=1495551048370"
    # url="http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=direct&pcevaname=pc4.1&qt=s&da_src=searchBox.button&wd=%E7%BE%8E%E9%A3%9F&c=131&src=0&wd2=&sug=0&l=12&b=(12971654.56,4806083.47;12972358.56,4844611.47)&from=webmap&biz_forward={%22scaler%22:2,%22styles%22:%22pl%22}&sug_forward=&tn=B_NORMAL_MAP&nn=0&u_loc=12952667,4832593&ie=utf-8&t=1495553020979"

    # url1 = "http://map.baidu.com/?newmap=1&reqflag=pcmap&biz=1&from=webmap&da_par=baidu&pcevaname=pc4.1&qt=s&da_src=searchBox.button&wd=%E7%BE%8E%E9%A3%9F&c=131&src=0&wd2=&sug=0&l=8&b=(12927835,4509215;12997467,5149215)&from=webmap&biz_forward={%22scaler%22:1,%22styles%22:%22pl%22}&sug_forward=&tn=B_NORMAL_MAP&nn=0&u_loc=12952155,4832191&ie=utf-8&t=1495523334044"
    # url_er=get_all_url_list(url1)
    # print url_er
    # print get_response_json(url_er)
    # print_dict(url_parse(url_er))


