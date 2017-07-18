# !/usr/python/bin
# -*- coding: UTF-8 -*-
import urllib

def print_list(list):
    for i in list:
        print i

#下面的方法保存了一个kamidox.html文件
#reporthook=progress显示了一个下载进度
def retrieve():
    filename, msg = urllib.urlretrieve("http://blog.kamidox.com", "kamidox.html", reporthook=progress)
    print filename
    print_list(msg)

#下载进度（当前传输的块数，块大小，数据总大小）
def progress(blk, blk_size, total_size):
    print ('%d/%d - %.02f%%' %(blk * blk_size, total_size, (float)(blk*blk_size)*100/total_size ))

if __name__ == '__main__':
    retrieve()