# !/usr/bin/python
# -*- coding: UTF-8 -*-
import pandas as pd
def read_data_to_list():
    a = pd.read_csv("data/fanwei_em1.csv")
    last_index = a[-1:]["Id"]
    list_all = []
    for i in range(0, last_index+1):
        list = []
        for index, row in a.iterrows():
            if row["Id"] == i:
                list.append(row)
        list_all.append(list)
    new_list_all = []
    for list in list_all:
        new_list =[]
        for row in list:
            dic = {}
            dic["Id"] = row["Id"]
            dic["FID_fanwei"] = row["FID_fanwei"]
            dic["area"] = row["area"]
            dic["area_mm"] = row["area_mm"]
            dic["FID_xian_3"] = row["FID_xian_3"]
            dic["FID_hebei"] = row["FID_hebei"]
            dic["diname"] = row["diname"]
            dic["FID_xian_4"] = row["FID_xian_4"]
            dic["tid"] = row["tid"]
            dic["Input_FID"] = row["Input_FID"]
            new_list.append(dic)
        new_list_all.append(new_list)
    return new_list_all

def get_data(new_list_all):
    for new_list in new_list_all:
        for list in new_list:
            # print list["Id"]
            print list


if __name__ == "__main__":
    new_list_all = read_data_to_list()
    get_data(new_list_all)