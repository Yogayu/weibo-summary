#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

import numpy as np
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

sys.path.append('../')
from app import Summary
from config import *
from utilities import *

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) != 1 or args[0] == 'None':
        print('error args - Topic')
        exit()
    topic = args[0]
    print ("topic_name")
    print (topic)

    stopWords = get_stop_words()

    vectorizer = CountVectorizer(stop_words = stopWords)
    transformer = TfidfTransformer()

    topic_name = topic.rstrip()
    print "\n话题:"
    print topic_name
    trian_set_result = get_train_set(topic)
    train_set = trian_set_result[0]
    line_tweet = trian_set_result[1]

    tfidf = transformer.fit_transform(vectorizer.fit_transform(train_set))
    word = vectorizer.get_feature_names() #所有文本的关键字
    weight = tfidf.toarray()              #对应的tfidf矩阵
    sums = weight.sum(1)
    sorted_indices = np.argsort(sums)

    # 将结果存入文件
    rFilePath = get_result_data_path() + '/TFIDF'
    sFilePath = get_rouge_sum_path()
    # 完整摘要放入ResultData
    result_output_file = ""
    # 分词的摘要放入ROUGE-Summary
    segment_output_file = ""

    sub_path = '/' + topic_name + '_TFIDFSyssum' + '.txt'

    if not os.path.exists(sFilePath):
        os.mkdir(sFilePath)
    segment_out = open(sFilePath + sub_path, 'w+')

    if not os.path.exists(rFilePath):
        os.mkdir(rFilePath)
    result_out = open(rFilePath + sub_path, 'w+')

    # print sorted_indices
    print "best"
    print sums[sorted_indices[-1]]
    print sorted_indices[-1]
    print line_tweet[sorted_indices[-1]]
    print "second best"
    print sums[sorted_indices[-2]]
    print line_tweet[sorted_indices[-2]]

    summaryItems = []
    # 存储前五条
    for i in xrange(1,6):
        segment_output_file += train_set[sorted_indices[-i]] + '\n'
        result_output_file += line_tweet[sorted_indices[-i]]
        summaryItems.append(Summary(topic_name,line_tweet[sorted_indices[-i]],train_set[sorted_indices[-i]],"TF-IDF"))
    segment_out.write(segment_output_file)
    segment_out.close()

    result_out.write(result_output_file)
    result_out.close()

    # save to the database
    for summaryItem in summaryItems:
        summaryItem.add()

    # recalculate 1
    # seenWords = stopWords + train_set[sorted_indices[-1]].split(' ')
    # vectorizer2 = CountVectorizer(stop_words = seenWords)
    # trainVectorizerArray = vectorizer2.fit_transform(train_set).toarray()
    # transformer2 = TfidfTransformer()
    # transformer2.fit(trainVectorizerArray)
    # sums = transformer2.transform(trainVectorizerArray).toarray().sum(1)
    # sorted_indices = np.argsort(sums)
    # print "recalculate 1"
    # print sums[sorted_indices[-1]]
    # print sorted_indices[-1]
    # print line_tweet[sorted_indices[-1]]

    # # recalculate 2
    # seenWords2 = seenWords + train_set[sorted_indices[-1]].split(' ')
    # vectorizer3 = CountVectorizer(stop_words = seenWords2)
    # trainVectorizerArray = vectorizer3.fit_transform(train_set).toarray()
    # transformer3 = TfidfTransformer()
    # transformer3.fit(trainVectorizerArray)
    # sums = transformer3.transform(trainVectorizerArray).toarray().sum(1)
    # sorted_indices = np.argsort(sums)
    # print "recalculate 2"
    # print sums[sorted_indices[-1]]
    # print sorted_indices[-1]
    # print line_tweet[sorted_indices[-1]]
        
print(20*'-')