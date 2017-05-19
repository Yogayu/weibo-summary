#! /usr/bin/env python
# coding=utf-8
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
# from nltk.corpus import stopwords
import numpy as np
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

# stopWords = stopwords.words('english')

stopWords = [",", "?", "、", "。", "“", "”", "《", "》", "！", "，", "：", "；", "？",
"的","了","在","是","我","有","和","就","不","人","都","一","一个","上","也","很","到","说","要","去","你","会","着","没有","看","好","自己","这"]
vectorizer = CountVectorizer(stop_words = stopWords)
transformer = TfidfTransformer()

topic_name = ""

print "reading topics from 05/16"
with open('topic_list-5-16.txt') as f:
  content = f.readlines()
  for topic in content:
    print "\n话题:"
    topic_name = topic.rstrip()
    print topic.rstrip()
    train_set = []
    with open('weiboData/'+topic.rstrip()+'.txt') as data:
      for tweet in data.readlines():
        train_set.append(tweet)
    trainVectorizerArray = vectorizer.fit_transform(train_set).toarray()
    transformer.fit(trainVectorizerArray)
    sums = transformer.transform(trainVectorizerArray).toarray().sum(1)
    sorted_indices = np.argsort(sums)
    print "First"
    print train_set[sorted_indices[-1]]
    print "Second"
    print train_set[sorted_indices[-2]]
    print "Third"
    print train_set[sorted_indices[-3]]
    sFilePath = '/Users/apple/scrapingEnv/weibo-summary/resultData/top-n'
    output_file = ""
    if not os.path.exists(sFilePath) :
        os.mkdir(sFilePath)
    out = open(sFilePath + '/'+ topic_name +'-'+'top-n'+'.txt','w+')
    output_file = output_file + train_set[sorted_indices[-1]]
    output_file = output_file + train_set[sorted_indices[-2]]
    output_file = output_file + train_set[sorted_indices[-3]]
    out.write(output_file)
    out.close()
