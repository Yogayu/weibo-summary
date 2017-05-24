#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu
# Hybrid TF-IDF
# Paper:Sharifi B, Hutton M A, Kalita J K.
# Experiments in microblog summarization[C]//Social Computing (SocialCom),
# 2010 IEEE Second International Conference on. IEEE, 2010: 49-56.

from sklearn.feature_extraction.text import TfidfVectorizer
from math import log
from utilities import *
import numpy as np
import sys
import json
import os

reload(sys)
sys.setdefaultencoding('utf-8')

print "reading topics from topicList"
with open('topicList.txt') as f:
    content = f.readlines()
    for topic in content:
        print "\n话题:"
        topic_name = topic.rstrip()
        print topic_name
        train_set = []
        line_tweet = []

        # 获取分词之后的数据集
        train_set_result = get_train_set(topic)
        train_set = train_set_result[0]
        line_tweet = train_set_result[1]

        # get posts per word and word counts
        all_post_counts = {}
        all_word_counts = {}
        total_word_count = 0

        # 1.计算每个词在所有文档中出现的频率
        for post in train_set:
            seen = []
            for word in post.split(' '):
                total_word_count += 1
                all_word_counts[word] = all_word_counts.get(word, 0) + 1
                if(word not in seen):
                    all_post_counts[word] = all_post_counts.get(word, 0) + 1
                seen.append(word)
        # print json.dumps(all_word_counts,encoding='UTF-8',ensure_ascii=False)

        # 2.计算所有词的idf值
        # word,所有文档中的词；
        # all_post_counts[word]，word对应出现的频率
        # all_idfs，所有词对应的idf值
        # all_idfs[word]，word对应的idf值
        all_idfs = {}
        train_set_length = len(train_set)
        for word in all_post_counts:
            # 公式六
            # 所有文档中的句子数/出现了该词的句子数
            all_idfs[word] = train_set_length / all_post_counts[word]
        # print json.dumps(all_idfs,encoding='utf-8',ensure_ascii=False)

        # 3.计算词的tf值
        all_tfs = {}
        for word in all_word_counts:
            # 公式五
            # 该词在全部文档出现的频率/全部文档中的词数
            all_tfs[word] = float(all_word_counts[word]) / total_word_count

        # 4.计算词的权重
        word_weights = {}
        for word in all_tfs:
            # 公式二
            word_weights[word] = all_tfs[word] * log(all_idfs[word])
        for i in xrange(0,80):
            # 5.计算文档权重
            weights = []
            for post in train_set:
                word_sum = 0
                for word in post.split(' '):
                    word_sum += word_weights[word]
                # 公式七：此处将句子中的词数:len(post.split(' ')作为归一化因子
                # 公式三
                MINIMUM_THRESHOLD = i;
                normalizing_factor = max(MINIMUM_THRESHOLD, len(post.split(' ')))
                # print normalizing_factor
                weights.append(word_sum/normalizing_factor)
            # print weights
            sorted_indices = np.argsort(weights)
            print sorted_indices
            # 将结果存入文件
            sFilePath = 'resultData/Hybrid-TFIDF'
            output_file = ""
            if not os.path.exists(sFilePath):
                os.mkdir(sFilePath)
            out = open(sFilePath + '/' + topic_name +
                       '-'+'Hybrid-TFIDF'+ '_Syssum' +str(i)+'.txt', 'w+')

            iterations = 5
            for i in xrange(1, iterations+1):
                tweet = train_set[sorted_indices[-i]]
                output_file = output_file + tweet + '\n'
                print tweet

            # 前十条摘要...
            # count = -1
            # seen = []
            # seen.append(tweet)
            # for x in range(0, iterations):
            #   print "iteration: " + str(x+1)
            #   while(tweet in seen):
            #     count -= 1
            #     tweet = line_tweet[sorted_indices[count]]
            #     print sorted_indices[count]
            #     print tweet
            #     output_file = output_file + tweet
            #   seen.append(tweet)
            out.write(output_file)
            out.close()
