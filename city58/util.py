# !/usr/bin/python
# -*- coding:UTF-8 -*-
if __name__ == "__main__":
    source_filname="12"
    goal_filename="buchong-xingong.txt.txt"
    source_file=open(source_filname)
    goal_file = open(goal_filename, "a")
    while 1:
        line = source_file.readline()
        if line == "":
            break
        goal_file.write(line)
    source_file.close()
    goal_file.close()
