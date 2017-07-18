# !/usr/python/bin
# -*- coding: UTF-8 -*-
from weibo_util import get_client
from mysql_util import insert_data
from weibo_util import get_information
from weibo_util import get_friends
from util import print_information
from util import write_features_to_file
from weibo_util import get_user_ids
from weibo_util import get_followers
def friends():
    initial_uid = 3006812112
    all_user_ids = get_user_ids(initial_uid)
    for id in all_user_ids:
        print id
        information = get_information(id)
        if information != None:
            insert_data(information)

def followers():
    initial_uid = 3006812112
    followers =get_followers(initial_uid)
    followers_ids = followers["ids"]
    for id in followers_ids:
        print id
        information = get_information(id)
        if information != None:
            insert_data(information)


if __name__ == "__main__":
    # followers()
    uid = 3006812112
    friends()
    # followers()
