#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu

import re
import os
import sys
from weiboModel import *
import xml.etree.ElementTree as ET

# 设置编码格式
reload(sys)
sys.setdefaultencoding('utf-8')
if __name__ == "__main__":
    topic_path = "../rawData/Topic/"
    topic_names = os.listdir(topic_path)
    for topic in topic_names:
        path = topic_path + topic
        if os.path.isdir(path): 
            files = os.listdir(path) # 得到文件夹下的所有文件名称
            output_file = ""
            topic_name = ""
            count = 0
            real_count = 0

            weiboItems = []
            # 遍历文件夹中文件
            for file in files:
                if not os.path.isdir(file):  # 判断是否是文件夹，不是文件夹才打开
                    file_path = path+"/"+file
                    if os.path.splitext(file_path)[1] == '.xml':
                        # print file_path
                        tree = ET.parse(file_path)
                        root = tree.getroot()
                        # print('--------------------------------')
                        # 获取博文结点
                        # weibo_node = root.find(u'\u5fae\u535a\u8bdd\u9898')
                        # 话题结点
                        weibo_topic = root.find(u'微博话题')[0]
                        # 话题相关信息
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

                        # 博文列表
                        list = weibo_topic.find(u'列')
                        for items in list:
                            for samples in items.iter(u'样例'):
                                for item in samples:
                                    count += 1
                                    trans_count = item.find(u'转发数').text
                                    comment_count = item.find(u'评论数').text
                                    like_count = item.find(u'点赞数').text
                                    # print trans_count
                                    # print comment_count
                                    # print like_count

                                    # 三者其中一个不为0，即视为有效微博
                                    if ((trans_count != "转发") or (comment_count != "评论") or (like_count != "赞")):
                                        weibo_content = item.find(u'博文')
                                        s = ET.tostring(weibo_content, 'utf-8').strip()
                                        result = ' '.join(s.split())
                                        res_tr = r'<博文>(.*?)</博文>'
                                        content = re.findall(res_tr, result, re.S | re.M)
                                        for nn in content:
                                            # 去掉左边空格并编码
                                            output_string = unicode(nn, 'utf-8').lstrip()
                                            # 去除无用词汇
                                            delete_strings = [
                                                '秒拍视频', '展开全文c', '评论配图', '网页链接']
                                            for delete_str in delete_strings:
                                                output_string = output_string.replace(
                                                    delete_str, '').rstrip()
                                            # 只包含话题的长度
                                            minLength = (len(topic_name) + 6)
                                            # 去掉少于5个字的微博
                                            if len(output_string) > (minLength + 5):
                                                real_count += 1
                                                output_file = output_file + output_string + '\n'
                                                if (trans_count == "转发"):
                                                    trans_count = '0'
                                                if (comment_count == "评论"):
                                                    comment_count = '0'
                                                if (like_count == "赞"):
                                                    like_count = '0'
                                                weiboItems.append(Weibo(topic_name,output_string,trans_count,like_count,comment_count))
            print weiboItems
            for weiboItem in weiboItems:
                weiboItem.add()
            print topic_name
            print ("微博条数:%i" % count)
            print ("有效微博条数:%i" % real_count)
            out = open('../weiboData' + "/" + topic_name + ".txt", "w")
            out.write(output_file)
            print("-------------------------------")