#! /usr/bin/env python
# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer
# from nltk.corpus import stopwords
import numpy as np
from math import log
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

stopWords = [",", "?", "、", "。", "“", "”", "《", "》", "！", "，", "：", "；", "？",
"的","了","在","是","我","有","和","就","不","人","都","一","一个","上","也","很","到","说","要","去","你","会","着","没有","看","好","自己","这"]

# stopWords = stopwords.words('english')

print "reading topics from 5-16"
# with open('topic_list-5-16.txt') as f:
# content = f.readlines()
# for topic in content:
  # print "\n话题:"
  # print topic.rstrip()
train_set = []
if(1==1):
  # with open('weiboData/'+topic.rstrip()+'.txt') as data:
  with open(u'/Users/apple/weibo/data/#校园网大规模病毒攻击#.txt') as data:
    for tweet in data.readlines():
      train_set.append(tweet)
  # get posts per word and word counts
  all_post_counts = {}
  all_word_counts = {}
  total_word_count = 0
  for post in train_set:
    seen = []
    for word in post.split(' '):
      total_word_count += 1
      all_word_counts[word] =  all_word_counts.get(word, 0) + 1
      if(word not in seen):
        all_post_counts[word] =  all_post_counts.get(word, 0) + 1
      seen.append(word)
  #calc idf of words
  all_idfs = {}
  for word in all_post_counts:
    #idf = #sentences / #sentances with word
    all_idfs[word] = len(train_set) / all_post_counts[word]
  #calc tf of words
  all_tfs = {}
  for word in all_word_counts:
    all_tfs[word] = float(all_word_counts[word]) / total_word_count
  #calc word weights
  word_weights = {}
  for word in all_tfs:
    word_weights[word] = all_tfs[word] * log(all_idfs[word])
  #calc post weights 
  weights = []
  for post in train_set:
    word_sum = 0
    for word in post.split(' '):
      word_sum += word_weights[word]
    #print post
    #print word_sum
    weights.append(word_sum/len(post.split(' ')))
  sorted_indices = np.argsort(weights)

  iterations = 10

  tweet = train_set[sorted_indices[-1]]
  print tweet
  count = -1
  seen = []
  seen.append(tweet)
  for x in range(0, iterations):
    #print "iteration: " + str(x+1)
    while(tweet in seen):
      count -= 1
      tweet = train_set[sorted_indices[count]]
    print tweet
    seen.append(tweet)
