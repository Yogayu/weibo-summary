#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import numpy as np
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# stopWords = stopwords.words('english')
stopWords = [",", "?", "、", "。", "“", "”", "《", "》", "！", "，", "：", "；", "？",
             "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好", "自己", "这"]

print "reading topics from 05/16"
with open('topic_list-5-16.txt') as f:
    content = f.readlines()
    for topic in content:
        print "\n话题:"
        print topic.rstrip()
        train_set = []
        with open('weiboData/'+topic.rstrip()+'.txt') as data:
            for tweet in data.readlines():
                train_set.append(tweet)
        vectorizer = TfidfVectorizer(stop_words=stopWords)
        vectorizer.fit(train_set)
        words = ' '.join(vectorizer.get_feature_names())
        idf_vals = vectorizer.transform([words]).toarray()
        words = words.split(' ')
        sorted_indices = np.argsort(idf_vals[0])
        print "First"
        print sorted_indices[0]
        print words[sorted_indices[0]]
        print "Second"
        print sorted_indices[1]
        print words[sorted_indices[1]]
        print "Third"
        print sorted_indices[2]
        print words[sorted_indices[2]]
