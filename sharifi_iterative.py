#! /usr/bin/env python
# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import numpy as np
import math

def calc_tf_idf(train_set):
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
      word_weights[word] = all_tfs[word] * math.log(all_idfs[word])
    #calc post weights 
    weights = []
    for post in train_set:
      word_sum = 0
      for word in post.split(' '):
        word_sum += word_weights.get(word, 0)
      #print post
      #print word_sum
      weights.append(word_sum/len(post.split(' ')))
    return word_weights, weights

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def shrink_corpus(tweet, train_set, word_weights):
    #print "given corpus size: " + str(len(train_set))
    new_corpus = []
    top_post_vec = {}
    for word in tweet.split(' '):
      top_post_vec[word] = word_weights[word]
    for post in train_set:
      #compute cosine similarity
      post_vec = {}
      for word in post.split(' '):
        post_vec[word] = word_weights[word]
      similarity =  get_cosine(post_vec, top_post_vec) 
      # if below threshold, add to new set
      if(similarity <= 0.5):
        new_corpus.append(post)
    #print "new corpus size: " + str(len(new_corpus))
    return new_corpus

stopWords = stopwords.words('english')

print "reading topics from 5-16"
with open('topic_list-5-16.txt') as f:
  content = f.readlines()
  for topic in content:
    print "\n话题:"
    print topic.rstrip()

    train_set = []
    if(1==1):
        with open('weiboData/'+topic.rstrip()+'.txt') as data:
        # with open(u'/Users/apple/weibo/data/#校园网大规模病毒攻击#.txt') as data:
          for tweet in data.readlines():
            train_set.append(tweet.lower())
        (word_weights, weights) = calc_tf_idf(train_set)
        sorted_indices = np.argsort(weights)
        tweet = train_set[sorted_indices[-1]]
        print tweet

        iterations = 10

        new_corpus = train_set
        # shrink recalulate
        for i in range(1, iterations+1):
          new_corpus = shrink_corpus(tweet, new_corpus, word_weights)
          (word_weights, weights) = calc_tf_idf(new_corpus)
          sorted_indices = np.argsort(weights)
          tweet = new_corpus[sorted_indices[-2]]
          coverage = 1 - float(len(new_corpus))/len(train_set)
          #print "iteration: " + str(i) + " coverage: " + str(coverage)
          print tweet
