# !/usr/bin/python
# -*- coding: UTF-8 -*-
# 传入火锅的url(>50和<50)，如果部分大于50或者小于50就用get_all_category_features这个函数
# def get_all_one_category_features(url, filename):
#     new_filename=filename
#     # filename="dianping.txt"
#     # delete_file(filename)
#     region_name=""
#     sub_region_name=""
#     init_page_num=get_total_page_num(url)
#     if init_page_num <50 :
#         print "category<50...", url
#         get_all_pages_features(url, filename)
#     else:
#         all_region_url_list=get_all_region_url_list(url)
#         if len(all_region_url_list) >0:
#             for region_url in all_region_url_list:
#                 region_name=region_url["name"]
#                 print "one_region_url...", region_name, ":", region_url["href"]
#                 region_page_num=get_total_page_num(region_url["href"])
#                 if region_page_num < 50:
#                     filename=new_filename+"-"+region_name+".txt"
#                     get_all_pages_features(region_url["href"], filename)
#                 else:
#                     all_sub_region_url_list=get_all_sub_region_url_list(region_url["href"])
#                     for sub_region_url in all_sub_region_url_list:
#                         sub_region_name=sub_region_url["name"]
#                         print "one_sub_region_url...", sub_region_url["name"], ":", sub_region_url["href"]
#                         filename=new_filename+"-"+region_name+"-"+sub_region_name+".txt"
#                         get_all_pages_features(sub_region_url["href"], filename)