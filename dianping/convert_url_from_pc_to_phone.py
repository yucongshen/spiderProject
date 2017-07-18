# !/usr/bin/python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
from webclient import WebBrowser
from headers import pc_headers
from headers import phone_headers
import spynner


def convert_url_from_pc_to_phone(self, pc_url):
    phone_url=""
    if "shop" in pc_url:
        index_shop=pc_url.index("shop/")+len("shop/")
        shop_id=pc_url[index_shop:]
        phone_url="http://m.dianping.com/shop/"+shop_id+"?from=shoplist&shoplistqueryid=b1a1d852-61b9-425c-8d58-0f1428359710"
    else:
        category_index = pc_url.index("/g") + len("/g")
        category_and_region = pc_url[category_index:]
        if "r" in category_and_region:
            cr_arry=category_and_region.split("r")
            if len(cr_arry) == 2:
                category=cr_arry[0]
                region=cr_arry[1]
                phone_url="http://m.dianping.com/shoplist/2/r/"+region+"/c/"+category+"/s/s_-1?from=m_nav_1_meishi"
            else:
                print "phone_url error......"
        else:
            phone_url = "http://m.dianping.com/shoplist/2/d/1/c/" + category_and_region + "/s/s_-1?from=m_nav_1_meishi"
    return phone_url

if __name__ == "__main__":
    phone_url_huoguo = "http://m.dianping.com/shoplist/2/d/1/c/110/s/s_-1?from=m_nav_1_meishi"
    pc_url_huoguo = "https://www.dianping.com/search/category/2/10/g110"
    pc_url_huoguo_chaoyang = "https://www.dianping.com/search/category/2/10/g110r14"
    pc_url_huoguo_chaoyang_sanlitun="https://www.dianping.com/search/category/2/10/g110r2580"
    pc_url_detail="https://www.dianping.com/shop/67001760"
    # convert_url_from_pc_to_phone(pc_url_detail)
    # setupSoup(pc_url_detail)

