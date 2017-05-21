#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu

import re
import os
import sys
import xml.etree.ElementTree as ET

#设置编码格式
reload(sys)
sys.setdefaultencoding('utf-8')

path = "rawData/豆瓣电影评分-p511293832" #文件夹目录
# path = "/Users/apple/weibo/关键字/雄安新区"
files= os.listdir(path) #得到文件夹下的所有文件名称

output_file = ""
topic_name = ""
count = 0

#遍历文件夹中文件
for file in files:
     if not os.path.isdir(file): #判断是否是文件夹，不是文件夹才打开  
     	file_path = path+"/"+file
     	if os.path.splitext(file_path)[1] == '.xml':
     		print file_path
	     	tree = ET.parse(file_path)
	     	root = tree.getroot()
	     	# print('--------------------------------')
	     	#获取博文结点
	     	# weibo_node = root.find(u'\u5fae\u535a\u8bdd\u9898')
	     	#话题结点
	     	weibo_topic = root.find(u'微博话题')[0]
	     	#话题相关信息
	     	topic_name = weibo_topic.find(u'话题').text
	     	topic_intro = weibo_topic.find(u'导语').text
	     	topic_reading_count = weibo_topic.find(u'阅读数').text
	     	topic_discuss_count = weibo_topic.find(u'讨论数').text
	     	topic_fans_count = weibo_topic.find(u'粉丝数').text

	     	# print topic_name
	     	# print topic_intro
	     	# print topic_reading_count
	     	# print topic_discuss_count
	     	# print topic_fans_count

	     	# print('---------------------------------')

	     	#博文列表
	     	list = weibo_topic.find(u'列')
	     	for items in list:
	     		for samples in items.iter(u'样例'):
	     			for item in samples:
	     				weibo_content = item.find(u'博文')
	     				s = ET.tostring(weibo_content,'utf-8').strip()
	     				result = ' '.join(s.split())
	     				res_tr = r'<博文>(.*?)</博文>'
	     				content = re.findall(res_tr,result,re.S|re.M)
	     				for nn in content:
	     					#去掉左边空格并编码
	     					count += 1
	     					output_file = output_file + unicode(nn,'utf-8').lstrip() + '\n'
# print output_file
print ("微博条数:%i" % count)
out = open('weiboData' + "/" + topic_name + ".txt", "w")
out.write(output_file)
print("End")