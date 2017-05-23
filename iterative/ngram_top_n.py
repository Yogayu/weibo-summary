#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu
from sklearn.feature_extraction.text import TfidfVectorizer
from utilities import *
import numpy as np
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

stopWords = get_stop_words()

print "reading topics from "
with open('topicList.txt') as f:
    content = f.readlines()
    for topic in content:
        print "\n话题:"
        topic_name = topic.rstrip()
        print topic_name
        # 获取分词之后的数据集
        train_set_result = get_train_set(topic)
        train_set = train_set_result[0]
        with open('weiboData/'+topic_name+'.txt') as data:
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
