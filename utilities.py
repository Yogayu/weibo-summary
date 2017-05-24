#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Author:youxinyu
# Github:yogayu

from textrank4zh import Segmentation
import json
import codecs

# 获取分词之后的数据集


def get_train_set(topic):
    # 分词之后的数据集
    train_set = []
    # 原始未分词数据集
    line_tweet = []
    split_line_tweet = []
    seg = Segmentation.Segmentation()
    with open('weiboData/'+topic.rstrip()+'.txt') as data:
        for tweet in data.readlines():
            # 原始每行数据
            line_tweet.append(tweet)
            # 中文分词之后的数据
            result = seg.segment(text=tweet, lower=True)
            for ss in result.words_no_stop_words:
                split_line_tweet.append(' '.join(ss))
            if split_line_tweet != []:
                train_set.append(split_line_tweet[0])#??
            split_line_tweet = []
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
            # print tweet
            result = seg.segment(text=tweet, lower=True)
            # json_print(result)
            for ss in result.words_no_stop_words:
                # json_print(ss)
                # print len(ss)
                split_line_tweet.append(' '.join(ss))
            # json_print(split_line_tweet)
            line_string = ""
            if split_line_tweet != []:
                for i in xrange(0,len(split_line_tweet)):
                    line_string += split_line_tweet[i]
            # json_print(line_string)
            train_set.append(line_string)
            split_line_tweet = []
    return train_set