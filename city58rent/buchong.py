# !/usr/bin/python
# -*- coding:UTF-8 -*-
from liuliqiaodong import get_features
from util import write_feautres_to_file
from util import print_features
def get_url_from_file(filename):
    file = open(filename, "r")
    url_list = []
    while True:
        url = file.readline()
        if not url:
            break
        url_list.append(url.replace("\n", ""))
    return url_list

def write_buchong_to_file(url_list):
    for url in url_list:
        print url
        features = get_features(url)
        write_feautres_to_file(features,"data/buchongresult.txt")

if __name__ == "__main__":
    url_list = get_url_from_file("data/buchong-5.txt")
    write_buchong_to_file(url_list)