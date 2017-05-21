#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu
# Most Recent Weibo
import json
import random
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

print "reading topics from 5-16"
with open('topic_list-5-16.txt') as f:
	content = f.readlines()
	for topic in content:
		topic_name = topic.rstrip()
		print "\n话题:"
		print topic_name
		train_set = []
		with open('weiboData/'+topic.rstrip()+'.txt') as data:
			for tweet in data.readlines():
				train_set.append(tweet)
		# print json.dumps(train_set,encoding='UTF-8',ensure_ascii=False)
		# 将结果存入文件
		sFilePath = '/Users/apple/scrapingEnv/weibo-summary/resultData/MostRecent'
		output_file = ""
		if not os.path.exists(sFilePath) :
		    os.mkdir(sFilePath)
		out = open(sFilePath + '/'+ topic_name +'-'+'MostRecent'+'.txt','w+')

		for i in xrange(0,4):
			print train_set[i]
			output_file = output_file + train_set[i]
		out.write(output_file)
		out.close()