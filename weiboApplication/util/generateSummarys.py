#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu
import subprocess
import sys, os
sys.path.append('../')
from config import *

# 设置编码格式
reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1 or args[0] == 'None':
        print('error args - Summary')
        exit()
    topic_name = args[0]
    file_path = get_base_dir()

# 生成算法摘要并存入数据库
random = subprocess.Popen(["python", get_base_dir() + "/Algorithms/Random.py", topic_name]); random.wait()

MostRecent   = subprocess.Popen(["python", get_base_dir() + "/Algorithms/MostRecent.py", topic_name]); MostRecent.wait()

TFIDF        = subprocess.Popen(["python", get_base_dir() + "/Algorithms/TFIDF.py", topic_name]); TFIDF.wait()

HybirdTFIDF  = subprocess.Popen(["python", get_base_dir() + "/Algorithms/Hybird-TFIDF.py", topic_name]); HybirdTFIDF.wait()

TextRank     = subprocess.Popen(["python", get_base_dir() + "/Algorithms/TextRank.py", topic_name]); TextRank.wait()
