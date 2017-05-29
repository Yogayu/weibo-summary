#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu
# Choice a Random Sentence as the summary

import random
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append('../')
from app import Summary
from config import *
from utilities import *

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1 or args[0] == 'None':
        print('error args - Topic')
        exit()
    topic_name = args[0]
    print ("topic_name")
    print (topic_name)

    topic = topic_name

    train_set = []
    summaryItems = []
    file_path = get_base_dir() + '/Data/weiboData/' +topic.rstrip()+'.txt'
    with open(file_path) as data:
        for tweet in data.readlines():
            train_set.append(tweet)
    
    # 将结果存入文件
    rFilePath = get_result_data_path() + '/Random'
    sFilePath = get_rouge_sum_path()
    # 完整摘要放入ResultData
    result_output_file = ""
    # 分词的摘要放入ROUGE-Summary
    segment_output_file = ""

    sub_path = '/' + topic_name + '_RandomSyssum' +'.txt'

    if not os.path.exists(sFilePath):
        os.mkdir(sFilePath)
    segment_out = open(sFilePath + sub_path, 'w+')

    if not os.path.exists(rFilePath):
        os.mkdir(rFilePath)
    result_out = open(rFilePath + sub_path, 'w+')

    for i in xrange(0,5):
        random_num = random.randint(0, len(train_set)-1)
        print train_set[random_num]
        result_output_file += train_set[random_num]
        summaryItems.append(Summary(topic_name,train_set[random_num],"","Random"))

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