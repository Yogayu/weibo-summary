#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu
# Choice a Random Sentence as the summary
from utilities import *

import random
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

print(20*'-')
print "Random"
print "reading topics from topicList"
with open('topicList.txt') as f:
    content = f.readlines()
    for topic in content:
        topic_name = topic.rstrip()
        print "\n话题:"
        print topic_name
        train_set = []
        with open('weiboData/'+topic.rstrip()+'.txt') as data:
            # with open('weiboData/'+'#北京电影学院性侵案#'+'.txt') as data:
            for tweet in data.readlines():
                train_set.append(tweet)
        # print json.dumps(train_set,encoding='UTF-8',ensure_ascii=False)
        
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

        result_out.write(result_output_file)
        result_out.close()

        segment_set = get_segment_set(rFilePath + sub_path)
        for line in segment_set:
            segment_output_file += line + '\n'
        segment_out.write(segment_output_file)
        segment_out.close()
print(20*'-')