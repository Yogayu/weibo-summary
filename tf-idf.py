 #! /usr/bin/env python
 # coding=utf-8
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.corpus import stopwords
import numpy as np
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# stopWords = stopwords.words('english')
stopWords = [",", "?", "、", "。", "“", "”", "《", "》", "！", "，", "：", "；", "？",
"的","了","在","是","我","有","和","就","不","人","都","一","一个","上","也","很","到","说","要","去","你","会","着","没有","看","好","自己","这"]

vectorizer = CountVectorizer(stop_words = stopWords)
transformer = TfidfTransformer()

print "reading topics from 11/19"
# with open('topic_list-11-21.txt') as f:
  # content = f.readlines()
  # for topic in content:
print "\n"
# print topic.rstrip()
train_set = []
# with open('data/'+topic.rstrip()+'.txt') as data:
with open(u'/Users/apple/weibo/data/#大连15中车祸#.txt') as data:
  for tweet in data.readlines():
    train_set.append(tweet)
trainVectorizerArray = vectorizer.fit_transform(train_set).toarray()
transformer.fit(trainVectorizerArray)
sums = transformer.transform(trainVectorizerArray).toarray().sum(1)
sorted_indices = np.argsort(sums)
print "best"
print sums[sorted_indices[-1]]
print train_set[sorted_indices[-1]]
print "second best"
print sums[sorted_indices[-2]]
print train_set[sorted_indices[-2]]
seenWords = stopWords + train_set[sorted_indices[-1]].split(' ')
# print seenWords
vectorizer2 = CountVectorizer(stop_words = seenWords)
trainVectorizerArray = vectorizer2.fit_transform(train_set).toarray()
transformer2 = TfidfTransformer()
transformer2.fit(trainVectorizerArray)
sums = transformer2.transform(trainVectorizerArray).toarray().sum(1)
sorted_indices = np.argsort(sums)
print "second best with recompiling"
print sums[sorted_indices[-1]]
print train_set[sorted_indices[-1]]
    
