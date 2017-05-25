#-*- encoding:utf-8 -*-
from utilities import *
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
        path = "ROUGE/manual_sentences/" + topic_name + ".txt"
        if os.path.exists(path):
	        segment_set = get_segment_set(path)
	        json_print(segment_set)

	        sFilePath = 'ROUGE/test-summarization/reference/'
	        output_file = ""
	        if not os.path.exists(sFilePath):
	            os.mkdir(sFilePath)
	        out = open(sFilePath + topic_name + '_Reference2.txt', 'w+')

	        for line in segment_set:
	            output_file += line + '\n'

	        out.write(output_file)
	        out.close()