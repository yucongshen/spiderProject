# !/usr/bin/python
# -*- coding:UTF-8 -*-

#改过代码里面的setupSoup里面的=headers
import os
from bs4 import BeautifulSoup
from webclient import WebBrowser
import time
def setupSoup(url):
    browser = WebBrowser(debug = False)
    headers = {
        'Host': 'bj.58.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cookie': 'id58=c5/ns1kKzfw3obBIA+xjAg==; commontopbar_city=1%7C%u5317%u4EAC%7Cbj; 58tj_uuid=131b47ad-b836-4545-944c-82acefff12b3; new_session=0; new_uv=1; utm_source=; spm=; init_refer=; ipcity=bj%7C%u5317%u4EAC%7C0; defraudName=defraud; als=0; commonTopbar_myfeet_tooltip=end'
    }
    content, rep_header = browser._request(url, headers = headers)
    soup=BeautifulSoup(content, 'html.parser', from_encoding = 'utf-8')
    title_302_tag = soup.find_all("title")
    if len(title_302_tag) != 0:
        title_302_tag=title_302_tag[0]
        if title_302_tag.string == "请输入验证码":
            print title_302_tag.string
            return None
    return soup

#得到一页手机详情
def get_phone_features(url):
    features={}
    features["title"] = ""
    features["money"] = ""
    features["room_type"] = ""
    features["address"] = ""
    features["lat"] = ""
    features["lon"] = ""
    features["id"] = ""
    browser = WebBrowser(debug=False)
    headers = {
        'Cookie': 'id58=jDEJK1i4vTyQBmCeFLyDSA==; cookieuid=d9d9e42e-e243-4133-bfef-a87756830db0; Hm_lvt_6cb5599f5beb8c077d7b770cc1a4f38d=1488502078; 58tj_uuid=172ffe55-7b87-4c76-a2a9-d8a9d2eb8ad0; new_uv=5; _ga=GA1.2.1225474288.1488502078'}
    if url[7:9] == "jx":
        url = url.replace(" ", "%20")
    content, rep_header = browser._request(url, headers=headers)
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    title_tag=soup.find_all(class_="meta-tit")
    if len(title_tag) == 0:
        print "there is no title_tag in get_phone_features"
    else:
        title_tag=title_tag[0]
        features["title"]=title_tag.string
    ul_detail_tag=soup.find_all(class_="houseInfo-detail bbOnepx")
    if len(ul_detail_tag) == 0:
        print "there is no ul_detail_tag in get_phone_features "
    else:
        ul_detail_tag=ul_detail_tag[0]
        li_detail_tags=ul_detail_tag.find_all("li")
        if len(li_detail_tags) != 3:
            print "there is no integrity li_detail_tags in get_phone_features"
        else:
            li_money=li_detail_tags[1]
            i_money=li_money.find_all("i")
            if len(i_money) == 0:
                print "there is no money i tag in get_phone_features"
            else:
                i_money=i_money[0]
                features["money"]=i_money.string.replace(" ", "").replace("\n", "")

            li_address=li_detail_tags[2]
            i_address=li_address.find_all("i")
            if len(i_address) == 0:
                print "there is no address i tag in get_phone_features"
            else:
                i_address=i_address[0]
                features["address"]=i_address.string

    ul_meta_tag=soup.find_all(class_="houseInfo-meta bbOnepx")
    if len(ul_meta_tag) == 0:
        print "there is no ul_meta_tag in get_phone_features"
    else:
        ul_meta_tag=ul_meta_tag[0]
        li_meta=ul_meta_tag.find_all("li")
        if len(li_meta) != 2:
            print "there is no integrity li room in get_phone_features"
        else:
            li_room=li_meta[1]
            span_room=li_room.find_all("span")
            if len(span_room) != 2:
                print "there is no integrity span_room in get_phone_features"
            else:
                room=span_room[0]
                features["room_type"]=room.string.replace(" ", "")

    script_tag = soup.find_all("script")
    if len(script_tag) < 5 :
        print "there is no script_tag in get_features"
    else:
        script_tag = script_tag[4]
        script = script_tag.string
        if script == None:
            print "script has no string"
        else:
            script_arrs = script.split("\n")
            if len(script_arrs) >= 8:
                lat_and_lon_arr = script_arrs[7]
                lat_and_lon_arrs = lat_and_lon_arr.split(",")
                for i in lat_and_lon_arrs:
                    if "\"lat\"" in i:
                        features["lat"] = i[6:]
                    if "\"lon\"" in i:
                        features["lon"] = i[6:]
            else:
                print "there is no lat and lon in get_features"
            if len(script_arrs) >=10:
                sid_arr = script_arrs[9]
                sid_arrs = sid_arr.split("\'")
                sid = sid_arrs[1]
                features["id"] = sid
            else:
                print "there is no sid in get_features"
    return features

#得到一页详情
def get_features(url):
    # url = 'http://jxjump.58.com/service?target=INKicKZPP1UEhIHuBQyP3HVk6MOpffA13j-bIiUeq6vS6UI2Ur6K93SPwy7LRseGvSjIQfQedPYdKftf5mAV2dsHjh8QsAp0fu3yKVPOPtUXxu4D5yfjteMxytthrUmom-kF6H8XeCVyBLAX8fznJX-Px5N1TLKOziqFmaedY6is57NkdXRy7vg4euiIN6Ts5ubTo0WZOKM&local=5992&pubid=10973506&apptype=0&psid=175545270195795872009504686&entinfo=29849496899370_0&cookie=||https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dw8aZQZYxYBLmKGgd9srL90jI-2ISBWuuGOJh-NfkZii%26wd%3D%26eqid%3Dd3b529ea00004e070000000659080a89|c5/ns1kIAi16TTZ A1vqAg=='
    browser = WebBrowser(debug=False)
    headers = {'Cookie': 'id58=jDEJK1i4vTyQBmCeFLyDSA==; cookieuid=d9d9e42e-e243-4133-bfef-a87756830db0; Hm_lvt_6cb5599f5beb8c077d7b770cc1a4f38d=1488502078; 58tj_uuid=172ffe55-7b87-4c76-a2a9-d8a9d2eb8ad0; new_uv=5; _ga=GA1.2.1225474288.1488502078'}
    if url[7:9] == "jx":
        url=url.replace(" ", "%20")
    content, rep_header = browser._request(url, headers=headers)
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    features={}
    features["title"]=""
    features["money"]=""
    features["room_type"]=""
    features["address"]=""
    features["lat"]=""
    features["lon"]=""
    features["id"]=""
    title_302_tag = soup.find_all("title")
    if len(title_302_tag) != 0:
        title_302_tag=title_302_tag[0]
        if title_302_tag.string == "请输入验证码":
            print title_302_tag.string
            if url[7:9] == "bj":
                variable=url[17:]
                phone_url_model = "http://m.58.com/bj/" + variable + "?reform=pcfront"
                features=get_phone_features(phone_url_model)
                print features["title"]
                return features
    title_tag=soup.find_all("h1")
    if len(title_tag) == 0:
        print "there is no title tag in get_feature"
    else:
        title_tag=title_tag[0]
        features["title"]=title_tag.string.replace(" ", "")
    house_desc_class_tag=soup.find_all(class_="house-desc-item")
    if len(house_desc_class_tag) == 0:
        print "there is no house_desc_class_tag in get_features"
    else:
        house_desc_class_tag=house_desc_class_tag[0]
        money_tag=house_desc_class_tag.find_all("b")
        if len(money_tag) == 0:
            print "there is no money tag in get_features"
        else:
            money_tag=money_tag[0]
            features["money"]=money_tag.string
        li_tags=house_desc_class_tag.find_all("li")
        if len(li_tags) != 6:
            print "there is no integrity li in get_features"
        else:
            room_tag=li_tags[1].find_all("span")
            if len(room_tag) != 2:
                print "there is no integrity room_tag in get_features"
            else:
                features["room_type"]=room_tag[-1].string.replace(" ", "")
            addr_tag=li_tags[3].find_all("a")
            if len(addr_tag) == 0:
                print "there is no addr_tag in get_features"
            else:
                addr_tag=addr_tag[0]
                if addr_tag.string ==None:
                    print "the address is none"
                else:
                    features["address"]=addr_tag.string.replace(" ", "")
    script_tag=soup.find_all("script")
    if len(script_tag) == 0:
        print "there is no script_tag in get_features"
    else:
        script_tag=script_tag[0]
        script=script_tag.string
        if script == None:
            print "script has no string"
        else:
            script_arrs=script.split("\n")
            if len(script_arrs) > 5:
                lat_and_lon_arr=script_arrs[5]
                lat_and_lon_arrs=lat_and_lon_arr.split(",")
                for i in lat_and_lon_arrs:
                    if "baidulat" in i:
                        features["lat"]=i[11:]
                    if "baidulon" in i:
                        features["lon"]=i[11:-1]
            else:
                print "there is no lat and lon in get_features"
            if len(script_arrs) > 7:
                sid_arr=script_arrs[7]
                sid_arrs=sid_arr.split("\'")
                sid=sid_arrs[1]
                features["id"]=sid
            else:
                print "there is no sid in get_features"
    return features



#得到一页的列表的url
def get_detail_url_list(url):
    one_list_url = []
    soup=setupSoup(url)
    if soup == None:
        print "请输入验证码,soup is none"
        if url[7:9] == "bj":
            variable = url[17:]
            phone_url_model = "http://m.58.com/bj/" + variable + "?reform=pcfront"
            # one_list_url=get_phone_detail_url_list(phone_url_model)
            return one_list_url

    class_des=soup.find_all(class_="des")
    if len(class_des) == 0:
        print "there is no class named .des in get_features"
    else:
        for des in class_des:
            a_tag=des.find_all("h2")[0].find_all("a")
            if len(a_tag) == 0:
                print "there is no a_tag in get_features"
            else:
                a_tag=a_tag[0]
                one_list_url.append(a_tag.get("href"))
    return one_list_url

def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

def print_dic(features):
    print features["title"]
    print features["money"]
    print features["room_type"]
    print features["address"]
    print features["lat"]
    print features["lon"]
    print features["id"]

def write_list_to_file(dic):
    filename = "ciyt_58.txt"
    fl = open(filename, "a")
    fl.write(dic["id"])
    fl.write(";")
    fl.write(dic["title"])
    fl.write(";")
    fl.write(dic["money"])
    fl.write(";")
    fl.write(dic["room_type"])
    fl.write(";")
    fl.write(dic["address"])
    fl.write(";")
    fl.write(dic["lat"])
    fl.write(";")
    fl.write(dic["lon"])
    fl.write(";")
    fl.write("\n")
    fl.close()


#输入朝阳区url
def get_sub_region_url(url):
    soup=setupSoup(url)
    sub_region_url = []
    if soup == None:
        print "请输入验证码,soup is none"
        if url[7:9] == "bj":
            variable = url[17:]
            phone_url_model = "http://m.58.com/bj/" + variable + "?reform=pcfront"
            # sub_region_url=get_phone_sub_region_url(phone_url_model)
            return sub_region_url
    area_list=soup.find_all(class_="arealist")
    if len(area_list) == 0:
        print "there is no area_list in get sub region url"
    else:
        area_list=area_list[0]
        href_tags=area_list.find_all("a")
        if len(href_tags) == 0:
            print "there is no href_tags in get_sub_region_url"
        else:
            for i in href_tags:
                sub_region_url.append("http://bj.58.com"+i.get("href"))
    return sub_region_url


def get_next_page_url(url):
    soup = setupSoup(url)
    next_page_url=""
    if soup == None:
        print "请输入验证码,soup is none"
        if url[7:9] == "bj":
            variable = url[17:]
            phone_url_model = "http://m.58.com/bj/" + variable + "?reform=pcfront"
            # next_page_url=get_phone_next_page_url(phone_url_model)
            return next_page_url
    next_tag = soup.find_all(class_="next")
    if len(next_tag) == 0:
        print "there is no next_tag in get_all_page_url_list"
    else:
        next_tag=next_tag[0]
        next_page_url=next_tag.get("href")
    return next_page_url

def get_all_page_url_list(url):
    all_pages_url=[]
    all_pages_url.append(url)
    next_page_url=url
    while next_page_url != "":
        next_page_url=get_next_page_url(next_page_url)
        if next_page_url != "":
            all_pages_url.append(next_page_url)
    return all_pages_url



def get_all(url):
    # 访问所有
    filename="city_58.txt"
    delete_file(filename)
    sub_region_urls=get_sub_region_url(url)
    for sub_region_url in sub_region_urls[5:]:
        print "sub_region_url....", sub_region_url
        all_page_list=get_all_page_url_list(sub_region_url)
        # time.sleep(1)
        for one_page_url in all_page_list:
            print "one page url...", one_page_url
            detail_list_url=get_detail_url_list(one_page_url)
            # time.sleep(1)
            for detail_url in detail_list_url:
                print "detail_url...", detail_url
                features=get_features(detail_url)
                # time.sleep(0.2)
                write_list_to_file(features)
            print "\n"

#页面关键字
def get_key_all(url):
    page_list = get_all_page_url_list(url)
    for one_page_url in page_list:
        print "one page url...", one_page_url
        detail_list_url = get_detail_url_list(one_page_url)
        # time.sleep(1)
        for detail_url in detail_list_url:
            print "detail_url...", detail_url
            features = get_features(detail_url)
            # time.sleep(0.5)
            write_list_to_file(features)
        print "\n"
#对list格式化输出
def print_list(list):
    for i in list:
        print i

if __name__ == "__main__":
    url_chaoyang="http://bj.58.com/chaoyang/hezu"
    url_haidian="http://bj.58.com/haidian/chuzu"
    url_shigezhuang = "http://bj.58.com/chuzu/?key=%E5%8F%B2%E5%90%84%E5%BA%84"
    url_picun = "http://bj.58.com/chuzu/?key=%E7%9A%AE%E6%9D%91"
    url_songzhuang = "http://bj.58.com/chuzu/?key=%E5%AE%8B%E5%BA%84"
    get_all(url_haidian)
    # phone_url = 'http://m.58.com/bj/hezu/29839576662600x.shtml?reform=pcfront'
    # get_phone_features(phone_url)
    # get_key_all(url_picun)
    # get_features("http://bj.58.com/hezu/29847462488617x.shtml")
    # url = 'http://jxjump.58.com/service?target=INKicKZPP1XJ2FI5AKZJ7lFm4eEH5-It-Q0EzRwdLL7bUBSQIdcg3wuof1OgHjeW1JZDs3uuxzAzKpzyrwFfS1d1R3BxuU5S0E1FDUub3jY2Izz4Hh89BIjuQ2ZWxh8s1AO2gSPrtlgeyFVcrgA_hVYc4DIqiidRL4erNs1uS6oJe4wfMIlDHFMEma0sM7xA5VsxGDbWtvM&local=7409&pubid=11168226&apptype=0&psid=190432986195805873817285016&entinfo=29916534671663_0&cookie=|||c5/ns1kIVLAJLDJoA5lPAg=='
    # url_rr="http://bj.58.com/hezu/29839576662600x.shtml"
    # phone_url='http://m.58.com/bj/hezu/29839576662600x.shtml?reform=pcfront'
    # print_dic(get_features(url_rr))

    # url_rr = "http://bj.58.com/hezu/29839576662600x.shtml"
    # phone_url = 'http://m.58.com/bj/hezu/29839576662600x.shtml?reform=pcfront'
    # print url_rr[17:]


    # get_all(url_chaoyang)
    # setupSoup("http://callback.58.com/firewall/valid/3550328212.do?namespace=hezuphp&url=bj.58.com%2Fhezu%2F29927656972088x.shtml")

    #得到一个分区的数据
    # all_page_list = get_all_page_url_list("http://bj.58.com/aolinpikegognyuan/chuzu/?PGTID=0d3090a7-0047-6240-d9ea-6f841e6690c8&ClickID=4")
    # time.sleep(1)
    # for one_page_url in all_page_list:
    #     print "one page url...", one_page_url
    #     detail_list_url = get_detail_url_list(one_page_url)
    #     # time.sleep(1)
    #     for detail_url in detail_list_url:
    #         print "detail_url...", detail_url
    #         features = get_features(detail_url)
    #         # time.sleep(1)
    #         write_list_to_file(features)
    #     print "\n"


    # filname="makup.txt"
    # file = open(filname)
    # while 1:
    #     line = file.readline()
    #     if not line:
    #         break
    #     features=get_features(line)
    #     write_list_to_file(features)

    # print_dic(get_features("http://bj.58.com/zufang/27892239940432x.shtml"))
    # print_dic(get_features("http://bj.58.com/hezu/29272160039087x.shtml"))

    #单独运行这句不能访问 ERROR 505 HTTP Error 505: HTTP Version Not Supported
    # print_dic(get_features("http://jxjump.58.com/service?target=INKicKZPP1UEhIHuBQyP3HVk6MOpffA13j-bIiUeq6vS6UI2Ur6K93SPwy7LRseGvSjIQfQedPYdKftf5mAV2dsHjh8QsAp0fu3yKVPOPtUXxu4D5yfjteMxytthrUmom-kF6H8XeCVyBLAX8fznJX-Px5N1TLKOziqFmaedY6is57NkdXRy7vg4euiIN6Ts5ubTo0WZOKM&local=5992&pubid=10973506&apptype=0&psid=175545270195795872009504686&entinfo=29849496899370_0&cookie=||https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dw8aZQZYxYBLmKGgd9srL90jI-2ISBWuuGOJh-NfkZii%26wd%3D%26eqid%3Dd3b529ea00004e070000000659080a89|c5/ns1kIAi16TTZ%20A1vqAg=="))

    # get_features("http://bj.58.com/hezu/29791399620672x.shtml")

    # print_list(get_sub_region_url(url_chaoyang))
    # url_anhuiqiao=get_sub_region_url(url_chaoyang)[0]
    # print_list(get_all_page_url_list(url_anhuiqiao))
    # print url_anhuiqiao
    # # print_list(get_detail_url_list(url_anhuiqiao))
    # # print len(get_detail_url_list(url_anhuiqiao))
    # one_feature_url=get_detail_url_list(url_anhuiqiao)[-1]
    # features=get_features(one_feature_url)
    # write_list_to_file(features)

    # 将一页列表写入文件中
    # for url in get_detail_url_list(url_anhuiqiao):
    #     print url
    #     features=get_features(url)
    #     write_list_to_file(features)
    #     print "\n"







