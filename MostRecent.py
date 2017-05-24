#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu
# Most Recent Weibo

from utilities import *
import random
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

print "Recent"
print "reading topics from topicList"
with open('topicList.txt') as f:
    content = f.readlines()
    for topic in content:
        topic_name = topic.rstrip()
        print "\n话题:"
        print topic_name
        train_set = []
        with open('weiboData/'+topic_name+'.txt') as data:
            for tweet in data.readlines():
                train_set.append(tweet)
        # json_print(train_set,encoding='UTF-8',ensure_ascii=False)
        # 将结果存入文件
        rFilePath = get_result_data_path() + '/MostRecent'
        sFilePath = get_rouge_sum_path()
        # 完整摘要放入ResultData
        result_output_file = ""
        # 分词的摘要放入ROUGE-Summary
        segment_output_file = ""

        sub_path = '/' + topic_name + '_MostRecentSyssum' + '.txt'

        if not os.path.exists(sFilePath):
            os.mkdir(sFilePath)
        segment_out = open(sFilePath + sub_path, 'w+')

        if not os.path.exists(rFilePath):
            os.mkdir(rFilePath)
        result_out = open(rFilePath + sub_path, 'w+')

        for i in xrange(0, 5):
            print train_set[i]
            result_output_file += train_set[i]

        result_out.write(result_output_file)
        result_out.close()

        segment_set = get_segment_set(rFilePath + sub_path)
        for line in segment_set:
            segment_output_file += line + '\n'
        segment_out.write(segment_output_file)
        segment_out.close()
print(20*'-')
