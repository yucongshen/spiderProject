# !/usr/python/bin
# -*- coding: UTF-8 -*-

def write_features_to_file(features):
    filename = "weibo_data.txt"
    path = "data/" + filename
    file = open(path.decode('utf-8'), "a")
    file.write(features["idstr"])
    file.write(";")
    file.write(features["screen_name"])
    file.write(";")
    file.write(features["province"])
    file.write(";")
    file.write(features["city"])
    file.write(";")
    file.write(features["location"])
    file.write(";")
    file.write(features["profile_image_url"])
    file.write(";")
    file.write(features["gender"])
    file.write(";")
    file.write(features["followers_count"])
    file.write(";")
    file.write(features["friends_count"])
    file.write(";")
    file.write(features["statuses_count"])
    file.write(";")
    file.write(features["created_at"])
    file.write(";")
    file.write(features["status"]["created_at"])
    file.write(";")
    file.write(features["status"]["idstr"])
    file.write(";")
    file.write(features["status"]["text"])
    file.write(";")
    file.write(features["status_geo_longitude"])
    file.write(";")
    file.write(features["status_geo_latitude"])
    file.write("\n")
def print_information(information):
    print information["idstr"]
    print information["screen_name"]
    print information["province"]
    print information["city"]
    print information["location"]
    print information["profile_image_url"]
    print information["gender"]
    print information["followers_count"]
    print information["friends_count"]
    print information["statuses_count"]
    print information["created_at"]
    print information["status"]["created_at"]
    print information["status"]["idstr"]
    print information["status"]["text"]
    print information["status_geo_longitude"]
    print information["status_geo_latitude"]

