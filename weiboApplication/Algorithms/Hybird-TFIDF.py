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
import numpy as np
import sys, os

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
    print ("Hybrid-TFIDF")
    print (topic)

    topic_name = topic.rstrip()
    
    train_set = []
    line_tweet = []

    summaryItems = []

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
    # for i in xrange(0,80):
    # 5.计算文档权重
    weights = []
    for post in train_set:
        word_sum = 0
        for word in post.split(' '):
            word_sum += word_weights[word]
        # 公式七：此处将句子中的词数:len(post.split(' ')作为归一化因子
        # 公式三
        MINIMUM_THRESHOLD = 37;
        normalizing_factor = max(MINIMUM_THRESHOLD, len(post.split(' ')))
        # print normalizing_factor
        weights.append(word_sum/normalizing_factor)
    # print weights
    sorted_indices = np.argsort(weights)
    # print sorted_indices
    
    # 将结果存入文件
    rFilePath = get_result_data_path() + '/Hybrid-TFIDF'
    sFilePath = get_rouge_sum_path()
    # 完整摘要放入ResultData
    result_output_file = ""
    # 分词的摘要放入ROUGE-Summary
    segment_output_file = ""

    sub_path = '/' + topic_name + '_Hybrid-TFIDFSyssum' +'.txt' #+str(i)

    if not os.path.exists(sFilePath):
        os.mkdir(sFilePath)
    segment_out = open(sFilePath + sub_path, 'w+')
    
    if not os.path.exists(rFilePath):
        os.mkdir(rFilePath)
    result_out = open(rFilePath + sub_path, 'w+')
    
    iterations = 5
    for i in xrange(1, iterations+1):
        tweet = train_set[sorted_indices[-i]]
        segment_output_file = segment_output_file + tweet + '\n'
        print line_tweet[sorted_indices[-i]]
        result_output_file += line_tweet[sorted_indices[-i]] + '\n'
        summaryItems.append(Summary(topic_name,line_tweet[sorted_indices[-i]],tweet,"Hybrid-TFIDF"))
    
    result_out.write(result_output_file)
    segment_out.write(segment_output_file)
    
    segment_out.close()
    result_out.close()

    # save to the database
    for summaryItem in summaryItems:
        summaryItem.add()
print(20*'-')