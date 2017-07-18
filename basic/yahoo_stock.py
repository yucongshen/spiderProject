# !/usr/python/bin
# -*- coding: UTF-8 -*-
import urllib

import datetime


def download_stock_data(stock_list):
    for sid in stock_list:
        url = 'http://table.finance.yahoo.com/table.csv?s=' + sid
        filename=sid + '.csv'
        print ("download %s from %s " %(filename, url))
        urllib.urlretrieve(url, filename)

def download_stock_data_in_period(stock_list, start, end):
    for sid in stock_list:
        params={'a':start.month-1, 'b':start.day, 'c':start.year, 'd':end.month-1, 'e':end.day, 'f':end.year, 's':sid}
        url="http://table.finance.yahoo.com/table.csv?"
        qs=urllib.urlencode(params)
        url=url+qs
        fname="%s_%d%d%d_%d%d%d.csv" %(sid, start.year, start.month, start.day, end.year, end.month, end.day)
        print ("download %s from %s" %(fname, url))
        urllib.urlretrieve(url, fname, reporthook=progress)
#下载进度（当前传输的块数，块大小，数据总大小）
def progress(blk, blk_size, total_size):
    print ('%d/%d - %.02f%%' %(blk * blk_size, total_size, (float)(blk*blk_size)*100/total_size ))

if __name__ == '__main__':
    stock_list=['300001.sz', '310002.sz']
    # download_stock_data(stock_list)
    start=datetime.date(year=2015, month=11, day=17)
    end=datetime.date(year=2015, month=12, day=17)
    download_stock_data_in_period(stock_list, start, end)


