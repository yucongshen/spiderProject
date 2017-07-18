# !/usr/python/bin
# -*- coding : UTF-8 -*-
import os
import pandas as pd
def csv_merge(flist,fo,cols=None,encoding='utf-8'):# encoding='gbk'
    l=len(flist)
    for i in range(l):
        s=pd.read_csv(flist[i],index_col=None, header=0, usecols=cols, na_values=[''],encoding=encoding)
        if i==0:
            s.to_csv(fo,encoding=encoding, index=False)
        else:
            s.to_csv(fo,encoding=encoding,mode='a', header=False, index=False)

def get_filename(secondary_dir_path, number):
    file_list=os.listdir(secondary_dir_path)
    for file in file_list:
        filename=secondary_dir_path + "\\" +file
        if filename[-5] == number and filename[-3:] == "csv" :
            return filename


def judge_number(dirname, number):
    filename_list= os.listdir(dirname)
    for filename in filename_list:
        if number in filename:
            return True
    return False

def scan_dir(dirname):
    final_file_list=[]
    secondary_dir_list = os.listdir(dirname)
    for secondary_dir in secondary_dir_list:
        secondary_dir_path=dirname + "\\" + secondary_dir
        if judge_number(secondary_dir_path, "2"):
            filename=get_filename(secondary_dir_path, "2")
            final_file_list.append(filename)
        elif judge_number(secondary_dir_path, "1"):
            filename=get_filename(secondary_dir_path, "1")
            final_file_list.append(filename)
        elif judge_number(secondary_dir_path, "0"):
            filename=get_filename(secondary_dir_path, "0")
            final_file_list.append(filename)
    return final_file_list


if __name__ == "__main__":
    final_file_list=scan_dir("C:\Users\shenyucong\Desktop\yyy")
    out1 = "C:\Users\shenyucong\Desktop\yyy\cew_csv1.csv"
    csv_merge(final_file_list, out1)