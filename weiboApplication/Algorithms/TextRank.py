#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu

from __future__ import print_function
from utilities import *

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
from app import Summary
from config import *
from utilities import *

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1 or args[0] == 'None':
        print('error args - Topic')
        exit()
    topic = args[0]
    print ("TextRank")
    print (topic)

    topic_name = topic.rstrip()
    file_path = get_base_dir() + '/Data/weiboData/' +topic_name+'.txt'
    text = codecs.open(file_path, 'r', 'utf-8').read()

    summaryItems = []

    # sFilePath = 'resultData/textrank'
     # 将结果存入文件
    rFilePath = get_result_data_path() + '/TextRank'
    sFilePath = get_rouge_sum_path()
    # 完整摘要放入ResultData
    result_output_file = ""
    # 分词的摘要放入ROUGE-Summary
    segment_output_file = ""

    sub_path = '/' + topic_name + '_TextRankSyssum' +'.txt'

    if not os.path.exists(sFilePath):
        os.mkdir(sFilePath)
    segment_out = open(sFilePath + sub_path, 'w+')

    if not os.path.exists(rFilePath):
        os.mkdir(rFilePath)
    result_out = open(rFilePath + sub_path, 'w+')
    
    tr4w = TextRank4Keyword()

    # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
    tr4w.analyze(text=text, lower=True, window=2)

    # print('关键词：')
    # for item in tr4w.get_keywords(20, word_min_len=1):
    #     print(item.word, item.weight)

    # print('关键短语：')
    # for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num=2):
    #     print(phrase)

    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source='all_filters')

    print('摘要：')
    for item in tr4s.get_key_sentences(num=5):
        result_output_file += item.sentence + '\n'
        summaryItems.append(Summary(topic_name,item.sentence,"","TextRank"))
        print(item.index, item.weight, item.sentence)

    result_out.write(result_output_file)
    result_out.close()

    segment_set = get_segment_set(rFilePath + sub_path)
    for i in xrange(0, len(segment_set)):
        segment_output_file += segment_set[i] + '\n'
        summaryItems[i].content_segment = segment_set[i]

    segment_out.write(segment_output_file)
    segment_out.close()

    # save to the database
    for summaryItem in summaryItems:
        summaryItem.add()
print(20*'-')