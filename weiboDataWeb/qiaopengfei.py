# !/usr/bin/python
# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
from webclient import WebBrowser
def fangwenliang(url):
    browser = WebBrowser(debug = False)
    qq_headers = {
        # ':authority':'user.qzone.qq.com',
        # ':method':'GET',
        # ':path': '/ 949936589',
        # ':scheme':'https',
        'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'accept-encoding':'gzip, deflate, br',
        'accept-language':'zh-CN,zh;q=0.8,en;q=0.6',
        'cache-control':'max-age=0',
        'cookie':'pgv_pvi=6791201792; pac_uid=0_5955b60201580; pgv_pvid=4875331760; _qpsvr_localtk=0.02503945741392255; pgv_si=s1896761344; RK=QPsDA3NbYS; zzpaneluin=; zzpanelkey=; pgv_info=ssid=s6759833015; ptisp=ctc; ptcz=2fa4037d13f9bbe09900f616186530c3ac8cd447d900c370437b9463c32d65ba; pt2gguin=o0490603883; uin=o0490603883; skey=@o9KAYMUtl; p_uin=o0490603883; p_skey=WUZxHekeEnzDvkmBgcLu1G7TBu7iVvvw8aYKXz3-6Kg_; pt4_token=4IDBLQoBErmzqHsYA734MvwCyGh6EW6U7yWeuvhgBfk_; rv2=806156949413FC303AFB946C063CF9874DF8CC3536A2627F6D; property20=6384D16746313DCA024671D3D1D254D3D51B4A0354BD26219F387BAAB3371527FF5BF4CEDD4C92D6; qqmusic_uin=; qqmusic_key=; qqmusic_fromtag=; qzmusicplayer=qzone_player_949936589_1500274200601if-modified-since:Mon, 17 Jul 2017 06:49:58 GMT',
        'upgrade-insecure-requests':'1',
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
    }
    content, rep_header = browser._request(url, headers = qq_headers)
    print content
    return content

if __name__ == "__main__":
    url = "https://user.qzone.qq.com/949936589"
    fangwenliang(url)