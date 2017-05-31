#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu

import os
import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

sys.path.append('../')
sys.path.append('../Algorithms/')
from app import Summary
from config import *
from utilities import *

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 2 or args[0] == 'None' or args[1] == 'None':
        print('error args - Manual')
        exit()
    topic = args[0]
    method = args[1]
    print ("topic_name")
    print (topic)
    print (method)

    topic_name = topic.rstrip()
    
    summaryItems = []

    path = get_base_dir() + "/Data/ROUGE/manual_sentences/" + topic_name + '-' + method + ".txt"
    if os.path.exists(path):
        with open(path) as data:
            for tweet in data.readlines():
                summaryItems.append(Summary(topic_name,tweet,"",method))

        segment_set = get_segment_set(path)
        json_print(segment_set)

        sFilePath = get_base_dir() + '/Data/ROUGE/test-summarization/reference/'
        output_file = ""
        if not os.path.exists(sFilePath):
            os.mkdir(sFilePath)

        method_num = method.replace('manual','')
        
        out = open(sFilePath + topic_name + '_Reference' + method_num +'.txt', 'w+')

        for i in xrange(0, len(segment_set)):
            output_file += segment_set[i] + '\n'
            summaryItems[i].content_segment = segment_set[i]

        out.write(output_file)
        out.close()
    # save to the database
    for summaryItem in summaryItems:
        summaryItem.add()