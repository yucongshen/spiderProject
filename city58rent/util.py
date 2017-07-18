# !/usr/bin/python
# -*- coding:UTF-8 -*-
import os
def set_blank_features():
    features = {}
    features["title"] = ""
    features["money"] = ""
    features["room_type"] = ""
    features["residential"] = ""
    features["address"] = ""
    features["rent_type"] = ""
    features["deposit"] = ""
    features["lat"] = ""
    features["lon"] = ""
    features["id"] = ""
    features["url"] = ""
    return features

def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

def write_feautres_to_file(dic, filename):
    fl = open(filename, "a")
    fl.write(dic["id"])
    fl.write(",")
    fl.write(dic["title"])
    fl.write(",")
    fl.write(dic["rent_type"])
    fl.write(",")
    fl.write(dic["deposit"])
    fl.write(",")
    fl.write(dic["money"])
    fl.write(",")
    fl.write(dic["room_type"])
    fl.write(",")
    fl.write(dic["residential"])
    fl.write(",")
    fl.write(dic["address"])
    fl.write(",")
    fl.write(dic["lat"])
    fl.write(",")
    fl.write(dic["lon"])
    fl.write(",")
    fl.write(dic["url"])
    fl.write("\n")
    fl.close()

def print_features(features):
    print features["title"]
    print features["money"]
    print features["room_type"]
    print features["residential"]
    print features["address"]
    print features["rent_type"]
    print features["deposit"]
    print features["lat"]
    print features["lon"]
    print features["id"]
    print features["url"]
if __name__ == "__main__":
    source_filname="12"
    goal_filename="buchong-xingong.txt.txt"
    source_file=open(source_filname)
    goal_file = open(goal_filename, "a")
    while 1:
        line = source_file.readline()
        if line == "":
            break
        goal_file.write(line)
    source_file.close()
    goal_file.close()
