#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu

from textrank4zh import Segmentation
import json, sys
import codecs

sys.path.append('../')
from config import *

# 获取分词之后的数据集


def get_train_set(topic):
    # 分词之后的数据集
    train_set = []
    # 原始未分词数据集
    line_tweet = []
    split_line_tweet = []
    seg = Segmentation.Segmentation()
    path = get_base_dir() + '/Data/weiboData/'+topic.rstrip()+'.txt'
    with open(path) as data:
        for tweet in data.readlines():
            # 原始每行数据
            line_tweet.append(tweet)
            # 中文分词之后的数据
            result = seg.segment(text=tweet, lower=True)
            for ss in result.words_no_stop_words:
                split_line_tweet.append(' '.join(ss))
            line_string = ""
            if split_line_tweet != []:
                for i in xrange(0,len(split_line_tweet)):
                    line_string += split_line_tweet[i]
            split_line_tweet = []
            train_set.append(line_string)
        # json_print(train_set)
        # json_print(line_tweet)
    return (train_set, line_tweet)

# 获取停等词


def get_stop_words():
    stop_words = []
    stop_words_file = Segmentation.get_default_stop_words_file()
    # if type(stop_words_file) is str:
    for word in codecs.open(stop_words_file, 'r', 'utf-8', 'ignore'):
        stop_words.append(word.strip())
    return stop_words

def json_print(item):
    print json.dumps(item,encoding='UTF-8',ensure_ascii=False)

def get_segment_set(file):
    # 分词之后的数据集
    train_set = []
    split_line_tweet = []
    seg = Segmentation.Segmentation()
    with open(file) as data:
        for tweet in data.readlines():
            # 中文分词之后的数据
            result = seg.segment(text=tweet, lower=True)
            for ss in result.words_no_stop_words:
                split_line_tweet.append(' '.join(ss))
            line_string = ""
            if split_line_tweet != []:
                for i in xrange(0,len(split_line_tweet)):
                    line_string += split_line_tweet[i]
            split_line_tweet = []
            train_set.append(line_string)
    return train_set

def get_result_data_path():
    path = get_base_dir() + '/Data/ResultData'
    return path

def get_rouge_sum_path():
    path = get_base_dir() + '/Data/ROUGE/test-summarization/system'
    return path
def get_rouge_sum_test_path():
    path = get_base_dir() + '/Data/ROUGE/test/system'
    return path