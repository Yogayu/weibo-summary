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

print(20*'-')
print ("TextRank")

with open('topicList.txt') as f:
    content = f.readlines()
    for topic in content:
        topic_name = topic.rstrip()
        file_path = 'weiboData/'+topic_name+'.txt'
        text = codecs.open(file_path, 'r', 'utf-8').read()

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

        print('关键词：')
        for item in tr4w.get_keywords(20, word_min_len=1):
            print(item.word, item.weight)

        print()
        print('关键短语：')
        for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num=2):
            print(phrase)

        tr4s = TextRank4Sentence()
        tr4s.analyze(text=text, lower=True, source='all_filters')

        print()
        print('摘要：')
        for item in tr4s.get_key_sentences(num=5):
            result_output_file += item.sentence + '\n'
            print(item.index, item.weight, item.sentence)

        result_out.write(result_output_file)
        result_out.close()

        segment_set = get_segment_set(rFilePath + sub_path)
        for line in segment_set:
            segment_output_file += line + '\n'
        segment_out.write(segment_output_file)
        segment_out.close()
print(20*'-')