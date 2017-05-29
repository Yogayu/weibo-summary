#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu

from __future__ import print_function
# from utilities import *

import sys
import os
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence

sys.path.append('../')
from app import Keywords
from config import *

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1 or args[0] == 'None':
        print('error args - Topic')
        exit()
    topic_name = args[0]
    print ("topic_name")
    print (topic_name)


    file_path = get_base_dir() + '/Data/weiboData/'+topic_name+'.txt'

    text = codecs.open(file_path, 'r', 'utf-8').read()

    keywordItems = []

    tr4w = TextRank4Keyword()

    # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
    tr4w.analyze(text=text, lower=True, window=2)

    print('关键词：')
    for item in tr4w.get_keywords(30, word_min_len=2):
        print (str(item.word))
        print (float(item.weight))
        keywordItems.append(Keywords(topic_name,str(item.word),float(item.weight)))
        # print(item.word, item.weight)

    print('关键短语：')
    for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num=2):
        print(phrase)

    # save to the database
    for keywordItem in keywordItems:
        print (keywordItem)
        keywordItem.add()
print(20*'-')