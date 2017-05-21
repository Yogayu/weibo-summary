#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu

from sklearn.feature_extraction.text import CountVectorizer
# from nltk.corpus import stopwords
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

print "rouge score for files " + sys.argv[1] + " and " + sys.argv[2]

# stopWords = stopwords.words('english')
stopWords = [",", "?", "、", "。", "“", "”", "《", "》", "！", "，", "：", "；", "？",
             "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一", "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有", "看", "好", "自己", "这"]

file1 = []
with open(sys.argv[1]) as data:
    for tweet in data.readlines():
        if len(tweet) > 1:
            file1.append(tweet)

file2 = []
with open(sys.argv[2]) as data:
    for tweet in data.readlines():
        if len(tweet) > 1:
            file2.append(tweet)

for x in range(0, min(len(file1), len(file2))):
    vectorizer = CountVectorizer(ngram_range=(1, 5), stop_words=stopWords)
    vectorizer.fit(file1)

    vectorizer2 = CountVectorizer(ngram_range=(1, 5), stop_words=stopWords)
    vectorizer2.fit(file2)
    intersect = set(vectorizer.get_feature_names()) & set(
        vectorizer2.get_feature_names())
    tp = len(intersect)
    fp = len(vectorizer.get_feature_names()) - len(intersect)
    fn = len(vectorizer2.get_feature_names()) - len(intersect)
    print tp
    print fp
    print fn
    precision = float(tp)/(tp+fp)
    recall = float(tp)/(tp+fn)
    fmeasure = 2 * precision * recall / (precision + recall)
    print min(len(file1), len(file2))
    print "precision: " + str(precision)
    print "recall: " + str(recall)
    print "fmeasure: " + str(fmeasure)

    file1.pop()
    file2.pop()
