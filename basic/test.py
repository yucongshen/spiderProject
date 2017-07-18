# !/usr/python/bin
# -*- coding: UTF-8 -*-
import sys
import os
# 遍历指定目录，显示目录下的所有文件名
def eachFile(filepath):
    # 先得到大目录下面所有的小目录，放到all_dirs中
    pathDir =  os.listdir(filepath)
    all_dirs=[]
    for allDir in pathDir:
        child = os.path.join(allDir)
        all_dirs.append(child)
    #遍历all_dirs中的所有小目录，得到小目录里面的文件
    for dir in all_dirs:
        subDir = os.listdir(filepath+"/"+dir)
        for dir in subDir:
            child = os.path.join(dir)
            print child

def get_child_files(filepath):
    # 先得到大目录下面所有的小目录，放到all_dirs中
    pathDir =  os.listdir(filepath)
    all_dirs=[]
    for allDir in pathDir:
        child = os.path.join(allDir)
        all_dirs.append(child)
    return all_dirs

def test(filename):
    dirs=get_child_files(filename)
    for dir in dirs:
        dir=filename+"\\"+dir
        childs=get_child_files(dir)
        new_file=open("D:\\eee\\cc\\newfile.csv", "a")
        for child in childs:
            child_filename=dir+"\\"+child
            print child_filename
            f=open(child_filename, "r")
            arr_line=f.readlines()
            for i in range(1, len(arr_line)):
                new_file.write(arr_line[i])

if __name__ == "__main__":
    filename = "D:\\eee"
    print sys.getdefaultencoding()
    # test(filename)
    # eachFile("D:\shenyucong")