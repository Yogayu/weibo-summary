#-*- encoding:utf-8 -*-
from utilities import *
from weiboApplication.weiboModel import *
import os
import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

print "reading topics from topicList"
with open('topicList.txt') as f:
    content = f.readlines()
    for topic in content:
        print "\n话题:"
        topic_name = topic.rstrip()
        
        summaryItems = []

        path = "ROUGE/manual_sentences/" + topic_name + ".txt"
        if os.path.exists(path):
            with open(path) as data:
                for tweet in data.readlines():
                    summaryItems.append(Summary(topic_name,tweet,"","Manual1"))

	        segment_set = get_segment_set(path)
	        json_print(segment_set)

	        sFilePath = 'ROUGE/test-summarization/reference/'
	        output_file = ""
	        if not os.path.exists(sFilePath):
	            os.mkdir(sFilePath)
	        # out = open(sFilePath + topic_name + '_Reference3.txt', 'w+')

            for i in xrange(0, len(segment_set)):
                output_file += segment_set[i] + '\n'
                summaryItems[i].content_segment = segment_set[i]

	        # out.write(output_file)
	        # out.close()
        # save to the database
        for summaryItem in summaryItems:
            summaryItem.add()