#-*- encoding:utf-8 -*-
from __future__ import print_function

import sys
import os
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence

path = "/Users/apple/scrapingEnv/weibo-summary/weiboData" #文件夹目录
files= os.listdir(path) #得到文件夹下的所有文件名称
topic_name = ""

for file in files:
	if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开  
		topic_name = os.path.splitext(file)[0]
		file_path = path + "/" + file

		text = codecs.open(file_path, 'r', 'utf-8').read()

		sFilePath = '/Users/apple/scrapingEnv/weibo-summary/resultData/textrank'
		output_file = ""
		if not os.path.exists(sFilePath) :
			os.mkdir(sFilePath)
		out = open(sFilePath + '/' + topic_name +'-'+'textrank'+'.txt','w+')

		tr4w = TextRank4Keyword()

		tr4w.analyze(text=text, lower=True, window=2)   # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象

		print( '关键词：' )
		for item in tr4w.get_keywords(20, word_min_len=1):
			print(item.word, item.weight)

		print()
		print( '关键短语：' )
		for phrase in tr4w.get_keyphrases(keywords_num=20, min_occur_num= 2):
		    print(phrase)

		tr4s = TextRank4Sentence()
		tr4s.analyze(text=text, lower=True, source = 'all_filters')

		print()
		print( '摘要：' )
		for item in tr4s.get_key_sentences(num=3):
			output_file = output_file + item.sentence + '\n'
			print(item.index, item.weight, item.sentence)
		out.write(output_file)
		out.close()