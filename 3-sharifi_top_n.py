#! /usr/bin/env python
# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer
# import tf-idf
import numpy as np
from math import log
from textrank4zh import Segmentation
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')

def get_train_set(topic):
    train_set = []
    line_tweet = []
    split_line_tweet = []
    seg = Segmentation.Segmentation()
    with open('weiboData/'+topic.rstrip()+'.txt') as data:
        for tweet in data.readlines():
            #原始每行数据
            line_tweet.append(tweet)
            #中文分词之后的数据
            result = seg.segment(text=tweet, lower=True)
            for ss in result.words_no_filter:
                split_line_tweet.append(' '.join(ss))
            if split_line_tweet != []:
                train_set.append(split_line_tweet[0])
            split_line_tweet = []
    return (train_set,line_tweet)

print "reading topics from 5-16"
with open('topic_list-5-16.txt') as f:
  content = f.readlines()
  for topic in content:
    print "\n话题:"
    print topic.rstrip()
    train_set = []
    line_tweet = []

    #获取分词之后的数据集
    train_set_result = get_train_set(topic)
    train_set = train_set_result[0]
    line_tweet = train_set_result[1]
    
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
    # print json.dumps(all_word_counts,encoding='UTF-8',ensure_ascii=False)
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
      print post
      print word_sum
      weights.append(word_sum/len(post.split(' ')))
    sorted_indices = np.argsort(weights)

    iterations = 10

    tweet = line_tweet[sorted_indices[-1]]
    print tweet
    count = -1
    seen = []
    seen.append(tweet)
    for x in range(0, iterations):
      print "iteration: " + str(x+1)
      while(tweet in seen):
        count -= 1
        tweet = line_tweet[sorted_indices[count]]
      print tweet
      seen.append(tweet)
