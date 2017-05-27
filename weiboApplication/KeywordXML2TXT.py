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
    # keyword_path = "rawData/keyword/"
    keyword_path = '../rawData/Keyword/'
    keyword_names = os.listdir(keyword_path)

    for keyword in keyword_names:
        path = keyword_path + keyword
        if os.path.isdir(path):
            files = os.listdir(path)

            output_file = ""
            keyword_name = ""
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
                        weibo_keyword = root.find(u'列表')[0]
                        # 关键字
                        keyword_name = weibo_keyword.find(u'关键字').text

                        # print('---------------------------------')

                        # 博文列表
                        list = weibo_keyword.find(u'列')
                        for item in list.iter(u'item'):
                            trans_count = item.find(u'转发数').text
                            comment_count = item.find(u'评论数').text
                            like_count = item.find(u'点赞数').text

                            weibo_content = item.find(u'博文')
                            s = ET.tostring(weibo_content, 'utf-8').strip()
                            result = ' '.join(s.split())
                            res_tr = r'<博文>(.*?)</博文>'
                            content = re.findall(
                                res_tr, result, re.S | re.M)
                            count += 1
                            if ((trans_count != None) or (comment_count != None) or (like_count != None)):
                                for nn in content:
                                    # 去掉左边空格并编码
                                    output_string = unicode(
                                        nn, 'utf-8').lstrip()
                                    # 去除无用词汇
                                    delete_strings = [
                                        '秒拍视频', '展开全文c', '评论配图', '网页链接','微辣Video...']
                                    for delete_str in delete_strings:
                                        output_string = output_string.replace(
                                            delete_str, '').rstrip()
                                    # 只包含话题的长度
                                    minLength = (len(keyword_name) + 6)
                                    # 去掉少于5个字的微博
                                    if len(output_string) > (minLength + 5):
                                        real_count += 1
                                        output_file = output_file + output_string + '\n'
                                        if (trans_count == None):
                                            trans_count = '0'
                                        if (comment_count == None):
                                            comment_count = '0'
                                        if (like_count == None):
                                            like_count = '0'
                                        weiboItems.append(Weibo(keyword_name,output_string,trans_count,like_count,comment_count))
            print weiboItems
            for weiboItem in weiboItems:
                weiboItem.add()
            print keyword_name
            print ("微博条数:%i" % count)
            print ("有效微博条数:%i" % real_count)
            out = open('../weiboData' + "/" + keyword_name +".txt", "w")
            out.write(output_file)
            print("-------------------------------")
