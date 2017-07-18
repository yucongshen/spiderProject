# !/usr/bin/python
# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
from webclient import WebBrowser
from headers import headers
from util import set_blank_features
import spynner
from util import print_features
from util import write_feautres_to_file
from util import delete_file
def get_cookie(browser):
    phoenixid=""
    jsessionid=""
    hcv=""
    for cookie in browser.cookiesjar.allCookies():
        print cookie.name()
        if cookie.name() == 'PHOENIX_ID':
            phoenixid = 'PHOENIX_ID=' + cookie.value()
        elif cookie.name() == '_hc.v':
            hcv = '_hc.v=' + cookie.value()
        elif cookie.name() == 'JSESSIONID':
            jsessionid = 'JSESSIONID=' + cookie.value()
    cookies=phoenixid + ";" + jsessionid + ";" +hcv
    return cookies
def setupSoup(url):
    browser = WebBrowser(debug = False)
    content, rep_header = browser._request(url, headers=headers)
    headers_jx = {
        'Cookie': 'id58=jDEJK1i4vTyQBmCeFLyDSA==; cookieuid=d9d9e42e-e243-4133-bfef-a87756830db0; Hm_lvt_6cb5599f5beb8c077d7b770cc1a4f38d=1488502078; 58tj_uuid=172ffe55-7b87-4c76-a2a9-d8a9d2eb8ad0; new_uv=5; _ga=GA1.2.1225474288.1488502078'}
    if url[7:9] == "jx":
        url = url.replace(" ", "%20")
        content, rep_header = browser._request(url, headers=headers_jx)
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    title_302_tag = soup.find_all("p", class_ = "title")
    if len(title_302_tag) != 0:
        title_302_tag = title_302_tag[0]
        if title_302_tag.string == "访问过于频繁，本次访问需要输入验证码":
            print title_302_tag.string
            phone_url = 'http://m.dianping.com'
            browser_spy = spynner.Browser()
            browser_spy.hide()
            browser_spy.load(phone_url, load_timeout=10, tries=2)
            cookies = get_cookie(browser_spy)
            headers["Cookie"] = cookies
            print headers["Cookie"]
            pc_content, pc_rep_header = browser._request(url, headers=headers)
            soup = BeautifulSoup(pc_content, 'html.parser', from_encoding='utf-8')
    return soup

#得到一页详情
def get_features(url, retry = 0):
    # url = 'http://jxjump.58.com/service?target=INKicKZPP1UEhIHuBQyP3HVk6MOpffA13j-bIiUeq6vS6UI2Ur6K93SPwy7LRseGvSjIQfQedPYdKftf5mAV2dsHjh8QsAp0fu3yKVPOPtUXxu4D5yfjteMxytthrUmom-kF6H8XeCVyBLAX8fznJX-Px5N1TLKOziqFmaedY6is57NkdXRy7vg4euiIN6Ts5ubTo0WZOKM&local=5992&pubid=10973506&apptype=0&psid=175545270195795872009504686&entinfo=29849496899370_0&cookie=||https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3Dw8aZQZYxYBLmKGgd9srL90jI-2ISBWuuGOJh-NfkZii%26wd%3D%26eqid%3Dd3b529ea00004e070000000659080a89|c5/ns1kIAi16TTZ A1vqAg=='
    browser = WebBrowser(debug=False)
    headers = {'Cookie': 'id58=jDEJK1i4vTyQBmCeFLyDSA==; cookieuid=d9d9e42e-e243-4133-bfef-a87756830db0; Hm_lvt_6cb5599f5beb8c077d7b770cc1a4f38d=1488502078; 58tj_uuid=172ffe55-7b87-4c76-a2a9-d8a9d2eb8ad0; new_uv=5; _ga=GA1.2.1225474288.1488502078'}
    if url[7:9] == "jx":
        url=url.replace(" ", "%20")
    content, rep_header = browser._request(url, headers=headers)
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    features = set_blank_features()
    features["url"] = url
    title_tag=soup.find_all("h1")
    if len(title_tag) == 0:
        print "there is no title tag in get_feature"
    else:
        title_tag=title_tag[0]
        features["title"]=title_tag.string.replace(" ", "").replace("\n", "")
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
            features["money"]=money_tag.string.replace(" ", "").replace("\n", "")
        li_tags=house_desc_class_tag.find_all("li")
        if len(li_tags) != 6:
            print "there is no integrity li in get_features"
        else:
            room_tag=li_tags[1].find_all("span")
            if len(room_tag) != 2:
                print "there is no integrity room_tag in get_features"
            else:
                features["room_type"]=room_tag[-1].string.replace(" ", "").replace("\n", "")
            rent_type_tag = li_tags[0].find_all("span")
            if len(rent_type_tag) == 0:
                print "rent type tag is not find"
            else:
                rent_type_tag = rent_type_tag[-1]
                str = rent_type_tag.string
                if str == None:
                    print "rent type tag is None"
                else:
                    features["rent_type"] = str.replace("\n", "").replace(" ", "")
            addr_tag=li_tags[3].find_all("a")
            if len(addr_tag) == 0:
                print "there is no addr_tag in get_features"
            else:
                addr_tag=addr_tag[0]
                if addr_tag.string ==None:
                    print "the address is none"
                else:
                    features["residential"]=addr_tag.string.replace(" ", "").replace("\n", "")
    em_tag = soup.find_all("em", class_ = "dt c_888 f12")
    if len(em_tag) == 0:
        print "there is no detail address in class dt c_888 f12"
    else:
        em_tag =em_tag[0]
        addr = em_tag.string
        if addr == None:
            print "detail address is none"
        else:
            features["address"] = addr.replace(" ", "").replace("\n", "")
    deposit_tag = soup.find_all(class_ = "house-pay-way f16")
    if len(deposit_tag) == 0:
        print "there is no deposit find"
    else:
        deposit_tag = deposit_tag[0]
        str_d = deposit_tag.contents[-1].string
        if str_d == None:
            print "deposit_tag is none"
        else:
            features["deposit"] = str_d.replace(" ", "").replace("\n", "")
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
                features["id"]=sid.replace(" ", "").replace("\n", "")
            else:
                print "there is no sid in get_features"
    return features

#得到一页的列表的url
def get_detail_url_list(url):
    one_list_url = []
    soup = setupSoup(url)
    class_des = soup.find_all(class_="des")
    if len(class_des) == 0:
        print "there is no class named .des in get_features"
    else:
        for des in class_des:
            a_tag = des.find_all("h2")[0].find_all("a")
            if len(a_tag) == 0:
                print "there is no a_tag in get_features"
            else:
                a_tag = a_tag[0]
                one_list_url.append(a_tag.get("href"))
    return one_list_url

def get_next_page_url(url):
    soup = setupSoup(url)
    next_page_url=""
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

def get_all_pages_features(url_all_pages):
    filename = "data/daxing-xingong-geren.txt"
    delete_file("data/daxing-xingong-geren.txt")
    all_pages_list = get_all_page_url_list(url_all_pages)
    for one_page in all_pages_list:
        print "one_page......", one_page
        list = get_detail_url_list(one_page)
        for i in list:
            print "detail url......", i
            features = get_features(i)
            write_feautres_to_file(features, filename)

if __name__ == "__main__":
    xingong = "http://bj.58.com/zufang/sub/l573045/s573046/0/j2/?pagetype=ditie&PGTID=0d300008-0000-1108-19cf-8a6d980326e7&ClickID=2"
    get_all_pages_features(xingong)